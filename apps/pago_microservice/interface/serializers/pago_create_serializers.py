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

    def validate_metodo_pago_id(self, value):
        if value <= 0:
            raise serializers.ValidationError("ID inválido.")
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
