# -*- coding: utf-8 *-*
"""
Adds admin configuration for subscribers.
"""
from django.contrib import admin
from holding_page.subscribers.models import Subscriber


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'subscribers_recruited')
admin.site.register(Subscriber, SubscriberAdmin)
