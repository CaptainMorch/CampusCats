from rest_framework.serializers import HyperlinkedModelSerializer, CharField
from ..models import Location, Campus


class LocationBriefSerializer(HyperlinkedModelSerializer):
    display = CharField(source='__str__')

    class Meta:
        model = Location
        fields = [
            'url', 'name', 'display', 'longitude', 'latitude'
            ]


class CampusBriefSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Campus
        fields = ['url', 'name', 'full_name']
