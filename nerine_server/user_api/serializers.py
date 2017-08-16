from rest_framework import serializers
from base.models import PersonPageRank, Person, Page


class PageRankSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonPageRank
        fields = ('__all__')


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('__all__')


class PagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('__all__',)


