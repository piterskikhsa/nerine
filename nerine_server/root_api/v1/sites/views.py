from django.shortcuts import render
from rest_framework import generics

from base.models import Person, KeyWord, Site
from root_api.serializers import (
    SiteDetailSerializer,
    SiteListSerializer
)


class SiteListView(generics.ListCreateAPIView):
    queryset = Site.objects.all()
    serializer_class = SiteListSerializer


class SiteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Site.objects.all()
    serializer_class = SiteDetailSerializer
