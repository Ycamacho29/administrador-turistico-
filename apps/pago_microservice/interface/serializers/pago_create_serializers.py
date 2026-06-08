from rest_framework import serializers
from decimal import Decimal


class PagoCreateSerializer(serializers.Serializer):
    """
    Serializador para registro de pagos con campos opcionales 
    que retornan un valor por defecto si no se proporcionan.
    """

    # IDs de Relaciones (Obligatorios)
    metodo_pago_id = serializers.IntegerField(required=True)
    estatus_pago_id = serializers.IntegerField(required=True)
    moneda_id = serializers.IntegerField(required=True)

    # Monto Base (Obligatorio)
    monto_bs = serializers.DecimalField(
        required=True,
        max_digits=15,
        decimal_places=2
    )

    # CAMPOS MODIFICADOS:
    # Al poner default, si el campo no viene en el JSON,
    # serializer.validated_data lo incluirá con el valor Decimal('0.00')
    monto_otra_moneda = serializers.DecimalField(
        required=False,
        max_digits=15,
        decimal_places=2,
        allow_null=True,
        default=Decimal('0.00')  # Retorna 0.00 si no se coloca
    )

    taza_bs = serializers.DecimalField(
        required=False,
        max_digits=12,
        decimal_places=2,
        allow_null=True,
        default=Decimal('0.00')  # Retorna 0.00 si no se coloca
    )

    comprobante = serializers.ImageField(
        required=False,
        allow_null=True,
        error_messages={
            'invalid': 'El archivo subido no es una imagen válida o está corrupto.'
        }
    )

    def validate_metodo_pago_id(self, value):
        if value <= 0:
            raise serializers.ValidationError("ID inválido.")
        return value
    
    def validate_comprobante(self, value):
        """Validaciones personalizadas para el tamaño o peso del archivo."""
        if value:
            # Validar que la imagen no pese más de 2MB (2 * 1024 * 1024 bytes)
            max_size = 2 * 1024 * 1024
            if value.size > max_size:
                raise serializers.ValidationError(
                    "La imagen es muy pesada. El tamaño máximo permitido es de 2MB.")

            # Validar extensiones explícitas para restringir formatos específicos
            extension = value.name.split('.')[-1].lower()
            if extension not in ['jpg', 'jpeg', 'png', 'webp']:
                raise serializers.ValidationError(
                    "Formato de imagen no permitido. Usa JPG, JPEG, PNG o WEBP.")

        return value

    def validate(self, data):
        """
        Validación cruzada: Si se envía monto_otra_moneda, 
        debería existir una tasa de cambio (taza_bs).
        """
        monto_extra = data.get('monto_otra_moneda')
        tasa = data.get('taza_bs')

        if monto_extra and monto_extra > 0 and (not tasa or tasa <= 0):
            raise serializers.ValidationError({
                "taza_bs": "Debe proporcionar una tasa de cambio válida si existe un monto en otra moneda."
            })

        if data.get('monto_otra_moneda') is None:
            data['monto_otra_moneda'] = Decimal('0.00')
        if data.get('taza_bs') is None:
            data['taza_bs'] = Decimal('0.00')

        return data
