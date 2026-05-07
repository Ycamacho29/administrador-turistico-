from rest_framework import serializers

class CiudadCreateRequestSerializer(serializers.Serializer):
    """
    Serializador para validar el JSON de entrada al crear una ciudad.
    Mapea: 
    {
        "nombre_ciudad": str,
        "pais_id": int
    }
    """
    # nombre_ciudad: Obligatorio, máximo 50 caracteres, no permite vacíos
    nombre_ciudad = serializers.CharField(
        required=True, 
        max_length=50, 
        allow_blank=False,
        error_messages={
            'required': 'El nombre de la ciudad es obligatorio.',
            'max_length': 'El nombre no puede exceder los 50 caracteres.',
            'blank': 'El nombre de la ciudad no puede estar vacío.'
        }
    )

    # pais_id: Obligatorio y debe ser un entero
    pais_id = serializers.IntegerField(
        required=True,
        error_messages={
            'required': 'El ID del país es obligatorio.',
            'invalid': 'El pais_id debe ser un número entero válido.'
        }
    )

    def validate_nombre_ciudad(self, value):
        """
        Validación personalizada adicional (opcional).
        Por ejemplo: evitar caracteres especiales.
        """
        if not value.strip():
            raise serializers.ValidationError("El nombre no puede consistir solo en espacios.")
        return value