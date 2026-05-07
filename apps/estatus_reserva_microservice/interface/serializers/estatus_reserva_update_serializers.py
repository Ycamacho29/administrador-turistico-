from rest_framework import serializers

class EstatusReservaUpdateSerializer(serializers.Serializer):
    """
    Serializador para validar la actualización de un estatus de reserva.
    Todos los campos son obligatorios y de tipo string.
    """
    
    # nombre_estatus_reserva: Obligatorio, string.
    nombre_estatus_reserva = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=50,
        error_messages={
            'required': 'El nombre del estatus de reserva es obligatorio.',
            'blank': 'El nombre del estatus no puede estar vacío.'
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

    # estatus: Obligatorio, string (1 carácter para representar el estado lógico).
    estatus = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=1,
        min_length=1,
        error_messages={
            'required': 'El estatus del registro es obligatorio.',
            'max_length': 'El estatus debe ser un único carácter (A o I).',
            'min_length': 'El estatus debe tener al menos un carácter.'
        }
    )

    def validate_nombre_estatus_reserva(self, value):
        """Limpia espacios en blanco."""
        return value.strip()

    def validate_descripcion(self, value):
        """Limpia espacios en blanco."""
        return value.strip()

    def validate_estatus(self, value):
        """Normaliza el estatus a mayúscula (A/I)."""
        return value.strip().upper()