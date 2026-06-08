from rest_framework import serializers
from decimal import Decimal

class PagoUpdateSerializer(serializers.Serializer):
    """
    Serializador para registrar pagos con lógica condicional:
    Si hay monto_otra_moneda, la tasa_bs es obligatoria.
    """
    
    # IDs de Relaciones
    metodo_pago_id = serializers.IntegerField(
        required=True,
        error_messages={'required': 'El ID del método de pago es obligatorio.'}
    )
    estatus_pago_id = serializers.IntegerField(
        required=True,
        error_messages={'required': 'El ID del estatus de pago es obligatorio.'}
    )
    moneda_id = serializers.IntegerField(
        required=True,
        error_messages={'required': 'El ID de la moneda es obligatorio.'}
    )

    # Monto principal
    monto_bs = serializers.DecimalField(
        required=True,
        max_digits=15,
        decimal_places=2,
        min_value=Decimal('0.01')
    )

    # Campos opcionales con valor por defecto
    monto_otra_moneda = serializers.DecimalField(
        required=False,
        max_digits=15,
        decimal_places=2,
        allow_null=True,
        default=Decimal('0.00') # Valor por defecto si no existe o viene vacío
    )
    
    taza_bs = serializers.DecimalField(
        required=False,
        max_digits=12,
        decimal_places=2,
        allow_null=True,
        default=Decimal('0.00') # Valor por defecto si no existe o viene vacío
    )

    comprobante = serializers.ImageField(
        required=False,
        allow_null=True,
        error_messages={
            'invalid': 'El archivo subido no es una imagen válida o está corrupto.'
        }
    )

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
        Validación condicional: 
        Si monto_otra_moneda tiene contenido (> 0), taza_bs debe ser > 0.
        """
        # Obtenemos los valores
        monto_extra = data.get('monto_otra_moneda', Decimal('0.00'))
        tasa = data.get('taza_bs', Decimal('0.00'))

        # Si el monto_extra es nulo por alguna razón, lo tratamos como 0
        if monto_extra is None:
            monto_extra = Decimal('0.00')
            data['monto_otra_moneda'] = monto_extra

        if tasa is None:
            tasa = Decimal('0.00')
            data['taza_bs'] = tasa

        # Lógica de validación: si hay monto extra, la tasa DEBE tener valor
        if monto_extra > 0 and tasa <= 0:
            raise serializers.ValidationError({
                "taza_bs": "Si especifica un monto en otra moneda, debe indicar una tasa de cambio válida mayor a 0."
            })

        return data