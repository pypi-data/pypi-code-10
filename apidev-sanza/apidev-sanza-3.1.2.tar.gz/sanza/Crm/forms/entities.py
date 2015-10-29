# -*- coding: utf-8 -*-
"""Crm forms"""

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext, ugettext_lazy as _

import floppyforms as forms

from sanza.Crm import models
from sanza.Crm.forms.base import ModelFormWithAddress
from sanza.Crm.settings import NO_ENTITY_TYPE
from sanza.Crm.widgets import EntityAutoComplete


class EntityForm(ModelFormWithAddress):
    """Edit entity form"""

    def __init__(self, *args, **kwargs):
        super(EntityForm, self).__init__(*args, **kwargs)
        
        if NO_ENTITY_TYPE:
            self.fields["type"].widget = forms.HiddenInput()
        
    class Meta:
        """form is defined from model"""
        model = models.Entity
        fields = (
            'type', 'name', 'description', 'relationship_date', 'website', 'email', 'phone', 'fax',
            'street_number', 'street_type', 'address', 'address2', 'address3', 'zip_code', 'city', 'cedex', 'country',
            'logo', 'billing_street_number', 'billing_street_type', 'billing_address', 'billing_address2',
            'billing_address3', 'billing_zip_code', 'billing_city', 'billing_cedex', 'billing_country',
        )
        fieldsets = [
            ('name', {'fields': ['type', 'name', 'description', 'relationship_date'], 'legend': _(u'Name')}),
            ('web', {'fields': ['website', 'email', 'phone', 'fax'], 'legend': _(u'Entity details')}),
            ('address', {
                'fields': [
                    'street_number', 'street_type', 'address', 'address2', 'address3', 'zip_code', 'city',
                    'cedex', 'country'
                ],
                'legend': _(u'Address')
            }),
            ('billing_address', {
                'fields': [
                    'billing_street_number', 'billing_street_type', 'billing_address', 'billing_address2',
                    'billing_address3', 'billing_zip_code', 'billing_city', 'billing_cedex', 'billing_country'
                ],
                'legend': _(u'Billing address')
            }),
            ('logo', {'fields': ['logo'], 'legend': _(u'Logo')}),
        ]
    
    def clean_logo(self):
        """logo validation"""
        logo = self.cleaned_data["logo"]
        instance = self.instance
        if not instance:
            instance = ""
            try:
                instance.id = models.Entity.objects.latest('id').id
            except models.Entity.DoesNotExist:
                instance.id = 1
        target_name = models.get_entity_logo_dir(instance, logo)
        if len(target_name) >= models.Entity._meta.get_field('logo').max_length:
            raise ValidationError(ugettext(u"The file name is too long"))
        return logo


class EntityTypeForm(forms.ModelForm):
    """form for EntityType"""

    class Meta:
        """form from model"""
        model = models.EntityType


class EntityRoleForm(forms.ModelForm):
    """form for entity role"""

    class Meta:
        """form from model"""
        model = models.EntityRole


class SelectEntityForm(forms.Form):
    """Select an entity"""
    entity = forms.CharField(label=_(u"Entity"))

    def __init__(self, *args, **kwargs):
        super(SelectEntityForm, self).__init__(*args, **kwargs)
        self.fields["entity"].widget = EntityAutoComplete(
            attrs={'placeholder': _(u'Enter the name of an entity'), 'size': '50', 'class': 'colorbox'})

    def clean_entity(self):
        """entity validation"""
        try:
            entity_id = int(self.cleaned_data["entity"])
            return models.Entity.objects.get(id=entity_id)
        except (ValueError, models.Entity.DoesNotExist):
            raise ValidationError(ugettext(u"The entity does'nt exist"))


