from rest_framework.viewsets import ModelViewSet

from utils.viewsets import DispatchSerializerMixin
from authen.permissions import IsMemberOrReadOnly
from .models import Campus, Location
from .serializers.brief import CampusBriefSerializer, LocationBriefSerializer
from .serializers.detail import (CampusDetailSerializer, CampusWriteSerializer,
    LocationDetailSerializer, LocationWriteSerializer)

class CampusViewSet(DispatchSerializerMixin, ModelViewSet):
    queryset = Campus.objects.all()
    permission_classes = [IsMemberOrReadOnly]
    retrieve_serializer = CampusDetailSerializer
    list_serializer = CampusBriefSerializer
    write_serializer = CampusWriteSerializer


class LocationViewSet(DispatchSerializerMixin, ModelViewSet):
    queryset = Location.objects.all()
    permission_classes = [IsMemberOrReadOnly]
    retrieve_serializer = LocationDetailSerializer
    list_serializer = LocationBriefSerializer
    write_serializer = LocationWriteSerializer