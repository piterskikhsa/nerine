from django.shortcuts import render
from rest_framework import generics
from rest_framework.renderers import JSONRenderer

from root_api.models import Person, KeyWord, Site
from root_api.v2.serializers import (
    SiteDetailSerializer,
    SiteListSerializer
)


class SiteListView(generics.ListCreateAPIView):
    queryset = Site.objects.all()
    serializer_class = SiteListSerializer
    renderer_classes = (JSONRenderer,)


class SiteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Site.objects.all()
    serializer_class = SiteDetailSerializer
    renderer_classes = (JSONRenderer,)
