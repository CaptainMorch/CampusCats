from rest_framework.serializers import HyperlinkedModelSerializer, HyperlinkedRelatedField

from ..models import Campus, Location
from .brief import LocationBriefSerializer, CampusBriefSerializer
#from cat.serializers.brief import CatBriefSerializer


class CampusDetailSerializer(HyperlinkedModelSerializer):
    locations = LocationBriefSerializer(many=True, required=False)
    
    class Meta:
        model = Campus
        fields = ['url', 'locations', 'name', 'full_name', 'longitude', 'latitude', 'zoom']


class CampusWriteSerializer(HyperlinkedModelSerializer):
    locations = None

    class Meta:
        model = Campus
        fields = ['url', 'name', 'full_name', 'longitude', 'latitude', 'zoom']
        read_only_fields = ['url']


class LocationDetailSerializer(HyperlinkedModelSerializer):
    # cats = CatBriefSerializer(many=True, required=False)
    campus = CampusBriefSerializer(required=False)

    class Meta:
        model = Location
        fields = ['url', 'campus', 'name', 'longitude', 'latitude'] # 'cats'


class LocationWriteSerializer(HyperlinkedModelSerializer):
    # cats = None

    class Meta:
        model = Location
        fields = ['url', 'campus', 'name', 'longitude', 'latitude']
        read_only_fields = ['url']    # 'cats'