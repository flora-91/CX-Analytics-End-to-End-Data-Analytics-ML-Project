# VITAHEALTH

# GUÍA DE GENERACIÓN DE DATOS OPERACIONALES

---

## Proyecto

Este módulo implementa la generación de los datos sintéticos que alimentan la base de datos operacional de **VitaHealth**, utilizada como origen del proceso ETL y del Data Warehouse desarrollado posteriormente en Snowflake.

La generación combina información sintética con un conjunto de comentarios reales anonimizados provenientes de encuestas de experiencia del paciente, preservando la coherencia entre todas las entidades del modelo.

---

# REQUISITOS PREVIOS

- PostgreSQL 12 o superior.
- Python 3.10 o superior.
- Dependencias del proyecto instaladas.
- Base de datos creada mediante el script del esquema operacional.

---

# CONTENIDO DE LA CARPETA

| Archivo | Descripción |
|----------|-------------|
| **01_FL_02_data_generation.py** | Script principal encargado de generar e insertar los datos sintéticos en PostgreSQL. |
| **01_FL_vitahealth_schema.sql** | Script SQL que crea el modelo relacional operacional de VitaHealth. |
| **business_rules.py** | Reglas de negocio utilizadas durante la generación de los datos sintéticos. |
| **encuestas_cx.csv** | Dataset de encuestas utilizado como base para generar la tabla de encuestas de Customer Experience. |
| **.env** | Configuración de conexión a PostgreSQL. |

---

# SECUENCIA DE IMPLEMENTACIÓN

## ETAPA 1 – CREACIÓN DE LA BASE OPERACIONAL

Ejecutar el siguiente script:

```sql
01_FL_vitahealth_schema.sql
```

Este script crea:

- Tablas operacionales.
- Claves primarias.
- Claves foráneas.
- Restricciones de integridad referencial.

---

## ETAPA 2 – CONFIGURACIÓN DEL ARCHIVO `.env`

Completar los datos de conexión a PostgreSQL.

Ejemplo:

```env
DB_NAME=vitahealth_db
DB_USER=postgres
DB_PASSWORD=*******
DB_HOST=localhost
DB_PORT=5432
```

---

## ETAPA 3 – GENERACIÓN DE DATOS

Ejecutar:

```bash
python 01_FL_02_data_generation.py
```

El proceso realiza automáticamente las siguientes tareas:

- Carga el dataset de encuestas.
- Anonimiza el identificador de los pacientes.
- Genera pacientes sintéticos.
- Genera turnos.
- Genera reclamos.
- Prepara las encuestas de Customer Experience.
- Inserta toda la información en PostgreSQL.

---

# DATOS GENERADOS

El proceso genera información para las siguientes entidades:

- Pacientes
- Turnos
- Reclamos
- Encuestas

Todos los registros mantienen la integridad referencial y respetan las reglas de negocio definidas para simular el funcionamiento de una institución de salud.

---

# VALIDACIÓN

Se recomienda verificar la correcta carga ejecutando consultas como las siguientes:

```sql
SELECT COUNT(*) FROM pacientes;

SELECT COUNT(*) FROM turnos;

SELECT COUNT(*) FROM reclamos;

SELECT COUNT(*) FROM encuestas;
```

También puede comprobarse la correcta creación de las tablas desde el cliente PostgreSQL utilizado.

---

# RESOLUCIÓN DE PROBLEMAS

## Error de conexión

Verificar:

- Que PostgreSQL se encuentre en ejecución.
- Que las credenciales del archivo `.env` sean correctas.

---

## Error al instalar dependencias

Ejecutar nuevamente:

```bash
pip install -r requirements.txt
```

---

## Error por claves duplicadas

Vaciar previamente las tablas operacionales antes de volver a ejecutar el proceso de generación de datos.

---

# NOTAS

- Los datos sintéticos fueron generados utilizando **Faker**, **NumPy** y reglas de negocio específicas del dominio de salud.
- El DNI presente en el dataset original es reemplazado por un identificador interno (`id_paciente`) para preservar la privacidad de los pacientes.
- Los comentarios de las encuestas mantienen su contenido original anonimizando la información sensible.
- Este módulo constituye el origen del pipeline de datos y sirve como fuente para el proceso ETL, el modelo dimensional, los modelos de Machine Learning y los tableros desarrollados en Power BI.