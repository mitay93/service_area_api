from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_extensions.cache.decorators import cache_response
from rest_framework_extensions.key_constructor.bits import QueryParamsKeyBit
from rest_framework_extensions.key_constructor.constructors import DefaultKeyConstructor
from drf_spectacular.utils import extend_schema, extend_schema_view
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.openapi import OpenApiParameter

from .models import Provider, ServiceArea
from .serializers import ProviderSerializer, ServiceAreaSerializer, SearchQuerySerializer


class ServiceAreaKeyConstructor(DefaultKeyConstructor):
    query_params = QueryParamsKeyBit(['lat', 'lng'])


@extend_schema_view(
    list=extend_schema(description="Retrieve a list of providers."),
    retrieve=extend_schema(description="Retrieve a single provider by ID."),
    create=extend_schema(description="Create a new provider."),
    update=extend_schema(description="Update an existing provider."),
    partial_update=extend_schema(description="Partially update an existing provider."),
    destroy=extend_schema(description="Delete a provider."),
)
class ProviderViewSet(viewsets.ModelViewSet):
    """
    CRUD for providers
    """
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


@extend_schema_view(
    list=extend_schema(description="Retrieve a list of service areas."),
    retrieve=extend_schema(description="Retrieve a single service area by ID."),
    create=extend_schema(description="Create a new service area."),
    update=extend_schema(description="Update an existing service area."),
    partial_update=extend_schema(description="Partially update an existing service area."),
    destroy=extend_schema(description="Delete a service area."),
    search=extend_schema(
        parameters=[
            OpenApiParameter(name='lat', type=OpenApiTypes.FLOAT, location=OpenApiParameter.QUERY,
                             description='Latitude of the point to search.'),
            OpenApiParameter(name='lng', type=OpenApiTypes.FLOAT, location=OpenApiParameter.QUERY,
                             description='Longitude of the point to search.'),
        ],
        responses={200: ServiceAreaSerializer(many=True)},
        description="Search for service areas containing the given point (latitude and longitude)."
    ),
)
class ServiceAreaViewSet(viewsets.ModelViewSet):
    """
    CRUD for service areas + search endpoint
    """
    queryset = ServiceArea.objects.select_related("provider")
    serializer_class = ServiceAreaSerializer

    @cache_response(key_func=ServiceAreaKeyConstructor(), timeout=300)
    @action(detail=False, methods=['get'], url_name="search")
    def search(self, request):
        """
        Cached search response (will cache for 300s)
        """
        params = SearchQuerySerializer(data=request.query_params)
        params.is_valid(raise_exception=True)
        point = params.validated_data["point"]
        service_areas = self.get_queryset().filter(polygon__contains=point)
        serializer = self.get_serializer(service_areas, many=True)
        return Response(serializer.data)
