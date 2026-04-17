# Proyecto Tecni Enes 

Zona-Segura-
El objetivo principal del proyecto es poder segmentar México en base a la base de datos Homicidios dolosos registrados en México por Entidad.


# Proyecto Cómputo en la Nube — Django en AWS EC2

Guía paso a paso para desplegar una aplicación Django en una instancia EC2 de AWS, incluyendo un ejercicio de consulta de datos abiertos sobre homicidios dolosos en México (1990–2024).

**Stack:** Python 3 · Django · pandas · AWS EC2 · Git

---

## 1. Conexión SSH a la instancia EC2

Posicionarse en la ruta del archivo `.pem` y conectar:

```bash
cd Documentos/Computo_en_la_nube
ssh -i "YAGA_development_pm.pem" ec2-user@ec2-3-128-21-79.us-east-2.compute.amazonaws.com
```

---

## 2. Entorno virtual

Un entorno virtual es un espacio aislado donde se instalan paquetes de Python sin afectar al sistema global.

```bash
# Crear entorno (solo la primera vez)
python -m venv nombre_del_entorno

# Activar entorno
source ~/venv/tecni_enes/bin/activate
```

---

## 3. Instalar Django y crear la app

```bash
pip install django
cd ~/venv/www/testing
python manage.py startapp polls
```

---

## 4. Configurar archivos del proyecto

### 4.1 `polls/urls.py` (crear archivo nuevo)

```bash
nano polls/urls.py
```

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
]
```

### 4.2 `polls/views.py`

```bash
nano polls/views.py
```

```python
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
```

### 4.3 `testing/urls.py` (URLs del proyecto)

```bash
nano testing/urls.py
```

```python
from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Hello, World! Django funciona correctamente.</h1>")

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('polls/', include("polls.urls")),
]
```

### 4.4 `settings.py` — Configurar IPs

Editar `ALLOWED_HOSTS` en **ambos** archivos `settings.py` (raíz y `testing/testing/`):

```python
ALLOWED_HOSTS = ['IP_PUBLICA', 'IP_PRIVADA', 'localhost']
```

Ejemplo con IP elástica:

```python
ALLOWED_HOSTS = ['3.128.21.79', '172.31.35.30', 'localhost']
```

---

## 5. Abrir puerto en AWS

En la consola de AWS, agregar regla de entrada al Security Group de la instancia:

| Tipo | Protocolo | Puerto | Origen |
|------|-----------|--------|--------|
| TCP personalizado | TCP | 6285 | 0.0.0.0/0 |

---

## 6. Ejecutar el servidor

```bash
python manage.py migrate
python manage.py runserver 0.0.0.0:6285
```

Abrir en el navegador:

- **Home:** `http://3.128.21.79:6285/`
- **Polls:** `http://3.128.21.79:6285/polls/`

---

## 7. Ejercicio: Consultas de datos abiertos (datamx.io)

### 7.1 Dependencias

```bash
nano requirements.txt
```

```
pandas>=2.0
requests>=2.28
```

```bash
pip install -r requirements.txt
```

### 7.2 Script de consultas (`consultas_homicidios.py`)

El script descarga el CSV desde [datamx.io](https://datamx.io/dataset/homicidios-dolosos-registrados-en-mexico-por-entidad-1990-2023) y ejecuta dos consultas:

1. **Top 5 entidades** con la tasa total de homicidios más alta por año
2. **Michoacán** — tasas de homicidio clasificadas por hombres y mujeres, año a año

**URL del dataset:**

```
https://datamx.io/dataset/8e8c980e-03c4-456a-b2dd-c8e8ea217c50/resource/7a67c1ce-88e4-42b0-915b-d38cfb6232f6/download/data.csv
```

**Fuente original:** INEGI — [Microdatos de homicidios dolosos](https://www.inegi.org.mx/programas/edr/#microdatos)

### 7.3 Integración con Django (`polls/views.py`)

El archivo `views.py` integra las consultas de pandas directamente en una vista Django, renderizando tablas HTML con los resultados en `http://IP:6285/polls/`.

---

## 8. IP Elástica (IP fija)

Para evitar que la IP pública cambie al reiniciar la instancia:

1. AWS Console → **EC2 → Elastic IPs** (Network & Security)
2. **Allocate Elastic IP address** → Allocate
3. Seleccionar la IP → **Actions → Associate Elastic IP address**
4. Seleccionar la instancia → Associate

> **Nota:** La IP elástica es gratuita mientras esté asociada a una instancia en ejecución. Si se desasocia o se detiene la instancia sin liberarla, AWS cobra por hora.

Después de asignarla, actualizar `ALLOWED_HOSTS` con la nueva IP.

---

## 9. Sincronización con GitHub

```bash
git init
git config user.name "TecniEnes"
git config user.email "tu_email@ejemplo.com"
git remote add origin https://github.com/TecniEnes/www.git
git add .
git commit -m "Django polls app con consultas de homicidios datamx.io"
git branch -M main
git push -u origin main
```

Para autenticarse se requiere un **Personal Access Token** (GitHub → Settings → Developer settings → Personal access tokens).

---

## Estructura del proyecto

```
~/venv/www/testing/
├── manage.py
├── requirements.txt
├── consultas_homicidios.py
├── settings.py
├── urls.py
├── polls/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py          ← rutas de la app
│   ├── views.py         ← vistas con consultas pandas
│   └── migrations/
├── testing/
│   ├── __init__.py
│   ├── settings.py      ← ALLOWED_HOSTS
│   ├── urls.py          ← rutas del proyecto
│   ├── wsgi.py
│   └── asgi.py
└── db.sqlite3
```

---

**Curso:** Tecnologías para la Información en Ciencias — ENES Morelia, UNAM
