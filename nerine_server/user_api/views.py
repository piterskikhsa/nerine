import datetime

from django.db.models import Q
from django.contrib.auth.models import User
#фильтры
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.generics import ListAPIView
from rest_framework import generics
#права доступа
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny
)
from base.models import (
    Person,
    Site,
    PersonPageRank,
    Page
)
from .permission import IsOwner
from .serializers import (
    SitesPersonRankSerialazer,
    SitesSerializer,
    UserInfoSerialaser
)

class UserUpdatePassword(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserInfoSerialaser
    lookup_field = 'username'
    permission_classes = [IsAuthenticated, IsOwner]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)



class SitesViewer(generics.ListAPIView):
    queryset = Site.objects.all()
    serializer_class = SitesSerializer
    permission_classes = [IsAuthenticated, IsOwner]



class SitesPersonViewer(generics.ListAPIView):
    date = Page.objects.latest('LastScanDate')
    date = date.LastScanDate
    date = date.date()
    queryset = PersonPageRank.objects.all() # filter(PageID__LastScanDate__date=date)
    serializer_class = SitesPersonRankSerialazer
    filter_backends = [SearchFilter]  # Виды фильтров
    search_fields = ['PageID__SiteID__Name']
    permission_classes = [IsAuthenticated, IsOwner]



class SitesPeriodViewer(generics.ListAPIView):
    serializer_class = SitesPersonRankSerialazer
    filter_backends = [SearchFilter]  # Виды фильтров
    search_fields = ['PageID__SiteID__Name']
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self, *args, **kwargs):
        queryset_list = PersonPageRank.objects.all()
        query = self.request.GET.get('from')
        if query:
            query = query.split(':')
            queryset_list = PersonPageRank.objects.filter(
               PageID__LastScanDate__date__range=(query[0],query[1]))
            print(queryset_list)
        return queryset_list