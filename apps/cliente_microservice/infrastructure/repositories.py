from datetime import datetime
from core_models.models.Cliente import Cliente
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class ClienteRepository:
    """
    Implementación del repositorio usando el ORM de Django.
    Esta capa aísla la lógica de negocio de la base de datos.
    """

    def __init__(self):
        self.model = Cliente

    def guardar_cliente(self, datos: dict) -> Cliente:
        """
        Realiza la persistencia física de un nuevo cliente en la base de datos.
        """
        instancia_user = User.objects.get(id=datos.get('user_id'))

        nuevo_cliente = Cliente.objects.create(
            user=instancia_user,
            primer_nombre=datos.get('primer_nombre'),
            segundo_nombre=datos.get('segundo_nombre'),
            primer_apellido=datos.get('primer_apellido'),
            segundo_apellido=datos.get('segundo_apellido'),
            telefono=datos.get('telefono'),
            cedula=datos.get('cedula'),
        )

        return nuevo_cliente

    def obtener_por_id(self, user_id: int) -> Cliente:
        """Busca un Cliente por su clave primaria"""
        try:
            return Cliente.objects.get(user_id=user_id)
        except Cliente.DoesNotExist:
            return None

    def listar_todos(self):
        """Retorna un QuerySet con todos los Clientes"""
        return Cliente.objects.all().order_by('-id')

    def actualizar_cliente(self, cliente_id: int, datos: dict) -> Cliente:
        """Actualiza los campos de un Cliente"""
        cliente = Cliente.objects.get(id=cliente_id)

        # Actualizamos los campos
        cliente.primer_nombre=datos.get('primer_nombre')
        cliente.segundo_nombre=datos.get('segundo_nombre')
        cliente.primer_apellido=datos.get('primer_apellido')
        cliente.segundo_apellido=datos.get('segundo_apellido')
        cliente.telefono=datos.get('telefono')
        cliente.cedula=datos.get('cedula')
        cliente.modificado_en=datetime.now()

        cliente.save()
        return cliente

    def eliminar_cliente(self, cliente_id: int) -> bool:
        """Elimina un Cliente y retorna True si tuvo éxito."""
        try:
            cliente = Cliente.objects.get(id=cliente_id)
            cliente.delete()
            return True
        except Cliente.DoesNotExist:
            return False
