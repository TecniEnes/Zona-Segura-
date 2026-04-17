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
