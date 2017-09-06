from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from root_api.models import KeyWord
from root_api.v2.serializers import (
    KeyWordDetailSerializer,
    KeyWordListSerializer,
)


class KeyWordViewSet(viewsets.ModelViewSet):
    queryset = KeyWord.objects.all()
    serializer_class = KeyWordDetailSerializer
    lookup_url_kwarg = 'keyword_id'
    renderer_classes = (JSONRenderer,)

    def perform_create(self, serializer):
        serializer.save(PersonID_id=self.kwargs['person_id'])

    def list(self, request, *args, **kwargs):
        person_id = self.kwargs['person_id']
        queryset = KeyWord.objects.filter(PersonID_id=person_id)
        serializer = KeyWordListSerializer(queryset, many=True)
        return Response(serializer.data)

    # def retrieve(self, request, *args, **kwargs):
    #     person_id = self.kwargs['person_id']
    #     keyword_id = self.kwargs['keyword_id']
    #     keyword = KeyWord.objects.filter(PersonID_id=person_id).filter(id=keyword_id)
    #     serializer = KeyWordDetailSerializer(keyword, many=True)
    #     return Response(serializer.data)
