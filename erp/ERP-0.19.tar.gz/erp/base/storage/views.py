from django.shortcuts import get_object_or_404, HttpResponse
from django.views.generic import ListView, TemplateView, DetailView, FormView
from django.forms.models import modelform_factory, inlineformset_factory
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.contrib.contenttypes.models import ContentType

from . import models
from erp.extras.views import AjaxFormMixin


class Index(TemplateView):

    template_name = 'storage/index.html'


class NomenclatureList(ListView):

    model = models.Nomenclature
    template_name = 'storage/products_list.html'
    context_object_name = 'nomenclature'
    paginate_by = 30


class NomenclatureView(DetailView):

    template_name = 'storage/product_info.html'
    context_object_name = 'nomenclature'

    def get_object(self, queryset=None):
        nom = get_object_or_404(models.Category, slug=self.kwargs.get('slug'))
        return nom

    def get_context_data(self, **kwargs):
        context = super(NomenclatureView, self).get_context_data(**kwargs)
        context['items'] = self.object.st_items
        return context


class AddNomenclature(AjaxFormMixin):

    template_name = 'storage/form_info.html'
    form_class = modelform_factory(models.Nomenclature, fields=['title', 'cat'])


class AddItem(AjaxFormMixin):
    template_name = 'storage/form_info.html'

    def get_form_class(self):
        if self.request.GET.get('type') == 'static':
            form = modelform_factory(models.StaticItem, fields=['title', 'slug', 'pos', 'invent_no'])
        elif self.request.GET.get('type') == 'dynamic':
            form = modelform_factory(models.DynamicItem, fields=['title', 'slug', 'pos'])
        return form


class AddLog(AjaxFormMixin):

    def get_form_class(self):
        if self.request.GET.get('type') == 'adoption':
            form = generic_inlineformset_factory(models.StorageItemAdoptionLog,
                                                 fields=['waybill', 'comment', 'content_type', 'object_id'])
        elif self.request.GET.get('type') == 'shipment':
            form = generic_inlineformset_factory(models.StorageItemShipmentLog,
                                                 fields=['shipped_to', 'comment', 'content_type', 'object_id'])
        else:
            return HttpResponse('Wrong type!')

        return form

    def form_valid(self, form):
        if self.request.GET.get('item') == 'dynamic':
            content_type = ContentType.objects.get_for_model(models.DynamicItem)
        elif self.request.GET.get('item') == 'static':
            content_type = ContentType.objects.get_for_model(models.StaticItem)
        object_id = self.request.GET.get('id')
        if self.request.GET.get('type') == 'adoption':
            for f in form:
                fields = f.cleaned_data
                if not bool(fields):
                    continue
                fields['content_type'] = content_type
                fields['object_id'] = object_id
                log = models.StorageItemAdoptionLog()
                log.save_from_ajax(fields)
        elif self.request.GET.get('type') == 'shipment':
            for f in form:
                fields = f.cleaned_data
                if not bool(fields):
                    continue
                fields['content_type'] = content_type
                fields['object_id'] = object_id
                log = models.StorageItemShipmentLog()
                log.save_from_ajax(fields)
        else:
            return HttpResponse('Wrong type!')
        return HttpResponse('OK')


class AddCategory(AjaxFormMixin):

    def get_form_class(self):
        form = modelform_factory(models.Category, fields=['title', 'slug'])
        return form


class ItemView(DetailView, FormView):

    def get_form_class(self):
        if issubclass(self.object, models.StaticItem):
            form = inlineformset_factory(models.StaticItem, models.StorageItemAdoptionLog)
            return form

#
# class CategoryCreateView(AjaxFormMixin):
#
#     form_class = modelform_factory(models.Category)
#
#
# class CategoryUpdateView(AjaxFormMixin):
#
#     form_class = modelform_factory(models.Category)
#
#
# class GoodsCreateView(AjaxFormMixin):
#
#     form_class = modelform_factory(models.StorageItem)
#
#
# class GoodsUpdateView(AjaxFormMixin):
#
#     form_class = modelform_factory(models.StorageItem)