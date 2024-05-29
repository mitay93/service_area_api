from django.contrib.gis.geos import Point, Polygon
from rest_framework import serializers

from .models import Provider, ServiceArea


class PolygonField(serializers.Field):
    """
    This field is needed to convert a GEOjson polygon to a Polygon type and back
    """
    def to_internal_value(self, data):
        try:
            return Polygon(data['coordinates'][0])
        except (KeyError, TypeError, ValueError):
            raise serializers.ValidationError("Invalid GeoJSON format for Polygon")

    def to_representation(self, value):
        return {
            "type": "Polygon",
            "coordinates": [list(value[0].coords)]
        }


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = '__all__'


class ServiceAreaSerializer(serializers.ModelSerializer):
    """
    Serializer for ServiceArea model. Provider will be displayed as ID
    """
    polygon = PolygonField()

    class Meta:
        model = ServiceArea
        fields = '__all__'


class SearchQuerySerializer(serializers.Serializer):
    """
    Serializer for latitune and longitune query. It will have Point object in validated_data after validation
    """
    lng = serializers.FloatField()
    lat = serializers.FloatField()

    def validate(self, attrs):
        try:
            attrs['point'] = Point(x=attrs["lng"], y=attrs["lat"])
        except ValueError:
            raise serializers.ValidationError("Invalid coordinates")
        return attrs
