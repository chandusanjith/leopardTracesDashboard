from django.contrib import admin
from django.urls import path, include
from traces.views import LoadPage, get_notifications, TraceMetadataView, PaginatedTracesView, DetectionGraphView

urlpatterns = [
    path('', LoadPage),
    path('notifications/', get_notifications, name='get_notifications'),
    path('api/metadata/', TraceMetadataView.as_view(), name='trace_metadata'),
    path('api/detection/chart/<int:id>/', DetectionGraphView.as_view(), name='detection_graph'),
    path('api/traces/', PaginatedTracesView.as_view(), name='paginated_traces'),
    ]
