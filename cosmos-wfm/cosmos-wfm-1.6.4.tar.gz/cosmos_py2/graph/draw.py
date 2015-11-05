#
# Task stuff
#

from __future__ import absolute_import
from ..util.helpers import groupby2
from .. import TaskStatus
from itertools import imap

try:
    import pygraphviz as _

    pygraphviz_available = True
except ImportError:
    pygraphviz_available = False


def draw_task_graph(task_graph, save_to=None, format=u'svg', url=False):
    a = taskgraph_to_agraph(task_graph, url=url)
    a.layout(u'dot')
    return a.draw(path=save_to, format=format)


def taskgraph_to_agraph(task_graph, url=True):
    u"""
    Converts a networkx graph into a pygraphviz Agraph
    """
    import pygraphviz as pgv

    agraph = pgv.AGraph(strict=False, directed=True, fontname=u"Courier")
    agraph.node_attr[u'fontname'] = u"Courier"
    # agraph.node_attr['fontcolor'] = '#000000'
    agraph.node_attr[u'fontsize'] = 8
    agraph.graph_attr[u'fontsize'] = 8
    agraph.edge_attr[u'fontcolor'] = u'#586e75'

    agraph.add_edges_from(task_graph.edges())
    for stage, tasks in groupby2(task_graph.nodes(), lambda x: x.stage):
        sg = agraph.add_subgraph(name=u"cluster_{0}".format(stage), label=unicode(stage), color=u'grey', style=u'dotted')
        for task in tasks:
            def truncate_val(kv):
                v = u"{0}".format(kv[1])
                v = v if len(v) < 10 else v[1:8] + u'..'
                return u"{0}: {1}".format(kv[0], v)

            label = u" \\n".join(imap(truncate_val, task.tags.items()))
            status2color = {TaskStatus.no_attempt: u'black',
                            TaskStatus.waiting: u'gold1',
                            TaskStatus.submitted: u'navy',
                            TaskStatus.successful: u'darkgreen',
                            TaskStatus.failed: u'darkred',
                            TaskStatus.killed: u'darkred'}

            sg.add_node(task, label=label, URL=task.url if url else u'#', target=u"_blank",
                        color=status2color.get(task.status, u'black'))

    return agraph


def taskgraph_to_image(taskgraph, path=None, url=False):
    taskgraph.layout(prog=u"dot")
    agraph = taskgraph_to_agraph(taskgraph, url=url)
    return agraph.draw(path=path, format=u'svg')


#
# Stage stuff
#
from .. import RelationshipType
from ..models.Stage import StageStatus


def draw_stage_graph(stage_graph, save_to=None, url=False, format=u'svg'):
    g = stagegraph_to_agraph(stage_graph, url=url)
    g.layout(prog=u"dot")
    return g.draw(path=save_to, format=format)


def stagegraph_to_agraph(stage_graph, url=True):
    u"""
    :param stage_graph: recipe_stage_G or stage_G
    """

    import pygraphviz as pgv

    agraph = pgv.AGraph(strict=False, directed=True, fontname=u"Courier", fontsize=11)
    agraph.node_attr[u'fontname'] = u"Courier"
    agraph.node_attr[u'fontsize'] = 8
    agraph.edge_attr[u'fontcolor'] = u'#586e75'

    status2color = {StageStatus.no_attempt: u'black',
                    StageStatus.running: u'navy',
                    StageStatus.successful: u'darkgreen',
                    StageStatus.failed: u'darkred'}
    rel2abbrev = {RelationshipType.one2one: u'o2o',
                  RelationshipType.one2many: u'o2m',
                  RelationshipType.many2one: u'm2o',
                  RelationshipType.many2many: u'm2m'}

    for stage in stage_graph.nodes():
        agraph.add_node(stage, color=status2color.get(getattr(stage, u'status', None), u'black'),
                        URL=stage.url if url else u'', label=stage.label)

    for u, v in stage_graph.edges():
        v.relationship_type = None
        if v.relationship_type == RelationshipType.many2one:
            agraph.add_edge(u, v, label=rel2abbrev.get(v.relationship_type, u''), style=u'dotted', arrowhead=u'odiamond')
        elif v.relationship_type == RelationshipType.one2many:
            agraph.add_edge(u, v, label=rel2abbrev.get(v.relationship_type, u''), style=u'dashed', arrowhead=u'crow')
        else:
            agraph.add_edge(u, v, label=rel2abbrev.get(v.relationship_type, u''), arrowhead=u'vee')

    return agraph
