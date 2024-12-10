# myapp/views.py

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from traces.models import Device
from .serializers import *

@api_view(['POST'])
def add_device(request):
    serializer = DeviceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def device_health_check(request):
    serializer = DeviceHealthCheckSerializer(data=request.data)
    if serializer.is_valid():
        device_id = serializer.validated_data['device_id']
        created_at = serializer.validated_data['last_active_on']
        cpu_usage = serializer.validated_data['cpu_usage']
        memory_usage = serializer.validated_data['memory_usage']
        disk_usage = serializer.validated_data['disk_usage']
        temperature = serializer.validated_data['temperature']
        forest = serializer.validated_data['forest_id']

        try:
            device = Device.objects.get(device_id=device_id)
            device.last_active_on = created_at
            device.cpu_usage = cpu_usage
            device.memory_usage = memory_usage
            device.disk_usage = disk_usage
            device.temperature = temperature
            device.forest = forest  # Update forest
            device.save()
            return Response({'status': 'success', 'message': 'Device health check updated.'}, status=status.HTTP_200_OK)
        except Device.DoesNotExist:
            return Response({'status': 'error', 'message': 'Device not found.'}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_leopard_trace(request):
    # Include both data and files in the serializer
    data = request.data.copy()  # Create a mutable copy of the request data
    data.update(request.FILES)  # Add files to the data dictionary

    # Validate the forest_id in the request
    forest_id = data.get("forest")
    if not Forest.objects.filter(forest_id=forest_id).exists():
        return Response(
            {"error": "Forest with the provided ID does not exist."},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = LeopardTracesSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
