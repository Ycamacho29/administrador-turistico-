from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(required=True, write_only=True)

    # Datos obligatorios para tu tabla Cliente
    primer_nombre = serializers.CharField(required=True)
    segundo_nombre = serializers.CharField(required=False, allow_blank=True, default="")
    primer_apellido = serializers.CharField(required=True)
    segundo_apellido = serializers.CharField(required=False, allow_blank=True, default="")
    cedula = serializers.CharField(required=True)
    telefono = serializers.CharField(required=True)

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "El nombre de usuario ya existe."})
        return data
