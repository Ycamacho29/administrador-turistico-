from rest_framework import serializers

class PaisUpdateSerializer(serializers.Serializer):
    """
    Serializador para validar la actualización o creación de un país.
    JSON esperado: { "nombre_pais": str, "estatus": str }
    """
    
    # nombre_pais: Obligatorio, string, no vacío.
    nombre_pais = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=100,
        error_messages={
            'required': 'El nombre del país es obligatorio.',
            'blank': 'El nombre del país no puede estar vacío.',
            'invalid': 'El nombre del país debe ser una cadena de texto.'
        }
    )

    # estatus: Obligatorio, string.
    estatus = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=1,
        error_messages={
            'required': 'El estatus es obligatorio.',
            'blank': 'El estatus no puede estar vacío.',
            'max_length': 'El estatus debe ser un único carácter (ej. A o I).'
        }
    )

    def validate_estatus(self, value):
        """Asegura que el estatus se guarde siempre en mayúscula."""
        return value.strip().upper()

    def validate_nombre_pais(self, value):
        """Limpia espacios adicionales en el nombre."""
        return value.strip()