class ChangeContactEntityForm(forms.Form):
    """Switch contact entity form"""
    OPTION_ADD_TO_EXISTING_ENTITY = 1
    OPTION_CREATE_NEW_ENTITY = 2
    OPTION_SWITCH_SINGLE_CONTACT = 3
    OPTION_SWITCH_ENTITY_CONTACT = 4

    OPTION_CHOICES = (
        (0, ""),
        (OPTION_ADD_TO_EXISTING_ENTITY, _(u"Reassign to an existing entity")),
        (OPTION_CREATE_NEW_ENTITY, _(u"Create a new entity")),
        (OPTION_SWITCH_SINGLE_CONTACT, _(u"Switch to single contact")),
        (OPTION_SWITCH_ENTITY_CONTACT, _(u"Switch to entity contact")),
    )

    option = forms.ChoiceField(label=_(u"What to do?"))
    entity = forms.IntegerField(
        label=_(u"Which one?"),
        required=False,
        widget=EntityAutoComplete(
            attrs={'placeholder': _(u'Enter the name of the entity'), 'size': '50', 'class': 'colorbox'}
        )
    )

    def __init__(self, contact, *args, **kwargs):
        self.contact = contact
        super(ChangeContactEntityForm, self).__init__(*args, **kwargs)

        if contact.entity.is_single_contact:
            single_contact_choices = (self.OPTION_CREATE_NEW_ENTITY, self.OPTION_SWITCH_SINGLE_CONTACT)
            choices = [choice for choice in self.OPTION_CHOICES if choice[0] not in single_contact_choices]
        else:
            choices = [choice for choice in self.OPTION_CHOICES if choice[0] != self.OPTION_SWITCH_ENTITY_CONTACT]

        self.fields['option'].choices = choices

        self.meth_map = {
            self.OPTION_ADD_TO_EXISTING_ENTITY: self._add_to_existing_entity,
            self.OPTION_CREATE_NEW_ENTITY: self._create_new_entity,
            self.OPTION_SWITCH_SINGLE_CONTACT: self._switch_single_contact,
            self.OPTION_SWITCH_ENTITY_CONTACT: self._switch_entity_contact,
        }

    def clean_option(self):
        """validation"""
        try:
            option = int(self.cleaned_data["option"])
            if option == 0:
                raise ValidationError(ugettext(u"Please select one of this options"))
            try:
                self.meth_map[option]
            except KeyError:
                raise ValidationError(ugettext(u"Invalid value"))
        except ValueError:
            raise ValidationError(ugettext(u"Invalid data"))
        return option

    def clean_entity(self):
        """validation"""
        option = self.cleaned_data.get("option", 0)
        if option != self.OPTION_ADD_TO_EXISTING_ENTITY:
            return None
        else:
            entity_id = self.cleaned_data["entity"]
            try:
                return models.Entity.objects.get(id=entity_id)
            except models.Entity.DoesNotExist:
                raise ValidationError(ugettext(u"Please select an existing entity"))

    def _add_to_existing_entity(self):
        """add to exsiting entity"""
        old_entity = self.contact.entity
        self.contact.entity = self.cleaned_data["entity"]
        self.contact.save()
        old_entity.save()

    def _create_new_entity(self):
        """create new entity"""
        old_entity = self.contact.entity
        self.contact.entity = models.Entity.objects.create()
        self.contact.save()
        old_entity.save()

    def _switch_single_contact(self):
        """switch to single contact"""
        old_entity = self.contact.entity
        self.contact.entity = models.Entity.objects.create(
            is_single_contact=True,
            name=u"{0.lastname} {0.firstname}".format(self.contact).lower()
        )
        self.contact.save()
        self.contact.entity.default_contact.delete()
        self.contact.entity.save()
        old_entity.save()

    def _switch_entity_contact(self):
        """switch to entity"""
        self.contact.entity.is_single_contact = False
        self.contact.entity.save()

    def change_entity(self):
        """change entity: call the method corresponding to the choice"""
        option = self.cleaned_data["option"]
        method = self.meth_map[option]
        method()
