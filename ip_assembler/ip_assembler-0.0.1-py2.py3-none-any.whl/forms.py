from django import forms
from django.utils.translation import ugettext as _


class IPBatchMergeForm(forms.Form):
    ips = forms.CharField(
        label=_('List of IPs'),
        required=False,
        widget=forms.Textarea
    )
    show_cleaned_list = forms.BooleanField(
        label=_('Show all IPs cleaned?'),
        required=False,
    )
