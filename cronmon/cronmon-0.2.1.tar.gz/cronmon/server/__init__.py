'''
Look at your logs in the brower
'''
import datetime
import os
from flask import Flask, make_response, render_template, json
from jinja2 import FileSystemLoader


class WebApp(object):
    def __init__(self, port=5000, location='~/cronmon'):
        self.template_path = os.path.join(os.path.dirname(__file__), "templates")
        self.app = Flask(__name__)
        self.app.jinja_loader = FileSystemLoader(self.template_path)
        self.location = location

    def serve(self):
        self._map_urls()
        self.app.debug = True
        self.app.run(host="0.0.0.0")

    def project_log(self, project, log):
        return {}

    def project(self, project):
        output = []
        for log in self._logs_for(project):
            output.append({
                'url': "/{}/{}".format(project, log),
                'created_at': datetime.datetime.fromtimestamp(int(log.split('.')[0])).strftime('%Y-%m-%d %H:%M:%S')
            })
        return make_response(
            json.dumps(output), 200, {'Content-type': 'application/json'})

    def index(self):
        return render_template(
            'index.html',
            directories=self._projects()
        )

    def _map_urls(self):
        self.app.add_url_rule('/<project>/<log>', "project_log", self.project_log)
        self.app.add_url_rule('/<project>', "project", self.project)
        self.app.add_url_rule('/', "index", self.index)

    def _projects(self):
        return os.listdir(self.location)

    def _logs_for(self, project):
        return os.listdir(os.path.join(self.location, project))


def start(port, location):
    WebApp(port, location).serve()


if __name__ == '__main__':
    print(__doc__)
