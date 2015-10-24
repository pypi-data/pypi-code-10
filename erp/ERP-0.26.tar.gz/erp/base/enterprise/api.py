__author__ = 'cltanuki'
import json

from django.contrib.auth import authenticate, login

from rest_framework import generics, status, views, permissions, viewsets
from rest_framework.response import Response

from . import serializers
from .permissions import IsAccountOwner
from erp.base.directory import models


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = models.CorpUser.objects.all()
    serializer_class = serializers.UserSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)

        if self.request.method == 'POST':
            return (permissions.AllowAny(),)

        return (permissions.IsAuthenticated(), IsAccountOwner(),)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            models.CorpUser.objects.create_user(**serializer.validated_data)

            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)


class GroupViewSet(generics.ListAPIView):
    model = models.CorpUnit
    serializer_class = serializers.UnitSerializer
    lookup_field = "title"


class ObjViewSet(generics.ListAPIView):
    model = models.CorpObject
    serializer_class = serializers.ObjSerializer
    lookup_field = "title"


class GroupView(generics.RetrieveAPIView):
    model = models.CorpUnit
    serializer_class = serializers.UnitSerializer


class ObjView(generics.RetrieveAPIView):
    model = models.CorpObject
    serializer_class = serializers.ObjSerializer


class LoginView(views.APIView):
    def post(self, request, format=None):
        data = json.loads(request.body)

        email = data.get('email', None)
        password = data.get('password', None)

        account = authenticate(email=email, password=password)

        if account is not None:
            if account.is_active:
                login(request, account)

                serialized = serializers.UserSerializer(account)

                return Response(serialized.data)
            else:
                return Response({
                    'status': 'Unauthorized',
                    'message': 'This account has been disabled.'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Username/password combination invalid.'
            }, status=status.HTTP_401_UNAUTHORIZED)