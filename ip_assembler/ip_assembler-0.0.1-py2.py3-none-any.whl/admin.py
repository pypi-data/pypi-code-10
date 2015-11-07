from django.conf.urls import patterns, url
from django.contrib import admin
from django.shortcuts import render
from django.utils.translation import ugettext as _

from ip_assembler.forms import IPBatchMergeForm
from ip_assembler.models import (
    IP,
    # LocationFTP,
    LocationLocal
)


class IPAdmin(admin.ModelAdmin):
    ordering = ['seg_0', 'seg_1', 'seg_2', 'seg_3', ]

    def get_urls(self):
        """
        Returns the urls for the model.
        """
        urls = super(IPAdmin, self).get_urls()
        my_urls = patterns(
            '',
            url(r'^batch_process_ips/$', self.admin_site.admin_view(self.batch_process_ips_view), name='batch_process_ips_view')
        )
        return my_urls + urls

    def batch_process_ips_view(self, request):
        info_text = _('No errors')

        if request.method == 'POST':
            form = IPBatchMergeForm(request.POST)
            if form.is_valid():
                ips = list(filter(lambda x: len(x) > 0, form.cleaned_data['ips'].split('\r\n')))
                ip_count_before = IP.objects.count()

                if len(ips) > 0:
                    # create the ips that are not already in database
                    ips_created = IP.batch_add_ips(ips)

                    # display an info
                    info_text = _('%(ip_count)d IPs were given,<br /> %(ips_created)d IPs were created' % {'ip_count': len(ips), 'ips_created': ips_created})

                # unify them
                clean_ips = form.cleaned_data['show_cleaned_list']
                if clean_ips:
                    processed_ips_count = IP.unify_ips()

                    info_text += ',<br /> ' + _('%(processed_ips_count)d IPs processed' % {'processed_ips_count': processed_ips_count})
                    info_text += ',<br /> ' + _('%(ip_count_before)d IPs before' % {'ip_count_before': ip_count_before})
                    info_text += ',<br /> ' + _('%(ip_count_after)d IPs after' % {'ip_count_after': IP.objects.count()})

        else:
            form = IPBatchMergeForm()

        return render(
            request,
            'admin/batch_process_ips.html',
            {
                'form': form,
                'info_text': info_text,
                # PostgreSQL specific!
                'ips': IP.objects.extra(
                    select={'seg0': 'seg_0::int', 'seg1': 'seg_1::int', 'seg2': 'seg_2::int'},
                    order_by=['seg0', 'seg1', 'seg2', 'seg_3']
                )
            }
        )

admin.site.register(IP, IPAdmin)
admin.site.register(LocationLocal)
# admin.site.register(LocationFTP)
