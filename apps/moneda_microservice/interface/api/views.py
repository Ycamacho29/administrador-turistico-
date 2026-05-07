from rest_framework import viewsets, status
from rest_framework.response import Response
from dataclasses import asdict

# Importamos DTOs y lógica
from apps.moneda_microservice.domain.entities.request import RequestDTO
from apps.moneda_microservice.application.use_cases import MonedaUseCases
from apps.moneda_microservice.infrastructure.repositories import MonedaRepository
from apps.moneda_microservice.interface.serializers.moneda_create_serializers import MonedaCreateSerializer
from apps.moneda_microservice.interface.serializers.moneda_update_serializers import MonedaUpdateSerializer

class MonedaViewSet(viewsets.ViewSet):
    """
    ViewSet estandarizado que orquesta la comunicación entre 
    HTTP (DRF) y la Lógica de Negocio (Use Cases).
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Inyección de dependencias: Repo -> UseCase
        self.repository = MonedaRepository()
        self.use_cases = MonedaUseCases(self.repository)

    def list(self, request):
        response_dto = self.use_cases.get_monedas()

        # Convertimos el dataclass a un diccionario de Python para que DRF lo haga JSON
        return Response(asdict(response_dto), status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        response_dto = self.use_cases.get_moneda(int(pk))

        if response_dto.estatus == "error":
            return Response(asdict(response_dto), status=status.HTTP_404_NOT_FOUND)

        return Response(asdict(response_dto), status=status.HTTP_200_OK)

    def create(self, request):
        '''
        Crea una nueva moneda en el sistema.

        Coordina el flujo de entrada desde la petición HTTP, valida la 
        integridad de los datos mediante un serializador, transforma la 
        información a un DTO de dominio y delega la persistencia al 
        caso de uso correspondiente.
        '''

        # Validar el JSON de entrada con el serializador
        serializer = MonedaCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Crear un Objeto Request con los datos validos
        request_dto = RequestDTO.of(
            data=serializer.validated_data,
            usuario=str(request.user)
        )

        # Llamar al caso de uso
        response_dto = self.use_cases.create_moneda(request_dto)

        # Respuesta estándar
        status_code = status.HTTP_201_CREATED if response_dto.estatus == "success" else status.HTTP_400_BAD_REQUEST
        return Response(asdict(response_dto), status=status_code)

    def update(self, request, pk=None):
        '''
        Actualiza una Moneda en el Sistema
        '''

        # Validar los Datos de Entrada
        serializer = MonedaUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request_dto = RequestDTO.of(
            data=serializer.validated_data,
            usuario=str(request.user)
        )

        response_dto = self.use_cases.update_moneda(int(pk), request_dto)

        if response_dto.estatus == "error":
            status_code = status.HTTP_404_NOT_FOUND if response_dto.codigo == "404" else status.HTTP_400_BAD_REQUEST
            return Response(asdict(response_dto), status=status_code)

        return Response(asdict(response_dto), status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        '''Elimina una Moneda'''
        response_dto = self.use_cases.delete_moneda(int(pk))

        if response_dto.estatus == "error":
            return Response(asdict(response_dto), status=status.HTTP_400_BAD_REQUEST)

        return Response(asdict(response_dto), status=status.HTTP_200_OK)
