import bunch

class MessageTemplate:

    """
    Class responsible for encapsulating
    multiple sub-templates, and when called,
    getting them all rendered.

    `env` must have a loader that supports an
    `add_templates` contextmanager for defining
    additional templates.

    `sub_templates` must be a dict, where
    the keys are names and the values
    are jinja2 templates.

    """

    def __init__(self, env, sub_templates):
        self.env = env
        self.sub_templates = sub_templates

    def render_part(self, name, **context):
        """
        Call this method with a given sub-template's
        name and the context to render it.

        Works by adding our sub-templates to the
        loader's search path just-in-time. This
        has an advantage over `Template.from_string`
        loading in that it supports base templates.

        """
        return self.env.get_template(name).render(**context)

    def render(self, **context):
        """
        Return a `bunch.Bunch` of the initialized
        sub-templates, rendered with the given
        context.

        """
        values = bunch.Bunch()
        with self.env.loader.add_templates(self.sub_templates):
            for name in list(self.sub_templates.keys()):
                values[name] = self.render_part(name, **context)
            return values
