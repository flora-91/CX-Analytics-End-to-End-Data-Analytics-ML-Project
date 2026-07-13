=====================================================================================
VITAHEALTH - GUÍA DE EJECUCIÓN DEL PIPELINE ETL
=====================================================================================

Proyecto:
Implementación de un proceso ETL para integrar los datos operacionales de
PostgreSQL con el Data Warehouse de Customer Experience desarrollado en
Snowflake.

=====================================================================================
ORDEN DE EJECUCIÓN
=====================================================================================

1. IMPLEMENTAR EL MODELO DIMENSIONAL EN SNOWFLAKE

Archivo:

03_FL_dimensional_model.sql

Ejecutar el script desde Snowsight con un rol que posea permisos para crear
esquemas y tablas.

Este script crea:

• Esquema DW_CX
• Tablas de dimensiones
• Tabla de hechos FACT_CUSTOMER_EXPERIENCE
• Relaciones del modelo dimensional

-------------------------------------------------------------------------------------

2. CONFIGURAR LAS CREDENCIALES

Archivo:

config/settings.ini

Completar los datos correspondientes a:

• PostgreSQL
• Snowflake

Verificar que las credenciales sean correctas antes de ejecutar el pipeline.

-------------------------------------------------------------------------------------

3. INSTALAR DEPENDENCIAS

Ejecutar:

pip install -r requirements.txt

Requisito recomendado:

Python 3.10 o superior.

-------------------------------------------------------------------------------------

4. EJECUTAR EL PIPELINE ETL

Comando:

python src/FL_main.py

Durante la ejecución el pipeline realiza automáticamente las siguientes etapas:

• Extracción de datos desde PostgreSQL.
• Transformación de la información.
• Generación del modelo dimensional.
• Carga de dimensiones.
• Carga de la tabla de hechos en Snowflake.

Los módulos involucrados son:

• FL_extract.py
• FL_transform.py
• FL_load.py

-------------------------------------------------------------------------------------

5. VALIDAR LA CARGA EN SNOWFLAKE

Ejecutar:

python src/FL_snowflake_verify.py

El módulo permite:

• Verificar la conexión con Snowflake.
• Consultar las tablas del Data Warehouse.
• Validar la carga de dimensiones.
• Validar la carga de la tabla de hechos.

=====================================================================================
SOLUCIÓN DE PROBLEMAS FRECUENTES
=====================================================================================

No se encuentra la sección PostgreSQL

• Revisar el archivo settings.ini.
• Verificar que exista la sección correspondiente a PostgreSQL.

-------------------------------------------------------------------------------------

Error de conexión con Snowflake

Verificar:

• Cuenta.
• Usuario.
• Contraseña.
• Warehouse.
• Base de datos.
• Esquema.

-------------------------------------------------------------------------------------

No existen las tablas del Data Warehouse

Ejecutar previamente el script:

03_FL_dimensional_model.sql

-------------------------------------------------------------------------------------

Error durante la extracción

• Verificar que PostgreSQL esté en ejecución.
• Confirmar que la base operacional contenga datos.

-------------------------------------------------------------------------------------

Error de dependencias

Instalar nuevamente:

pip install -r requirements.txt

=====================================================================================
REGISTRO DE EJECUCIÓN
=====================================================================================

Durante la ejecución se recomienda revisar los mensajes generados por el
pipeline para verificar:

• Extracción de registros.
• Transformación de datos.
• Inserción de dimensiones.
• Inserción de la tabla de hechos.
• Finalización correcta del proceso ETL.

=====================================================================================
VALIDACIÓN DEL DATA WAREHOUSE
=====================================================================================

Al finalizar el ETL se recomienda comprobar:

• Cantidad de registros cargados en cada dimensión.
• Cantidad de registros de FACT_CUSTOMER_EXPERIENCE.
• Integridad de las claves sustitutas.
• Correcta relación entre dimensiones y hechos.

Ejemplo:

SELECT COUNT(*)
FROM DW_CX.FACT_CUSTOMER_EXPERIENCE;

=====================================================================================
ESTRUCTURA DEL PROYECTO
=====================================================================================

config/settings.ini

src/FL_main.py

src/FL_extract.py

src/FL_transform.py

src/FL_load.py

src/FL_snowflake_verify.py

sql/03_FL_dimensional_model.sql

=====================================================================================