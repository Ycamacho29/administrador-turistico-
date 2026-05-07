from rest_framework import serializers

class MetodoPagoUpdateSerializer(serializers.Serializer):
    """
    Serializador para validar la actualización de un método de pago.
    JSON esperado: { "nombre_metodo_pago": str, "estatus": str }
    """
    
    # nombre_metodo_pago: Obligatorio, string, máximo 50 caracteres.
    nombre_metodo_pago = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=50,
        error_messages={
            'required': 'El nombre del método de pago es obligatorio.',
            'blank': 'El nombre del método de pago no puede estar vacío.',
        }
    )

    # estatus: Obligatorio, string (1 carácter: A o I).
    estatus = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=1,
        min_length=1,
        error_messages={
            'required': 'El estatus es obligatorio.',
            'max_length': 'El estatus debe ser un único carácter (A o I).',
            'min_length': 'El estatus debe tener al menos un carácter.'
        }
    )

    def validate_nombre_metodo_pago(self, value):
        """Limpia espacios en blanco."""
        return value.strip()

    def validate_estatus(self, value):
        """Normaliza el estatus a mayúscula y valida que sea letra."""
        value = value.strip().upper()
        if not value.isalpha():
            raise serializers.ValidationError("El estatus debe ser una letra (A o I).")
        return value