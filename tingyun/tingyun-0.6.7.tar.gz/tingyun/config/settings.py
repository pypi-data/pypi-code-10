import copy
import logging
import os
import re

from tingyun import get_version

console = logging.getLogger(__name__)
filter_pro = ["log_level_mapping", ]


class Settings(object):
    """
    """
    def __repr__(self):
        return repr(self.__dict__)

    def __iter__(self):
        """return the iteration for setting item
        """
        return iter(flatten_settings(self).items())


class ErrorCollectorSettings(Settings):
    pass


class ActionTracerSettings(Settings):
    pass


class TransactionTracerSettings(Settings):
    pass


_settings = Settings()
_settings.transaction_tracer = TransactionTracerSettings()
_settings.error_collector = ErrorCollectorSettings()
_settings.action_tracer = ActionTracerSettings()

# configure file
_settings.app_name = "Python App"
_settings.plugins = ''  # split with ','
_settings.license_key = "This is default license"
_settings.enabled = True
_settings.log_file = None
_settings.log_level = logging.INFO
_settings.audit_mode = False
_settings.ssl = True
_settings.daemon_debug = False
_settings.host = "redirect.networkbench.com"
_settings.port = None
_settings.tingyun_id_secret = ''

# python environment variable
_settings.config_file = None
_settings.enable_profile = True
_settings.max_profile_depth = 600

# internal use constance
_settings.shutdown_timeout = float(os.environ.get("TINGYUN_AGENT_SHUTDOWN_TIMEOUT", 2.5))
_settings.startup_timeout = float(os.environ.get("TINGYUN_AGENT_STARTUP_TIMEOUT", 0.0))
_settings.data_version = 1.0
_settings.agent_version = get_version()
_settings.data_report_timeout = 15.0
_settings.stack_trace_count = 30  # used to limit the depth of action tracer stack
_settings.explain_plan_count = 30  # used to limit the depth of sql explain tracer stack
_settings.action_tracer_nodes = 2000
_settings.slow_sql_count = 20
_settings.action_apdex = {}
_settings.web_action_uri_params_captured = {}
_settings.external_url_params_captured = {}

# server configuration & some limitation about the data
# set the default value for it.
_settings.action_tracer.enabled = True
_settings.action_tracer.action_threshold = 2 * 1000  # 2s
_settings.action_tracer.top_n = 40
_settings.action_tracer.stack_trace_threshold = 500  # 500ms

_settings.action_tracer.slow_sql = True
_settings.action_tracer.slow_sql_threshold = 500
_settings.action_tracer.log_sql = False
_settings.action_tracer.explain_enabled = True
_settings.action_tracer.explain_threshold = 500  # 500ms
_settings.action_tracer.record_sql = "obfuscated"

# transaction tracer settings
_settings.transaction_tracer.enabled = False

_settings.auto_action_naming = True
_settings.urls_captured = []
_settings.ignored_params = []

_settings.error_collector.enabled = True
_settings.error_collector.ignored_status_codes = []

_settings.apdex_t = 500
_settings.capture_params = False


_settings.log_level_mapping = {
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
}


def flatten_settings(settings):
    """get the iteration for setting item, include Settings object in Setting
    """

    def _flatten(settings_item, name, setting_object):
        for key, value in setting_object.__dict__.items():
            if key in filter_pro:
                console.debug("skip flatten property %s", key)
                continue

            if isinstance(value, Settings):
                if name:
                    _flatten(settings_item, '%s.%s' % (name, key), value)
                else:
                    _flatten(settings_item, key, value)
            else:
                if name:
                    settings_item['%s.%s' % (name, key)] = value
                else:
                    settings_item[key] = value

        return settings_item

    return _flatten({}, None, settings)


def get_upload_settings():
    """ construct the settings for upload to server
    :return: settings
    """
    dump_settings = {}
    
    settings = flatten_settings(_settings)
    for key in settings:
        dump_settings["nbs.%s" % key] = settings[key]

    return dump_settings


def apply_config_setting(settings_object, name, value):
    target = settings_object
    fields = name.split('.', 1)

    while len(fields) > 1:
        # for additional Settings from server
        if not hasattr(target, fields[0]):
            setattr(target, fields[0], Settings())
        target = getattr(target, fields[0])
        fields = fields[1].split('.', 1)

    # transfer the string ignored ignored_status_codes to list
    if fields[0] == "ignored_status_codes" and value:
        try:
            value = [int(v) for v in value.split(",")]
        except Exception as err:
            console.warning("got invalid ignore status code %s, errors %s", value, err)
    elif fields[0] == "ignored_status_codes" and not value:
        value = []

    # transfer the urls_captured to list
    # Warning in windows, the split with \n will get incorrect result
    if fields[0] == "urls_captured" and value:
        try:
            value = [re.compile(r"%s" % v) for v in value.split("\n")]
        except Exception as err:
            console.warning("compile re url failed, %s, %s", value, err)
    elif fields[0] == "urls_captured" and not value:
        value = []

    # transfer the ignored_params to list
    if fields[0] == "ignored_params" and value:
        value = [str(v) for v in value.split(",")]
    elif fields[0] == "ignored_params" and not value:
        value = []

    setattr(target, fields[0], value)


def uri_params_captured(original):
    """parse the web_action_uri_params_captured with protocal
    :param original:
    :return: formatted uri with param
    """
    uri_params = {}
    try:
        for uri_param in original.split('|'):
            parts = uri_param.split(",")
            uri = parts.pop(0).encode('utf-8')
            uri_params[uri] = str(parts)
    except Exception as err:
        console.error("Parse the uri occurred errors. %s", err)

    return uri_params


def merge_settings(server_side_config=None):
    """
    :param server_side_config: the config downloaded from server
    :return: the merged settings
    """
    settings_snapshot = copy.deepcopy(_settings)
    global_conf_name = ["applicationId", "enabled", "appSessionKey", "dataSentInterval", "apdex_t", "tingyunIdSecret"]

    if not server_side_config:
        console.warn("update server config failed %s, local settings will be used.", server_side_config)
        return settings_snapshot

    # pop the structured config
    server_conf = server_side_config.pop("config", {})

    # get the individual settings
    if 'actionApdex' in server_side_config:
        original_apdex = server_side_config.pop("actionApdex", {})
        urls_apdexs = dict((key, original_apdex[key]) for key in original_apdex)
        action_apdex_urls = dict((key.encode("utf8"), urls_apdexs[key]) for key in urls_apdexs if key)

        server_side_config.update({"action_apdex": action_apdex_urls})

    for name in global_conf_name:
        if name not in server_side_config:
            console.warning("Lost server configure %s", name)
            continue

        apply_config_setting(settings_snapshot, name, server_side_config.get(name, ""))

    # transfer specified params captured with same uri
    if 'nbs.web_action_uri_params_captured' in server_conf:
        web_uri_params_captured = server_conf.pop("nbs.web_action_uri_params_captured", '')
        settings_snapshot.web_action_uri_params_captured = uri_params_captured(web_uri_params_captured)

    if 'nbs.external_url_params_captured' in server_conf:
        external_uri_params_captured = server_conf.pop("nbs.external_url_params_captured", '')
        settings_snapshot.external_url_params_captured = uri_params_captured(external_uri_params_captured)

    for item in server_conf:
        value = server_conf[item]
        # drop the first part of name with point
        start_pos = str(item).find('.') + 1
        apply_config_setting(settings_snapshot, item[start_pos:], value)

    console.debug("return merged settings %s", settings_snapshot)
    return settings_snapshot


def global_settings():
    return _settings