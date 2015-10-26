"""

"""


def defined_repertoire():
    """
    :return:
    """
    hookers = {
        "memcached": [
            {"target": "memcache", 'hook_func': 'detect', 'hook_module': 'tingyun.armoury.database_memcached'},
        ],

        # mysql db
        "mysql": [
            {"target": "MySQLdb", 'hook_func': 'detect', 'hook_module': 'tingyun.armoury.database_dbapi2'},
        ],
        "pymysql": [
            {"target": "pymysql", 'hook_func': 'detect', 'hook_module': 'tingyun.armoury.database_dbapi2'},
        ],
        "oursql": [
            {"target": "oursql", 'hook_func': 'detect', 'hook_module': 'tingyun.armoury.database_dbapi2'},
        ],

        # oracle
        "oracle": [
            {"target": "cx_Oracle", 'hook_func': 'detect', 'hook_module': 'tingyun.armoury.database_dbapi2'},
        ],

        # postgres SQL
        "postgresql": [
            {"target": "postgresql.interface.proboscis.dbapi2", 'hook_func': 'detect',
             'hook_module': 'tingyun.armoury.database_dbapi2'},
        ],
        # postgres SQL
        "psycopg2": [
            {"target": "psycopg2", 'hook_func': 'detect', 'hook_module': 'tingyun.armoury.database_dbapi2'},
        ],
        "psycopg2ct": [
            {"target": "psycopg2ct", 'hook_func': 'detect', 'hook_module': 'tingyun.armoury.database_dbapi2'},
        ],
        "psycopg2cffi": [
            {"target": "psycopg2cffi", 'hook_func': 'detect', 'hook_module': 'tingyun.armoury.database_dbapi2'},
        ],

        # ODBC A Python DB API 2 module for ODBC
        "pyodbc": [
            {"target": "pyodbc", 'hook_func': 'detect', 'hook_module': 'tingyun.armoury.database_dbapi2'},
        ],

        # nosql mongodb
        "mongodb": [
            {"target": "pymongo.mongo_client", 'hook_func': 'detect_mongo_client',
             'hook_module': 'tingyun.armoury.database_mongo'},
            {"target": "pymongo.connection", 'hook_func': 'detect_connection',
             'hook_module': 'tingyun.armoury.database_mongo'},
            {"target": "pymongo.collection", 'hook_func': 'detect_collection',
             'hook_module': 'tingyun.armoury.database_mongo'},
        ],

        # nosql redis
        "redis": [
            {"target": "redis.connection", 'hook_func': 'detect_connection',
             'hook_module': 'tingyun.armoury.database_redis'},
            {"target": "redis.client", 'hook_func': 'detect_client_operation',
             'hook_module': 'tingyun.armoury.database_redis'},
        ],

        # external call
        "urllib": [
            {"target": "urllib", 'hook_func': 'detect', 'hook_module': 'tingyun.armoury.external_urllib'},
        ],
        "urllib2": [
            {"target": "urllib2", 'hook_func': 'detect', 'hook_module': 'tingyun.armoury.external_urllib2'},
        ],
        "urllib3": [
            {"target": "urllib3.request", 'hook_func': 'detect', 'hook_module': 'tingyun.armoury.external_urllib3'},
        ],
        "thrift": [
            {"target": "thrift.transport.TSocket", 'hook_func': 'detect_tsocket',
             'hook_module': 'tingyun.armoury.external_thrift'},
        ],

        "requests": [
            {"target": "requests.api", 'hook_func': 'detect_requests_request',
             'hook_module': 'tingyun.armoury.external_requests'},
            {"target": "requests.sessions", 'hook_func': 'detect_requests_sessions',
             'hook_module': 'tingyun.armoury.external_requests'},
        ],
        "httplib2": [
            {"target": "httplib2", 'hook_func': 'detect_httplib2_http',
             'hook_module': 'tingyun.armoury.external_httplib2'},
            {"target": "httplib2", 'hook_func': 'detect_http_connect_with_timeout',
             'hook_module': 'tingyun.armoury.external_httplib2'},
            {"target": "httplib2", 'hook_func': 'detect_https_connect_with_timeout',
             'hook_module': 'tingyun.armoury.external_httplib2'},
        ],

        # django, this weapon must not be removed.
        "django": [
            {"target": "django.core.handlers.base", 'hook_func': 'detect_middleware',
             'hook_module': 'tingyun.armoury.framework_django'},
            {"target": "django.core.handlers.wsgi", 'hook_func': 'detect_wsgi_entrance',
             'hook_module': 'tingyun.armoury.framework_django'},
            {"target": "django.core.urlresolvers", 'hook_func': 'detect_urlresolvers',
             'hook_module': 'tingyun.armoury.framework_django'},
            {"target": "django.views.generic.base", 'hook_func': 'detect_views_dispatch',
             'hook_module': 'tingyun.armoury.framework_django'},

            {"target": "django.template.loader_tags", 'hook_func': 'detect_template_block_render',
             'hook_module': 'tingyun.armoury.framework_django'},
            {"target": "django.template.base", 'hook_func': 'detect_django_template',
             'hook_module': 'tingyun.armoury.framework_django'},

            {"target": "django.http.multipartparser", 'hook_func': 'detect_http_multipartparser',
             'hook_module': 'tingyun.armoury.framework_django'},

            {"target": "django.core.mail", 'hook_func': 'detect_core_mail',
             'hook_module': 'tingyun.armoury.framework_django'},
            {"target": "django.core.mail.message", 'hook_func': 'detect_core_mail_message',
             'hook_module': 'tingyun.armoury.framework_django'},
        ],

        # flask, 0.6-1.0
        "flask": [
            {"target": "flask.app", 'hook_func': 'detect_wsgi_entrance',
             'hook_module': 'tingyun.armoury.framework_flask'},
            {"target": "flask.app", 'hook_func': 'detect_app_entrance',
             'hook_module': 'tingyun.armoury.framework_flask'},
            {"target": "flask.app", 'hook_func': 'detect_templates',
             'hook_module': 'tingyun.armoury.framework_flask'},
        ],

        # jinja2 2.3-2.8
        'jinja2': [
            {"target": "jinja2.loaders", 'hook_func': 'detect_template_loader',
             'hook_module': 'tingyun.armoury.template_jinja2'},
            {"target": "jinja2.environment", 'hook_func': 'detect_jinja2',
             'hook_module': 'tingyun.armoury.template_jinja2'},
            ],

        # version 2.8.1-2.12.x
        # 'web2py': [
        #     {"target": "gluon.main", 'hook_func': 'detect_wsgi_entrance',
        #      'hook_module': 'tingyun.armoury.framework_web2py'},
        #     {"target": "gluon.compileapp", 'hook_func': 'detect_compileapp',
        #      'hook_module': 'tingyun.armoury.framework_web2py'},
        #     {"target": "gluon.template", 'hook_func': 'detect_template',
        #      'hook_module': 'tingyun.armoury.framework_web2py'},
        # ],

        # version 0.3.x
        'webpy': [
            {"target": "web.application", 'hook_func': 'detect_wsgi_entrance',
             'hook_module': 'tingyun.armoury.framework_webpy'},

            {"target": "web.application", 'hook_func': 'detect_application',
             'hook_module': 'tingyun.armoury.framework_webpy'},
        ],

        # "tornado": [
        #     {"target": "tornado.wsgi", 'hook_func': 'detect_wsgi_entrance',
        #      'hook_module': 'tingyun.armoury.framework_tornado'},
        #     {"target": "tornado.httpserver", 'hook_func': 'detect_tornado3_main_process',
        #      'hook_module': 'tingyun.armoury.framework_tornado'},
        # ],

        # mako v0.7.x-v1.0.x
        "mako": [
            {"target": "mako.template", 'hook_func': 'detect_template',
             'hook_module': 'tingyun.armoury.template_mako'},
        ],
    }

    return hookers
