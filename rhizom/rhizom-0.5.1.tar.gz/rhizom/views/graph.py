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

from datetime import datetime

from flask import g, render_template, abort, jsonify, url_for
from flask_login import current_user
from flask_babel import gettext

from .. import app
from ..models import Graph, Person, Relationship, PermissionLevel, RelationshipType
from ..lib import compute_node_circles, compute_node_branch, has_permission_level


__all__ = (
    "view",
    "data",
    )


@app.route('/graph/<int:graph_id>')
def view(graph_id):
    graph = g.db.query(Graph).get(graph_id)
    if not graph:
        return render_template("error.html",
            code=404, message=gettext("Can't find the graph")), 404
    if not has_permission_level(graph_id, PermissionLevel.view):
        return render_template("error.html", code=403, graph=graph,
                               message=gettext("Access unauthorized")), 403
    if not current_user.is_master:
        # Admins don't count as visitors, so they can list old graphs and still
        # visit them without touching them.
        graph.last_access = datetime.utcnow()
        g.db.commit()
    rel_types = g.db.query(RelationshipType).filter_by(
        graph_id=graph_id).order_by(RelationshipType.name).all()
    return render_template("view.html", graph=graph, rel_types=rel_types)


@app.route('/api/graph/<int:graph_id>/data.js')
def data(graph_id):
    graph = g.db.query(Graph).get(graph_id)
    if not graph:
        abort(404)
    if not has_permission_level(graph_id, PermissionLevel.view):
        abort(403)
    graph_data = {"nodes": [], "links": [], "center": None,
                  "anonymous": graph.anonymous}
    node_index = {}
    for index, person in enumerate(g.db.query(Person).filter_by(
        graph_id=graph_id).order_by(Person.id)):
        node = {
                "id": person.id,
                "edit_url": url_for("edit_person",
                    graph=graph.id, person=person.id),
                }
        #node["fixed"] = True
        if graph.center_id == person.id:
            node.update({"size": 15, "fixed": True, "center": True})
            graph_data["center"] = index
        node["name"] = person.name
        graph_data["nodes"].append(node)
        node_index[person.id] = index
    for rel in g.db.query(Relationship).filter_by(graph_id=graph_id).all():
        link = {"source": node_index[rel.source_id],
                "target": node_index[rel.target_id],
                "css": rel.type.cssname.lower(),
                "dotted": rel.dotted,
                }
        graph_data["links"].append(link)
    # Compute link siblings
    siblings = {}
    for link in graph_data["links"]:
        siblings_count = len([
            l for l in graph_data["links"] if l["source"] == link["source"]
            and l["target"] == link["target"]
            ])
        link["siblings"] = siblings_count
        if link["siblings"] > 0:
            # compute sibling_id
            if (link["source"], link["target"]) in siblings:
                siblings[(link["source"], link["target"])] += 1
                sibling_id = siblings[(link["source"], link["target"])]
            elif (link["target"], link["source"]) in siblings:
                siblings[(link["target"], link["source"])] += 1
                sibling_id = siblings[(link["target"], link["source"])]
            else:
                siblings[(link["source"], link["target"])] = sibling_id = 0
            link["sibling_id"] = sibling_id
    if graph_data["center"] is not None:
        compute_node_circles(
            graph_data["nodes"], graph_data["links"], graph_data["center"])
        compute_node_branch(graph_data["nodes"], graph_data["links"])
    return jsonify(**graph_data)
