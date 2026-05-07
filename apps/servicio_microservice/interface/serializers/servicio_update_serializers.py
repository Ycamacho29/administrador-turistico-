from rest_framework import serializers

class ServicioUpdateSerializer(serializers.Serializer):
    """
    Serializador para validar la actualización de un servicio.
    JSON esperado: { 
        "nombre_servicio": str, 
        "descripcion": str, 
        "costo_bs": decimal,
        "estatus": str 
    }
    """
    
    # nombre_servicio: Obligatorio, string.
    nombre_servicio = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=100,
        error_messages={'required': 'El nombre del servicio es obligatorio.'}
    )

    # descripcion: Obligatorio, string.
    descripcion = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={'required': 'La descripción es obligatoria.'}
    )

    # costo_bs: Obligatorio, número con 2 decimales.
    costo_bs = serializers.DecimalField(
        required=True,
        max_digits=12,
        decimal_places=2,
        min_value=0,
        error_messages={
            'required': 'El costo es obligatorio.',
            'invalid': 'El costo debe ser un número válido.',
            'max_decimal_places': 'El costo solo puede tener dos decimales.'
        }
    )

    # estatus: Obligatorio, string (1 carácter).
    estatus = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=1,
        min_length=1,
        error_messages={
            'required': 'El estatus es obligatorio.',
            'max_length': 'El estatus debe ser un único carácter (A o I).'
        }
    )

    def validate_estatus(self, value):
        """Normaliza el estatus a mayúscula."""
        return value.strip().upper()

    def validate_nombre_servicio(self, value):
        """Limpia espacios en blanco."""
        return value.strip()