<<<<<<< HEAD
import datetime

from django.db.models import Q
from django.contrib.auth.models import User
#фильтры
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.generics import ListAPIView
from rest_framework import generics
=======
from django.db.models import Q
#фильтры
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from base.models import Person
from .serializers import PersonSerializer
from rest_framework.generics import ListAPIView
>>>>>>> d43379b329012fb820dac3a27079a96f58f5b778
#права доступа
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny
)
<<<<<<< HEAD
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
=======
from rest_framework.generics import ListAPIView
>>>>>>> d43379b329012fb820dac3a27079a96f58f5b778

class UserUpdatePassword(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserInfoSerialaser
    lookup_field = 'username'
    permission_classes = [IsAuthenticated, IsOwner]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)



class SitesViewer(generics.ListAPIView):
<<<<<<< HEAD
    queryset = Site.objects.all()
=======
    queryset = Sites.objects.all()
>>>>>>> d43379b329012fb820dac3a27079a96f58f5b778
    serializer_class = SitesSerializer
    permission_classes = [IsAuthenticated, IsOwner]



class SitesPersonViewer(generics.ListAPIView):
<<<<<<< HEAD
    date = Page.objects.latest('LastScanDate')
    date = date.LastScanDate
    date = date.date()
    queryset = PersonPageRank.objects.all() # filter(PageID__LastScanDate__date=date)
    serializer_class = SitesPersonRankSerialazer
    filter_backends = [SearchFilter]  # Виды фильтров
    search_fields = ['PageID__SiteID__Name']
=======
    date = Page.objects.latest('lastScanDate').lastScanDate
    queryset = PersonPageRank.objects.filter(pageId__lastScanDate=date)
    serializer_class = SitesPersonRankSerialazer
    filter_backends = [SearchFilter]  # Виды фильтров
    search_fields = ['pageId__siteId__name']
>>>>>>> d43379b329012fb820dac3a27079a96f58f5b778
    permission_classes = [IsAuthenticated, IsOwner]



class SitesPeriodViewer(generics.ListAPIView):
    serializer_class = SitesPersonRankSerialazer
    filter_backends = [SearchFilter]  # Виды фильтров
<<<<<<< HEAD
    search_fields = ['PageID__SiteID__Name']
=======
    search_fields = ['pageId__siteId__name']
>>>>>>> d43379b329012fb820dac3a27079a96f58f5b778
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self, *args, **kwargs):
        queryset_list = PersonPageRank.objects.all()
        query = self.request.GET.get('from')
<<<<<<< HEAD
        if query:
            query = query.split(':')
            queryset_list = PersonPageRank.objects.filter(
               PageID__LastScanDate__date__range=(query[0],query[1]))
            print(queryset_list)
=======
        query = query.split(':')
        if query:
            queryset_list = PersonPageRank.objects.filter(
                pageId__lastScanDate__range=(query[0], query[1])
            )
>>>>>>> d43379b329012fb820dac3a27079a96f58f5b778
        return queryset_list