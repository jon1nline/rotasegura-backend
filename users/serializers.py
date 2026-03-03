from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile, History


class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(
        max_length=150,
        help_text='Nome completo do usuário',
        style={'placeholder': 'João Silva'}
    )
    email = serializers.EmailField(
        help_text='E-mail do usuário (usado no login)',
        style={'placeholder': 'joao@email.com'}
    )
    password = serializers.CharField(
        write_only=True,
        min_length=6,
        help_text='Senha com no mínimo 6 caracteres',
        style={'input_type': 'password', 'placeholder': '******'}
    )
    phone = serializers.CharField(
        max_length=20,
        required=False,
        allow_blank=True,
        help_text='Telefone (opcional)',
        style={'placeholder': '(11) 99999-9999'}
    )

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('E-mail já cadastrado.')
        return value

    def create(self, validated_data):
        name = validated_data['name'].strip()
        email = validated_data['email'].strip().lower()
        password = validated_data['password']
        phone = validated_data.get('phone', '')

        username_base = email.split('@')[0]
        username = username_base
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f'{username_base}{counter}'
            counter += 1

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=name,
        )
        UserProfile.objects.create(user=user, phone=phone, level=1, xp=0, max_xp=1000)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        help_text='E-mail cadastrado',
        style={'placeholder': 'usuario@email.com'}
    )
    password = serializers.CharField(
        write_only=True,
        help_text='Senha do usuário',
        style={'input_type': 'password', 'placeholder': '******'}
    )


class UserProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.first_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    maxXp = serializers.IntegerField(source='max_xp', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['name', 'email', 'phone', 'address', 'city', 'state', 'level', 'xp', 'maxXp']
        read_only_fields = ['name', 'email', 'level', 'xp', 'maxXp']


class HistorySerializer(serializers.ModelSerializer):
    time = serializers.ReadOnlyField()

    class Meta:
        model = History
        fields = ['id', 'title', 'location', 'time', 'status', 'icon', 'color', 'likes', 'views', 'verified']
