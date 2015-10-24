#! __author__ = 'cltanuki'
from datetime import datetime
from django.db import models
from django_enumfield import enum
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.forms.models import model_to_dict
from django.core.exceptions import ValidationError
from erp.base.directory.models import CorpUnit
from erp.base.directory.models import Person


class Status(enum.Enum):
    PLANNED = 0
    ACTIVE = 1
    BLOCKED = 2
    DONE = 3

    labels = {
        PLANNED: _('PLANNED'),
        ACTIVE: _('ACTIVE'),
        BLOCKED: _('BLOCKED'),
        DONE: _('DONE')
    }

    _transitions = {
        ACTIVE: (PLANNED, BLOCKED),
        BLOCKED: (ACTIVE, PLANNED),
        DONE: (ACTIVE, BLOCKED)
    }


class Role(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=20)
    desc = models.TextField(verbose_name=_('Desc'))

    def __str__(self):
        return self.title


class TaskRole(models.Model):
    role = models.ForeignKey(Role, verbose_name=_('Role'))
    person = models.OneToOneField(Person)
    task = models.OneToOneField('Task', editable=False)
    since = models.DateField(_('Since'), auto_now_add=True)


class TaskPerfRole(models.Model):
    person = models.OneToOneField(Person)
    task = models.OneToOneField('Task', editable=False)
    desc = models.TextField()
    since = models.DateField(_('Since'), auto_now_add=True)


class PrjRole(models.Model):
    role = models.ForeignKey(Role, verbose_name=_('Role'))
    person = models.OneToOneField(Person)
    prj = models.OneToOneField('Project', editable=False)
    since = models.DateField(_('Since'), auto_now_add=True)


class Priority(models.Model):
    name = models.CharField(max_length=30)


class Project(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=20, unique=True)
    slug = models.SlugField(verbose_name=_('Alias'), unique=True)
    desc = models.TextField(verbose_name=_('Desc'))
    status = enum.EnumField(Status)
    # status = models.IntegerField(choices=STATUS_CHOICES)
    owner = models.ForeignKey(Person, related_name='owned_prjs', verbose_name=_('Owner'), editable=False)
    responsible = models.ForeignKey(CorpUnit, related_name='prj_resp_unit', verbose_name=_('Resp unit'))
    performer = models.ForeignKey(Person, related_name='prj_performer',
                                  verbose_name=_("Performer"), blank=True, null=True)
    started_at = models.DateField(verbose_name=_('Started at'), null=True, auto_now_add=True, editable=False)
    deadline = models.DateField(verbose_name=_('Deadline'))
    done_at = models.DateField(verbose_name=_('Done at'), blank=True, null=True, editable=False)
    public = models.BooleanField(verbose_name=_('Public'), default=False)
    party = models.ManyToManyField(Person, related_name='prj_assigned_users', through=PrjRole, editable=False,
                                   verbose_name=_('Participants'))
    item_type = models.ForeignKey(ContentType, verbose_name=_('Category'))
    item_id = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('Data'))
    data = generic.GenericForeignKey('item_type', 'item_id')

    class Meta:
        managed = True

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('prj_item', kwargs={'slug': self.slug})

    def can_manage(self, user):
        return user == self.owner

    @property
    def data_dict(self):
        return model_to_dict(self.data)

    @property
    def data_model(self):
        return self.item_type.model_class()

    def close(self, user):
        if self.can_manage(user):
            self.done_at = datetime.now().date()
            self.save()
            return True
        return False


class Task(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=20, unique=True)
    slug = models.SlugField(verbose_name=_('Alias'), unique=True)
    order = models.PositiveSmallIntegerField()
    desc = models.TextField(verbose_name=_('Description'))
    owner = models.ForeignKey(Person, related_name='owned_tasks', verbose_name=_('Owner'), editable=False)
    public = models.BooleanField(verbose_name=_('Public'), default=False)
    task_in = models.ForeignKey('Task', related_name='before_task', verbose_name=_('Task in'), blank=True, null=True)
    task_out = models.ForeignKey('Task', related_name='after_task', verbose_name=_('Task out'), blank=True, null=True)
    responsible = models.ForeignKey(CorpUnit, related_name='task_resp_unit',
                                    verbose_name=_('Resp unit'), blank=True, null=True)
    performer = models.ForeignKey(Person, related_name='task_performer',
                                  verbose_name=_('Performer'), null=True, blank=True)
    started_at = models.DateField(verbose_name=_('Started at'), blank=True, null=True,
                                  auto_now_add=True, editable=False)
    deadline = models.DateField(verbose_name=_('Deadline'))
    done_at = models.DateField(verbose_name=_('Done at'), blank=True, null=True, editable=False)
    status = enum.EnumField(Status)
    # status = models.IntegerField(choices=STATUS_CHOICES)
    prj = models.ForeignKey(Project, related_name='task_prj_container', verbose_name=_('Prj'), blank=True, null=True)
    party = models.ManyToManyField(Person, verbose_name=_('Participants'), related_name='task_assigned_users',
                                   blank=True, through=TaskRole, editable=False)
    item_type = models.ForeignKey(ContentType, verbose_name=_('Category'))
    item_id = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('Data'))
    data = generic.GenericForeignKey('item_type', 'item_id')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('task_item', kwargs={'slug': self.slug})

    def can_manage(self, user):
        return user == self.owner

    def save(self, *args, **kwargs):
        # print(args)
        # print(kwargs)
        # self.owner = self.request.user.person
        super(Task, self).save(*args, **kwargs)

    def close(self, user):
        if self.can_manage(user):
            self.done_at = datetime.now().date()
            self.save()
            return True
        return False


class CheckList(models.Model):
    perf = models.ForeignKey(Person)
    task = models.ForeignKey(Task)
    desc = models.CharField(max_length=200, null=True, blank=True)


class TaskTemplate(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=20, unique=True)
    slug = models.SlugField(verbose_name=_('Alias'), unique=True)
    desc = models.TextField(verbose_name=_('Desc'))
    responsible = models.ForeignKey(CorpUnit, related_name='resp_unit', verbose_name=_('Resp unit'))
    item_type = models.ForeignKey(ContentType, verbose_name=_('Category'))

    def __str__(self):
        return self.title


class ProjectTemplate(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=20, unique=True)
    slug = models.SlugField(verbose_name=_('Alias'), unique=True)
    desc = models.TextField(verbose_name=_('Desc'))
    req_tasks = models.ManyToManyField(TaskTemplate, related_name='req_task_templates', verbose_name=_('Req task'))
    opt_tasks = models.ManyToManyField(TaskTemplate, related_name='opt_task_templates',
                                       verbose_name=_('Opt tasks'), blank=True)
    responsible = models.ForeignKey(CorpUnit, related_name='prj_tmpl_resp_unit', verbose_name=_('Resp unit'))
    item_type = models.ForeignKey(ContentType, verbose_name=_('Category'))

    def __str__(self):
        return self.title
