"""
===========================================================
VITAHEALTH - ETL | ETAPA DE EXTRACCIÓN
===========================================================

Proyecto:
Customer Experience Analytics

Autora:
Florencia Lombardi

Descripción:
Este módulo extrae la información de la base operacional
(PostgreSQL) para alimentar el Data Warehouse implementado
en Snowflake.

Funcionalidades:
- Conexión a PostgreSQL.
- Conexión a Snowflake.
- Validación de conexiones.
- Extracción de tablas operacionales.
- Generación de archivos staging para el proceso ETL.

===========================================================
"""

import os
import warnings
import configparser
import pandas as pd

from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL

warnings.filterwarnings(
    "ignore",
    message=".*pandas only supports SQLAlchemy.*"
)

# ==================================================
# CONEXIÓN POSTGRESQL
# ==================================================

def get_postgres_connection():

    config = configparser.ConfigParser()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)

    config_path = os.path.join(
        project_root,
        "config",
        "settings.ini"
    )

    config.read(config_path)

    connection_string = (

        f"postgresql://"

        f"{config['postgres']['user']}:"

        f"{config['postgres']['password']}@"

        f"{config['postgres']['host']}:"

        f"{config['postgres']['port']}/"

        f"{config['postgres']['database']}"

    )

    engine = create_engine(connection_string)

    print("Conexión PostgreSQL establecida")

    return engine


# ==================================================
# CONEXIÓN SNOWFLAKE
# ==================================================

def get_snowflake_connection():

    config = configparser.ConfigParser()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)

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

    print("Conexión Snowflake establecida")

    return engine


# ==================================================
# VALIDACIÓN DE CONEXIÓN
# ==================================================

def check_connections():

    try:

        pg = get_postgres_connection()

        sf = get_snowflake_connection()

        print("Conexiones verificadas correctamente")

        pg.dispose()

        sf.dispose()

        return True

    except Exception as e:

        print(e)

        return False


# ==================================================
# EXTRACCIÓN DE TABLAS
# ==================================================

def extract_tables():

    engine = get_postgres_connection()

    queries = {

        "pacientes":

        """
        SELECT *
        FROM pacientes
        """,

        "planes":

        """
        SELECT *
        FROM planes
        """,

        "servicios":

        """
        SELECT *
        FROM servicios
        """,

        "centros_medicos":

        """
        SELECT *
        FROM centros_medicos
        """,

        "turnos":

        """
        SELECT *
        FROM turnos
        """,

        "encuestas":

        """
        SELECT *
        FROM encuestas
        """,

        "reclamos":

        """
        SELECT *
        FROM reclamos
        """

    }

    data = {}

    print("=" * 60)
    print("EXTRAYENDO TABLAS DESDE POSTGRESQL")
    print("=" * 60)

    for table, query in queries.items():

        df = pd.read_sql(query, engine)

        data[table] = df

        print(f"{table:<20} {len(df):>8} registros")

    engine.dispose()

    return data


# ==================================================
# GUARDAR ARCHIVOS STAGING
# ==================================================

def save_staging(data):

    output_dir = "../data/staging"

    os.makedirs(output_dir, exist_ok=True)

    print()
    print("=" * 60)
    print("GENERANDO ARCHIVOS PARQUET")
    print("=" * 60)

    for name, df in data.items():

        file_path = os.path.join(
            output_dir,
            f"{name}.parquet"
        )

        df.to_parquet(
            file_path,
            index=False
        )

        print(f"{name}.parquet generado")


        # ==================================================
# RESUMEN DE LA EXTRACCIÓN
# ==================================================

def show_summary(data):

    print()
    print("=" * 60)
    print("RESUMEN DE EXTRACCIÓN")
    print("=" * 60)

    total = 0

    for name, df in data.items():

        registros = len(df)

        total += registros

        print(f"{name:<20} {registros:>8,} registros")

    print("-" * 60)

    print(f"{'TOTAL':<20} {total:>8,} registros")

    print("=" * 60)


# ==================================================
# FUNCIÓN PRINCIPAL
# ==================================================

def main():

    print("=" * 60)
    print("VITAHEALTH ETL - ETAPA DE EXTRACCIÓN")
    print("=" * 60)
    print()

    # ------------------------------------------
    # Verificar conexiones
    # ------------------------------------------

    if not check_connections():

        print()

        print("No fue posible establecer las conexiones.")

        return

    print()

    # ------------------------------------------
    # Extraer tablas
    # ------------------------------------------

    data = extract_tables()

    print()

    # ------------------------------------------
    # Guardar archivos staging
    # ------------------------------------------

    save_staging(data)

    print()

    # ------------------------------------------
    # Mostrar resumen
    # ------------------------------------------

    show_summary(data)

    print()

    print("=" * 60)
    print("PROCESO FINALIZADO CORRECTAMENTE")
    print("=" * 60)

    print()

    print("Archivos generados:")

    print()

    for tabla in data.keys():

        print(f"  data/staging/{tabla}.parquet")

    print()

    print("Los archivos están listos para la etapa de transformación.")

    print()

    return


# ==================================================
# EJECUCIÓN
# ==================================================

if __name__ == "__main__":

    main()