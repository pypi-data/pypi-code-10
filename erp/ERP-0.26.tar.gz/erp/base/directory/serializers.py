__author__ = 'cltanuki'
from rest_framework import serializers

from . import models
from erp.base.enterprise.serializers import UnitSerializer


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Position
        fields = ('id', 'unit', 'title', 'since', 'until')


class PositionFullSerializer(PositionSerializer, serializers.ModelSerializer):

    unit = UnitSerializer()


class EMailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.EMail
        fields = ('id', 'cat', 'body')


class PhoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Phone
        fields = ('id', 'cat', 'country_code', 'area_code', 'number')


class PersonSerializer(serializers.ModelSerializer):

    emails = EMailSerializer(many=True, read_only=True)
    phones = PhoneSerializer(many=True, read_only=True)
    positions = PositionSerializer(many=True, read_only=True)

    class Meta:
        model = models.Person
        fields = ('user', 'first_name', 'last_name', 'mid_name', 'date_of_birth', 'sex',
                  'avatar', 'emails', 'positions', 'phones', 'salt')


class PersonNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Person
        fields = ('full_name', 'url')


class UserSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(max_length=20)

    class Meta:
        model = models.User
        fields = ('email', 'username', 'password', 'password_confirmation')

    def validate_password_confirmation(self, value):
        if value != self.initial_data['password']:
            raise serializers.ValidationError('Passwords not match!')
        return value


# class AddressSerializer(serializers.HyperlinkedModelSerializer):
#
#     class Meta:
#         model = models.Address
#         fields = ('person', 'title', 'unit')
