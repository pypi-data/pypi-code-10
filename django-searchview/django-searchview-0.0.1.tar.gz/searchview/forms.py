# -*- coding: utf-8 -*-

from collections import OrderedDict

from django.contrib.gis.db import models
from django.core.exceptions import ImproperlyConfigured
from django.db.models.fields.related import RelatedField
from django import forms
from django.forms.models import ALL_FIELDS, BaseModelForm
from django.forms.forms import BaseForm, DeclarativeFieldsMetaclass
from django.utils import six
from django.utils.translation import ugettext as _


def get_model_field(model, field_name):
    if isinstance(field_name, six.string_types):
        field_name = field_name.split('__')

    field = model._meta.get_field(field_name.pop(0))
    if field_name and isinstance(field, RelatedField):
        return get_model_field(field.related_model, field_name)

    return field


def get_form_field(
    model, field_name,
    widget=None, formfield_callback=None,
    label=None, help_text=None, error_message=None,
):
    model_field = get_model_field(model, field_name)

    kwargs = {}
    if widget:
        kwargs['widget'] = widget
    if label:
        kwargs['label'] = label
    if help_text:
        kwargs['help_text'] = help_text
    if error_message:
        kwargs['error_message'] = error_message

    if formfield_callback is None:
        return model_field.formfield(**kwargs)

    if not callable(formfield_callback):
        raise TypeError('formfield_callback must be a function or callable')

    return formfield_callback(model_field, **kwargs)


class SearchFormOptions(object):
    def __init__(self, options=None):
        self.model = getattr(options, 'model', None)
        self.widgets = getattr(options, 'widgets', {})
        self.labels = getattr(options, 'labels', {})
        self.help_texts = getattr(options, 'help_texts', {})
        self.error_messages = getattr(options, 'error_messages', {})

        self.order_fields = getattr(options, 'order_fields', tuple())
        self.order_field_name = getattr(options, 'order_field_name', 'order')
        self.keyword_fields = getattr(options, 'keyword_fields', tuple())
        self.keyword_field_name = getattr(options, 'keyword_field_name', 'keyword')

        # TODO: ALL_FIELD
        self.fields = OrderedDict([
            self.normalize_field_conf(field)
            for field in getattr(options, 'fields', [])
        ])
        self.lookups = {}
        self.aliases = {}

        for field, field_options in six.iteritems(self.fields):
            self.lookups[field] = field_options['lookup']
            self.aliases[field] = field_options['as']

    def normalize_field_conf(self, field_conf):
        default_options = {'lookup': None, 'as': None}

        if isinstance(field_conf, six.string_types):
            field_conf = (field_conf, default_options)
        elif isinstance(field_conf, (list, tuple)):
            if len(field_conf) == 1:
                field_conf.append(default_options)
            else:
                field, options = field_conf[0:2]
                if not isinstance(options, dict):
                    raise ImproperlyConfigured('A field options must be dict instance.')
                default_options.update(options)
                field_conf = (field, default_options)
        else:
            raise ImproperlyConfigured('A field must be str or list or tuple.')

        return field_conf

    def get_aliase(self, field):
        aliase = self.aliases.get(field)
        if aliase is None:
            return field
        return aliase

    def get_lookup(self, field):
        lookup = self.lookups.get(field)
        if lookup is None:
            return ''
        return lookup


class SearchFormMetaclass(DeclarativeFieldsMetaclass):
    def __new__(self, name, bases, attrs):
        formfield_callback = attrs.pop('formfield_callback', None)
        new_class = super(SearchFormMetaclass, self).__new__(self, name, bases, attrs)
        if bases == (BaseModelForm,):
            return new_class

        opts = new_class._meta = SearchFormOptions(getattr(new_class, 'Meta', None))
        for opt in ['fields']:
            self.check_require_options(self, opt, opts, new_class)

        if not opts.model:
            fields = new_class.declared_fields
            new_class.base_fields = fields
            return new_class

        if opts.fields is None:
            raise ImproperlyConfigured(
                "Creating a SearchForm without either the 'fields' attribute "
                "is prohibited; form %s needs updating." % name
            )

        # Get form fields from model
        fields = self.get_fields(self, opts, formfield_callback)
        for field_name, field in six.iteritems(fields):
            field.requred = False

        # Add keyword field
        if opts.keyword_fields:
            if opts.keyword_field_name in fields:
                msg = 'Field "%s" is already declared.' % opts.keyword_field_name
                raise ImproperlyConfigured(msg)
            fields[opts.keyword_field_name] = self.get_keyword_field(self)

        # Add order field
        if opts.order_fields:
            if opts.order_field_name in fields:
                msg = 'Field "%s" is already declared.' % opts.order_field_name
                raise ImproperlyConfigured(msg)
            fields[opts.order_field_name] = self.get_order_field(
                self,
                opts.order_fields,
                opts.model,
            )

        fields.update(new_class.declared_fields)
        new_class.base_fields = fields

        return new_class

    def check_require_options(self, name, options, new_class):
        value = getattr(options, name)
        if isinstance(value, six.string_types) and value != ALL_FIELDS:
            msg = "%(model)s.Meta.%(name)s cannot be a string. " \
                  "Did you mean to type: ('%(value)s',)?"
            msg = msg % {
                'model': new_class.__name__,
                'name': name,
                'value': value,
            }
            raise TypeError(msg)

    def get_fields(self, opts, formfield_callback):
        return OrderedDict([
            (
                opts.get_aliase(field),
                get_form_field(
                    opts.model,
                    field,
                    opts.widgets.get(field),
                    formfield_callback,
                    opts.labels.get(field),
                    opts.help_texts.get(field),
                    opts.error_messages.get(field),
                )
            )
            for field in opts.fields.keys()
        ])

    def get_keyword_field(self):
        return forms.CharField(
            label=_('Keyword'),
            max_length=255,
            required=False,
        )

    def get_order_field(self, fields, model):
        choices = []
        for field in fields:
            model_field = get_model_field(model, field)
            verbose_name = model_field.verbose_name
            choices.append((field, _('%s in ascending') % verbose_name))
            choices.append(('-' + field, _('%s in descending') % verbose_name))

        return forms.MultipleChoiceField(
            label=_('Order'),
            choices=choices,
            required=False,
        )


