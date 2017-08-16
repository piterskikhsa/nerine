from rest_framework import serializers
from .models import PersonPageRank, Persons, Pages


class PageRankSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonPageRank
        fields = ('__all__')


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persons
        fields = ('__all__')


class PagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pages
        fields = ('__all__',)


