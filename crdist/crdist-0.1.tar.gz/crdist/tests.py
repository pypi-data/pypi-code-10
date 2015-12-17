from django.test import TestCase

# Create your tests here.

from crdist.widgets import DistrictSelect
from crdist.models import District
from django import forms
from django.shortcuts import render

"""
# models.py
class Test(models.Model):
    name = models.CharField(max_length=64, verbose_name=_('Name'))
    district = models.ForeignKey(District) 
    province = models.ForeignKey(District, related_name="prov")
    
# admin.py
class TestAdminForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = '__all__'
        widgets = {
          'district': DistrictSelect(attrs={"class": "form-control"}),
          'province': DistrictSelect(),
        }


class TestAdmin(admin.ModelAdmin):
    form = TestAdminForm


"""


class CRForm(forms.Form):
    district = forms.ModelChoiceField(queryset=District.objects.all(),
                                  widget=DistrictSelect,
                                  label="Provincia")


def view_test_form(request):

    form = CRForm()
    return render(request, 'form_ejemplo.html', {'form': form})