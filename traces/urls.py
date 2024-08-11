from django.contrib import admin
from django.urls import path, include
from traces.views import LoadPage, get_notifications

urlpatterns = [
    path('', LoadPage),
    path('notifications/', get_notifications, name='get_notifications'),
    ]
