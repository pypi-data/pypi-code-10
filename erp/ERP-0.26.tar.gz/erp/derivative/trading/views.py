from django.shortcuts import get_object_or_404, HttpResponse
from django.views.generic import ListView, TemplateView, DetailView
from django.forms.models import modelform_factory, inlineformset_factory, modelformset_factory
# from django.contrib.contenttypes.models import ContentType

from . import models
from erp.extras.views import AjaxFormMixin


class Index(TemplateView):
    pass
    # template_name = 'trading/index.html'


class CategoryList(ListView):
    model = models.Category
    # template_name = 'trading/products_list.html'
    context_object_name = 'category'
    paginate_by = 30


class ProductList(ListView):

    model = models.Product
    context_object_name = 'product'
    paginate_by = 30


class ProductView(DetailView):

    # template_name = 'trading/product_info.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        nom = get_object_or_404(models.Product, id=self.kwargs.get('id'))
        return nom

    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)
        context['items'] = self.object.items
        return context


class CategoryView(DetailView):
    context_object_name = 'category'

    def get_object(self, queryset=None):
        cat = get_object_or_404(models.Category, id=self.kwargs.get('id'))
        return cat

    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)
        return context


class AddProductAssoc(AjaxFormMixin):

    def get_form_class(self):
        form = inlineformset_factory(models.ProductAssoc,
                                     fields=['content_type', 'object_id', 'count'])
        return form

    def form_valid(self, form):
        if self.request.GET.get('product_id'):
            product_id = self.request.GET.get('product_id')
            for f in form:
                fields = f.cleaned_data
                if not bool(fields):
                    continue
                fields['product_id'] = product_id
                g = models.ProductAssoc()
                g.save_from_ajax(fields)
            return HttpResponse('OK')
        else:
            return HttpResponse('There is no product_id!')


def product_sale(request, id=None):
        if request.method == 'GET':
            return HttpResponse('There must be a POST request!')
        prod_id = id
        product = models.Product.objects.get(pk=prod_id)
        if product is None:
            return HttpResponse('Invalid product id')
        if product.sale(person_id=request.user.person.id):
            return HttpResponse('Product was successfully sold.')
        else:
            return HttpResponse('Something goes wrong.')




class AddProductGallery(AjaxFormMixin):

    def get_form_class(self):
        p_id = self.request.GET.get('product_id')
        product = models.Product.objects.get(pk=p_id)
        form = inlineformset_factory(product, models.ProductAssoc,
                                     fields=['image'])
        return form


class AddProduct(AjaxFormMixin):

    def get_form_class(self):
        form = modelform_factory(models.Product,
                                 fields=['title', 'desc', 'slug', 'logo', 'cat', 'rel_cat'])
        return form


class AddCategory(AjaxFormMixin):
    def get_form_class(self):
        form_class = modelformset_factory(models.Category, fields=['title', 'slug', 'parent', 'pic'])
        return form_class
