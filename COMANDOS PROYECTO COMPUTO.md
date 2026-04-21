# COMANDOS PROYECTO COMPUTO_EN_LA_NUBE

#1- Posicionarse en la ruta correcta del archivo .pem

Ejemplo

cd Documentos
cd Computo_en_la_nube
ssh -i "YAGA_development_pm.pem" ec2-user@ec2-13-58-246-32.us-east-2.compute.amazonaws.com

""A newer release of "Amazon Linux" is available.
  Version 2023.11.20260413:
Run "/usr/bin/dnf check-release-update" for full release and version update info
   ,     #_
   ~\_  ####_        Amazon Linux 2023
  ~~  \_#####\
  ~~     \###|
  ~~       \#/ ___   https://aws.amazon.com/linux/amazon-linux-2023
   ~~       V~' '->
    ~~~         /
      ~~._.   _/
         _/ _/
       _/m/'
Last login: Fri Apr 17 02:43:22 2026 from 187.173.129.82
[ec2-user@ip-172-31-35-30 ~]$

#2- Activar entorno 

source ~/venv/tecni_enes/bin/activate



Un entorno virtual es un espacio aislado dentro de tu sistema donde puedes instalar paquetes de Python sin afectar a otros proyectos ni al Python global del sistema.

#Comando Crear entorno

python -m venv nombre_del_entorno

(tecni_enes) [ec2-user@ip-172-31-35-30 ~]$ 

#En el entorno tecni_enes, instalar framework Django
pip install django

python manage.py startapp polls

nano polls/urls.py

#Contenido polls
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
]

# Editar archivo views.py

nano polls/views.py

#contenido views.py 
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
    
# Editar archivo urls.py
nano testing/urls.py
#contenido urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('polls/', include("polls.urls")),
    path('admin/', admin.site.urls),
]

# Editar seetings.py (Ruta previa testing/testing) en ambos setting.py se edita IP
-rw-r--r--. 1 ec2-user ec2-user    771 Apr 10 19:37 '#urls.py#'
drwxr-xr-x. 5 ec2-user ec2-user  16384 Apr 17 06:19  .
drwxr-xr-x. 3 ec2-user ec2-user     38 Apr  9 17:29  ..
-rw-r--r--. 1 ec2-user ec2-user      0 Apr  9 17:29  __init__.py
-rw-r--r--. 1 ec2-user ec2-user    391 Apr  9 17:29  asgi.py
-rw-r--r--. 1 ec2-user ec2-user   4516 Apr 17 06:22  consultas_homicidios.py
-rw-r--r--. 1 ec2-user ec2-user 131072 Apr 10 18:53  db.sqlite3
-rwxr-xr-x. 1 ec2-user ec2-user    663 Apr  9 17:29  manage.py
drwxr-xr-x. 4 ec2-user ec2-user    175 Apr 17 05:36  polls
-rw-r--r--. 1 ec2-user ec2-user     27 Apr 17 06:18  requirements.txt
-rw-r--r--. 1 ec2-user ec2-user   3280 Apr 17 05:48  settings.py
drwxr-xr-x. 3 ec2-user ec2-user    108 Apr  9 17:31  testing
-rw-r--r--. 1 ec2-user ec2-user    816 Apr 17 05:53  urls.py
-rw-r--r--. 1 ec2-user ec2-user    763 Apr  9 17:29  urls.py~
-rw-r--r--. 1 ec2-user ec2-user    391 Apr  9 17:29  wsgi.py
host
# Contenido settings.py con IP de cada instancia
ALLOWED_HOSTS = ['13.58.246.32', '172.31.35.30', 'localhost']

#Contenido settings.py /testing/testing
(tecni_enes) [ec2-user@ip-172-31-35-30 testing]$ ls -la
total 32
drwxr-xr-x. 3 ec2-user ec2-user   108 Apr  9 17:31 .
drwxr-xr-x. 5 ec2-user ec2-user 16384 Apr 17 06:19 ..
-rw-r--r--. 1 ec2-user ec2-user     0 Apr  9 17:29 __init__.py
drwxr-xr-x. 2 ec2-user ec2-user   122 Apr 17 06:01 __pycache__
-rw-r--r--. 1 ec2-user ec2-user   391 Apr  9 17:29 asgi.py
-rw-r--r--. 1 ec2-user ec2-user  3267 Apr 17 06:00 settings.py
-rw-r--r--. 1 ec2-user ec2-user   815 Apr 17 05:58 urls.py
-rw-r--r--. 1 ec2-user ec2-user   391 Apr  9 17:29 wsgi.py
(tecni_enes) [ec2-user@ip-172-31-35-30 testing]$ 

# Contenido a modificar con la IP de cada instanica
ALLOWED_HOSTS = ['13.58.246.32', '172.31.35.30', 'localhost']


