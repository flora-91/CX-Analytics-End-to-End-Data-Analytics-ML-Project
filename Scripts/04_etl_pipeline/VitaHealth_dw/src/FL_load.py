"""
===========================================================
VITAHEALTH - ETL | ETAPA DE CARGA
===========================================================

Proyecto:
Customer Experience Analytics

Autora:
Florencia Lombardi

Descripción:
Este módulo carga las dimensiones y la tabla de hechos
del Data Warehouse de VitaHealth en Snowflake.

Funcionalidades principales:

- Conexión a Snowflake.
- Carga de dimensiones.
- Carga de la tabla de hechos.
- Validación de registros cargados.

===========================================================
"""

# ==================================================
# IMPORTS
# ==================================================

import os
import logging
import configparser

import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy import text
from snowflake.sqlalchemy import URL


# ==================================================
# CONFIGURACIÓN DEL LOGGING
# ==================================================

logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s - %(levelname)s - %(message)s"

)

logger = logging.getLogger(__name__)


# ==================================================
# CONEXIÓN A SNOWFLAKE
# ==================================================

def get_snowflake_connection():

    config = configparser.ConfigParser()

    current_dir = os.path.dirname(
        os.path.abspath(__file__)
    )

    project_root = os.path.dirname(
        current_dir
    )

    config_path = os.path.join(

        project_root,

        "config",

        "settings.ini"

    )

    config.read(config_path)

    engine = create_engine(

        URL(

            account=config["snowflake"]["account"],

            user=config["snowflake"]["user"],

            password=config["snowflake"]["password"],

            database=config["snowflake"]["database"],

            schema=config["snowflake"]["schema"],

            warehouse=config["snowflake"]["warehouse"],

            role=config["snowflake"]["role"]

        )

    )

    logger.info("Conexión a Snowflake establecida")

    return engine


# ==================================================
# CARGA DE UNA TABLA
# ==================================================

def load_table(

    engine,

    dataframe,

    table_name

):

    if dataframe.empty:

        logger.warning(

            f"{table_name}: DataFrame vacío"

        )

        return

    logger.info(

        f"Cargando {table_name}..."

    )

    dataframe.to_sql(

        table_name,

        engine,

        if_exists="append",

        index=False,

        method="multi",

        chunksize=1000

    )

    logger.info(

        f"{table_name}: "

        f"{len(dataframe):,} registros cargados"

    )


# ==================================================
# VALIDAR CANTIDAD DE REGISTROS
# ==================================================

def count_records(

    engine,

    table_name

):

    query = text(

        f"""

        SELECT COUNT(*)

        FROM {table_name}

        """

    )

    with engine.connect() as conn:

        total = conn.execute(

            query

        ).scalar()

    logger.info(

        f"{table_name}: "

        f"{total:,} registros"

    )

    return total


# ==================================================
# CARGAR DIMENSIONES
# ==================================================

def load_dimensions(

    engine,

    dimensions

):

    logger.info(

        "=" * 60

    )

    logger.info(

        "CARGANDO DIMENSIONES"

    )

    logger.info(

        "=" * 60

    )

    load_table(

        engine,

        dimensions["DIM_PATIENT"],

        "DIM_PATIENT"

    )

    load_table(

        engine,

        dimensions["DIM_PLAN"],

        "DIM_PLAN"

    )

    load_table(

        engine,

        dimensions["DIM_SERVICE"],

        "DIM_SERVICE"

    )

    load_table(

        engine,

        dimensions["DIM_MEDICAL_CENTER"],

        "DIM_MEDICAL_CENTER"

    )

    load_table(

        engine,

        dimensions["DIM_DATE"],

        "DIM_DATE"

    )

    # ==================================================
# CARGAR TABLA DE HECHOS
# ==================================================

def load_fact(

    engine,

    dimensions

):

    logger.info(

        "=" * 60

    )

    logger.info(

        "CARGANDO FACT_CUSTOMER_EXPERIENCE"

    )

    logger.info(

        "=" * 60

    )

    load_table(

        engine,

        dimensions["FACT_CUSTOMER_EXPERIENCE"],

        "FACT_CUSTOMER_EXPERIENCE"

    )


# ==================================================
# VALIDACIÓN FINAL
# ==================================================

def verify_load(

    engine

):

    logger.info("")

    logger.info("=" * 60)

    logger.info("VALIDACIÓN DE CARGA")

    logger.info("=" * 60)

    tables = [

        "DIM_PATIENT",

        "DIM_PLAN",

        "DIM_SERVICE",

        "DIM_MEDICAL_CENTER",

        "DIM_DATE",

        "FACT_CUSTOMER_EXPERIENCE"

    ]

    for table in tables:

        count_records(

            engine,

            table

        )

    logger.info("=" * 60)


# ==================================================
# PIPELINE COMPLETO
# ==================================================

def load_complete_pipeline(

    dimensions

):

    logger.info("")

    logger.info("=" * 60)

    logger.info("INICIANDO CARGA EN SNOWFLAKE")

    logger.info("=" * 60)

    engine = get_snowflake_connection()

    try:

        #------------------------------------------
        # Cargar dimensiones
        #------------------------------------------

        load_dimensions(

            engine,

            dimensions

        )

        #------------------------------------------
        # Cargar Fact Table
        #------------------------------------------

        load_fact(

            engine,

            dimensions

        )

        #------------------------------------------
        # Validar carga
        #------------------------------------------

        verify_load(

            engine

        )

        logger.info("")

        logger.info("=" * 60)

        logger.info("CARGA FINALIZADA CORRECTAMENTE")

        logger.info("=" * 60)

        return True

    except Exception as e:

        logger.error(f"Error durante la carga: {e}")

        return False

    finally:

        engine.dispose()


# ==================================================
# EJECUCIÓN DEL MÓDULO
# ==================================================

if __name__ == "__main__":

    print("=" * 60)

    print("VITAHEALTH ETL - ETAPA DE CARGA")

    print("=" * 60)

    print()

    print("Este módulo debe ejecutarse desde FL_main.py.")

    print()