import sys
if not '../' in sys.path:
    sys.path.insert(0, '../../')

from flask import Flask
from flask.ext import restful
import argparse
import signal
from flask import request
from server.utils.AMSSettings import *
from server.utils.AMSSingletons import AMSAppConfig
from server.routes.AMSSimpleRoute import AMSSimpleRoute, EndToEndProtected, TestProtected

app = Flask(__name__)

#app.config['DEBUG'] = True
app.config.update(PROPAGATE_EXCEPTIONS=True)
api = restful.Api(app, prefix='/v1')
#api = restful.Api(app, prefix='/v1', decorators=[dkcrossdomain(origin='*')])

@app.after_request
def after(response):
    return response

# routing
api.add_resource(AMSSimpleRoute, '/endtoend')
api.add_resource(EndToEndProtected, '/endtoendprotected')
api.add_resource(TestProtected, '/testurl/<string:recipeuuid>')

sample_config = """
    Sample AMSConfig.json
        {
            "port-number:" "14001"
        }
            """

def main(parser, config_json_path='./AMSConfig.json'):

    if parser is not None:
        mutually_exclusive_group = parser.add_mutually_exclusive_group()

        mutually_exclusive_group.add_argument('--config', '-config', action='store', dest='config_json',
                                          help='AMSConfig json string')
        results = parser.parse_args()
        cj = results.config_json
    else:
        cj = config_json_path
    if cj is not None:
        if AMSAppConfig().init_from_file(cj) is False:
            print 'ERROR AMSApp.py unable to read config file'
            print sample_config
        else:
            print "AMSApp config is: %s" % AMSAppConfig().__str__()
            try:
                port_number = int(AMSAppConfig().get(AMSAPP_PORT))
            except Exception:
                print 'ERROR AMSApp.py requires a port-number in config'
                port_number = -1

            if port_number != -1:
                print 'AMSServer starting on port %i' % port_number
                app.run(host='0.0.0.0', port=port_number)
    else:
        print 'ERROR AMSapp.py Requires a AMSConfig json with - config option'
        print sample_config

if __name__ == '__main__':
    def signal_handler(signal, frame):
        sys.stdout.write('ending ... \n')
        try:
            func = request.environ.get('werkzeug.server.shutdown')
            if func is not None:
                func()
        except Exception, e:
            pass
        sys.exit(130)
    signal.signal(signal.SIGINT, signal_handler)
    cmdline_parser = argparse.ArgumentParser(description="Welcome to the Analytic Micro Server")
    main(cmdline_parser)
