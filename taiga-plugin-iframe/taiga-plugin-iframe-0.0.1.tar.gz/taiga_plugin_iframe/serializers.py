from taiga.base.api import serializers

from .models import IframePlugin


class IframePluginSerializer(serializers.ModelSerializer):
    class Meta:
        model = IframePlugin
