from random import choice
from sensei2.sensei.field_handlers import BaseHandler


class Plugin(BaseHandler):
    def __init__(self):
        super(Plugin, self).__init__()

        from xml.dom import minidom
        import urllib2

        print "Download latest youtube video.."

        doc = minidom.parse(
            urllib2.urlopen('http://gdata.youtube.com/feeds/api/charts/movies/trending?v=2&max-results=50'))
        self.data = ["http://www.youtube.com/watch?v=%s" % i.firstChild.firstChild.nodeValue.split(':')[-1] for i in
                     doc.getElementsByTagName('entry')]

    def prepare_value(self, obj, field, sensei):
        return choice(self.data)