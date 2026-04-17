# Proyecto Tecni Enes 

Zona-Segura-
El objetivo principal del proyecto es poder segmentar México en base a la base de datos Homicidios dolosos registrados en México por Entidad.

"""
Consultas sobre homicidios dolosos en México (1990-2024)
Fuente: https://datamx.io/dataset/homicidios-dolosos-registrados-en-mexico-por-entidad-1990-2023

Descripción:
    1. Descarga el CSV desde datamx.io
    2. Top 5 entidades con TASA_TOTAL máxima por año
    3. Tasas de homicidios en Michoacán por año (hombres y mujeres)
"""

import pandas as pd
import requests
import io

# ============================================================
# 1. DESCARGA DE DATOS
# ============================================================

URL = (
    "https://datamx.io/dataset/8e8c980e-03c4-456a-b2dd-c8e8ea217c50/resource/7a67c1ce-88e4-42b0-915b-d38cfb6232f6/download/data.csv"
)

def descargar_datos(url: str) -> pd.DataFrame:
    """Descarga el CSV desde la URL y retorna un DataFrame."""
    print(f"Descargando datos desde:\n  {url}\n")
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    # Detectar encoding; el archivo es UTF-8 pero se verifica
    encoding = response.apparent_encoding or "utf-8"
    print(f"  Encoding detectado: {encoding}")

    df = pd.read_csv(
        io.StringIO(response.content.decode(encoding)),
        dtype={"CVE_ENT": str},
    )

    print(f"  Registros descargados: {len(df)}")
    print(f"  Columnas: {list(df.columns)}")
    print(f"  Rango de años: {df['AÑO'].min()} – {df['AÑO'].max()}")
    print(f"  Entidades únicas: {df[df['CVE_ENT'] != '0']['ENTIDAD'].nunique()}")
    print()
    return df


# ============================================================
# 2. CONSULTA 1: Top 5 entidades con TASA_TOTAL máxima por año
# ============================================================

def top5_tasa_total_por_anio(df: pd.DataFrame) -> pd.DataFrame:
    """
    Para cada año, obtiene las 5 entidades con la tasa total
    de homicidios más alta (excluyendo el registro Nacional).
    """
    # Excluir el agregado nacional
    df_ent = df[df["CVE_ENT"] != "0"].copy()

    resultados = []
    for anio, grupo in df_ent.groupby("AÑO"):
        top5 = grupo.nlargest(5, "TASA_TOTAL")[
            ["AÑO", "ENTIDAD", "TASA_TOTAL", "TOTAL", "POBLACION_TOTAL"]
        ]
        top5["RANK"] = range(1, 6)
        resultados.append(top5)

    return pd.concat(resultados, ignore_index=True)


# ============================================================
# 3. CONSULTA 2: Michoacán – tasas hombres y mujeres por año
# ============================================================

def michoacan_por_anio(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filtra Michoacán y retorna las tasas de homicidio
    clasificadas por hombres y mujeres, año a año.
    """
    df_mich = df[df["ENTIDAD"] == "Michoacán"].copy()
    df_mich = df_mich.sort_values("AÑO")

    return df_mich[
        ["AÑO", "HOMBRES", "MUJERES", "TOTAL",
         "TASA_HOMBRES", "TASA_MUJERES", "TASA_TOTAL"]
    ].reset_index(drop=True)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    # --- Descarga ---
    df = descargar_datos(URL)

    # --- Consulta 1 ---
    print("=" * 70)
    print("CONSULTA 1: Top 5 entidades con mayor TASA_TOTAL por año")
    print("=" * 70)
    df_top5 = top5_tasa_total_por_anio(df)

    # Mostrar un resumen por año
    for anio in sorted(df_top5["AÑO"].unique()):
        bloque = df_top5[df_top5["AÑO"] == anio]
        print(f"\n  Año {anio}:")
        for _, row in bloque.iterrows():
            print(
                f"    {row['RANK']}. {row['ENTIDAD']:<25s} "
                f"Tasa: {row['TASA_TOTAL']:>8.2f}  "
                f"(Total: {int(row['TOTAL']):>6,}  "
                f"Pob: {int(row['POBLACION_TOTAL']):>10,})"
            )

    # --- Consulta 2 ---
    print("\n" + "=" * 70)
    print("CONSULTA 2: Michoacán – Homicidios por año (Hombres / Mujeres)")
    print("=" * 70)
    df_mich = michoacan_por_anio(df)

    print(f"\n  {'AÑO':>4s}  {'HOMBRES':>8s}  {'MUJERES':>8s}  {'TOTAL':>6s}  "
          f"{'T.HOMBRES':>10s}  {'T.MUJERES':>10s}  {'T.TOTAL':>8s}")
    print("  " + "-" * 68)
    for _, row in df_mich.iterrows():
        print(
            f"  {int(row['AÑO']):>4d}  "
            f"{int(row['HOMBRES']):>8,}  {int(row['MUJERES']):>8,}  "
            f"{int(row['TOTAL']):>6,}  "
            f"{row['TASA_HOMBRES']:>10.2f}  {row['TASA_MUJERES']:>10.2f}  "
            f"{row['TASA_TOTAL']:>8.2f}"
        )

    print("\n✓ Consultas completadas.")

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
