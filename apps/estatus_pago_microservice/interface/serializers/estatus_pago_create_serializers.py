from rest_framework import serializers

class EstatusPagoCreateSerializer(serializers.Serializer):
    """
    Serializador para validar la creación de un estatus de pago.
    JSON esperado: { 
        "nombre_estatus_pago": str, 
        "descripcion": str 
    }
    """
    
    # nombre_estatus_pago: Obligatorio, string, máximo 50 caracteres.
    nombre_estatus_pago = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=50,
        error_messages={
            'required': 'El nombre del estatus de pago es obligatorio.',
            'blank': 'El nombre del estatus no puede estar vacío.',
            'max_length': 'El nombre del estatus no puede exceder los 50 caracteres.'
        }
    )

    # descripcion: Obligatoria, string.
    descripcion = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            'required': 'La descripción es obligatoria.',
            'blank': 'La descripción no puede estar vacía.'
        }
    )

    def validate_nombre_estatus_pago(self, value):
        """Limpia espacios y normaliza el texto."""
        return value.strip().capitalize()

    def validate_descripcion(self, value):
        """Limpia espacios en blanco adicionales."""
        return value.strip()