class BaseSearchForm(BaseForm):
    def __init__(self, *args, **kwargs):
        if self._meta.model is None:
            raise ValueError('SearchForm has no model class specified.')
        self.queryset = kwargs.pop('queryset', None)
        super(BaseSearchForm, self).__init__(*args, **kwargs)
        self.apply_limit_choices_to()

    def apply_limit_choices_to(self):
        for field_name in self.fields:
            formfield = self.fields[field_name]
            if not hasattr(formfield, 'queryset'):
                continue
            if not hasattr(formfield, 'get_limit_choices_to'):
                continue
            limit_choices_to = formfield.get_limit_choices_to()
            if limit_choices_to is not None:
                formfield.queryset = formfield.queryset.complex_filter(limit_choices_to)

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self._meta.model._default_manager.all()
        return self.queryset

    def create_condition(self, field_name, lookup, value):
        if not value:
            return models.Q()
        key = field_name + '__' + lookup if lookup else field_name
        return models.Q(**{key: value})

    def create_keyword_condition(self, data):
        keyword_fields = self._meta.keyword_fields
        if not keyword_fields:
            return models.Q()

        value = data.get(self._meta.keyword_field_name, None)
        if not value:
            return models.Q()

        conditions = models.Q()
        for field_name in keyword_fields:
            conditions |= models.Q(**{field_name + '__icontains': value})
        return conditions

    def search(self):
        qs = self.get_queryset()

        if not self.is_bound:
            return qs

        if not hasattr(self, 'cleaned_data'):
            self.full_clean()

        conditions = [
            self.create_condition(
                field_name,
                self._meta.get_lookup(field_name),
                self.cleaned_data.get(self._meta.get_aliase(field_name)),
            )
            for field_name in self._meta.fields.keys()
        ]
        conditions.append(self.create_keyword_condition(self.cleaned_data))
        qs = qs.filter(*conditions)

        if self._meta.order_fields:
            name = self._meta.order_field_name
            qs = qs.order_by(*self.cleaned_data[name])

        return qs


class SearchForm(six.with_metaclass(SearchFormMetaclass, BaseSearchForm)):
    pass


def searchform_factory(
    model,
    fields,
    form=SearchForm,
    keyword_fields=None, keyword_field_name=None,
    order_fields=None, order_field_name=None,
    formfield_callback=None,
    widgets=None, labels=None, help_texts=None, error_messages=None,
):
    attrs = {
        'model': model,
        'fields': fields,
    }
    if keyword_fields is not None:
        attrs['keyword_fields'] = keyword_fields
    if keyword_field_name is not None:
        attrs['keyword_field_name'] = keyword_field_name
    if order_fields is not None:
        attrs['order_fields'] = order_fields
    if order_field_name is not None:
        attrs['order_field_name'] = order_field_name
    if widgets is not None:
        attrs['widgets'] = widgets
    if labels is not None:
        attrs['labels'] = labels
    if help_texts is not None:
        attrs['help_texts'] = help_texts
    if error_messages is not None:
        attrs['error_messages'] = error_messages

    parent = (form.Meta, object) if hasattr(form, 'Meta') else (object,)
    Meta = type(str('Meta'), parent, attrs)
    form_class_attrs = {
        'Meta': Meta,
        'formfield_callback': formfield_callback
    }

    return type(form)(
        model.__name__ + str('SearchForm'),
        (form,),
        form_class_attrs,
    )
