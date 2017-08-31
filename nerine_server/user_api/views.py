from django.db.models import Q
#фильтры
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from base.models import Person
from .serializers import PersonSerializer
from rest_framework.generics import ListAPIView
#права доступа
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny
)
from rest_framework.generics import ListAPIView

class UserUpdatePassword(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserInfoSerialaser
    lookup_field = 'username'
    permission_classes = [IsAuthenticated, IsOwner]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)



class SitesViewer(generics.ListAPIView):
    queryset = Sites.objects.all()
    serializer_class = SitesSerializer
    permission_classes = [IsAuthenticated, IsOwner]



class SitesPersonViewer(generics.ListAPIView):
    date = Page.objects.latest('lastScanDate').lastScanDate
    queryset = PersonPageRank.objects.filter(pageId__lastScanDate=date)
    serializer_class = SitesPersonRankSerialazer
    filter_backends = [SearchFilter]  # Виды фильтров
    search_fields = ['pageId__siteId__name']
    permission_classes = [IsAuthenticated, IsOwner]



class SitesPeriodViewer(generics.ListAPIView):
    serializer_class = SitesPersonRankSerialazer
    filter_backends = [SearchFilter]  # Виды фильтров
    search_fields = ['pageId__siteId__name']
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self, *args, **kwargs):
        queryset_list = PersonPageRank.objects.all()
        query = self.request.GET.get('from')
        query = query.split(':')
        if query:
            queryset_list = PersonPageRank.objects.filter(
                pageId__lastScanDate__range=(query[0], query[1])
            )
        return queryset_list