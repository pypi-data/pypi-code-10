# -*- coding: utf-8 -*-
"""
Rhizom - Relationship grapher

Copyright (C) 2015  Aurelien Bompard <aurelien@bompard.org>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import unicode_literals, print_function

from flask import request, g, render_template, abort, jsonify
from flask_babel import gettext
from sqlalchemy import or_
from sqlalchemy.orm.exc import NoResultFound

from .. import app
from ..models import Graph, Person, Relationship, PermissionLevel
from ..lib import has_permission_level, get_rel_types
from ..forms import NewRelationship


__all__ = (
    "edit_all",
    "edit_person",
    "api_rel_add",
    "api_rel_edit",
    )


@app.route('/graph/<int:graph_id>/edit', methods=["GET"])
def edit_all(graph_id):
    graph = g.db.query(Graph).get(graph_id)
    if not graph:
        abort(404)
    if not has_permission_level(graph_id, PermissionLevel.edit):
        return render_template("error.html", code=403, graph=graph,
                               message=gettext("Access unauthorized")), 403
    newrel_form = NewRelationship()
    rel_types = get_rel_types(graph)
    newrel_form.rtype.choices = [ (rt, rt) for rt in rel_types ]
    context = dict(
        graph = graph,
        newrel_form = newrel_form,
        rel_types = rel_types,
    )
    return render_template("edit.html", **context)


@app.route('/graph/<int:graph>/edit/person/<int:person>', methods=["GET"])
def edit_person(graph, person):
    graph = g.db.query(Graph).get(graph)
    if not graph:
        abort(404)
    if not has_permission_level(graph.id, PermissionLevel.edit):
        return render_template("error.html", code=403, graph=graph,
                               message=gettext("Access unauthorized")), 403
    person = g.db.query(Person).get(person)
    if not person:
        abort(404)
    newrel_form = NewRelationship()
    rel_types = get_rel_types(graph)
    newrel_form.rtype.choices = [ (rt, rt) for rt in rel_types ]
    relationships = []
    for rel in g.db.query(Relationship).filter_by(source_id=person.id):
        rel.other = rel.target
        relationships.append(rel)
    for rel in g.db.query(Relationship).filter_by(target_id=person.id):
        rel.other = rel.source
        relationships.append(rel)
    relationships.sort(key=lambda rel: rel.other.name)
    context = dict(
        graph = graph,
        newrel_form = newrel_form,
        person = person,
        relationships = relationships,
        rel_types = rel_types,
    )
    return render_template("edit.html", **context)


@app.route('/api/graph/<int:graph>/relationships/', methods=["POST"])
def api_rel_add(graph):
    graph = g.db.query(Graph).get(graph)
    if not graph:
        abort(404)
    if not has_permission_level(graph.id, PermissionLevel.edit):
        return render_template("error.html", code=403, graph=graph,
                               message=gettext("Access unauthorized")), 403
    if "person" in request.form:
        person = g.db.query(Person).get(request.form["person"])
    else:
        person = None
    newrel_form = NewRelationship()
    rel_types = get_rel_types(graph)
    newrel_form.rtype.choices = [ (rt, rt) for rt in rel_types ]
    if not newrel_form.validate():
        content = render_template('edit/add_rel.html',
            graph=graph, newrel_form=newrel_form)
        return jsonify({"status": "error", "action": "replace",
                        "content": content})
    try:
        source = g.db.query(Person).filter_by(
            graph_id=graph.id, name=newrel_form.source.data).one()
    except NoResultFound:
        source = Person(graph_id=graph.id, name=newrel_form.source.data)
        g.db.add(source)
    try:
        target = g.db.query(Person).filter_by(
            graph_id=graph.id, name=newrel_form.target.data).one()
    except NoResultFound:
        target = Person(graph_id=graph.id, name=newrel_form.target.data)
        g.db.add(target)
    g.db.flush() # flushing is required to give IDs for the next step
    if source.id > target.id:
        source, target = target, source # the source is always the lowest id
    if g.db.query(Relationship).filter_by(
            source_id=source.id, target_id=target.id,
            type_name=newrel_form.rtype.data).count() != 0:
        return jsonify({
                "status": "error", "action": "replace",
                "message": gettext("This relationship already exists.")})
    newlink = Relationship(
        source_id=source.id, target_id=target.id,
        type_name=newrel_form.rtype.data, graph_id=graph.id,
        dotted=newrel_form.dotted.data)
    g.db.add(newlink)
    g.db.commit()
    result = {"status": "OK", "message": gettext("Relationship added.")}
    if person:
        if source.id == person.id:
            newlink.other = newlink.target
        elif target.id == person.id:
            newlink.other = newlink.source
        content = render_template('edit/edit_rel.html',
            graph=graph, rel=newlink, rel_types=rel_types)
        result.update({"action": "add", "content": content})
    else:
        newrel_form = NewRelationship(formdata=None) # Get a clean instance
        newrel_form.rtype.choices = [ (rt, rt) for rt in rel_types ]
        content = render_template('edit/new_rel.html',
            graph=graph, rel_types=rel_types, newrel_form=newrel_form)
        result.update({"action": "replace", "content": content})
    return jsonify(result)



@app.route('/api/graph/<int:graph>/relationships/<int:rel>',
           methods=["PUT", "DELETE"])
def api_rel_edit(graph, rel):
    graph = g.db.query(Graph).get(graph)
    if not graph:
        abort(404)
    if not has_permission_level(graph.id, PermissionLevel.edit):
        return render_template("error.html", code=403, graph=graph,
                               message=gettext("Access unauthorized")), 403
    rel = g.db.query(Relationship).get(rel)
    if rel is None:
        abort(404)
    if request.method == "PUT":
        newtype = request.form["ltype"]
        dotted = request.form.get("dotted") not in ("", "false", None)
        if rel.type_name != newtype and g.db.query(Relationship).filter_by(
                source_id=rel.source_id, target_id=rel.target_id,
                type_name=newtype).count() > 0:
            return jsonify({
                    "status": "error",
                    "message": gettext("This relationship already exists.")})
        rel.type_name = newtype
        rel.dotted = dotted
        g.db.commit()
        rel_types = get_rel_types(graph)
        rel.other = g.db.query(Person).get(request.form["other"])
        assert rel.other.id in (rel.source.id, rel.target.id)
        content = render_template('edit/edit_rel.html',
            graph=graph, rel=rel, rel_types=rel_types)
        return jsonify({"status": "OK", "action": "replace",
                        "content": content,
                        "message": gettext("Relationship modified.")})
    if request.method == "DELETE":
        g.db.delete(rel)
        g.db.flush() # flushing is required for the next step
        # Cleanup orphans
        for pid in (rel.source_id, rel.target_id):
            if g.db.query(Relationship).filter(or_(
                Relationship.source_id == pid,
                Relationship.target_id == pid)).count() == 0:
                g.db.delete(g.db.query(Person).get(pid))
        g.db.commit()
        return jsonify({"status": "OK", "action": "delete",
                        "message": gettext("Relationship removed.")})
