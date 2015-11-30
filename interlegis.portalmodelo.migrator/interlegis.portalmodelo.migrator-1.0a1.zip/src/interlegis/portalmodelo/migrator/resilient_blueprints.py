import traceback

from collective.jsonmigrator import logger
from collective.transmogrifier.interfaces import ISection, ISectionBlueprint
from zope.component import getUtility, getGlobalSiteManager
from zope.interface import classProvides, implements


def wrap_and_reregister_blueprints(blueprint_ids, session):
    '''Should be called exactly once, before transmogrifier is called'''

    tracebacks = []
    gsm = getGlobalSiteManager()
    for blueprint_id in blueprint_ids:
        original_blueprint = getUtility(ISectionBlueprint, blueprint_id)
        resilient_blueprint = wrap_blueprint(original_blueprint,
                                             tracebacks,
                                             session)
        # override blueprint
        gsm.registerUtility(resilient_blueprint, ISectionBlueprint, blueprint_id)

    return tracebacks


def wrap_blueprint(original_blueprint, tracebacks, session):

    class ResilientWrapperBlueprint(object):

        classProvides(ISectionBlueprint)
        implements(ISection)

        def __init__(self, transmogrifier, name, options, previous):
            self.transmogrifier = transmogrifier
            self.name = name
            self.options = options
            self.previous = previous

            self.previous = previous
            self.context = transmogrifier.context

        def build_pipeline(self):
            return iter(original_blueprint(
                self.transmogrifier, self.name, self.options, self.previous))

        def __iter__(self):
            pipeline = self.build_pipeline()

            while True:
                try:
                    item = next(pipeline)
                    path = item.get('_path', '<< UNKNOWN PATH >>')
                    session['current_item_path'] = path
                    yield item
                except StopIteration:
                    raise
                except Exception as e:
                    msg = '\n'.join('    ' + l for l in e.message.split('\n'))
                    path = session['current_item_path']
                    logger.error('Error while processing [%s]: %s\n' % (path, msg))
                    tracebacks.append((path, traceback.format_exc()))

                    # forgive original_blueprint and give it another chance
                    pipeline = self.build_pipeline()

    return ResilientWrapperBlueprint
