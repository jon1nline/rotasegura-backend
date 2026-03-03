from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    IncidentViewSet, StopViewSet, AlertViewSet,
    TransportLineViewSet, ReportViewSet,
    line_itinerary
)

router = DefaultRouter()
router.register(r'incidents', IncidentViewSet)
router.register(r'stops', StopViewSet)
router.register(r'alerts', AlertViewSet)
router.register(r'lines', TransportLineViewSet)
router.register(r'reports', ReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('lines/<str:line_id>/itinerary/', line_itinerary, name='line-itinerary'),
]
