from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rotasegura.throttles import AuthThrottle
from .models import UserProfile, History
from .serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer, HistorySerializer


@swagger_auto_schema(
	method='post',
	operation_summary='Cadastro de usuário',
	request_body=openapi.Schema(
		type=openapi.TYPE_OBJECT,
		required=['name', 'email', 'password'],
		properties={
			'name': openapi.Schema(type=openapi.TYPE_STRING, description='Nome completo', example='João Silva'),
			'email': openapi.Schema(type=openapi.TYPE_STRING, format='email', description='E-mail', example='joao@email.com'),
			'password': openapi.Schema(type=openapi.TYPE_STRING, description='Senha (mínimo 6 caracteres)', example='123456'),
			'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Telefone (opcional)', example='(11) 99999-9999'),
		},
	),
	responses={
		201: openapi.Response(
			description='Usuário cadastrado com sucesso',
			schema=openapi.Schema(
				type=openapi.TYPE_OBJECT,
				properties={
					'success': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
					'token': openapi.Schema(type=openapi.TYPE_STRING),
					'user': openapi.Schema(
						type=openapi.TYPE_OBJECT,
						properties={
							'name': openapi.Schema(type=openapi.TYPE_STRING),
							'email': openapi.Schema(type=openapi.TYPE_STRING, format='email'),
							'phone': openapi.Schema(type=openapi.TYPE_STRING),
							'level': openapi.Schema(type=openapi.TYPE_INTEGER),
							'xp': openapi.Schema(type=openapi.TYPE_INTEGER),
							'maxXp': openapi.Schema(type=openapi.TYPE_INTEGER),
						},
					),
				},
			),
		),
	},
)
@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([AuthThrottle])
def register_view(request):
	serializer = RegisterSerializer(data=request.data)
	serializer.is_valid(raise_exception=True)
	user = serializer.save()
	refresh = RefreshToken.for_user(user)
	profile = UserProfileSerializer(user.profile).data
	return Response(
		{
			'success': True,
			'token': str(refresh.access_token),
			'user': profile,
		},
		status=status.HTTP_201_CREATED,
	)


@swagger_auto_schema(
	method='post',
	operation_summary='Login de usuário',
	request_body=openapi.Schema(
		type=openapi.TYPE_OBJECT,
		required=['email', 'password'],
		properties={
			'email': openapi.Schema(type=openapi.TYPE_STRING, format='email', description='E-mail cadastrado', example='usuario@email.com'),
			'password': openapi.Schema(type=openapi.TYPE_STRING, description='Senha', example='123456'),
		},
	),
	responses={
		200: openapi.Response(
			description='Login efetuado com sucesso',
			schema=openapi.Schema(
				type=openapi.TYPE_OBJECT,
				properties={
					'token': openapi.Schema(type=openapi.TYPE_STRING, description='JWT token de acesso'),
				},
			),
		),
		400: openapi.Response(description='Credenciais inválidas'),
	},
)
@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([AuthThrottle])
def login_view(request):
	serializer = LoginSerializer(data=request.data)
	serializer.is_valid(raise_exception=True)

	email = serializer.validated_data['email'].strip().lower()
	password = serializer.validated_data['password']

	user = User.objects.filter(email__iexact=email).first()
	if not user:
		return Response({'detail': 'Credenciais inválidas.'}, status=status.HTTP_400_BAD_REQUEST)

	authenticated_user = authenticate(username=user.username, password=password)
	if not authenticated_user:
		return Response({'detail': 'Credenciais inválidas.'}, status=status.HTTP_400_BAD_REQUEST)

	refresh = RefreshToken.for_user(authenticated_user)
	UserProfile.objects.get_or_create(user=authenticated_user)

	return Response({'token': str(refresh.access_token)}, status=status.HTTP_200_OK)


@swagger_auto_schema(
	method='get',
	operation_summary='Perfil do usuário',
	operation_description='Retorna o perfil do usuário autenticado. Requer JWT token no header Authorization: Bearer <token>',
	responses={200: UserProfileSerializer()},
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile_view(request):
	profile, _ = UserProfile.objects.get_or_create(user=request.user)
	return Response(UserProfileSerializer(profile).data)


@swagger_auto_schema(
	method='patch',
	operation_summary='Editar perfil do usuário',
	operation_description='Atualiza o perfil do usuário autenticado. Requer JWT token no header Authorization: Bearer <token>. Campos aceitos: phone, address, city, state.',
	request_body=openapi.Schema(
		type=openapi.TYPE_OBJECT,
		properties={
			'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Telefone', example='(11) 99999-9999'),
			'address': openapi.Schema(type=openapi.TYPE_STRING, description='Endereço completo', example='Rua das Flores, 123'),
			'city': openapi.Schema(type=openapi.TYPE_STRING, description='Cidade', example='São Paulo'),
			'state': openapi.Schema(type=openapi.TYPE_STRING, description='Estado (UF)', example='SP'),
		},
	),
	responses={
		200: openapi.Response(
			description='Perfil atualizado com sucesso',
			schema=UserProfileSerializer(),
		),
		400: openapi.Response(description='Dados inválidos'),
	},
)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def user_profile_update_view(request):
	profile, _ = UserProfile.objects.get_or_create(user=request.user)
	serializer = UserProfileSerializer(profile, data=request.data, partial=True)
	serializer.is_valid(raise_exception=True)
	serializer.save()
	return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
	method='get',
	operation_summary='Histórico do usuário',
	operation_description='Retorna o histórico de contribuições do usuário autenticado. Requer JWT token no header Authorization: Bearer <token>',
	responses={200: HistorySerializer(many=True)},
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_history_view(request):
	history_qs = History.objects.filter(user=request.user)
	return Response(HistorySerializer(history_qs, many=True).data)
