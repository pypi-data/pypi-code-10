try: # Zope 2.12
    from Zope.ZPublisher.HTTPResponse import HTTPResponse
except:
    from ZPublisher.HTTPResponse import HTTPResponse
    
from Products.CMFCore.utils import getToolByName
from os import path
from DateTime import DateTime

_this_dir = path.dirname(path.abspath(__file__))
error_template = open(path.join(_this_dir, 'error_template.html')).read()

from zope.app.component.hooks import getSite

last_sent_404 = DateTime()
last_sent_500 = DateTime()
one_minute = 1.0/24.0/60.0
one_day = 0.8 # just less than a day since most servers are restarted every day

original_error_html = HTTPResponse._error_html

ERRORS = {}
# an error will be held for the during of the running instance
# and only unique errors will be reported

# an error entry will look like 
# 'url' : {
#   'last_reported' : 'time'
#   'number_reported' : 5
#   'body' : 'bodytext of error',
#   'status' : 404,
#   'referrer' : url,
#   'email_sent' : False
#}

def format_error(url, error):
    return """url: %s, last_reported : %s, status: %s, number reported: %s""" % (url, error['last_reported'], error['status'], error['number_reported'])

def _error_html(self, title, body):
    try:
        # wrap it all up just in case it screws up
        # it'd be even worse to not send a response!
        site = getSite()
        if not site:
            return
            
        from uwosh.default import monkey
        now = DateTime()
        mailhost = getToolByName(site, 'MailHost', None)
        pp = getToolByName(site, 'portal_properties', None)
        to_ = pp.site_properties.getProperty('error_recipients', ['ploneerrors@uwosh.edu', ])
        req = site.REQUEST

        if self.status != 500 and not req.environ.get('HTTP_REFERER', False):
            pass
        elif not monkey.ERRORS.has_key(req.URL):
            monkey.ERRORS[req.URL] = {}
            monkey.ERRORS[req.URL]['body'] = body
            monkey.ERRORS[req.URL]['status']  = self.status
            monkey.ERRORS[req.URL]['number_reported'] = 1
            monkey.ERRORS[req.URL]['last_reported'] = DateTime()
            monkey.ERRORS[req.URL]['referrer'] = req.environ.get('HTTP_REFERER', '')
            monkey.ERRORS[req.URL]['email_sent'] = False
        else:
            monkey.ERRORS[req.URL]['number_reported'] += 1
            monkey.ERRORS[req.URL]['last_reported'] = DateTime()
            monkey.ERRORS[req.URL]['referrer'] = req.environ.get('HTTP_REFERER', '')
        
        if self.status != 500 and (monkey.last_sent_404 + one_day) <= now:
            monkey.last_sent_404 = now
            body = body + "\n\nComplete set of errors\n\n" + '\n'.join([format_error(k, error) for k, error in monkey.ERRORS.items()])
            if hasattr(mailhost, 'secureSend'):
                mailhost.secureSend(body, to_, 'ploneerror@uwosh.edu', 'Plone UW Oshkosh ERROR!')
            else:
                mailhost.send(body, to_, 'ploneerror@uwosh.edu', 'Plone UW Oshkosh ERROR!')
                
        elif self.status == 500 and (monkey.last_sent_500 + one_minute) <= now and not monkey.ERRORS[req.URL]['email_sent']:
            monkey.last_sent_500 = now
            monkey.ERRORS[req.URL]['email_sent'] = True
            if hasattr(mailhost, 'secureSend'):
                mailhost.secureSend(body, to_, 'ploneerror@uwosh.edu', 'Plone UW Oshkosh ERROR!')
            else:
                mailhost.send(body, to_, 'ploneerror@uwosh.edu', 'Plone UW Oshkosh ERROR!')
    
        return error_template.replace('{{title}}', title).replace('{{body}}', body)
    except:
        return original_error_html(self, title, body)
    

def installExceptionHook():
    from ZPublisher.HTTPResponse import HTTPResponse    
    HTTPResponse._error_html = _error_html
