from django.contrib import admin
from .models import Incident, Stop, Alert, TransportLine, Report


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'title', 'lat', 'lng', 'created_at']
    list_filter = ['type', 'created_at']
    search_fields = ['title', 'description']


@admin.register(Stop)
class StopAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type', 'lat', 'lng']
    list_filter = ['type']
    search_fields = ['name']


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'category', 'title', 'created_at']
    list_filter = ['type', 'category', 'created_at']
    search_fields = ['title', 'description']


@admin.register(TransportLine)
class TransportLineAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type', 'color']
    list_filter = ['type']
    search_fields = ['name']


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'user', 'lat', 'lng', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['category', 'description', 'user__username']
