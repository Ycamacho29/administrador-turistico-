from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from dataclasses import asdict

# Importamos DTOs y lógica
from apps.destino_turistico_microservice.domain.entities.request import RequestDTO
from apps.destino_turistico_microservice.application.use_cases import DestinoTuristicoUseCases
from apps.destino_turistico_microservice.infrastructure.repositories import DestinoTuristicoRepository
from apps.destino_turistico_microservice.interface.serializers.destino_turistico_create_serializers import DestinoTuristicoCreateSerializer
from apps.destino_turistico_microservice.interface.serializers.destino_turistico_update_serializers import DestinoTuristicoUpdateSerializer

class DestinoTuristicoViewSet(viewsets.ViewSet):
    """
    ViewSet estandarizado que orquesta la comunicación entre 
    HTTP (DRF) y la Lógica de Negocio (Use Cases).
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Inyección de dependencias: Repo -> UseCase
        self.repository = DestinoTuristicoRepository()
        self.use_cases = DestinoTuristicoUseCases(self.repository)


    def get_permissions(self):
        """
        Sobreescribe las restricciones globales de Django REST Framework
        dependiendo de la acción que ejecute el cliente.
        """
        # 'list' corresponde al GET general (Ver todos)
        # 'retrieve' corresponde al GET por ID (Ver detalle de uno)
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            # 'create' (POST), 'update' (PUT/PATCH), 'destroy' (DELETE) exigen JWT
            permission_classes = [IsAuthenticated]
            
        # Retornamos las instancias de los permisos mapeados
        return [permission() for permission in permission_classes]

    def list(self, request):
        response_dto = self.use_cases.get_destinos_turisticos()

        # Convertimos el dataclass a un diccionario de Python para que DRF lo haga JSON
        return Response(asdict(response_dto), status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        response_dto = self.use_cases.get_destino_turistico(int(pk))

        if response_dto.estatus == "error":
            return Response(asdict(response_dto), status=status.HTTP_404_NOT_FOUND)

        return Response(asdict(response_dto), status=status.HTTP_200_OK)

    def create(self, request):
        '''
        Crea un nuevo Destino Turistico en el sistema.

        Coordina el flujo de entrada desde la petición HTTP, valida la 
        integridad de los datos mediante un serializador, transforma la 
        información a un DTO de dominio y delega la persistencia al 
        caso de uso correspondiente.
        '''

        # Validar el JSON de entrada con el serializador
        serializer = DestinoTuristicoCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Crear un Objeto Request con los datos validos
        request_dto = RequestDTO.of(
            data=serializer.validated_data,
            usuario=str(request.user)
        )

        # Llamar al caso de uso
        response_dto = self.use_cases.create_destino_turistico(request_dto)

        # Respuesta estándar
        status_code = status.HTTP_201_CREATED if response_dto.estatus == "success" else status.HTTP_400_BAD_REQUEST
        return Response(asdict(response_dto), status=status_code)

    def update(self, request, pk=None):
        '''
        Actualiza un Destino Turistico en el Sistema
        '''

        # Validar los Datos de Entrada
        serializer = DestinoTuristicoUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request_dto = RequestDTO.of(
            data=serializer.validated_data,
            usuario=str(request.user)
        )
        response_dto = self.use_cases.update_destino_turistico(int(pk), request_dto)

        if response_dto.estatus == "error":
            status_code = status.HTTP_404_NOT_FOUND if response_dto.codigo == "404" else status.HTTP_400_BAD_REQUEST
            return Response(asdict(response_dto), status=status_code)

        return Response(asdict(response_dto), status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        '''Elimina un Destino Turistico'''
        response_dto = self.use_cases.delete_destino_turistico(int(pk))

        if response_dto.estatus == "error":
            return Response(asdict(response_dto), status=status.HTTP_400_BAD_REQUEST)

        return Response(asdict(response_dto), status=status.HTTP_200_OK)
