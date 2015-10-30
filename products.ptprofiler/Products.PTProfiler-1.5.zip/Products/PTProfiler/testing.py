from plone.testing import z2
from plone.testing import Layer


class PTProfilerLayer(Layer):

    defaultBases = (z2.STARTUP,)

    def setUp(self):
        with z2.zopeApp() as app:
            z2.installProduct(app, 'Products.PTProfiler')

    def tearDown(self):
        with z2.zopeApp() as app:
            z2.installProduct(app, 'Products.PTProfiler')


PTPROFILER = PTProfilerLayer(name='PTPROFILER')

PTPROFILER_INTEGRATION = z2.IntegrationTesting(
    bases=(PTPROFILER, ),
    name='PTPROFILER_INTEGRATION'
)
