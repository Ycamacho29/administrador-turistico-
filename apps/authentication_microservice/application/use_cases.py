from django.db import transaction
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from apps.authentication_microservice.domain.entities.response import ResponseDTO



class AuthUseCases:

    def __init__(self, cliente_repository):
        self.cliente_repository = cliente_repository

    def login(self, request_dto):
        data = request_dto.data
        user = authenticate(
            username=data['username'], password=data['password'])

        if user is not None:
            refresh = RefreshToken.for_user(user)
            payload = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            }
            return ResponseDTO.success(data=payload, mensaje="Login exitoso")

        return ResponseDTO.error(mensaje="Credenciales inválidas")

    def register(self, request_dto):
        data = request_dto.data
        try:
            # Iniciamos una transacción atómica para asegurar consistencia
            with transaction.atomic():

                # 1. Verificar si el usuario o el email ya existen en Django Auth
                if User.objects.filter(username=data['username']).exists():
                    return ResponseDTO.error("El nombre de usuario ya está registrado", "400")
                if User.objects.filter(email=data['email']).exists():
                    return ResponseDTO.error("El correo electrónico ya está registrado", "400")

                # 2. Crear el usuario en la tabla auth_user de Django
                nuevo_usuario = User.objects.create_user(
                    username=data['username'],
                    email=data['email'],
                    password=data['password']
                )

                # 3. Preparar los datos para la tabla puente/perfil Cliente
                # Vinculamos al cliente con su respectivo ID de usuario de Django si tu modelo lo requiere
                datos = {
                    "user_id": nuevo_usuario.id, 
                    "primer_nombre": data['primer_nombre'],
                    "segundo_nombre": data.get('segundo_nombre', ''),
                    "primer_apellido": data['primer_apellido'],
                    "segundo_apellido": data.get('segundo_apellido', ''),
                    "cedula": data['cedula'],
                    "telefono": data['telefono']
                }

                # 4. Guardar en tu tabla Cliente usando su repositorio
                self.cliente_repository.guardar_cliente(self, datos)

            return ResponseDTO.success(
                data={
                    "mensaje": "Usuario y Cliente registrados con éxito"}
            )

        except Exception as e:
            return ResponseDTO.error(f"Error interno durante el registro: {str(e)}", "500")

    def logout(self, request_dto):
        try:
            # Extraemos el token de refresco para invalidarlo
            refresh_token = request_dto.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()  # Requiere 'rest_framework_simplejwt.token_blacklist' en INSTALLED_APPS

            return ResponseDTO.success(mensaje="Sesión cerrada correctamente")
        except Exception:
            return ResponseDTO.error(mensaje="Token inválido o ya expirado")
