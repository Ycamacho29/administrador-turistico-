from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from apps.authentication_microservice.domain.entities.response import ResponseDTO


class AuthUseCases:
    def login(self, request_dto):
        data = request_dto.data
        user = authenticate(username=data['username'], password=data['password'])

        if user is not None:
            refresh = RefreshToken.for_user(user)
            payload = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'username': user.username,
                    'email': user.email
                }
            }
            return ResponseDTO.success(data=payload, mensaje="Login exitoso")

        return ResponseDTO.error(mensaje="Credenciales inválidas")

    def register(self, request_dto):
        data = request_dto.data
        try:
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password']
            )
            return ResponseDTO.success(
                data={"id": user.id, "username": user.username},
                mensaje="Usuario registrado exitosamente"
            )
        except Exception as e:
            return ResponseDTO.error(mensaje=str(e))

    def logout(self, request_dto):
        try:
            # Extraemos el token de refresco para invalidarlo
            refresh_token = request_dto.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()  # Requiere 'rest_framework_simplejwt.token_blacklist' en INSTALLED_APPS

            return ResponseDTO.success(mensaje="Sesión cerrada correctamente")
        except Exception:
            return ResponseDTO.error(mensaje="Token inválido o ya expirado")
