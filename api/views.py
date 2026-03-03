from math import cos, radians

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.db.models import F, FloatField, Value, ExpressionWrapper
from django.db.models.functions import Power
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rotasegura.throttles import (
    ListAnonThrottle,
    ListUserThrottle,
    CreateAnonThrottle,
    CreateUserThrottle,
)
from .models import Incident, Stop, Alert, TransportLine, Report
from .serializers import (
    IncidentSerializer, StopSerializer, AlertSerializer,
    TransportLineSerializer, ReportSerializer
)


class IncidentViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint para incidentes"""
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    throttle_classes = [ListAnonThrottle, ListUserThrottle]

    @swagger_auto_schema(
        operation_summary='Listar incidentes',
        operation_description='Retorna a lista de incidentes disponíveis. Se informado, aplica filtro geográfico por raio (km) e ordena pelos mais próximos.',
        manual_parameters=[
            openapi.Parameter(
                'lat',
                openapi.IN_QUERY,
                description='Latitude do ponto central do filtro',
                type=openapi.TYPE_NUMBER,
                format=openapi.FORMAT_FLOAT,
            ),
            openapi.Parameter(
                'lng',
                openapi.IN_QUERY,
                description='Longitude do ponto central do filtro',
                type=openapi.TYPE_NUMBER,
                format=openapi.FORMAT_FLOAT,
            ),
            openapi.Parameter(
                'radius',
                openapi.IN_QUERY,
                description='Raio de busca em quilômetros',
                type=openapi.TYPE_NUMBER,
                format=openapi.FORMAT_FLOAT,
            ),
        ],
        responses={200: IncidentSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Detalhar incidente',
        operation_description='Retorna os dados de um incidente pelo ID (UUID).',
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description='UUID do incidente',
                type=openapi.TYPE_STRING,
                format='uuid',
            )
        ],
        responses={200: IncidentSerializer()},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Incident.objects.all()

        lat_param = self.request.query_params.get('lat')
        lng_param = self.request.query_params.get('lng')
        radius_param = self.request.query_params.get('radius')

        if not any([lat_param, lng_param, radius_param]):
            return queryset

        if not all([lat_param, lng_param, radius_param]):
            raise ValidationError('Para filtro geográfico, envie lat, lng e radius juntos.')

        try:
            lat = float(lat_param)
            lng = float(lng_param)
            radius_km = float(radius_param)
        except ValueError as exc:
            raise ValidationError('lat, lng e radius devem ser números válidos.') from exc

        if radius_km <= 0:
            raise ValidationError('radius deve ser maior que 0.')

        lat_delta = radius_km / 111.0
        cos_lat = max(abs(cos(radians(lat))), 0.01)
        lng_delta = radius_km / (111.0 * cos_lat)

        queryset = queryset.filter(
            lat__gte=lat - lat_delta,
            lat__lte=lat + lat_delta,
            lng__gte=lng - lng_delta,
            lng__lte=lng + lng_delta,
        )

        lat_km_factor = 111.0
        lng_km_factor = 111.0 * cos_lat
        distance_sq_expr = ExpressionWrapper(
            Power((F('lat') - Value(lat)) * Value(lat_km_factor), 2) +
            Power((F('lng') - Value(lng)) * Value(lng_km_factor), 2),
            output_field=FloatField(),
        )
        queryset = queryset.annotate(distance_sq=distance_sq_expr).order_by('distance_sq')

        return queryset


class StopViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint para paradas de transporte"""
    queryset = Stop.objects.all()
    serializer_class = StopSerializer
    throttle_classes = [ListAnonThrottle, ListUserThrottle]

    @swagger_auto_schema(
        operation_summary='Listar paradas',
        operation_description='Retorna a lista de paradas de transporte.',
        responses={200: StopSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Detalhar parada',
        operation_description='Retorna os dados de uma parada pelo ID (UUID).',
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description='UUID da parada',
                type=openapi.TYPE_STRING,
                format='uuid',
            )
        ],
        responses={200: StopSerializer()},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class AlertViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint para alertas"""
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    throttle_classes = [ListAnonThrottle, ListUserThrottle]

    @swagger_auto_schema(
        operation_summary='Listar alertas',
        operation_description='Retorna alertas de segurança e operação.',
        responses={200: AlertSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Detalhar alerta',
        operation_description='Retorna os dados de um alerta pelo ID (UUID).',
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description='UUID do alerta',
                type=openapi.TYPE_STRING,
                format='uuid',
            )
        ],
        responses={200: AlertSerializer()},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class TransportLineViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint para linhas de transporte"""
    queryset = TransportLine.objects.all()
    serializer_class = TransportLineSerializer
    throttle_classes = [ListAnonThrottle, ListUserThrottle]

    @swagger_auto_schema(
        operation_summary='Listar linhas de transporte',
        operation_description='Retorna linhas de transporte, com filtro opcional por tipo.',
        manual_parameters=[
            openapi.Parameter(
                'type',
                openapi.IN_QUERY,
                description='Filtra por tipo de linha',
                type=openapi.TYPE_STRING,
                enum=['metro', 'trem', 'bus'],
            )
        ],
        responses={200: TransportLineSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Detalhar linha',
        operation_description='Retorna os dados de uma linha pelo ID (UUID).',
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description='UUID da linha de transporte',
                type=openapi.TYPE_STRING,
                format='uuid',
            )
        ],
        responses={200: TransportLineSerializer()},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        queryset = TransportLine.objects.all()
        line_type = self.request.query_params.get('type', None)
        if line_type:
            queryset = queryset.filter(type=line_type)
        return queryset


