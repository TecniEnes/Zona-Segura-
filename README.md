
# Proyecto ZONA SEGURA. Tecni Enes 
Humberto Medina Verduzco 

Pablo Adolfo Mijangos Pimienta 

Ortega Mendoza Roman Yair

# Zona-Segura (Primera Prueba)
El objetivo principal del proyecto es poder segmentar el Estado de Michoacán por regiones, municipios y colonias con relación a la tasa de  Homicidios dolosos. Para posteriormente desplegar un análisis sobre las regiones con mayor indice de violencia y representarlo en un Mapa Coroplético ( "Mapa de Calor" por Regiones). 

## ¿Qué hace?

El codigo actualemente descarga el dataset "Homicidios dolosos registrados en México por Entidad (1990-2024)" que cuenta con  (1,155 registros, 32 entidades, 34 años). El dataSet es un resumen de "Estadísticas de Defunciones Registradas (EDR)" especificamente por homicidios(Hombres/Muejeres) por parte del INEGI. (2024) 

- **Estudio de violencia en las entidades** con la tasa de homicidios más alta por cada año

Los resultados se presentan en tablas directamente en el navegador. Se muestra el top 5 por año.

---

## Próximos Pasos: Segmentación de Michoacán
Para evolucionar el proyecto hacia un análisis local profundo, se han definido los siguientes objetivos inmediatos:

1.  **Ampliación del Dataset:** Descarga e integración de nuevas bases de datos con microdatos delictivos que permitan bajar el nivel de análisis de "Entidad" a "Región", "Municipio" y "Codigo postal".
2.  **Segmentación Regional:** Clasificación técnica de Michoacán por sus regiones socioeconómicas para identificar patrones de violencia específicos.
3.  **Visualización Geoespacial:** Implementación de un **mapa de calor (coroplético)** interactivo. Este mapa representará visualmente los índices de violencia, permitiendo distinguir las zonas de mayor riesgo dentro del estado mediante intensidades de color.

## Fuente de datos

| Campo | Descripción |
|-------|-------------|
| Origen | INEGI — Microdatos de homicidios dolosos |
| Distribución | datamx.io (Codeando México) |
| Periodo | 1990 – 2024 |
| Variables | Entidad, año, víctimas por sexo, población, tasas por 100,000 habitantes |
| Licencia | Creative Commons CC0 |

---

## Tecnologías utilizadas

| Componente | Tecnología |
|------------|------------|
| Backend | Django 4.2 / Python 3 |
| Procesamiento de datos | pandas |
| Infraestructura | AWS EC2 |
| Control de versiones | Git / GitHub |

---

## Acceso
Comando para correr servidor: python3 manage.py runserver 0.0.0.0:6285

```
https://datamx.io/dataset/homicidios-dolosos-registrados-en-mexico-por-entidad-1990-2023
http://3.210.28.15:6285/polls/
http://100.26.61.153:6285/polls/
```

---

**Materia:** Cómputo en la Nube — ENES Morelia, UNAM
