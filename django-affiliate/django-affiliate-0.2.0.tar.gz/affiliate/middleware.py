import logging

from . import app_settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import SimpleLazyObject
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from .models import NoAffiliate
from .utils import get_model

l = logging.getLogger(__name__)


AffiliateModel = get_model(app_settings.AFFILIATE_MODEL)

def get_affiliate(request, new_aid, prev_aid, prev_aid_dt):
    if not hasattr(request, '_cached_affiliate'):
        affiliate = AffiliateModel.objects.filter(pk=new_aid).first()
        if affiliate is None or not affiliate.is_active:
            prev_affiliate = None
            if prev_aid:
                prev_affiliate = AffiliateModel.objects.filter(pk=prev_aid).first()
            if prev_affiliate is None or not prev_affiliate.is_active:
                affiliate = affiliate or prev_affiliate or NoAffiliate()
            else:
                affiliate = prev_affiliate
                if app_settings.SAVE_IN_SESSION:
                    request.session['_aid'] = prev_aid
                    if prev_aid_dt:
                        request.session['_aid_dt'] = prev_aid_dt
        request._cached_affiliate = affiliate
    return request._cached_affiliate


class AffiliateMiddleware(object):

    def process_request(self, request):
        new_aid, prev_aid, prev_aid_dt = None, None, None
        if app_settings.SAVE_IN_SESSION:
            session = getattr(request, 'session', None)
            if not session:
                raise ImproperlyConfigured(
                    "session attribute should be set for request. Please add "
                    "'django.contrib.sessions.middleware.SessionMiddleware' "
                    "to your MIDDLEWARE_CLASSES")
            elif app_settings.SAVE_IN_SESSION:
                prev_aid = session.get('_aid', None)
                prev_aid_dt = session.get('_aid_dt', None)
        now = timezone.now()
        new_aid = request.GET.get(app_settings.PARAM_NAME, None)
        if new_aid:
            if app_settings.SAVE_IN_SESSION:
                session['_aid'] = new_aid
                session['_aid_dt'] = now.isoformat()
        if prev_aid and app_settings.SAVE_IN_SESSION:
            if prev_aid_dt is None:
                l.error('_aid_dt not found in session')
                if not new_aid:
                    session['_aid_dt'] = now.isoformat()
            else:
                prev_aid_dt_obj = parse_datetime(prev_aid_dt)
                if (now - prev_aid_dt_obj).total_seconds() > app_settings.SESSION_AGE:
                    # aid expired
                    prev_aid = None
                    prev_aid_dt = None
                    if not new_aid:
                        session.pop('_aid')
                        session.pop('_aid_dt')
        request.affiliate = SimpleLazyObject(lambda: get_affiliate(request, new_aid, prev_aid, prev_aid_dt))
