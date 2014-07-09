from django.contrib.auth.models import User
from antragsfabrik.models import Application, Type
from antragsfabrik.serializers import ApplicationSerializer, TypeSerializer, UserSerializer
from rest_framework import viewsets, filters


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ApplicationViewSet(viewsets.ReadOnlyModelViewSet):
    model = Application
    serializer_class = ApplicationSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = (
        'id', 'number', 'status'
    )


class TypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer