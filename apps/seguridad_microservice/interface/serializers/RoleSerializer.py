from django.contrib.auth.models import Group, Permission
from rest_framework import serializers
from .PermissionSerializer import PermissionSerializer

class RoleSerializer(serializers.ModelSerializer):
    # Mostramos los detalles de los permisos asociados al rol
    permissions_details = PermissionSerializer(source='permissions', many=True, read_only=True)
    # Recibimos una lista de IDs de permisos al crear/modificar
    permissions = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Permission.objects.all(), write_only=True, required=False
    )

    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions', 'permissions_details']