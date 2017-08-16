from django.shortcuts import render, get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.response import Response

from base.models import Person, KeyWord, Site
from root_api.serializers import (
    PersonDetailSerializer,
    PersonListSerializer,
)


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonListSerializer
    lookup_url_kwarg = 'person_id'

    def list(self, request, *args, **kwargs):
        queryset = Person.objects.all()
        serializer = PersonListSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        queryset = Person.objects.all()
        person = get_object_or_404(queryset, pk=kwargs['person_id'])
        serializer = PersonDetailSerializer(person, context={'request': request})
        return Response(serializer.data)
