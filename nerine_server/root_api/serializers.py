from rest_framework import serializers

from base.models import Person, KeyWord, Site


class PersonListSerializer(serializers.ModelSerializer):
    key_words_count = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = ['id', 'Name', 'key_words_count']

    def get_key_words_count(self, obj):
        object_id = obj.id
        k_qs = KeyWord.objects.filter(PersonID_id=object_id)
        if k_qs:
            return k_qs.count()
        return 0


class PersonDetailSerializer(serializers.ModelSerializer):
    key_words = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = ['id', 'Name', 'key_words']

    def get_key_words(self, obj):
        object_id = obj.id
        k_qs = KeyWord.objects.filter(PersonID_id=object_id)
        key_words = KeyWordListSerializer(k_qs, many=True).data
        return key_words


class KeyWordListSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyWord
        fields = ['id', 'Name']


class KeyWordDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyWord
        fields = ['id', 'Name']


class SiteListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ['id', 'Name']


class SiteDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ['id', 'Name']
