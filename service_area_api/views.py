from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.gis.geos import Point
from .models import Provider, ServiceArea
from .serializers import ProviderSerializer, ServiceAreaSerializer


class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class ServiceAreaViewSet(viewsets.ModelViewSet):
    queryset = ServiceArea.objects.all()
    serializer_class = ServiceAreaSerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        point = Point(float(lng), float(lat))
        service_areas = ServiceArea.objects.filter(polygon__contains=point)
        serializer = self.get_serializer(service_areas, many=True)
        return Response(serializer.data)
