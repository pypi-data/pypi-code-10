import logging
from StringIO import StringIO
from collections import defaultdict

from Products.Five.browser import BrowserView
from plone.z3cform.layout import wrap_form
from z3c.form import button, field, form
from zope.interface import Interface
from zope.schema import ASCIILine, TextLine, URI, Password

from collective.jsonmigrator import msgFact as _, logger
from pm2_migration import run_migration


class IPortalModeloMigrator(Interface):

    remote_url = URI(
        title=_(u"URL"),
        description=_(u"URL for the remote portal modelo 2 to migrate"),
        required=True,
    )

    remote_username = ASCIILine(
        title=_(u"Remote Username"),
        description=_(u"Username to log in to the remote site"),
        required=True,
    )

    remote_password = Password(
        title=_(u"Remote Password"),
        description=_(u"Password to log in to the remote site"),
        required=True,
    )

    remote_path = TextLine(
        title=_(u"Remote path"),
        description=_(u"Path where to start crawling and importing"),
        required=True,
    )

    destiny_path = TextLine(
        title=_(u"Destiny path HERE"),
        description=_(u"Path (on this site) where the migrated content will be put"),
        required=True,
        default=u'/institucional'
    )


class PortalModeloMigrator(form.Form):

    label = _(u"Migrate from Portal Modelo 2")
    fields = field.Fields(IPortalModeloMigrator)
    ignoreContext = True

    @button.buttonAndHandler(u'Run')
    def handleRun(self, action):
        data, errors = self.extractData()
        if errors:
            return False
        overrides = {
            'remotesource': {k.replace('_', '-'): v for k, v in data.iteritems()},
            'pm2_custom': {
                'remote-path': data['remote_path'],
                'destiny-path': data['destiny_path'],
            }
        }

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        log_handler = logging.StreamHandler(StringIO())
        log_handler.setFormatter(formatter)
        logger.addHandler(log_handler)

        classify_by_level_handler = ClassifyByLevelHandler()
        classify_by_level_handler.setFormatter(formatter)
        logger.addHandler(classify_by_level_handler)

        session = self.request.SESSION
        tracebacks = run_migration(self.context, overrides, session)

        log_handler.flush()

        session['log_message_output'] = log_handler.stream.getvalue()
        session['all_but_info'] = classify_by_level_handler.all_but_info()
        session['traceback_output'] = get_traceback_output(tracebacks)

        self.request.RESPONSE.redirect('/'.join((self.context.absolute_url(), '@@migrate_result')))


PortalModeloMigratorView = wrap_form(PortalModeloMigrator)


class PortalModeloMigratorResultView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        session = self.request.SESSION
        if not session.has_key('log_message_output'):  # noqa
            return '''
------------------------------------------ NO DATA ------------------------------------------------
'''
        msgs = [l for l in session['log_message_output'].split('\n')
                if ' - INFO - :: Skipping -> ' not in l]

        actually_skipped = [a.split(' -> ')[-1] for a in msgs if 'ACTUALLY SKIPPED -> ' in a]
        filtered_msgs = [l for l in msgs if all(a not in l for a in actually_skipped)]

        all_but_info_mgs = session['all_but_info']
        traceback_output = session['traceback_output']

        return '''
##################################### ERRORS + WARNINGS ###########################################
%s


######################################## ALL MESSAGES #############################################
%s
######################################## TRACEBACKS ###############################################
%s
''' % ('\n'.join(all_but_info_mgs),
       '\n'.join(filtered_msgs),
       '\n'.join(traceback_output))


class ClassifyByLevelHandler(logging.Handler):

    def __init__(self):
        super(ClassifyByLevelHandler, self).__init__()
        self.messages = defaultdict(list)

    def emit(self, record):
        self.messages[record.levelname].append(self.format(record))

    def all_but_info(self):
        return [msg for key in self.messages.keys()
                for msg in self.messages[key]
                if key != 'INFO']


def get_traceback_output(tracebacks):
    template = '''
-------------------------------------------------------------------------------
PATH: %s
-------------------------------------------------------------------------------
TRACEBACK:

%s
'''
    return [template % (path, traceback) for
        path, traceback in tracebacks]
