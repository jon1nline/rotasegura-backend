import uuid
from django.contrib.auth.models import User
from django.db import models


class Incident(models.Model):
    """Incidentes/ocorrências reportados no mapa"""
    TYPE_CHOICES = [
        ('Avaria', 'Avaria'),
        ('Lotação', 'Lotação'),
        ('Segurança', 'Segurança'),
        ('Seguro', 'Seguro'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    lat = models.FloatField()
    lng = models.FloatField()
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.type} - {self.title}"
    
    class Meta:
        ordering = ['-created_at']


class Stop(models.Model):
    """Paradas de transporte público"""
    TYPE_CHOICES = [
        ('bus', 'Ônibus'),
        ('subway', 'Metrô'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    lat = models.FloatField()
    lng = models.FloatField()
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class Alert(models.Model):
    """Alertas do sistema"""
    TYPE_CHOICES = [
        ('critical', 'Crítico'),
        ('warning', 'Aviso'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    category = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.category} - {self.title}"
    
    @property
    def time(self):
        """Retorna tempo relativo"""
        from django.utils import timezone
        diff = timezone.now() - self.created_at
        
        if diff.seconds < 60:
            return 'agora'
        elif diff.seconds < 3600:
            mins = diff.seconds // 60
            return f'há {mins} min'
        elif diff.seconds < 86400:
            hours = diff.seconds // 3600
            return f'há {hours}h'
        else:
            days = diff.days
            return f'há {days}d'
    
    class Meta:
        ordering = ['-created_at']


class TransportLine(models.Model):
    """Linhas de transporte (metrô/trem)"""
    TYPE_CHOICES = [
        ('metro', 'Metrô'),
        ('trem', 'Trem'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name


class Report(models.Model):
    """Reportes enviados pelos usuários"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.CharField(max_length=50)
    description = models.TextField()
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    photo_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.category} - {self.created_at.strftime('%d/%m/%Y %H:%M')}"
    
    class Meta:
        ordering = ['-created_at']
