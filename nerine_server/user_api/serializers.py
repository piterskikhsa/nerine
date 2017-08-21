from rest_framework.serializers import (
                    ModelSerializer,
                    SerializerMethodField
)
from base.models import (
                     PersonPageRank,
                     Person
)


class PersonSerializer(ModelSerializer):
    class Meta:
        model = Person
        fields = ('Name', 'ranks_on_pages')

class PageRankSerializer(ModelSerializer):
    Name = SerializerMethodField()

    class Meta:
        model = PersonPageRank
        fields = ('Name', 'rank')

    def get_name(self, obj):
        return str(obj.personId.Name)




