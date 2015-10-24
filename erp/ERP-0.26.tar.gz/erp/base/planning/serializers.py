__author__ = 'cltanuki'
from rest_framework import serializers

from . import models


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Role

class PrjRoleSerializer(serializers.ModelSerializer):

    role = RoleSerializer()

    class Meta:
        model = models.PrjRole
        fields = ('id', 'since', 'until', 'role')


class PrjPartySerializer(serializers.ModelSerializer):

    project_role = PrjRoleSerializer()

    class Meta:
        model = models.Person
        fields = ('id', 'first_name', 'last_name', 'project_role')




class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Task
        #fields = ('title', 'status')


class PrjSerializer(serializers.ModelSerializer):

    #data_dict = serializers.Field()
    # data_model = serializers.Field()
    party = PrjPartySerializer(many=True, read_only=True)
    #party = PrjRoleSerializer(many=True, read_only=True)
    #owner = PersonSerializer(read_only=True)
    owner = serializers.HyperlinkedIdentityField(view_name='person-detail')

    # def __init__(self, *args, **kwargs):
    #     super(PrjSerializer, self).__init__(*args, **kwargs)
    #     data_serializer = self.object.data.serializer
    #     self.data_info = data_serializer()

    class Meta:
        model = models.Project
        #fields = ('title', 'slug', 'desc', 'status', 'owner', 'responsible', 'performer', 'started_at',
         #         'deadline', 'done_at', 'public', 'party')#, 'data_dict')


class PrjListSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Project
        #fields = ('title', 'status', 'slug')


class PrjTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectTemplate

class TaskTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TaskTemplate



