
from rest_framework import serializers
from traces.models import Device, LeopardTraces

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['device_id', 'device_name', 'last_active_on']

class DeviceHealthCheckSerializer(serializers.Serializer):
    device_id = serializers.CharField(max_length=100)
    last_active_on = serializers.DateTimeField()
    cpu_usage = serializers.CharField(max_length=100)
    memory_usage = serializers.CharField(max_length=100)
    disk_usage = serializers.CharField(max_length=100)
    temperature = serializers.CharField(max_length=100)

class LeopardTracesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeopardTraces
        fields = ['type','lat', 'long', 'area_code', 'confidence', 'device', 'traced_on']

    def validate_device(self, value):
        if not Device.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Device does not exist.")
        return value
