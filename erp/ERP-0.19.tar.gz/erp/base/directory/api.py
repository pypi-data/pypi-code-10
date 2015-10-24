__author__ = 'cltanuki'
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework import status
from rest_framework.response import Response
from . import serializers, models


class NewUser(generics.CreateAPIView):
    permission_classes = ()
    serializer_class = serializers.UserSerializer

    def post(self, request, *args, **kwargs):
        serialized = serializers.UserSerializer(data=request.data)
        if serialized.is_valid():
            user_id = models.User.objects.create_user(
                serialized.initial_data['username'],
                serialized.initial_data['email'],
                serialized.initial_data['password']
            ).id
            person = models.Person(user_id=user_id)
            person.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED, headers=self.headers)
        else:
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST, headers=self.headers)


class PersonBase():

    def get_queryset(self):
        person_id = self.kwargs.get('person_pk')
        person = get_object_or_404(models.Person, pk=person_id)
        queryset = self.model.objects.filter(person=person)
        return queryset

    def perform_create(self, serializer):
        person_id = self.kwargs.get('person_pk')
        person = get_object_or_404(models.Person, pk=person_id)
        serializer.save(person=person)


class PhonesViewSet(PersonBase, viewsets.ModelViewSet):

    serializer_class = serializers.PhoneSerializer
    model = models.Phone


class PositionsViewSet(PersonBase, viewsets.ModelViewSet):

    model = models.Position

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.PositionFullSerializer
        return serializers.PositionSerializer


class EMailsViewSet(PersonBase, viewsets.ModelViewSet):

    serializer_class = serializers.EMailSerializer
    model = models.EMail


class PersonViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.PersonSerializer
    queryset = models.Person.objects.all()
