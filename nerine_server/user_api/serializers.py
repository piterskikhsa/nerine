from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
<<<<<<< HEAD
from rest_framework.serializers import (
                    ModelSerializer,
                    SerializerMethodField
)
from rest_framework import serializers
from base.models import (
                     PersonPageRank,
                     Page,
                     Site
)
=======
rom rest_framework.serializers import (
                    ModelSerializer,
                    SerializerMethodField
)
from base.models import (
                     PersonPageRank,
                     Page,
                     Sites
)

User = get_user_model()

class UserInfoSerialaser(ModelSerializer):
    username = CharField(read_only=True, allow_blank=True)
    email = CharField(read_only=True, allow_blank=True)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

        extra_kwargs = {'password':
                            {'write_only':True}
                        }
    def update(self, instance, validated_data):
        password = validated_data['password']
        password_hush = make_password(password)
        validated_data['password'] = password_hush
        return super(UserInfoSerialaser, self).update(instance, validated_data)
>>>>>>> d43379b329012fb820dac3a27079a96f58f5b778

User = get_user_model()

<<<<<<< HEAD
class UserInfoSerialaser(ModelSerializer):
    username = serializers.CharField(read_only=True, allow_blank=True)
    email = serializers.CharField(read_only=True, allow_blank=True)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

        extra_kwargs = {'password':
                            {'write_only':True}
                        }
    def update(self, instance, validated_data):
        password = validated_data['password']
        password_hush = make_password(password)
        validated_data['password'] = password_hush
        return super(UserInfoSerialaser, self).update(instance, validated_data)


class SitesSerializer(ModelSerializer):
    """Сайты для списка выбора"""
    class Meta:
        model = Site
        fields = ('__all__')
=======
class SitesSerializer(ModelSerializer):
    """Сайты для списка выбора"""
    class Meta:
        model = Sites
        fields = ('__all__')


class SitesPersonRankSerialazer(ModelSerializer):
    person = SerializerMethodField()
    rank = SerializerMethodField()
    lastDate = SerializerMethodField()
    class Meta:
        model = Sites
        fields = ('lastDate', 'person', 'rank')
>>>>>>> d43379b329012fb820dac3a27079a96f58f5b778

    def get_person(self, obj):
        return str(obj.personId.name)

<<<<<<< HEAD
class SitesPersonRankSerialazer(ModelSerializer):
    Person = SerializerMethodField()
    Rank = SerializerMethodField()
    LastDate = SerializerMethodField()
    class Meta:
        model = Site
        fields = ('LastDate', 'Person', 'Rank')

    def get_Person(self, obj):
        return str(obj.PersonID.Name)

    def get_Rank(self, obj):
        return obj.Rank

    def get_LastDate(self, obj):
        return obj.PageID.LastScanDate
=======
    def get_rank(self, obj):
        return obj.rank

    def get_lastDate(self, obj):
        return obj.pageId.lastScanDate
>>>>>>> d43379b329012fb820dac3a27079a96f58f5b778


