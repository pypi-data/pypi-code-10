"""Event Handlers.
"""
from datetime import datetime as _datetime
from pytsite import lang as _lang, console as _console, router as _router, validation as _validation, util as _util, \
    hreflang as _hreflang, reg as _reg
from . import _functions

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def app_setup():
    """'setup' Event Handler.
    """
    # Creating roles
    admin_role = ('admin', 'pytsite.auth@admin_role_description')
    user_role = ('user', 'pytsite.auth@user_role_description')
    for role in admin_role, user_role:
        if not _functions.get_role(name=role[0]):
            role_entity = _functions.create_role(role[0], role[1])
            if role_entity.f_get('name') == 'admin':
                role_entity.f_add('permissions', 'admin')
            role_entity.save()
            _console.print_success(_lang.t('pytsite.auth@role_has_been_created', {'name': role_entity.f_get('name')}))

    # Creating administrator

    email = input(_lang.t('pytsite.auth@enter_admin_email') + ': ')
    try:
        _validation.rule.NonEmpty(email, 'pytsite.auth@email_cannot_be_empty').validate()
        _validation.rule.Email(email).validate()
    except _validation.error.RuleError as e:
        raise _console.Error(e)

    admin_user = _functions.create_user(email)
    admin_user.f_set('first_name', _lang.t('pytsite.auth@administrator'))
    admin_user.f_set('nickname', _util.transform_str_2(admin_user.full_name))
    admin_user.f_add('roles', _functions.get_role('admin'))
    admin_user.save()
    _console.print_success(_lang.t('pytsite.auth@user_has_been_created', {'login': admin_user.f_get('login')}))


def router_dispatch():
    """pytsite.router.dispatch Event Handler.
    """
    # Update user activity timestamp
    user = _functions.get_current_user()
    if not user.is_anonymous:
        _router.no_cache = True
        user.f_set('last_activity', _datetime.now()).save(True, False)

    # Alternate languages
    base_path = _reg.get('auth.base_path', '/auth/login')
    if base_path == _router.current_path(True):
        for lng in _lang.langs(False):
            _hreflang.add(lng, _router.url(base_path, lang=lng))


def update(version: str):
    if version == '0.13.0':
        _update_0_13()


def _update_0_13():
    for user in _functions.find_users(False).get():
        if not user.nickname:
            if not user.full_name:
                user.f_set('first_name', _util.random_str())
            user.f_set('nickname', _util.transform_str_2(user.full_name)).save()
            _console.print_info('User updated: {}'.format(user.login))
