from rest_framework import viewsets, status
from rest_framework.response import Response
from dataclasses import asdict

# Importamos DTOs y lógica
from apps.pago_microservice.domain.entities.request import RequestDTO
from apps.pago_microservice.application.use_cases import PagoUseCases
from apps.pago_microservice.infrastructure.repositories import PagoRepository
from apps.pago_microservice.interface.serializers.pago_create_serializers import PagoCreateSerializer
from apps.pago_microservice.interface.serializers.pago_update_serializers import PagoUpdateSerializer 

class PagoViewSet(viewsets.ViewSet):
    """
    ViewSet estandarizado que orquesta la comunicación entre 
    HTTP (DRF) y la Lógica de Negocio (Use Cases).
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Inyección de dependencias: Repo -> UseCase
        self.repository = PagoRepository()
        self.use_cases = PagoUseCases(self.repository)

    def list(self, request):
        response_dto = self.use_cases.get_pagos()

        # Convertimos el dataclass a un diccionario de Python para que DRF lo haga JSON
        return Response(asdict(response_dto), status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        response_dto = self.use_cases.get_pago(int(pk))

        if response_dto.estatus == "error":
            return Response(asdict(response_dto), status=status.HTTP_404_NOT_FOUND)

        return Response(asdict(response_dto), status=status.HTTP_200_OK)

    def create(self, request):
        '''
        Crea un nuevo pago en el sistema.

        Coordina el flujo de entrada desde la petición HTTP, valida la 
        integridad de los datos mediante un serializador, transforma la 
        información a un DTO de dominio y delega la persistencia al 
        caso de uso correspondiente.
        '''

        # Validar el JSON de entrada con el serializador
        serializer = PagoCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Crear un Objeto Request con los datos validos
        request_dto = RequestDTO.of(
            data=serializer.validated_data,
            usuario=str(request.user)
        )

        # Llamar al caso de uso
        response_dto = self.use_cases.create_pago(request_dto)

        # Respuesta estándar
        status_code = status.HTTP_201_CREATED if response_dto.estatus == "success" else status.HTTP_400_BAD_REQUEST
        return Response(asdict(response_dto), status=status_code)

    def update(self, request, pk=None):
        '''
        Actualiza un Pago en el Sistema
        '''

        # Validar los Datos de Entrada
        serializer = PagoUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request_dto = RequestDTO.of(
            data=serializer.validated_data,
            usuario=str(request.user)
        )
        response_dto = self.use_cases.update_pago(int(pk), request_dto)

        if response_dto.estatus == "error":
            status_code = status.HTTP_404_NOT_FOUND if response_dto.codigo == "404" else status.HTTP_400_BAD_REQUEST
            return Response(asdict(response_dto), status=status_code)

        return Response(asdict(response_dto), status=status.HTTP_200_OK)

    # def destroy(self, request, pk=None):
    #     '''Elimina un Pago'''
    #     response_dto = self.use_cases.delete_pago(int(pk))

    #     if response_dto.estatus == "error":
    #         return Response(asdict(response_dto), status=status.HTTP_400_BAD_REQUEST)

    #     return Response(asdict(response_dto), status=status.HTTP_200_OK)
