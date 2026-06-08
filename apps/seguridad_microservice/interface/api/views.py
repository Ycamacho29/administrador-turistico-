from django.contrib.auth.models import Group, Permission, User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser

from apps.seguridad_microservice.interface.serializers.AssignRoleSerializer import AssignRoleSerializer
from apps.seguridad_microservice.interface.serializers.RoleSerializer import RoleSerializer
from apps.seguridad_microservice.interface.serializers.PermissionSerializer import PermissionSerializer

class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    CRUD de Permisos (Solo lectura desde API, Django los crea automáticamente por modelos)
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAdminUser] # Solo administradores globales acceden


class RoleViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para Roles (Creación, Consulta, Modificación y Eliminación)
    """
    queryset = Group.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdminUser]

    # --- MÉTODO EXTRA: Asignar Roles a un Usuario ---
    @action(detail=False, methods=['post'], url_path='asignar-usuario')
    def asignar_rol_usuario(self, request):
        serializer = AssignRoleSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(User, id=serializer.validated_data['user_id'])
            roles = Group.objects.filter(id__in=serializer.validated_data['role_ids'])
            
            # Sincronizar los grupos del usuario
            user.groups.set(roles)
            user.save()
            
            return Response(
                {"message": f"Roles asignados correctamente al usuario {user.username}"}, 
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)