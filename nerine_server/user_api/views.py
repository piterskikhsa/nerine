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


class FilterView(ListAPIView):
    """
    Этот класс отвечает за отображение списка или списка с фильтром
    """
    serializer_class = PersonSerializer
    permission_classes = [IsAuthenticated] #разгарничение прав
    filter_backends = [SearchFilter] # фильтр ?search<name>
    search_fields = ['name', 'ranks_on_pages__pageId__siteId__name'] #имена для поиска search в GET
    pagination_class = LimitOffsetPagination # пагинация через limit

    def get_queryset(self, *args, **kwargs):
        """
        Метод получения объекта  Query set через параметр в GET запросе

        :return: queryset_list - сортированный queryset
        """
        queryset_list = Person.objects.all()
        query = self.request.GET.get('date')
        if query:
            queryset_list = queryset_list.filter(ranks_on_pages__pageId__lastScanDate__icontains=query)
        return queryset_list