class ReportViewSet(viewsets.ModelViewSet):
    """API endpoint para reportes"""
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    throttle_classes = [ListAnonThrottle, ListUserThrottle, CreateAnonThrottle, CreateUserThrottle]

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        return [AllowAny()]

    @swagger_auto_schema(
        operation_summary='Listar reportes',
        operation_description='Retorna reportes enviados pelos usuários.',
        responses={200: ReportSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Detalhar reporte',
        operation_description='Retorna os dados de um reporte pelo ID (UUID).',
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description='UUID do reporte',
                type=openapi.TYPE_STRING,
                format='uuid',
            )
        ],
        responses={200: ReportSerializer()},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Criar reporte',
        operation_description='Cria um novo reporte de incidente. Requer autenticação via Bearer token (Header: Authorization: Bearer <seu_token>).',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['category', 'description'],
            properties={
                'category': openapi.Schema(type=openapi.TYPE_STRING, description='Categoria do reporte', example='Segurança'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='Descrição detalhada', example='Assalto relatado próximo à estação'),
                'lat': openapi.Schema(type=openapi.TYPE_NUMBER, format='float', description='Latitude', example=-23.5505),
                'lng': openapi.Schema(type=openapi.TYPE_NUMBER, format='float', description='Longitude', example=-46.6333),
                'photo_url': openapi.Schema(type=openapi.TYPE_STRING, format='uri', description='URL da foto (opcional)', example='https://exemplo.com/foto.jpg'),
            },
        ),
        security=[{'Bearer': []}],
        responses={
            201: openapi.Response(
                description='Reporte criado com sucesso',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                        'id': openapi.Schema(type=openapi.TYPE_STRING, format='uuid', description='UUID do reporte criado'),
                    },
                ),
            ),
            401: openapi.Response(description='Não autenticado - Token inválido ou ausente'),
        },
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            'success': True,
            'id': serializer.data['id']
        }, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@swagger_auto_schema(
    method='get',
    operation_summary='Itinerário da linha',
    operation_description='Retorna o itinerário mock de uma linha específica.',
    manual_parameters=[
        openapi.Parameter(
            'line_id',
            openapi.IN_PATH,
            description='UUID da linha de transporte (formato: UUID)',
            type=openapi.TYPE_STRING,
            format='uuid',
            required=True,
        )
    ],
    responses={
        200: openapi.Response(
            description='Itinerário retornado com sucesso',
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_STRING),
                        'name': openapi.Schema(type=openapi.TYPE_STRING),
                        'time': openapi.Schema(type=openapi.TYPE_STRING),
                        'status': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
        )
    },
)
@api_view(['GET'])
def line_itinerary(request, line_id):
    """Endpoint para itinerário de uma linha específica"""
    data = [
        {'id': '1', 'name': 'Terminal Lapa', 'time': 'Passou', 'status': 'past'},
        {'id': '2', 'name': 'Rua Clélia', 'time': 'Passou', 'status': 'past'},
        {'id': '3', 'name': 'Sesc Pompéia', 'time': 'Agora', 'status': 'current'},
        {'id': '4', 'name': 'Metrô Sumaré', 'time': '4 min', 'status': 'future'},
        {'id': '5', 'name': 'Av. Paulista (MASP)', 'time': '10 min', 'status': 'future'},
        {'id': '6', 'name': 'Metrô Ana Rosa', 'time': '15 min', 'status': 'future'},
    ]
    return Response(data)
