from rest_framework import serializers

from .models import SimpleParent


class SimpleParentSerializer(serializers.ModelSerializer):

    class Meta:
        model = SimpleParent
