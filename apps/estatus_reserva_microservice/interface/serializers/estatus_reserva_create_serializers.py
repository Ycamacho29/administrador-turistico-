from rest_framework import serializers

class EstatusReservaCreateSerializer(serializers.Serializer):
    """
    Serializador para validar la creación de un estatus de reserva.
    JSON esperado: { 
        "nombre_estatus_reserva": str, 
        "descripcion": str 
    }
    """
    
    # nombre_estatus_reserva: Obligatorio, string, máximo 50 caracteres.
    nombre_estatus_reserva = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=50,
        error_messages={
            'required': 'El nombre del estatus de reserva es obligatorio.',
            'blank': 'El nombre del estatus no puede estar vacío.',
            'max_length': 'El nombre del estatus no puede exceder los 50 caracteres.'
        }
    )

    # descripcion: Obligatorio, string.
    descripcion = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            'required': 'La descripción es obligatoria.',
            'blank': 'La descripción no puede estar vacía.'
        }
    )

    def validate_nombre_estatus_reserva(self, value):
        """Limpia espacios y asegura formato tipo Título."""
        return value.strip().title()

    def validate_descripcion(self, value):
        """Limpia espacios en blanco adicionales."""
        return value.strip()