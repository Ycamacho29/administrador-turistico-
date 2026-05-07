from rest_framework import viewsets, status
from rest_framework.response import Response
from dataclasses import asdict

from apps.pais_microservice.domain.entities.response import ResponseDTO
from apps.pais_microservice.domain.entities.request import RequestDTO
from apps.pais_microservice.application.use_cases import PaisUseCases
from apps.pais_microservice.infrastructure.repositories import PaisRepository
from apps.pais_microservice.interface.serializers.pais_create_serializer import PaisCreateSerializer
from apps.pais_microservice.interface.serializers.pais_update_serializer import PaisUpdateSerializer


class PaisViewSet(viewsets.ViewSet):
    '''
    ViewSet estandarizado que orquesta la comunicación entre 
    HTTP (DRF) y la Lógica de Negocio (Use Cases).
    '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Inyección de dependencias: Repo -> UseCase
        self.repository = PaisRepository()
        self.use_cases = PaisUseCases(self.repository)

    def list(self, request):
        response_dto = self.use_cases.get_paises()

        # Convertimos el dataclass a un diccionario de Python para que DRF lo haga JSON
        return Response(asdict(response_dto), status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        response_dto = self.use_cases.get_pais(int(pk))

        if response_dto.estatus == "error":
            return Response(asdict(response_dto), status=status.HTTP_404_NOT_FOUND)

        return Response(asdict(response_dto), status=status.HTTP_200_OK)

    def create(self, request):
        '''
        Crea un nuevo pais en el sistema.
        '''

        # Validar el JSON de entrada con el serializador
        serializer = PaisCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Crear un Objeto Request con los datos validos
        request_dto = RequestDTO.of(
            data=serializer.validated_data,
            usuario=str(request.user)
        )

        # Llamar al caso de uso
        response_dto = self.use_cases.create_pais(request_dto)

        # Respuesta estándar
        status_code = status.HTTP_201_CREATED if response_dto.estatus == "success" else status.HTTP_400_BAD_REQUEST
        return Response(asdict(response_dto), status=status_code)

    def update(self, request, pk=None):
        '''
        Actualiza un Pais en el Sistema
        '''

        # Validar los Datos de Entrada
        serializer = PaisUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request_dto = RequestDTO.of(
            data=serializer.validated_data,
            usuario=str(request.user)
        )
        response_dto = self.use_cases.update_pais(int(pk), request_dto)

        if response_dto.estatus == "error":
            status_code = status.HTTP_404_NOT_FOUND if response_dto.codigo == "404" else status.HTTP_400_BAD_REQUEST
            return Response(asdict(response_dto), status=status_code)

        return Response(asdict(response_dto), status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        '''Elimina un Pais'''
        response_dto = self.use_cases.delete_pais(int(pk))

        if response_dto.estatus == "error":
            return Response(asdict(response_dto), status=status.HTTP_400_BAD_REQUEST)

        return Response(asdict(response_dto), status=status.HTTP_200_OK)
