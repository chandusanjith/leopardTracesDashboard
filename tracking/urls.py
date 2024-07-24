from django.urls import path
from .views import *

urlpatterns = [
    path('api/add-device/', add_device, name='add_device'),
    path('api/device-health-check/', device_health_check, name='device_health_check'),
    path('api/add-leopard-trace/', add_leopard_trace, name='add_leopard_trace'),

]