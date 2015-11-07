# TODO still necessary?
# from bootstrap import admin_actions_registry

from django.db import models
from django.utils.translation import ugettext as _, ugettext_lazy


# TODO still necessary?
# # admin action to be displayed in action row
# from django.core.urlresolvers import reverse
# admin_actions_registry['ip_assembler'] = lambda: \
#     '<a href="%s" class="button">IP Batch Processing</a>' % reverse('admin:batch_process_ips_view')


class LocationLocal(models.Model):
    """
    Location of a local .htaccess file.
    """
    path = models.CharField(max_length=1000)

    def __str__(self):
        """
        Returns the name of the IP.
        :return: the name
        :rtype: unicode
        """
        return self.path

    class Meta:
        app_label = 'ip_assembler'
        verbose_name = ugettext_lazy('Local location')
        verbose_name_plural = ugettext_lazy('Local locations')


# TODO django_fields does not work with Python 3
# class LocationFTP(models.Model):
#     """
#     Location of an external, via FTP reachable, .htaccess file.
#     """
#     host = models.CharField(max_length=255, verbose_name=_('Host'))
#     username = models.CharField(max_length=255, verbose_name=_('Username'))
#     password = fields.EncryptedCharField(cipher='AES', block_type='MODE_CBC', verbose_name=_('Password'))
#     path = models.CharField(max_length=1000)
#
#     def __unicode__(self):
#         """
#         Returns the name of the IP.
#         :return: the name
#         :rtype: unicode
#         """
#         return u'%(host)s:%(path)s' % {'host': self.host, 'path': self.path}
#
#     class Meta:
#         app_label = 'ip_assembler'
#         verbose_name = ugettext_lazy('FTP location')
#         verbose_name_plural = ugettext_lazy('FTP locations')


class IP(models.Model):
    seg_0 = models.CharField(max_length=3, verbose_name=_('Segment 1'))
    seg_1 = models.CharField(max_length=3, verbose_name=_('Segment 2'))
    seg_2 = models.CharField(max_length=3, verbose_name=_('Segment 3'))
    seg_3 = models.CharField(max_length=3, verbose_name=_('Segment 4'))

    @staticmethod
    def batch_add_ips(ips):
        """
        Adds the given list of IPs to the database if the IP is not already there.
        :param ips: list of IPs
        :return: number of created IPs
        :type ips: list
        :rtype: int
        """
        ips_created = 0
        if len(ips) > 0:
            # for each ip, check if already existent, if not add
            for ip in ips:
                (s0, s1, s2, s3) = ip.split('.')
                (ip_db, is_ip_created) = IP.objects.get_or_create(seg_0=s0, seg_1=s1, seg_2=s2, seg_3=s3, )
                if is_ip_created:
                    ips_created += 1
        return ips_created

    @staticmethod
    def unify_ips():
        """
        Unifies the currently saved IPs.
        Unification is based on last IP segment.
        So if there are is e.g. 192.168.128.121 and 192.168.128.122 tthey will be merged to 192.168.128.121.
        This is a little aggressive but the spammers are aggressive, too.
        :return: number of merged ips
        :rtype: int
        """
        processed_ips = 0
        ips = {}

        # query for the IPs, also includes the starred IPs
        for ip in IP.objects.raw(
            'select distinct a.id, a.seg_0, a.seg_1, a.seg_2 '
            'from ip_assembler_ip a, ip_assembler_ip b '
            'where a.seg_0 = b.seg_0 and a.seg_1 = b.seg_1 and a.seg_2 = b.seg_2 and a.seg_3 != b.seg_3 '
            'order by a.seg_0, a.seg_1, a.seg_2',
        ):
            key = '%d.%d.%d' % (int(ip.seg_0), int(ip.seg_1), int(ip.seg_2))
            if not key in ips:
                ips[key] = []
            ips[key].append(ip)

        for key, ip_list in ips.items():
            # check if a starred ip is in list
            starred_ip = None
            for ip in ip_list:
                if ip.seg_3 == '*':
                    starred_ip = ip

            if starred_ip is None:
                IP.objects.create(seg_0=ip_list[0].seg_0, seg_1=ip_list[0].seg_1, seg_2=ip_list[0].seg_2, seg_3='*', )

            # delete the other ips
            for ip in ip_list:
                if ip != starred_ip:
                    processed_ips += 1
                    ip.delete()

        return processed_ips

    def __str__(self):
        """
        Returns the name of the IP.
        :return: the name
        :rtype: unicode
        """
        return u'%s.%s.%s.%s' % (self.seg_0, self.seg_1, self.seg_2, self.seg_3)

    class Meta:
        app_label = 'ip_assembler'
        verbose_name = ugettext_lazy('IP')
        verbose_name_plural = ugettext_lazy('IPs')