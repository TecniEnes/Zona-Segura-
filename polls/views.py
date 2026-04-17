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
