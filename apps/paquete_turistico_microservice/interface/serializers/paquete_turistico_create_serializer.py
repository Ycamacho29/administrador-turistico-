from rest_framework import serializers
from decimal import Decimal

class PaqueteTuristicoCreateSerializer(serializers.Serializer):
    """
    Serializador para validar la creación de paquetes turísticos.
    """
    
    # Campos de Texto
    nombre_paquete_turistico = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=150,
        error_messages={'required': 'El nombre del paquete es obligatorio.'}
    )
    
    # Descripción opcional: se guarda como "" si no se envía o viene vacía
    descripcion = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        default=""
    )

    # IDs de Relaciones (Obligatorios)
    destino_id = serializers.IntegerField(required=True)
    tipo_paquete_id = serializers.IntegerField(required=True)

    # Campos Numéricos
    duracion_dias = serializers.IntegerField(
        required=True,
        min_value=1,
        error_messages={'min_value': 'La duración debe ser al menos de 1 día.'}
    )
    
    precio_base_bs = serializers.DecimalField(
        required=True,
        max_digits=15,
        decimal_places=2,
        min_value=Decimal('0.01')
    )
    
    capacidad_maxima_integrantes = serializers.IntegerField(
        required=True,
        min_value=1
    )

    # Fechas (Formato DD/MM/YYYY)
    fecha_inico = serializers.DateField(
        required=True,
        input_formats=['%d/%m/%Y'],
        error_messages={'invalid': 'Formato de fecha de inicio inválido (DD/MM/YYYY).'}
    )
    
    fecha_fin = serializers.DateField(
        required=True,
        input_formats=['%d/%m/%Y'],
        error_messages={'invalid': 'Formato de fecha de fin inválido (DD/MM/YYYY).'}
    )

    def validate_descripcion(self, value):
        """Asegura que siempre retorne un string (vacío si es nulo)."""
        return value.strip() if value else ""

    def validate(self, data):
        """
        Validación de coherencia temporal.
        """
        f_inicio = data.get('fecha_inico')
        f_fin = data.get('fecha_fin')

        if f_inicio and f_fin and f_fin < f_inicio:
            raise serializers.ValidationError({
                "fecha_fin": "La fecha de finalización no puede ser anterior a la de inicio."
            })
            
        return data