# Proyecto Tecni Enes 
Humberto Medina Verduzco Pablo Adolfo Mijangos Pimienta 
Ortega Mendoza Roman Yair

# Zona-Segura-
El objetivo principal del proyecto es poder segmentar México en base a la base de datos Homicidios dolosos registrados en México por Entidad.

## ¿Qué hace?

La aplicación descarga el dataset del INEGI (1,155 registros, 32 entidades, 34 años) y genera dos consultas:

- **Estudio de violencia en las entidades** con la tasa de homicidios más alta por cada año

Los resultados se presentan en tablas directamente en el navegador.

---

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
| Infraestructura | AWS EC2 con IP elástica |
| Control de versiones | Git / GitHub |

---

## Acceso

```
https://datamx.io/dataset/homicidios-dolosos-registrados-en-mexico-por-entidad-1990-2023
http://3.128.21.79:6285/polls/
http://100.26.61.153:6285/polls/
```

---

**Materia:** Cómputo en la Nube — ENES Morelia, UNAM
