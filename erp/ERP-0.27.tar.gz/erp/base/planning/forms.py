__author__ = 'cltanuki'
from django import forms
from django.contrib.admin.widgets import AdminDateWidget

from . import models


class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = '__all__'
        widgets = {'prj': forms.HiddenInput()}
        exclude = ['data', ]


class PrjForm(forms.ModelForm):

    class Meta:
        model = models.Project
        exclude = ['data', ]


class TmplTaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = '__all__'
        widgets = {
            'prj': forms.HiddenInput(),
            'responsible': forms.HiddenInput(),
            'performer': forms.HiddenInput(),
            'item_type': forms.HiddenInput(),
            'item_id': forms.HiddenInput(),
            'deadline': AdminDateWidget(),
        }


class PrjTmplForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = '__all__'
        widgets = {
            # 'prj': forms.HiddenInput(),
            # 'responsible': forms.HiddenInput(),
            # 'performer': forms.HiddenInput(),
            # 'item_type': forms.HiddenInput(),
            # 'item_id': forms.HiddenInput(),
            'deadline': AdminDateWidget(),
        }