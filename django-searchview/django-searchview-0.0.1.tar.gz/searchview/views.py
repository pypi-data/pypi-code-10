# -*- coding: utf-8 -*-

from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from django.utils.translation import ugettext as _
from django.views.generic import ListView
from django.views.generic.edit import FormMixin

from .forms import searchform_factory


class SearchFormMixin(FormMixin):
    fields = None
    keyword_fields = None
    order_fields = None

    def get_form_class(self):
        if self.form_class:
            if self.fields:
                raise ImproperlyConfigured(
                    "Specifying both 'fields' and 'form_class' is not permitted."
                )
            return self.form_class

        if self.model:
            model = self.model
        else:
            model = self.get_queryset().model

        if self.fields is None:
            raise ImproperlyConfigured(
                "Using SearchFormMixin (base class of %s) without "
                "the 'fields' attribute is prohibited." % self.__class__.__name__
            )

        return searchform_factory(
            model,
            fields=self.fields,
            keyword_fields=self.keyword_fields,
            order_fields=self.order_fields,
        )

    def get_form_kwargs(self):
        return {
            'data': self.request.GET,
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
            'queryset': self.get_queryset()
        }


class SearchView(SearchFormMixin, ListView):
    def get(self, request, *args, **kwargs):
        form = self.get_form()
        self.object_list = form.search()
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            if (self.get_paginate_by(self.object_list) and hasattr(self.object_list, 'exists')):
                is_empty = not self.object_list.exists()
            else:
                is_empty = len(self.object_list) == 0
            if is_empty:
                raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.") % {
                    'class_name': self.__class__.__name__
                })

        context = self.get_context_data(**{
            'object_list': self.object_list,
            'form': form,
        })

        return self.render_to_response(context)

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)
