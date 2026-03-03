from rest_framework import serializers
from .models import Incident, Stop, Alert, TransportLine, Report


class IncidentSerializer(serializers.ModelSerializer):
    desc = serializers.CharField(source='description', read_only=True)
    
    class Meta:
        model = Incident
        fields = ['id', 'type', 'lat', 'lng', 'title', 'desc']


class StopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stop
        fields = ['id', 'type', 'lat', 'lng', 'name']


class AlertSerializer(serializers.ModelSerializer):
    desc = serializers.CharField(source='description', read_only=True)
    time = serializers.ReadOnlyField()
    
    class Meta:
        model = Alert
        fields = ['id', 'type', 'category', 'title', 'desc', 'icon', 'time']


class TransportLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportLine
        fields = ['id', 'name', 'color']


class ReportSerializer(serializers.ModelSerializer):
    category = serializers.CharField(
        help_text='Categoria do reporte (ex: Segurança, Lotação, Avaria)'
    )
    description = serializers.CharField(
        help_text='Descrição detalhada do incidente',
        style={'base_template': 'textarea.html'}
    )
    lat = serializers.FloatField(
        required=False,
        allow_null=True,
        help_text='Latitude da localização (-23.5505)'
    )
    lng = serializers.FloatField(
        required=False,
        allow_null=True,
        help_text='Longitude da localização (-46.6333)'
    )
    photo_url = serializers.URLField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text='URL da foto (opcional)'
    )

    class Meta:
        model = Report
        fields = ['id', 'category', 'description', 'lat', 'lng', 'photo_url', 'created_at']
        read_only_fields = ['id', 'created_at']
