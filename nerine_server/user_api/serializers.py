from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
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

User = get_user_model()

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
        date = obj.PageID.LastScanDate
        f_date = str(date.date()).split('-')

        return "{}-{}-{}".format(f_date[-1], f_date[1], f_date[0])


