"""
::WebPortfolio::

https://github.com/mardix/webportfolio

serve_{project_name}.py

This is the entry point of the application.

--------------------------------------------------------------------------------

** To run the development serve

> wp serve -a {project_name}

#---------

** To deploy with Propel ( https://github.com/mardix/propel )

> propel -w

#---------

** To deploy with Gunicorn

> gunicorn serve_{project_name}:app

"""

from webportfolio import WebPortfolio

# Import the application's views
import application.{project_name}.views

# 'app' variable name is required if you intend to use WebPortfolio Cli
app = WebPortfolio.init(__name__, project="{project_name}")

