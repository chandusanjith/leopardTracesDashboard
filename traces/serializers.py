from rest_framework import serializers
from .models import *

# Serializer for the trace counts (metadata)
class TraceMetadataSerializer(serializers.Serializer):
    type = serializers.CharField()
    area_code = serializers.CharField()
    occurrence_count = serializers.IntegerField()

# Serializer for the paginated trace data
class LeopardTraceSerializer(serializers.ModelSerializer):
    forest_id = serializers.CharField(source="device.forest.forest_id", read_only=True)
    forest_name = serializers.CharField(source="device.forest.forest_name", read_only=True)

    class Meta:
        model = LeopardTraces
        fields = ['type', 'area_code', 'lat', 'long', 'traced_on', 'image', 'forest_id', 'forest_name']
