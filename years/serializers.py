from rest_framework import serializers
from Metten.years.models import Adder


class AdderSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.Field(source='user.username')
    #api_url = serializers.SerializerMethodField('get_api_url')

    class Meta:
        model = Adder
        fields = ('id', 'title', 'description', 'is_completed', 'content_type')
        read_only_fields = ('id', 'title')

    def get_api_url(self, obj):
        return "#/api/adder/" 