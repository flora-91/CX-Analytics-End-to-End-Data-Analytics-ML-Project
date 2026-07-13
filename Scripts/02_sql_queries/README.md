# VITAHEALTH

# GUÍA DE CONSULTAS SQL

---

## Proyecto

Este módulo reúne el conjunto de consultas SQL desarrolladas sobre la base de datos operacional de **VitaHealth**.

Las consultas permiten validar la calidad de los datos generados, analizar la información operacional y responder distintos problemas de negocio relacionados con la experiencia del paciente.

---

# REQUISITOS PREVIOS

- PostgreSQL 12 o superior.
- Base de datos operacional creada.
- Datos sintéticos cargados mediante el módulo **01_data_generation**.

---

# CONTENIDO DE LA CARPETA

| Archivo | Descripción |
|----------|-------------|
| **02_FL_12Queries_vitahealth.sql** | Script con consultas SQL de nivel básico, intermedio y complejo para el análisis de la base operacional. |

---

# ESTRUCTURA DE LAS CONSULTAS

El script se encuentra organizado en tres niveles de complejidad:

## Consultas Básicas

Permiten obtener indicadores generales del sistema.

Ejemplos:

- Pacientes por plan.
- Turnos por servicio.
- Indicadores generales de satisfacción (NPS y CSAT).

---

## Consultas Intermedias

Analizan información agregada para responder preguntas de negocio.

Ejemplos:

- Tiempo promedio de espera por centro médico.
- Reclamos por criticidad.
- Uso de servicios.
- Indicadores operacionales.

---

## Consultas Complejas

Combinan múltiples tablas, agregaciones y funciones analíticas para obtener información estratégica sobre la experiencia del paciente.

---

# EJECUCIÓN

Abrir el archivo:

```sql
02_FL_12Queries_vitahealth.sql
```

Ejecutar cada consulta de forma individual o el script completo desde el cliente PostgreSQL utilizado (DBeaver, pgAdmin o equivalente).

---

# OBJETIVOS DE LAS CONSULTAS

Las consultas fueron desarrolladas para:

- Validar la consistencia de los datos sintéticos.
- Analizar indicadores operacionales.
- Obtener métricas de Customer Experience.
- Responder preguntas de negocio mediante SQL.
- Servir como base para las etapas posteriores del proyecto (ETL, Data Warehouse y Power BI).

---

# VALIDACIÓN

Se recomienda verificar que todas las consultas:

- Se ejecuten sin errores.
- Devuelvan resultados consistentes.
- Utilicen correctamente las relaciones entre tablas.
- Aprovechen las claves primarias y foráneas definidas en el modelo relacional.

---

# NOTAS

- Las consultas fueron desarrolladas utilizando PostgreSQL.
- El script incluye consultas de dificultad creciente para demostrar distintos niveles de dominio de SQL.
- Los resultados obtenidos sirven como insumo para el análisis exploratorio y la validación del modelo operacional antes del proceso ETL.