from rest_framework import serializers

class DestinoTuristicoCreateSerializer(serializers.Serializer):
    """
    Serializador para validar la creación de un destino turístico.
    Maneja múltiples relaciones (IDs) y campos de texto con valores por defecto.
    """
    
    # nombre_destino_turistico: Obligatorio, string, no puede estar vacío.
    nombre_destino_turistico = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=150,
        error_messages={
            'required': 'El nombre del destino turístico es obligatorio.',
            'blank': 'El nombre del destino no puede estar vacío.'
        }
    )

    # descripcion: Opcional, string. 
    # Si no existe o viene vacía, se asigna un string vacío "" por defecto.
    descripcion = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        default=""
    )

    # IDs de Relaciones: Todos obligatorios y de tipo entero.
    pais_id = serializers.IntegerField(
        required=True,
        error_messages={'required': 'El ID del país es obligatorio.'}
    )
    ciudad_id = serializers.IntegerField(
        required=True,
        error_messages={'required': 'El ID de la ciudad es obligatorio.'}
    )
    idioma_id = serializers.IntegerField(
        required=True,
        error_messages={'required': 'El ID del idioma es obligatorio.'}
    )
    moneda_id = serializers.IntegerField(
        required=True,
        error_messages={'required': 'El ID de la moneda es obligatorio.'}
    )

    def validate_nombre_destino_turistico(self, value):
        """Limpia espacios en blanco y normaliza el texto."""
        return value.strip()

    def validate_descripcion(self, value):
        """Asegura que si el valor es None o nulo, retorne un string vacío."""
        if value is None:
            return ""
        return value.strip()

    def validate(self, data):
        """Validaciones adicionales de lógica de negocio si fueran necesarias."""
        for field in ['pais_id', 'ciudad_id', 'idioma_id', 'moneda_id']:
            if data.get(field) <= 0:
                raise serializers.ValidationError({field: "El ID debe ser un número entero positivo."})
        return data