## ABRIR PUERTOS EN AWS, REGLAS DE ENTRADA PUERTO 6285 
sgr-044081d1603068c75
IPv4
TCP personalizado
TCP
6285
0.0.0.0/0
–

## Visualiazcion "Hello_Word" Gracias a Framework Dejango

python manage.py migrate
python manage.py runserver 0.0.0.0:6285

#URL navegador

http://13.58.246.32:6285/polls/


# txt.requirements.py

nano requirements.txt

#contenido 
pandas>=2.0
requests>=2.28

#Ejecutar
pip install -r requirements.txt

#Script_consultas_homicidios
nano consultas_homicidios.py

#contenido
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


##Editar Views.py

nano polls/views.py

###contenido
from django.http import HttpResponse
import pandas as pd
import requests
import io

URL = "https://datamx.io/dataset/8e8c980e-03c4-456a-b2dd-c8e8ea217c50/resource/7a67c1ce-88e4-42b0-915b-d38cfb6232f6/download/data.csv"


def descargar_datos():
    response = requests.get(URL, timeout=30)
    response.raise_for_status()
    encoding = response.apparent_encoding or "utf-8"
    df = pd.read_csv(
        io.StringIO(response.content.decode(encoding)),
        dtype={"CVE_ENT": str},
    )
    return df


def index(request):
    try:
        df = descargar_datos()
    except Exception as e:
        return HttpResponse(f"<h2>Error al descargar datos: {e}</h2>")

    html = "<h1>Homicidios Dolosos en México (1990-2024)</h1>"
    html += f"<p>Registros: {len(df)} | Entidades: {df[df['CVE_ENT'] != '0']['ENTIDAD'].nunique()} | Años: {df['AÑO'].min()}-{df['AÑO'].max()}</p>"

    # --- CONSULTA 1: Top 5 por año ---
    html += "<h2>Top 5 Entidades con Mayor Tasa Total por Año</h2>"
    df_ent = df[df["CVE_ENT"] != "0"]

    html += "<table border='1' cellpadding='5' cellspacing='0'>"
    html += "<tr><th>Año</th><th>Rank</th><th>Entidad</th><th>Tasa Total</th><th>Homicidios</th><th>Población</th></tr>"

    for anio in sorted(df_ent["AÑO"].unique()):
        grupo = df_ent[df_ent["AÑO"] == anio]
        top5 = grupo.nlargest(5, "TASA_TOTAL")
        for rank, (_, row) in enumerate(top5.iterrows(), 1):
            html += (
                f"<tr>"
                f"<td>{int(anio)}</td>"
                f"<td>{rank}</td>"
                f"<td>{row['ENTIDAD']}</td>"
                f"<td>{row['TASA_TOTAL']:.2f}</td>"
                f"<td>{int(row['TOTAL']):,}</td>"
                f"<td>{int(row['POBLACION_TOTAL']):,}</td>"
                f"</tr>"
            )
    html += "</table>"

    # --- CONSULTA 2: Michoacán ---
    html += "<h2>Michoacán - Tasas por Año (Hombres / Mujeres)</h2>"
    df_mich = df[df["ENTIDAD"] == "Michoacán"].sort_values("AÑO")

    html += "<table border='1' cellpadding='5' cellspacing='0'>"
    html += "<tr><th>Año</th><th>Hombres</th><th>Mujeres</th><th>Total</th><th>Tasa Hombres</th><th>Tasa Mujeres</th><th>Tasa Total</th></tr>"

    for _, row in df_mich.iterrows():
        html += (
            f"<tr>"
            f"<td>{int(row['AÑO'])}</td>"
            f"<td>{int(row['HOMBRES']):,}</td>"
            f"<td>{int(row['MUJERES']):,}</td>"
            f"<td>{int(row['TOTAL']):,}</td>"
            f"<td>{row['TASA_HOMBRES']:.2f}</td>"
            f"<td>{row['TASA_MUJERES']:.2f}</td>"
            f"<td>{row['TASA_TOTAL']:.2f}</td>"
            f"</tr>"
        )
    html += "</table>"

    html += "<br><p><em>Fuente: datamx.io / INEGI</em></p>"
    return HttpResponse(html)
    
#Reiniciar servidor

python manage.py runserver 0.0.0.0:6285

http://3.128.21.79:6285/polls/

#Asignar IP Elastica

En la consola de AWS, ve a EC2 → Elastic IPs (en el menú lateral bajo "Network & Security")
Click Allocate Elastic IP address → Allocate
Selecciona la IP que se creó → Actions → Associate Elastic IP address
Selecciona tu instancia ip-172-31-35-30 → Associate

#editar settings.py
ALLOWED_HOSTS = ['NUEVA_ELASTIC_IP', '172.31.35.30', 'localhost']

#testing
python manage.py runserver 0.0.0.0:6285
http://3.128.21.79:6285/polls/
