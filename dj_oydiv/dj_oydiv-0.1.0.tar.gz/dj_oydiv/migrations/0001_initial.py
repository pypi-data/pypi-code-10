# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import dj_oydiv.models
from django.conf import settings
import django.core.validators



try:
# Try and import the legacy application, and depend on its last migration which
# renames our db tables, from which this application takes over.
# If not, we are starting a new migration, and don't need the legacy cruft.
    import ajentavidyo
    dependencies = [
            ('ajentavidyo', '0008_final'),
            ('contenttypes', '0002_remove_content_type_name'),
            migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ]
except ImportError:
    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]


class Migration(migrations.Migration):
    dependencies = dependencies
    operations = [
        migrations.CreateModel(
            name='IPModel',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('ip', models.GenericIPAddressField(help_text='Add the IP address of every authorised client', default='127.0.0.1', validators=[django.core.validators.validate_ipv46_address])),
            ],
        ),
        migrations.CreateModel(
            name='PasswordCrypt',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('ciphertext', models.TextField(editable=False, null=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='VidyoAdmin',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('portal_user', models.CharField(help_text='The admin/operator user on the VidyoPortal', default='admin', verbose_name='API username', max_length=255)),
                ('portal_host', models.CharField(help_text='FQDN of the portal', default='example.com', verbose_name='VidyoPortal hostname', validators=[dj_oydiv.models._validate_hostname], max_length=65535)),
                ('portal_prefix', models.CharField(help_text='Tenant prefix (for multitenant portals)', default='001', verbose_name='Prefix', validators=[dj_oydiv.models._validate_prefix], max_length=4)),
                ('user_proxy', models.CharField(help_text='Default Proxy name for TCP tunneling of conferences', default='No Proxy', verbose_name='Default Proxy', max_length=128)),
                ('user_group', models.CharField(help_text='Default Group for new accounts. This is used to limit bandwidth and concurrency on the portal', default='Default', verbose_name='Default Group', max_length=128)),
                ('user_role', models.CharField(editable=False, default='Normal', choices=[('Normal', 'Normal'), ('Operator', 'Operator'), ('Admin', 'Admin')], max_length=128)),
                ('user_location_tag', models.CharField(help_text='Default location tag for new users (router affinity) formultiple router configuration.', default='Default', verbose_name='Location Tag', max_length=128)),
                ('replay_host', models.CharField(help_text="The FQDN of the given tenant's replay", default='example.com', verbose_name='VidyoReplay hostname', blank=True, validators=[dj_oydiv.models._validate_hostname], max_length=65535, null=True)),
                ('cdr_enabled', models.BooleanField(default=False, verbose_name='Allow collection of Call Detail Records')),
                ('cdr_port', models.PositiveIntegerField(default=3306, verbose_name='MySQL port for CDR access')),
                ('cdr_host', models.CharField(null=True, blank=True, verbose_name='MySQL hostname', validators=[dj_oydiv.models._validate_hostname], max_length=65535)),
                ('cdr_password', models.CharField(null=True, blank=True, verbose_name='MySQL password for CDR access', max_length=128)),
                ('cdr_user', models.CharField(default='cdraccess', verbose_name='MySQL user for CDR access', max_length=128)),
                ('use_ip_auth', models.BooleanField(default=True, verbose_name='Client IP whitelisting enabled')),
                ('ssl', models.BooleanField(default=True, verbose_name='SSL enabled VidyoPortal')),
                ('dj_auth_user', models.OneToOneField(help_text='The user to which this VidyoAdmin belongs.', null=True, verbose_name='Assigned Owner', to=settings.AUTH_USER_MODEL)),
            ],
            bases=(dj_oydiv.models.VidyoCredentialsMixin, models.Model),
        ),
        migrations.AddField(
            model_name='ipmodel',
            name='_admin_model',
            field=models.ForeignKey(to='dj_oydiv.VidyoAdmin'),
        ),
        migrations.AlterUniqueTogether(
            name='passwordcrypt',
            unique_together=set([('content_type', 'object_id')]),
        ),
    ]
