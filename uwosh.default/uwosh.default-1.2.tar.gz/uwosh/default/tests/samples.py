from uwosh.core.utils import MethodView
from Products.CMFCore.utils import getToolByName
from zope.app.component.hooks import getSite



class SampleMethodView(MethodView):
    """
    Example MethodView to be used for testing...
    """
    def sayHello(self):
        return "Hello"
        
    def add(self, one, two):
        return one + two