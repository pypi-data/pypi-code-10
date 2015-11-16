from flask import abort
from flask import Flask
from flask import render_template
from flask import request


def create_app(config_file=None):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)

    @app.route("/")
    def nothing():
        return "SUCCESS"

    @app.route("/<blogpost>")
    def serve_blog(blogpost):
        user_agent = request.headers.get('User-Agent')
        iscurl = user_agent.lower().startswith('curl')
        root_directory = app.config['BLOGROOT']
        blogpost = "/".join((root_directory, blogpost))
        try:
            with open(blogpost) as article:
                content = "".join(article.read())
                if iscurl:
                    return content
                else:
                    return render_template("strapdown.html",
                                           theme=app.config['THEME'],
                                           text=content,
                                           title=app.config['BLOGTITLE'])
        except IOError:
            if iscurl:
                abort(404)
            else:
                return render_template('404.html'), 404
    return app

if __name__ == "__main__":
        app = create_app('.blogit.conf')
        app.run()
