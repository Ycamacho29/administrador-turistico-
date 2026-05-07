from rest_framework import viewsets, status
from rest_framework.response import Response
from dataclasses import asdict

from apps.paquete_turistico_microservice.domain.entities.response import ResponseDTO
from apps.paquete_turistico_microservice.domain.entities.request import RequestDTO
from apps.paquete_turistico_microservice.application.use_cases import PaqueteTuristicoUseCases
from apps.paquete_turistico_microservice.infrastructure.repositories import PaqueteTuristicoRepository
from apps.paquete_turistico_microservice.interface.serializers.paquete_turistico_create_serializer import PaqueteTuristicoCreateSerializer
from apps.paquete_turistico_microservice.interface.serializers.paquete_turistico_update_serializer import PaqueteTuristicoUpdateSerializer


class PaqueteTuristicoViewSet(viewsets.ViewSet):
    '''
    ViewSet estandarizado que orquesta la comunicación entre 
    HTTP (DRF) y la Lógica de Negocio (Use Cases).
    '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Inyección de dependencias: Repo -> UseCase
        self.repository = PaqueteTuristicoRepository()
        self.use_cases = PaqueteTuristicoUseCases(self.repository)

    def list(self, request):
        response_dto = self.use_cases.get_paquetes_turisticos()

        # Convertimos el dataclass a un diccionario de Python para que DRF lo haga JSON
        return Response(asdict(response_dto), status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        response_dto = self.use_cases.get_paquete_turistico(int(pk))

        if response_dto.estatus == "error":
            return Response(asdict(response_dto), status=status.HTTP_404_NOT_FOUND)

        return Response(asdict(response_dto), status=status.HTTP_200_OK)

    def create(self, request):
        '''
        Crea un nuevo Paquete Turistico en el sistema.
        '''

        # Validar el JSON de entrada con el serializador
        serializer = PaqueteTuristicoCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Crear un Objeto Request con los datos validos
        request_dto = RequestDTO.of(
            data=serializer.validated_data,
            usuario=str(request.user)
        )

        # Llamar al caso de uso
        response_dto = self.use_cases.create_paquete_turistico(request_dto)

        # Respuesta estándar
        status_code = status.HTTP_201_CREATED if response_dto.estatus == "success" else status.HTTP_400_BAD_REQUEST
        return Response(asdict(response_dto), status=status_code)

    def update(self, request, pk=None):
        '''
        Actualiza un Paquete Turistico en el Sistema
        '''

        # Validar los Datos de Entrada
        serializer = PaqueteTuristicoUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request_dto = RequestDTO.of(
            data=serializer.validated_data,
            usuario=str(request.user)
        )
        response_dto = self.use_cases.update_paquete_turistico(int(pk), request_dto)

        if response_dto.estatus == "error":
            status_code = status.HTTP_404_NOT_FOUND if response_dto.codigo == "404" else status.HTTP_400_BAD_REQUEST
            return Response(asdict(response_dto), status=status_code)

        return Response(asdict(response_dto), status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        '''Elimina un Paquete Turistico en el Sistema'''
        response_dto = self.use_cases.delete_paquete_turistico(int(pk))

        if response_dto.estatus == "error":
            return Response(asdict(response_dto), status=status.HTTP_400_BAD_REQUEST)

        return Response(asdict(response_dto), status=status.HTTP_200_OK)
