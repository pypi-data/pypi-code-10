__author__ = 'cltanuki'
from rest_framework import serializers
from django.contrib.auth import update_session_auth_hash

from .models import CorpUser
from erp.base.directory.models import CorpUnit, CorpObject


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CorpUser
        fields = ('id', 'email', 'username', 'created_at', 'updated_at',
                  'frst_name', 'last_name', 'tagline', 'password',
                  'confirm_password', 'salt')
        read_only_fields = ('created_at', 'updated_at',)

        def create(self, validated_data):
            return CorpUser.objects.create(**validated_data)

        def update(self, instance, validated_data):
            instance.username = validated_data.get('username', instance.username)
            instance.tagline = validated_data.get('tagline', instance.tagline)

            instance.save()

            password = validated_data.get('password', None)
            confirm_password = validated_data.get('confirm_password', None)

            if password and confirm_password and password == confirm_password:
                instance.set_password(password)
                instance.save()

            update_session_auth_hash(self.context.get('request'), instance)

            return instance


class UnitSerializer(serializers.HyperlinkedModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CorpUnit
        fields = ('id', 'title', 'parent')


class UnitListSerializer(serializers.HyperlinkedModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CorpUnit
        fields = ('id', 'title', 'parent')


class ObjSerializer(serializers.HyperlinkedModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CorpObject
        fields = ('id', 'title', 'parent')

# TODO: What is it???
#UnitSerializer.fields['parent'] = UnitSerializer()
#ObjSerializer.fields['parent'] = ObjSerializer()