from django.shortcuts import render, get_object_or_404
from rest_framework import generics, viewsets, permissions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from nerine_server import settings
from root_api.models import Person, KeyWord, Site
from root_api.v2.serializers import (
    PersonDetailSerializer,
    PersonListSerializer,
)
from root_api.v2.permissions import IsOwner


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonListSerializer
    lookup_url_kwarg = 'person_id'
    renderer_classes = (JSONRenderer,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwner)

    def perform_create(self, serializer):
        serializer.save(Owner=self.request.user)

    def list(self, request, *args, **kwargs):
        owner = self.request.user
        queryset = Person.objects.filter(Owner=owner)
        serializer = PersonListSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        owner = self.request.user
        queryset = Person.objects.filter(Owner=owner)
        person = get_object_or_404(queryset, pk=kwargs['person_id'])
        serializer = PersonDetailSerializer(person, context={'request': request})
        return Response(serializer.data)
