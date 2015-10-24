__author__ = 'cltanuki'
import logging
from itertools import chain
from operator import attrgetter

from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.forms.models import modelform_factory
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, View
from django.contrib.admin.widgets import AdminDateWidget

from . import models, forms
from erp.extras.views import AjaxFormMixin

logger = logging.getLogger(__name__)
template_dict = {'task': 'TaskTemplate', 'prj': 'ProjectTemplate'}


def public_tasks(request):
    tasks = models.Task.objects.filter(public=True)
    if request.GET.get('type') is not None:
        type_name = get_object_or_404(ContentType, name=request.GET.get('type'))
        tasks = models.Task.objects.filter(public=True).filter(item_type=type_name)
    return render(request, 'planning/public.html', locals())


def public_prjs(request):
    prjs = models.Project.objects.filter(public=True)
    if 'smth' not in request.session.keys():
        request.session['smth'] = 'smth'
    if request.GET.get('type') is not None:
        type_name = get_object_or_404(ContentType, name=request.GET.get('type'))
        prjs = models.Project.objects.filter(public=True).filter(item_type=type_name)
    return render(request, 'planning/public_prj.html', locals())


class TaskTypes(ListView):

    def get(self, request, *args, **kwargs):
        perms = [x.split('_', 1)[-1] for x in request.user.get_all_permissions()]
        present = models.Task.objects.filter(owner=request.user).values_list('item_type__model', flat=True)
        types = [i for i in present if i in perms]
        return render(request, 'planning/filter_template.html', locals())


class PrjTypes(ListView):

    def get(self, request, *args, **kwargs):
        perms = [x.split('_', 1)[-1] for x in request.user.get_all_permissions()]
        present = models.Project.objects.filter(owner=request.user).values_list('item_type__model', flat=True)
        types = [i for i in present if i in perms]
        return render(request, 'planning/filter_template.html', locals())


def user_taskset(request):
    if request.user.person is not None:
        owned_tasks = request.user.person.owned_tasks.all()
        performer_of = request.user.person.task_performer.all()
        joined_tasks = request.user.person.task_assigned_users.all()
        tasks = sorted(chain(owned_tasks, performer_of, joined_tasks),
                       key=attrgetter('deadline'))
        if request.GET.get('type') is not None:
            type_name = get_object_or_404(ContentType, name=request.GET.get('type'))
            tasks = request.user.owned_tasks.filter(item_type=type_name)
        return render(request, 'planning/tasks_list_template.html', locals())
    # else:
    #     return HttpResponseRedirect(reverse('dir-add'))


def user_prjset(request):
    if request.user.person is not None:
        owned_prjs = request.user.person.owned_prjs.all()
        performer_of = request.user.person.prj_performer.all()
        joined_prjs = request.user.person.prj_assigned_users.all()
        prjs = sorted(chain(owned_prjs, performer_of, joined_prjs),
                      key=attrgetter('deadline'))
        if request.GET.get('type') is not None:
            type_name = get_object_or_404(ContentType, name=request.GET.get('type'))
            prjs = request.user.owned_prjs.filter(item_type=type_name)
        return render(request, 'planning/prj_list_template.html', locals())
    # else:
    #     return HttpResponseRedirect(reverse('dir-add'))


def show_templates(request, item_type):
    #user_groups = request.user.corp_group.all()
    if item_type == 'prj':
        model = models.ProjectTemplate
    elif item_type == 'task':
        model = models.TaskTemplate
    else:
        raise Http404
    templates = model.objects.all()
    return render(request, 'planning/item_templates.html', locals())


class CreateTaskFromTemplate(View):
    form_class = forms.TaskForm
    template_name = 'planning/create_from_template.html'

    def get(self, request, *args, **kwargs):
        template = get_object_or_404(models.TaskTemplate, id=request.GET.get('tmpl_id'))
        data = {'name': template.title, 'desc': template.desc}
        if request.GET.get('prj_id'):
            data['prj'] = request.GET.get('prj_id')
        form = self.form_class(initial=data)
        data_form = modelform_factory(template.item_type.model_class())
        return render(request, self.template_name, {'form': form, 'data_form': data_form, 'template': template})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        template = get_object_or_404(models.TaskTemplate, id=request.GET.get('tmpl_id'))
        data_form = modelform_factory(template.item_type.model_class())
        data_form = data_form(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.owner = request.user.person
            new_task.responsible = template.responsible
            new_task_data = data_form.save()
            new_task.item_id = new_task_data
            new_task.save()
            return redirect(new_task.get_absolute_url())

        return render(request, self.template_name, {'form': form})


class CreatePrjFromTemplate(View):
    form_class = forms.PrjTmplForm
    template_name = 'planning/create_from_template.html'

    def get_master(self, to_create):
        form_list = []
        init_dict = {}
        for idx, i in enumerate(to_create):
            template = get_object_or_404(models.TaskTemplate, id=i)
            data = {'name': template.title, 'desc': template.desc, 'responsible': template.responsible,
                    'item_type': template.item_type}
            form_list.append(modelform_factory(models.Task))
            init_dict[str(idx)] = data
        logger.error(init_dict)
        prj_dict = {'form_list': form_list, 'init_dict': init_dict}
        return prj_dict

    def get(self, request, *args, **kwargs):
        template = get_object_or_404(models.ProjectTemplate, id=request.GET.get('tmpl_id'))
        data = {'name': template.title, 'desc': template.desc, 'item_type': template.item_type,
                'responsible': template.responsible}
        logger.error(data)
        form = self.form_class(initial=data)
        data_form = modelform_factory(template.item_type.model_class())
        return render(request, self.template_name, {'form': form, 'data_form': data_form, 'template': template})

    def post(self, request, *args, **kwargs):
        logger.error(request.POST)
        form = self.form_class(request.POST)
        template = get_object_or_404(models.ProjectTemplate, id=request.GET.get('tmpl_id'))
        data_form = modelform_factory(template.item_type.model_class())
        data_form = data_form(request.POST)
        if form.is_valid() and data_form.is_valid():
            to_create = list(template.req_tasks.values_list('id', flat=True))
            if request.POST.get('opt_tasks') is not None:
                opt_tasks = request.POST.get('opt_tasks').split(',')
                for task in opt_tasks:
                    to_create.append(int(task))
            new_prj = form.save(commit=False)
            new_prj.owner = request.user.person
            new_prj.responsible = template.responsible
            new_prj_data = data_form.save()
            new_prj.item_id = new_prj_data.id
            new_prj.save()
            if to_create:
                request.session[str(new_prj.id)] = self.get_master(to_create)
                return redirect('prj-wiz', prj=str(new_prj.id))
            else:
                return redirect(new_prj.get_absolute_url())

        return render(request, self.template_name, {'form': form, 'data_form': data_form})


class TaskCreate(CreateView):
    form_class = modelform_factory(models.Task, widgets={'deadline': AdminDateWidget})
    template_name = 'form.html'

    def get(self, request, *args, **kwargs):
        if request.GET.get('prj_id'):
            prj = get_object_or_404(models.Project, id=request.GET.get('prj_id'))
            form = self.form_class(initial={'prj': prj})
        else:
            form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def form_valid(self, form):
        task = form.save(commit=False)
        task.owner = self.request.user.person
        #TODO: Add undefined tasks responsible CorpUnit
        form.save()
        return HttpResponseRedirect(task.get_absolute_url())


class PrjCreate(CreateView):
    model = models.Project
    template_name = 'form.html'
    fields = '__all__'

    def form_valid(self, form):
        form.instance.owner = self.request.user.person
        return super(PrjCreate, self).form_valid(form)


class TaskUserAssign(AjaxFormMixin):
    form_class = modelform_factory(models.TaskRole)


class PrjUserAssign(AjaxFormMixin):
    form_class = modelform_factory(models.PrjRole)


class PMItemView(DetailView):

    def get_context_data(self, **kwargs):
        context = super(PMItemView, self).get_context_data(**kwargs)
        if self.object.data:
            context['data'] = [(field.verbose_name, field.value_to_string(self.object.data)) for field
                               in self.object.data._meta.fields if field.verbose_name != 'ID']
        else:
            context['data'] = None
        return context