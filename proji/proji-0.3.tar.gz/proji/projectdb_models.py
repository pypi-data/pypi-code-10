from booby import Model,fields
from booby.validators import nullable

from restkit import Resource, BasicAuth
try:
    import simplejson as json
except ImportError:
    import json # py2.6 only


# Extra models ========================================
class DateValidator(object):
    """This validator forces fields values to be an instance of `basestring`."""

    @nullable
    def validate(self, value):
        if not isinstance(value, basestring):
            raise errors.ValidationError('should be a string')

class Date(fields.Field):
    """:class:`Field` subclass with builtin `date` validation."""

    def __init__(self, *args, **kwargs):
        super(Date, self).__init__(DateValidator(), *args, **kwargs)



# Models ========================================

class division(Model):

    id = fields.Integer()
    code = fields.String()
    name = fields.String()
    parent = fields.Field()


class externalReference(Model):

    id = fields.Integer()
    projectId = fields.Integer()
    description = fields.String()
    uri = fields.String()
    date = Date()


class facility(Model):

    id = fields.Integer()
    name = fields.String()


class institutionalRole(Model):

    id = fields.Integer()
    name = fields.String()


class institution(Model):

    id = fields.Integer()
    code = fields.String()
    name = fields.String()


class kpiCategory(Model):

    id = fields.Integer()
    kpiId = fields.Integer()
    name = fields.String()


class kpi(Model):

    id = fields.Integer()
    measures = fields.String()
    number = fields.Integer()
    title = fields.String()
    type = fields.String()


class person(Model):

    id = fields.Integer()
    affiliations = fields.Collection(fields.Field)
    email = fields.Email()
    endDate = Date()
    fullName = fields.String()
    lastModified = fields.Integer()
    notes = fields.String()
    phone = fields.String()
    pictureUrl = fields.String()
    preferredName = fields.String()
    startDate = Date()
    status = fields.String()

class personRole(Model):

    id = fields.Integer()
    name = fields.String()

class project(Model):

    id = fields.Integer()
    divisions = fields.Collection(fields.String)
    status = fields.String()
    type = fields.String()
    description = fields.String()
    endDate = Date()
    title = fields.String()
    nextReviewDate = Date()
    notes = fields.String()
    code = fields.String()
    requirements = fields.String()
    startDate = Date()
    todo = fields.String()

class personProject(Model):

    id = fields.Integer()
    person = fields.Embedded(person)
    personId = fields.Integer()
    notes = fields.String()
    personRoleId = fields.Integer()
    personRole = fields.Embedded(personRole)
    projectId = fields.Integer()
    project = fields.Embedded(project)

class personProperty(Model):

    id = fields.Integer()
    personId = fields.Integer()
    propname = fields.String()
    propvalue = fields.String()
    timestamp = fields.Integer()

class personRole(Model):

    id = fields.Integer()
    name = fields.String()


class personStatus(Model):

    id = fields.Integer()
    name = fields.String()


class projectActionType(Model):

    id = fields.Integer()
    name = fields.String()


class projectFacility(Model):

    facilityId = fields.Integer()
    id = fields.Integer()
    projectId = fields.Integer()


class projectKpi(Model):

    id = fields.Integer()
    date = Date()
    kpiId = fields.Integer()
    kpiCategoryId = fields.Integer()
    personId = fields.Integer()
    projectId = fields.Integer()
    notes = fields.String()
    value = fields.Float()

    kpiCategory = fields.String()
    kpiType = fields.String()
    kpiNumber = fields.Integer()
    personFullName = fields.String()

class projectStatus(Model):

    id = fields.Integer()
    name = fields.String()
