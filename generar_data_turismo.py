import os
import django
import random
from decimal import Decimal
from datetime import date, timedelta

# 1. Configurar entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Importar todos los modelos mapeados
from django.contrib.auth.models import User
from core_models.models.Pais import Pais
from core_models.models.Ciudad import Ciudad
from core_models.models.Idioma import Idioma
from core_models.models.Moneda import Moneda
from core_models.models.DestinoTuristico import DestinoTuristico
from core_models.models.EstatusPago import EstatusPago
from core_models.models.EstatusReserva import EstatusReserva
from core_models.models.MetodoPago import MetodoPago
from core_models.models.Pago import Pago
from core_models.models.TipoPaquete import TipoPaquete
from core_models.models.Servicio import Servicio
from core_models.models.PaqueteTuristico import PaqueteTuristico
from core_models.models.PaqueteTuristicoServicio import PaqueteTuristicoServicio
from core_models.models.Reserva import Reserva
from core_models.models import Cliente

from faker import Faker

fake = Faker('es_ES')  # Localización

def poblar_sistema_turistico():
    print("🚀 Iniciando carga masiva de datos dummy...")

    # --- 1. IDIOMAS ---
    print("\n[1/10] Generando Idiomas...")
    idiomas_nombres = ['Español', 'Inglés', 'Portugués', 'Francés', 'Italiano']
    idiomas_instancias = []
    for nome in idiomas_nombres:
        idioma, _ = Idioma.objects.get_or_create(nombre=nome, defaults={'estatus': 'A'})
        idiomas_instancias.append(idioma)

    # --- 2. MONEDAS ---
    print("[2/10] Generando Monedas...")
    monedas_datos = [
        {'nombre': 'Bolívares', 'acronimo': 'VES'},
        {'nombre': 'Dólares Americanos', 'acronimo': 'USD'},
        {'nombre': 'Euros', 'acronimo': 'EUR'}
    ]
    monedas_instancias = []
    for m_data in monedas_datos:
        moneda, _ = Moneda.objects.get_or_create(
            acronimo=m_data['acronimo'], 
            defaults={'nombre': m_data['nombre'], 'estatus': 'A'}
        )
        monedas_instancias.append(moneda)

    # --- 3. METODOS Y ESTATUS DE PAGO / RESERVA ---
    print("[3/10] Generando Estatus y Métodos...")
    metodos = ['Pago Móvil', 'Transferencia Bancaria', 'Zelle', 'Efectivo']
    metodos_instancias = [MetodoPago.objects.get_or_create(nombre=m)[0] for m in metodos]

    estatus_p = ['Pendiente', 'Aprobado', 'Rechazado']
    estatus_p_instancias = [EstatusPago.objects.get_or_create(nombre=e)[0] for e in estatus_p]

    estatus_r = ['Confirmada', 'En Espera', 'Cancelada']
    estatus_r_instancias = [EstatusReserva.objects.get_or_create(nombre=e)[0] for e in estatus_r]

    # --- 4. PAÍSES Y CIUDADES ---
    print("[4/10] Generando Geografía (Países y Ciudades)...")
    geografia = {
        'Venezuela': ['Caracas', 'Maracaibo', 'Valencia', 'Barquisimeto', 'Mérida'],
        'Colombia': ['Bogotá', 'Medellín', 'Cartagena'],
        'Brasil': ['Brasilia', 'Río de Janeiro', 'São Paulo'],
        'España': ['Madrid', 'Barcelona', 'Sevilla']
    }

    ciudades_instancias = []
    for pais_nom, ciudades in geografia.items():
        pais, _ = Pais.objects.get_or_create(nombre=pais_nom, defaults={'estatus': 'A'})
        for ciu_nom in ciudades:
            ciudad, _ = Ciudad.objects.get_or_create(nombre=ciu_nom, defaults={'pais_id': pais, 'estatus': 'A'})
            ciudades_instancias.append(ciudad)

    # --- 5. DESTINOS TURÍSTICOS ---
    print("[5/10] Generando Destinos Turísticos...")
    destinos_ejemplos = [
        'Parque Nacional Morrocoy', 'Gran Sabana y Salto Ángel', 'Playas de Choroní', 
        'Centro Histórico de Cartagena', 'Playas de Copacabana', 'Museo del Prado'
    ]
    destinos_instancias = []
    for des_nom in destinos_ejemplos:
        ciudad_random = random.choice(ciudades_instancias)
        destino, _ = DestinoTuristico.objects.get_or_create(
            nombre=des_nom,
            defaults={
                'descripcion': fake.paragraph(nb_sentences=3)[:255],
                'pais_id': ciudad_random.pais_id,
                'ciudad_id': ciudad_random,
                'idioma_principal_id': random.choice(idiomas_instancias),
                'moneda_local_id': random.choice(monedas_instancias),
                'estatus': 'A',
                'imagen_principal': 'https://imagenes.desarrollo.com/destino_placeholder.jpg'
            }
        )
        destinos_instancias.append(destino)

    # --- 6. TIPOS DE PAQUETE Y SERVICIOS ---
    print("[6/10] Generando Tipos de Paquetes y Servicios...")
    tipos = ['Todo Incluido', 'Luna de Miel', 'Aventura / Excursión', 'Familiar']
    tipos_instancias = [TipoPaquete.objects.get_or_create(nombre=t, defaults={'descripcion': fake.sentence()[:255]})[0] for t in tipos]

    servicios_lista = [
        {'nombre': 'Hospedaje Hotel 5 Estrellas', 'costo': 2500.00},
        {'nombre': 'Traslado Aeropuerto - Hotel', 'costo': 600.00},
        {'nombre': 'Guiatura Turística Certificada', 'costo': 450.00},
        {'nombre': 'Desayunos y Cenas Bufé', 'costo': 1200.00},
        {'nombre': 'Full Day Paseo en Lancha', 'costo': 1800.00}
    ]
    servicios_instancias = []
    for serv in servicios_lista:
        s_instancia, _ = Servicio.objects.get_or_create(
            nombre=serv['nombre'],
            defaults={'descripcion': fake.sentence()[:255], 'costo_bs': Decimal(serv['costo']), 'estatus': 'A'}
        )
        servicios_instancias.append(s_instancia)

    # --- 7. PAQUETES TURÍSTICOS ---
    print("[7/10] Generando Paquetes Turísticos...")
    paquetes_instancias = []
    for i in range(1, 7):
        try:
            nombre_paquete = f"Paquete Especial Tour {random.choice(destinos_ejemplos)} V{i}"
            fecha_inicio_rand = date.today() + timedelta(days=random.randint(10, 60))
            duracion = random.randint(3, 10)
            fecha_fin_rand = fecha_inicio_rand + timedelta(days=duracion)

            paquete, _ = PaqueteTuristico.objects.get_or_create(
                nombre=nombre_paquete,
                defaults={
                    'descripcion': fake.paragraph(nb_sentences=2)[:255],
                    'destino_id': random.choice(destinos_instancias),
                    'tipo_paquete_id': random.choice(tipos_instancias),
                    'duracion_dias': duracion,
                    'precio_base_bs': Decimal(round(random.uniform(5000.00, 25000.00), 2)),
                    'capacidad_maxima_integrantes': random.choice([10, 15, 20, 30]),
                    'fecha_inico': fecha_inicio_rand,
                    'fecha_fin': fecha_fin_rand,
                    'disponible': 'A',
                    'estatus': 'A',
                    'imagen_principal': 'https://imagenes.desarrollo.com/paquete_placeholder.jpg'
                }
            )
            paquetes_instancias.append(paquete)
        except Exception as e:
            print(f"       ⚠️ Saltando paquete duplicado: {e}")

    # --- 8. RELACIÓN PAQUETE - SERVICIOS (Tabla Puente) ---
    print("[8/10] Enlazando Servicios a los Paquetes...")
    for paq in paquetes_instancias:
        # Asignar aleatoriamente entre 2 y 4 servicios a cada paquete
        servicios_aleatorios = random.sample(servicios_instancias, k=random.randint(2, 4))
        for serv in servicios_aleatorios:
            PaqueteTuristicoServicio.objects.get_or_create(
                paquete_turistico_id=paq,
                servico_id=serv
            )

    # --- 9. CLIENTES ---
    print("[9/10] Creando Clientes Dummy...")
    clientes_creados = []
    for _ in range(10):
        try:
            username = f"{fake.user_name()}_{random.randint(10, 99)}"
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=fake.unique.email(),
                    password="PasswordDummy123!"
                )
                cliente = Cliente.objects.create(
                    user=user,
                    primer_nombre=fake.first_name(),
                    segundo_nombre=random.choice([fake.first_name(), ""]),
                    primer_apellido=fake.last_name(),
                    segundo_apellido=random.choice([fake.last_name(), ""]),
                    telefono=fake.unique.msisdn()[:12],
                    cedula=f"V-{random.randint(15000000, 32000000)}"
                )
                clientes_creados.append(cliente)
        except Exception as e:
            print(f"       ⚠️ Saltando un cliente por colisión de datos aleatorios: {e}")

    # --- 10. PAGOS Y RESERVAS ---
    print("[10/10] Generando Historial de Pagos y Reservas...")
    
    for i in range(12):
        try:
            tasa = Decimal(round(random.uniform(36.50, 45.00), 2))
            monto_ext = Decimal(round(random.uniform(150.00, 800.00), 2))
            monto_bs = monto_ext * tasa

            # 1. Crear el pago primero
            nuevo_pago = Pago.objects.create(
                metodo_pago_id=random.choice(metodos_instancias),
                estatus_pago_id=random.choice(estatus_p_instancias),
                moneda_id=random.choice(monedas_instancias),
                monto_bs=round(monto_bs, 2),
                monto_otra_moneda=monto_ext,
                taza_bs=tasa,
                comprobante=f"REF-TX-{random.randint(100000, 999999)} - Archivo: comprobante_pago_{i}.pdf"
            )

            # 2. Crear la reserva enlazada al pago, cliente y paquete correspondientes
            Reserva.objects.create(
                pago_id=nuevo_pago,
                paquete_id=random.choice(paquetes_instancias),
                cliente_id=random.choice(clientes_creados),
                cantidad_personas=random.randint(1, 5),
                estatus_id=random.choice(estatus_r_instancias)
            )
        except Exception as e:
            print(f"       ⚠️ Error al enlazar reserva/pago: {e}")

    print("\n✨ ¡Población masiva completada de manera limpia y consistente!")

if __name__ == '__main__':
    poblar_sistema_turistico()