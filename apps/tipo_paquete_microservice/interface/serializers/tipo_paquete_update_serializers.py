from rest_framework import serializers

class TipoPaqueteUpdateSerializer(serializers.Serializer):
    """
    Serializador para validar la actualización de un tipo de paquete.
    JSON esperado: { 
        "nombre_tipo_paquete": str, 
        "descripcion": str (opcional),
        "estatus": str 
    }
    """
    
    # nombre_tipo_paquete: Obligatorio, string, máximo 100 caracteres.
    nombre_tipo_paquete = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=100,
        error_messages={'required': 'El nombre del tipo de paquete es obligatorio.'}
    )

    # descripcion: Opcional, string. Puede ser nulo o estar vacío.
    descripcion = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        default=""
    )

    # estatus: Obligatorio, string de 1 carácter.
    estatus = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=1,
        min_length=1,
        error_messages={
            'required': 'El estatus es obligatorio.',
            'max_length': 'El estatus debe ser un único carácter (A o I).',
        }
    )

    def validate_nombre_tipo_paquete(self, value):
        """Limpia espacios en blanco."""
        return value.strip()

    def validate_descripcion(self, value):
        """Asegura que la descripción no guarde nulos, sino strings vacíos si no viene nada."""
        return value.strip() if value else ""

    def validate_estatus(self, value):
        """Normaliza el estatus a mayúscula y valida que sea letra."""
        value = value.strip().upper()
        if not value.isalpha():
            raise serializers.ValidationError("El estatus debe ser una letra (A o I).")
        return value