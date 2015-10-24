from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist

from erp.extras.views import AjaxFormMixin, AjaxUpdateFormMixin
from . import models, forms


class Index(TemplateView):

    template_name = 'directory/index.html'


class AddPersonalData(AjaxFormMixin):

    template_name = 'directory/inline.html'
    model = models.Person
    form_class = forms.PersonForm

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = request.user.person if request.user.person else None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        address_formset = forms.AddressFormSet()
        phone_formset = forms.PhoneFormSet()
        email_formset = forms.EMailFormSet()
        formsets = []
        formsets.extend([address_formset, phone_formset, email_formset])
        return render(request, self.template_name, {'form': form, 'formsets': formsets})

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = request.user.person if request.user.person else None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        address_formset = forms.AddressFormSet(self.request.POST)
        phone_formset = forms.PhoneFormSet(self.request.POST)
        email_formset = forms.EMailFormSet(self.request.POST)
        if (form.is_valid() and address_formset.is_valid() and
            phone_formset.is_valid() and email_formset.is_valid):
            return self.form_valid(form, address_formset, phone_formset, email_formset)
        else:
            return self.form_invalid(form, address_formset, phone_formset, email_formset)

    def form_valid(self, form, address_formset, phone_formset, email_formset):
        """
        Called if all forms are valid. Creates a Recipe instance along with
        associated Ingredients and Instructions and then redirects to a
        success page.
        """
        form.user = self.request.user
        self.object = form.save()
        address_formset.instance = self.object
        address_formset.save()
        phone_formset.instance = self.object
        phone_formset.save()
        return HttpResponse(self.get_success_url())

    def form_invalid(self, form, address_formset, phone_formset, email_formset):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        formsets = []
        formsets.extend([address_formset, phone_formset, email_formset])
        return render(self.request, self.template_name,
                      self.get_context_data(form=form,
                                            address_form=address_formset,
                                            phone_form=phone_formset,
                                            email_form=email_formset))


class PersonFormView(AjaxUpdateFormMixin):

    model = models.Person

    def get_object(self, queryset=None):
        try:
            return self.request.user.person
        except ObjectDoesNotExist:
            return None


class PersonInfoFormView(AjaxUpdateFormMixin):

    template_name = 'formset_ajax.html'
    form_class = forms.EMailFormSet
    # context_object_name = 'formset'

    def get_object(self, queryset=None):
        try:
            return self.request.user.person
        except ObjectDoesNotExist:
            return None

    def get_context_data(self, **kwargs):
        """
        Get the context for this view.
        """
        kwargs['formset'] = kwargs['form']
        del kwargs['form']
        return super(PersonInfoFormView, self).get_context_data(**kwargs)


class EMailFormView(PersonInfoFormView):

    form_class = forms.EMailFormSet


class PhoneFormView(PersonInfoFormView):

    form_class = forms.PhoneFormSet


class AddressFormView(PersonInfoFormView):

    form_class = forms.AddressFormSet