from rest_framework import serializers

class TipoPaqueteCreateSerializer(serializers.Serializer):
    """
    Serializador para validar la creación de un tipo de paquete.
    JSON esperado: { 
        "nombre_tipo_paquete": str, 
        "descripcion": str (opcional) 
    }
    """
    
    # nombre_tipo_paquete: Obligatorio, string, máximo 100 caracteres.
    nombre_tipo_paquete = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=100,
        error_messages={
            'required': 'El nombre del tipo de paquete es obligatorio.',
            'blank': 'El nombre del tipo de paquete no puede estar vacío.'
        }
    )

    # descripcion: Opcional, string.
    # required=False permite que la llave no venga en el JSON.
    # allow_blank=True permite que el valor sea "" (string vacío).
    # allow_null=True permite que el valor sea null.
    descripcion = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        default="" 
    )

    def validate_nombre_tipo_paquete(self, value):
        """Limpia espacios y normaliza el texto."""
        return value.strip().capitalize()

    def validate_descripcion(self, value):
        """Si viene descripción, limpiamos espacios adicionales."""
        return value.strip() if value else ""