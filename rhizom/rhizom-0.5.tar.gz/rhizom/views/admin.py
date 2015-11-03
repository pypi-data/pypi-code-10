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

import json

from flask import request, g, render_template, abort, redirect, url_for, flash, jsonify
from flask_babel import gettext

from .. import app
from ..models import Graph, Person, User, Permission, PermissionLevel, RelationshipType
from ..lib import has_permission_level
from ..forms import NewAccess, RelationshipTypes, GraphProperties

__all__ = (
    "admin",
    "api_reltype",
    "api_access",
    )


@app.route('/graph/<int:graph_id>/admin', methods=["GET", "POST"])
def admin(graph_id):
    graph = g.db.query(Graph).get(graph_id)
    if not graph:
        abort(404)
    if not has_permission_level(graph_id, PermissionLevel.admin):
        return render_template("error.html", code=403, graph=graph,
                               message=gettext("Access unauthorized")), 403
    graphprops_form = GraphProperties(obj=graph, prefix="graphprops")
    graphprops_form.center_id.choices = [("0", gettext("(no one)"))] + [
        (str(p.id), p.name) for p in g.db.query(Person).filter_by(graph_id=graph_id
        ).order_by(Person.name) ]
    context = dict(
        graph = graph,
        graphprops_form = graphprops_form,
    )
    context.update(_get_reltype_context(graph))
    context.update(_get_access_context(graph))

    if request.method == "POST":
        # Graph: properties edition
        if request.form.get("formname") == "graphprops":
            if not graphprops_form.validate():
                return render_template("admin.html", **context)
            graph.name = graphprops_form.name.data
            graph.center_id = int(graphprops_form.center_id.data)
            if graph.center_id == 0:
                graph.center_id = None
            graph.anonymous = graphprops_form.anonymous.data
            g.db.commit()
            flash(gettext("Graph updated."), "success")
            return redirect(url_for("admin", graph_id=graph_id))
        # Graph: import
        elif request.form.get("formname") == "graphimport":
            if not request.files['import']:
                flash(gettext("No graph data."), "danger")
                return redirect(url_for("admin", graph_id=graph_id))
            try:
                data = json.load(request.files['import'])
            except ValueError:
                #log.warning("Failed to load the graph data for graph %s: %s", graph.id, e)
                flash(gettext("Invalid graph data."), "danger")
                return redirect(url_for("admin", graph_id=graph_id))
            graph.import_dict(data)
            g.db.commit()
            flash(gettext("Graph imported."), "success")
            return redirect(url_for("admin", graph_id=graph_id))
        # Graph: deletion
        elif request.form.get("formname") == "graphdel":
            g.db.delete(graph)
            g.db.commit()
            flash(gettext("Graph deleted."), "success")
            return redirect(url_for("index"))
    return render_template("admin.html", **context)



def _get_reltype_context(graph):
    reltypes_form = RelationshipTypes()
    context = dict(
        graph = graph,
        reltypes_form = reltypes_form,
        rel_types = g.db.query(RelationshipType).filter_by(
            graph_id=graph.id).order_by(RelationshipType.name),
    )
    return context


