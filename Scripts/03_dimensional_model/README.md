# VITAHEALTH

# GUÍA DE IMPLEMENTACIÓN DEL MODELO DIMENSIONAL

---

## Proyecto

Este módulo implementa el **Data Warehouse de VitaHealth** utilizando un modelo dimensional tipo **Star Schema** en Snowflake.

El objetivo es transformar los datos operacionales en un modelo optimizado para el análisis de indicadores de Customer Experience, permitiendo su explotación mediante procesos ETL, modelos de Machine Learning y tableros desarrollados en Power BI.

---

# REQUISITOS PREVIOS

- Snowflake.
- Base de datos operacional previamente cargada.
- Proceso ETL ejecutado correctamente.
- Permisos para crear esquemas y tablas.

---

# CONTENIDO DE LA CARPETA

| Archivo | Descripción |
|----------|-------------|
| **03_FL_dimensional_model.sql** | Script que implementa el modelo dimensional (Star Schema) del Data Warehouse de VitaHealth en Snowflake. |

---

# SECUENCIA DE IMPLEMENTACIÓN

## ETAPA 1 – CREACIÓN DEL ESQUEMA

El script crea el esquema del Data Warehouse.

```sql
CREATE SCHEMA DW_CX;
```

---

## ETAPA 2 – CREACIÓN DE DIMENSIONES

Se implementan las dimensiones necesarias para el análisis histórico de Customer Experience.

Dimensiones incluidas:

- DIM_PATIENT
- DIM_PLAN
- DIM_SERVICE
- DIM_MEDICAL_CENTER
- DIM_DATE

Cada dimensión almacena los atributos descriptivos utilizados durante el análisis.

---

## ETAPA 3 – CREACIÓN DE LA TABLA DE HECHOS

Se crea la tabla de hechos que centraliza los principales indicadores de experiencia del paciente.

La tabla relaciona las distintas dimensiones mediante claves sustitutas (Surrogate Keys) y almacena las métricas utilizadas para el análisis de Customer Experience.

---

# MODELO IMPLEMENTADO

El Data Warehouse sigue una arquitectura **Star Schema**, compuesta por:

### Dimensiones

- Paciente
- Plan
- Servicio
- Centro Médico
- Fecha

### Tabla de hechos

- Fact Customer Experience

Esta estructura optimiza las consultas analíticas y simplifica la construcción de indicadores para Business Intelligence.

---

# EJECUCIÓN

Abrir el archivo:

```sql
03_FL_dimensional_model.sql
```

Ejecutar el script completo desde Snowflake.

El proceso crea automáticamente:

- Esquema DW_CX.
- Tablas de dimensiones.
- Tabla de hechos.
- Relaciones entre dimensiones y hechos.

---

# VALIDACIÓN

Una vez ejecutado el script se recomienda verificar:

```sql
SHOW TABLES IN SCHEMA DW_CX;
```

También puede comprobarse la correcta creación de las tablas mediante consultas como:

```sql
SELECT COUNT(*) FROM DIM_PATIENT;

SELECT COUNT(*) FROM DIM_SERVICE;

SELECT COUNT(*) FROM FACT_CUSTOMER_EXPERIENCE;
```

---

# ESTRUCTURA DEL MODELO

```
DW_CX
│
├── DIM_PATIENT
├── DIM_PLAN
├── DIM_SERVICE
├── DIM_MEDICAL_CENTER
├── DIM_DATE
│
└── FACT_CUSTOMER_EXPERIENCE
```

---

# NOTAS

- El modelo dimensional fue diseñado siguiendo la metodología **Star Schema**, optimizando el rendimiento de consultas analíticas.
- Todas las dimensiones utilizan claves sustitutas (Surrogate Keys) para facilitar la integración con los procesos ETL.
- La tabla de hechos centraliza los principales indicadores de Customer Experience y constituye la base para los análisis desarrollados en Snowflake, Machine Learning y Power BI.
- Este modelo representa la capa analítica del proyecto y sirve como soporte para la explotación de datos y la toma de decisiones basada en indicadores.