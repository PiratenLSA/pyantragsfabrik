from django.contrib.auth.models import User
from antragsfabrik.models import Application, Type
from antragsfabrik.serializers import ApplicationSerializer, TypeSerializer, UserSerializer
from rest_framework import generics, viewsets


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ApplicationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer


class TypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer