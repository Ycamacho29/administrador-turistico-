# Administrador Turístico - API 🌴

Este proyecto es un sistema de gestión turística desarrollado con **Django** y **Django REST Framework (DRF)**, siguiendo una **Arquitectura Limpia (Clean Architecture)** y gestionado mediante **Pipenv**.

## Requisitos Previos

Antes de instalar, asegúrate de tener:
* **Python 3.12** o superior.
* **MariaDB** o **MySQL** server activo.

---

## A. Instalación del Proyecto

Sigue estos pasos en tu terminal:

### 1. Instalar Pipenv
```bash
pip install pipenv
```

### 2. Clonar el repositorio.
```bash
git clone https://github.com/Ycamacho29/administrador-turistico-.git
cd administrador-turistico
```

### 3. Instalar dependencias con Pipenv.
```bash
pipenv install
```

### 4. Activar el entorno virtual.
```bash
pipenv shell
```

## B. Configuración de Variables de Entorno

> **Nota:** Guiarce del archivo .env.example

Crea un archivo llamado .env en la raíz del proyecto y ajusta tus credenciales de acceso.

## C. Base de Datos y Migraciones

> **Nota:** Asegúrate de que la base de datos definida en DB_NAME exista en tu servidor.

### 1. Ejecuta las migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### D. Ejecuta del Servidor
```bash
python manage.py runserver
```