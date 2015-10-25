from formbar.rules import Rule

class Field(object):

    """Formbar field object"""

    def __init__(self, id, name, label=None, value=None):
        """TODO: to be defined1.

        :id: TODO
        :name: TODO
        :label: TODO
        :value: TODO

        """
        self.id = id
        """Id of the field. Usally only used to refer to the field.
        Example labels."""
        self.name = name
        """Name of the field. values will be submitted using this name"""
        if label is None:
            label = name.capitalize()
        self.label = label 
        """Label of the field. If no label is provied the a capitalized
        form of the name is used. To not render a label at all define a
        label with an empty string."""
        self.type = type
        """The datatype for this field. The data type is important for
        converting the submitted data into a python value. Note that
        this option is ignored if the form is used to render an
        SQLAlchemy mapped item."""
        self.value = value
        """Default value of the field. Note that this value might be
        overwritten while rendering the form if the field is within the
        submitted values on a form submission. Defaults to empty
        string. This attribute is also used for Infofields to define the
        value which should be displayed (If no expression is defined)"""
        self.renderer = None
        """Renderer configuration used for this field"""

        self.number = None
        """A ordering number for the field. In some form it is helpfull
        to be able to refer to a specific field by its number. The
        number will be rendered next to the label of the field."""
        self.placeholder = None
        """Defines a placeholder for this field that overrides the default
        placeholder."""
        self.css = ""
        """A string which will be added to the class tag of the form"""
        self.required = False
        """Flag to mark the field as a required field. If this tag is
        set an additional rule will be added to the field and an astrix
        is rendered at the label of the field. Note that this option
        might not be needed to be set if the form is used to render a
        SQLAlchemy mapped item as this. In this case the required flag
        is already set by the underlying FormAlchemy library by checking
        if the database field is 'NOT NULL'. Defaults to False"""
        self.desired= False
        """Flag to mark the field as a desired field. If this tag is
        set an additional rule will be added to the field and an star
        symbol is rendered at the label of the field. Defaults to
        False"""
        self.readonly = False
        """Flag to set the field as a readonly field. If set the field
        will be rendered as a simple textfield which does not allow to
        change or enter any data. Defaults to False"""
        self.autocomplete = True
        """Flag to enable or disable the automcomplete feature for this
        field. Defaults to enabled autocompletion"""
        self.autofocus = False
        """Flag to enable focusing the field on pageload. Note that only
        one field in the form can have the autofocus attribute."""
        self.tags = []
        """Tags of the field. Fields can have tags. Tags can be used to
        mark fields in the form and become handy if a application wants
        to find fields having a specific tag."""
        self.help = None
        """Help text for the field"""
        self.rules = []
        """List of Rules attached to this field"""
        # Add automatic genertated rules based on the required or
        # desired flag
        if self.required:
            expr = "bool($%s)" % self.name
            msg = _("This field is required. You must provide a value")
            mode = "pre"
            self.rules.append(Rule(expr, msg, mode))
        if self.desired:
            expr = "bool($%s)" % self.name
            msg = _("This field is desired. Please provide a value")
            mode = "pre"
            triggers = "warning"
            self.rules.append(Rule(expr, msg, mode, triggers))

        def add_rule(self, rule):
            """Adds a new Rule instance to the field

            :rule: Rule instance
            """
            self.rule.append(rule) 

        def add_tag(self, tag):
            """Adds a new Tag to the field

            :tag: String of the tag
            """
            self.rule.append(tag.strip())

class TextField(Field):

    """Docstring for TextField. """

    def __init__(self):
        """TODO: to be defined1. """
        Field.__init__(self)

class TextareaField(Field):

    """Docstring for TextField. """

    def __init__(self):
        """TODO: to be defined1. """
        Field.__init__(self)

class NumberField(Field):

    """Docstring for TextField. """

    def __init__(self):
        """TODO: to be defined1. """
        Field.__init__(self)

class DateField(Field):

    """Docstring for TextField. """

    def __init__(self):
        """TODO: to be defined1. """
        Field.__init__(self)

class TimeField(Field):

    """Docstring for TextField. """

    def __init__(self):
        """TODO: to be defined1. """
        Field.__init__(self)

class IntervalField(Field):

    """Docstring for TextField. """

    def __init__(self):
        """TODO: to be defined1. """
        Field.__init__(self)

class HiddenField(Field):

    """Docstring for TextField. """

    def __init__(self):
        """TODO: to be defined1. """
        Field.__init__(self)

class HiddenField(Field):

    """Docstring for TextField. """

    def __init__(self):
        """TODO: to be defined1. """
        Field.__init__(self)

class OptionField(Field):

    """Docstring for TextField. """

    def __init__(self):
        """TODO: to be defined1. """
        Field.__init__(self)
        self.options = []

    def add_option(self, label, value):
        self.options.append((label, value))

class DropdownField(OptionField):

    """Docstring for TextField. """

    def __init__(self):
        """TODO: to be defined1. """
        OptionField.__init__(self)

class RadioField(OptionField):

    """Docstring for TextField. """

    def __init__(self):
        """TODO: to be defined1. """
        OptionField.__init__(self)

class CheckboxField(OptionField):

    """Docstring for TextField. """

    def __init__(self):
        """TODO: to be defined1. """
        OptionField.__init__(self)
