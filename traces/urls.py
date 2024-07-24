from django.contrib import admin
from django.urls import path, include
from traces.views import LoadPage
urlpatterns = [
    path('', LoadPage)
    ]