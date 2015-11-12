import jinja2
import os
from .templates import classpath_template, project_template

def _render_project_file(project_name):
    template = jinja2.Template(project_template)
    return template.render(project_name=project_name)


def _write_classpath_file(destination):
    classpath_file = os.path.join(destination, ".classpath")
    with open(os.path.join(classpath_file), "w") as f:
        f.write(classpath_template)


def _write_project_file(destination, project_name):
    project_file = os.path.join(destination, ".project")
    with open(project_file, "w") as f:
        f.write(_render_project_file(project_name))


def write_metadata_files(destination, project_name, force_write):
    if destination is None:
        destination = project_name

    classpath_file = os.path.join(destination, ".classpath")
    project_file = os.path.join(destination, ".project")

    if not os.path.exists(classpath_file) or force_write:
        _write_classpath_file(destination)
    if not os.path.exists(project_file) or force_write:
        _write_project_file(destination, project_name)