from rest_framework import serializers

class ServicioCreateSerializer(serializers.Serializer):
    """
    Serializador para validar la creación de un servicio.
    JSON esperado: { 
        "nombre_servicio": str, 
        "descripcion": str, 
        "costo_bs": decimal 
    }
    """
    
    # nombre_servicio: Obligatorio, string, máximo 100 caracteres.
    nombre_servicio = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=100,
        error_messages={
            'required': 'El nombre del servicio es obligatorio.',
            'blank': 'El nombre del servicio no puede estar vacío.'
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

    # costo_bs: Obligatorio, numérico con 2 decimales.
    costo_bs = serializers.DecimalField(
        required=True,
        max_digits=12,      # Permite hasta 999,999,999.99
        decimal_places=2,   # Obliga a tener 2 decimales
        min_value=0,        # Evita costos negativos
        error_messages={
            'required': 'El costo en bolívares es obligatorio.',
            'invalid': 'El costo debe ser un número válido.',
            'max_digits': 'El costo excede el número de dígitos permitido.',
            'max_decimal_places': 'El costo no puede tener más de 2 decimales.'
        }
    )

    def validate_nombre_servicio(self, value):
        """Limpia espacios en blanco."""
        return value.strip()