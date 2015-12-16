# -*- encoding: utf-8 -*-

from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm

from collective.sgvizler import _

charts = SimpleVocabulary([
    # Google Visualization API
    SimpleTerm(value=u'google.visualization.AnnotatedTimeLine ', title=_(u'Google Annotated Time Line')),
    SimpleTerm(value=u'google.visualization.AreaChart', title=_(u'Google Area Chart')),
    SimpleTerm(value=u'google.visualization.BarChart', title=_(u'Google Bar Chart')),
    SimpleTerm(value=u'google.visualization.BubbleChart', title=_(u'Google Bubble Chart')),
    SimpleTerm(value=u'google.visualization.CandlestickChart ', title=_(u'Google Candelstick Chart')),
    SimpleTerm(value=u'google.visualization.ColumnChart', title=_(u'Google Column Chart')),
    SimpleTerm(value=u'google.visualization.Gauge', title=_(u'Google Gauge')),
    SimpleTerm(value=u'google.visualization.GeoChart ', title=_(u'Google Geo Chart')),
    SimpleTerm(value=u'google.visualization.GeoMap ', title=_(u'Google Geo Map')),
    SimpleTerm(value=u'google.visualization.ImageSparkLine', title=_(u'Google Image Spark Line')),
    SimpleTerm(value=u'google.visualization.LineChart', title=_(u'Google Line Chart')),
    SimpleTerm(value=u'google.visualization.Map', title=_(u'Google Map')),
    SimpleTerm(value=u'google.visualization.MotionChart', title=_(u'Google Motion Chart')),
    SimpleTerm(value=u'google.visualization.OrgChart', title=_(u'Google Org Chart')),
    SimpleTerm(value=u'google.visualization.PieChart', title=_(u'Google Pie Chart')),
    SimpleTerm(value=u'google.visualization.ScatterChart', title=_(u'Google Scatter Chart')),
    SimpleTerm(value=u'google.visualization.SteppedAreaChart', title=_(u'Google Stepped Area Chart')),
    SimpleTerm(value=u'google.visualization.Table', title=_(u'Google Table')),
    SimpleTerm(value=u'google.visualization.TreeMap', title=_(u'Google Tree Map')),
    # SGVizler Visualization Integration
    SimpleTerm(value=u'sgvizler.visualization.DefList', title=_(u'Sgvizler Definition List')),
    SimpleTerm(value=u'sgvizler.visualization.D3ForceGraph', title=_(u'Sgvizler D3 Force-directed Graph')),
    SimpleTerm(value=u'sgvizler.visualization.DraculaGraph', title=_(u'Sgvizler Dracula Graph')),
    SimpleTerm(value=u'sgvizler.visualization.List', title=_(u'Sgvizler List')),
    SimpleTerm(value=u'sgvizler.visualization.Map', title=_(u'Sgvizler Map')),
    SimpleTerm(value=u'sgvizler.visualization.MapWKT', title=_(u'Sgvizler Well-known Text (WKT) Map')),
    SimpleTerm(value=u'sgvizler.visualization.Table', title=_(u'Sgvizler Table')),
    SimpleTerm(value=u'sgvizler.visualization.Text', title=_(u'Sgvizler Generic HTML')),
])

output_mode = SimpleVocabulary([
    SimpleTerm(value=u'json', title=_(u'JSON')),
    SimpleTerm(value=u'jsonp', title=_(u'JSON P')),
    SimpleTerm(value=u'xml', title=_(u'XML')),
])