@app.route('/api/graph/<int:graph>/reltypes/', methods=["POST"])
@app.route('/api/graph/<int:graph>/reltypes/<name>', methods=["PUT", "DELETE"])
def api_reltype(graph, name=None):
    graph = g.db.query(Graph).get(graph)
    if not graph:
        abort(404)
    if not has_permission_level(graph.id, PermissionLevel.admin):
        return render_template("error.html", code=403, graph=graph,
                               message=gettext("Access unauthorized")), 403
    context = _get_reltype_context(graph)

    if request.method == "POST":
        reltypes_form  = context["reltypes_form"]
        if not reltypes_form.validate():
            content = render_template('admin/edit_reltypes.html', **context)
            return jsonify({"status": "error", "action": "replace-table",
                            "content": content})
        reltype = RelationshipType(graph_id=graph.id,
                                   name=reltypes_form.name.data,
                                   color=reltypes_form.color.data)
        for existing_types in g.db.query(RelationshipType
            ).filter_by(graph_id=graph.id):
            if reltype.cssname == existing_types.cssname:
                reltypes_form.name.errors.append(gettext("This name is already used."))
                content = render_template('admin/edit_reltypes.html', **context)
                return jsonify({"status": "error", "action": "replace-table",
                                "content": content})
        g.db.add(reltype)
        g.db.commit()
        context["reltypes_form"] = RelationshipTypes(
            prefix="reltypes", formdata=None) # get a blank form
        content = render_template('admin/edit_reltypes.html', **context)
        return jsonify({
                "status": "OK", "action": "replace-table", "content": content,
                "message": gettext("Relationship added.")
                })

    if request.method == "DELETE":
        reltype = g.db.query(RelationshipType).get((graph.id, name))
        if reltype is None:
            return jsonify({"status": "error",
                            "message": gettext("Invalid relationship type")})
        g.db.delete(reltype)
        g.db.commit()
        return jsonify({"status": "OK", "action": "delete",
                        "message": gettext("Relationship type removed.")})

    elif request.method == "PUT":
        reltype = g.db.query(RelationshipType).get((graph.id, name))
        if reltype is None:
            return jsonify({"status": "error",
                            "message": gettext("Invalid relationship type")})
        reltype.name = request.form["newname"]
        reltype.color = request.form["color"]
        g.db.commit()
        content = render_template('admin/edit_reltypes.html', **context)
        return jsonify({
            "status": "OK", "action": "replace-table", "content": content,
            "message": gettext("Relationship type modified.")})



def _get_access_context(graph):
    newaccess_form = NewAccess(prefix="newaccess")
    perm_choices = [ (int(getattr(PermissionLevel, l)), n) for l, n in
                  ( ("view", gettext("View")), ("edit", gettext("Edit")),
                    ("admin", gettext("Admin")) ) ]
    newaccess_form.level.choices = perm_choices
    context = dict(
        graph = graph,
        newaccess_form = newaccess_form,
        permissions = g.db.query(Permission).join(User).filter(
            Permission.graph_id == graph.id).order_by(User.name),
        perm_choices = perm_choices,
    )
    return context


@app.route('/api/graph/<int:graph>/accesses/', methods=["POST"])
@app.route('/api/graph/<int:graph>/accesses/<email>', methods=["PUT", "DELETE"])
def api_access(graph, email=None):
    graph = g.db.query(Graph).get(graph)
    if not graph:
        abort(404)
    if not has_permission_level(graph.id, PermissionLevel.admin):
        return render_template("error.html", code=403, graph=graph,
                               message=gettext("Access unauthorized")), 403
    context = _get_access_context(graph)

    if request.method == "POST":
        newaccess_form = context["newaccess_form"]
        if not newaccess_form.validate():
            content = render_template('admin/edit_accesses.html', **context)
            return jsonify({"status": "error", "action": "replace-table",
                            "content": content})
        user = g.db.query(User).get(newaccess_form.email.data)
        if user is None:
            user = User(email=newaccess_form.email.data)
            g.db.add(user)
        perm = Permission(graph_id=graph.id,
                          user_email=newaccess_form.email.data,
                          level=newaccess_form.level.data)
        g.db.add(perm)
        g.db.commit()
        newaccess_form = NewAccess(prefix="newaccess", formdata=None) # get a blank form
        newaccess_form.level.choices = context["newaccess_form"].level.choices
        context["newaccess_form"] = newaccess_form
        content = render_template('admin/edit_accesses.html', **context)
        return jsonify({
                "status": "OK", "action": "replace-table", "content": content,
                "message": gettext("Access added.")
                })

    if request.method == "DELETE":
        perm = g.db.query(Permission).get((graph.id, email))
        if perm is None:
            return jsonify({"status": "error",
                            "message": gettext("Invalid permission.")})
        user = perm.user
        g.db.delete(perm)
        g.db.flush() # flushing is required for the next step
        if len(user.permissions) == 0:
            g.db.delete(user) # no permissions left, delete it
        g.db.commit()
        return jsonify({"status": "OK", "action": "delete",
                        "message": gettext("Access removed.")})

    elif request.method == "PUT":
        perm = g.db.query(Permission).get((graph.id, email))
        if perm is None:
            return jsonify({"status": "error",
                            "message": gettext("Invalid permission.")})
        perm.level = request.form["level"]
        g.db.commit()
        content = render_template('admin/edit_accesses.html', **context)
        return jsonify({
            "status": "OK", "action": "replace-table", "content": content,
            "message": gettext("User modified.")})
