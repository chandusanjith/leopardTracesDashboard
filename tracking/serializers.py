
from rest_framework import serializers
from traces.models import *

class DeviceSerializer(serializers.ModelSerializer):
    forest_id = serializers.PrimaryKeyRelatedField(
        queryset=Forest.objects.all(), source="forest", write_only=True
    )
    forest_name = serializers.CharField(source="forest.forest_name", read_only=True)

    class Meta:
        model = Device
        fields = ['device_id', 'device_name', 'last_active_on', 'forest_id', 'forest_name']


class DeviceHealthCheckSerializer(serializers.Serializer):
    device_id = serializers.CharField(max_length=100)
    last_active_on = serializers.DateTimeField()
    cpu_usage = serializers.CharField(max_length=100)
    memory_usage = serializers.CharField(max_length=100)
    disk_usage = serializers.CharField(max_length=100)
    temperature = serializers.CharField(max_length=100)
    forest_id = serializers.PrimaryKeyRelatedField(queryset=Forest.objects.all())  # New field

class LeopardTracesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeopardTraces
        fields = "__all__"

    def validate_device(self, value):
        if not Device.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Device does not exist.")
        return value

    def validate_forest(self, value):
        if not Forest.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Forest does not exist.")
        return value
