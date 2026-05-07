from dataclasses import asdict
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from apps.core.entities.response import ResponseDTO, ErrorDetalle

def custom_exception_handler(exc, context):
    # Primero obtenemos la respuesta estándar de DRF
    response = exception_handler(exc, context)

    # Si es una excepción de validación (400 Bad Request)
    if response is not None and response.status_code == status.HTTP_400_BAD_REQUEST:
        detalles_errores = []

        # DRF devuelve los errores en response.data (dict o list)
        if isinstance(response.data, dict):
            for campo, mensajes in response.data.items():
                mensaje = mensajes[0] if isinstance(mensajes, list) else mensajes
                detalles_errores.append(
                    ErrorDetalle(campo=campo, mensaje=str(mensaje), codigo_error="VALIDATION_ERROR")
                )
        
        # Creamos nuestro ResponseDTO de error
        response_dto = ResponseDTO.error(
            mensaje="Error de validación en los datos de entrada",
            errores=detalles_errores
        )
        
        # Sobrescribimos la respuesta de DRF con nuestro DTO
        response.data = asdict(response_dto)

    return response