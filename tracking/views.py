# myapp/views.py

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from traces.models import Device
from .serializers import *

@api_view(['POST'])
def add_device(request):
    if request.method == 'POST':
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
        created_at = serializer.validated_data['created_at']

        try:
            device = Device.objects.get(device_id=device_id)
            device.last_active_on = created_at
            device.save()
            return Response({'status': 'success', 'message': 'Device health check updated.'}, status=status.HTTP_200_OK)
        except Device.DoesNotExist:
            return Response({'status': 'error', 'message': 'Device not found.'}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_leopard_trace(request):
    serializer = LeopardTracesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)