"""
===========================================================
VITAHEALTH - ETL | ETAPA DE TRANSFORMACIÓN
===========================================================

Proyecto:
Customer Experience Analytics

Autora:
Florencia Lombardi

Descripción:
Este módulo aplica las reglas de negocio y transforma los
datos extraídos desde PostgreSQL para construir las tablas
dimensionales y la tabla de hechos del Data Warehouse.

Funcionalidades principales:

- Limpieza y validación de datos.
- Construcción de dimensiones.
- Construcción de la tabla de hechos.
- Preparación para Snowflake.

===========================================================
"""

import warnings
import pandas as pd
import numpy as np

warnings.filterwarnings(
    "ignore",
    category=pd.errors.SettingWithCopyWarning
)

# ==================================================
# DIMENSIÓN PACIENTES
# ==================================================

def build_dim_patient(df):

    print("Construyendo DIM_PATIENT...")

    dim = df[[
        "id_paciente",
        "edad",
        "sexo",
        "zona",
        "antiguedad_meses"
    ]].drop_duplicates()

    dim = dim.sort_values("id_paciente")

    dim.insert(
        0,
        "PATIENT_KEY",
        range(1, len(dim) + 1)
    )

    print(f"   {len(dim)} pacientes")

    return dim


# ==================================================
# DIMENSIÓN PLANES
# ==================================================

def build_dim_plan(df):

    print("Construyendo DIM_PLAN...")

    dim = df.drop_duplicates(
        subset="id_plan"
    ).copy()

    dim = dim.sort_values("id_plan")

    dim.insert(
        0,
        "PLAN_KEY",
        range(1, len(dim) + 1)
    )

    print(f"   {len(dim)} planes")

    return dim


# ==================================================
# DIMENSIÓN SERVICIOS
# ==================================================

def build_dim_service(df):

    print("Construyendo DIM_SERVICE...")

    dim = df.drop_duplicates(
        subset="id_servicio"
    ).copy()

    dim = dim.sort_values("id_servicio")

    dim.insert(
        0,
        "SERVICE_KEY",
        range(1, len(dim) + 1)
    )

    print(f"   {len(dim)} servicios")

    return dim


# ==================================================
# DIMENSIÓN CENTROS MÉDICOS
# ==================================================

def build_dim_medical_center(df):

    print("Construyendo DIM_MEDICAL_CENTER...")

    dim = df.drop_duplicates(
        subset="id_centro"
    ).copy()

    dim = dim.sort_values("id_centro")

    dim.insert(
        0,
        "CENTER_KEY",
        range(1, len(dim) + 1)
    )

    print(f"   {len(dim)} centros")

    return dim


# ==================================================
# DIMENSIÓN FECHA
# ==================================================

def build_dim_date(df_turnos):

    print("Construyendo DIM_DATE...")

    fechas = pd.DataFrame()

    fechas["FECHA"] = pd.to_datetime(
        df_turnos["fecha_turno"]
    ).drop_duplicates()

    fechas = fechas.sort_values("FECHA")

    fechas["DATE_KEY"] = (
        fechas["FECHA"]
        .dt.strftime("%Y%m%d")
        .astype(int)
    )

    fechas["DIA"] = fechas["FECHA"].dt.day

    fechas["MES"] = fechas["FECHA"].dt.month

    meses = {
        1: "Enero",
        2: "Febrero",
        3: "Marzo",
        4: "Abril",
        5: "Mayo",
        6: "Junio",
        7: "Julio",
        8: "Agosto",
        9: "Septiembre",
        10: "Octubre",
        11: "Noviembre",
        12: "Diciembre"
    }

    fechas["NOMBRE_MES"] = fechas["MES"].map(meses)

    fechas["TRIMESTRE"] = fechas["FECHA"].dt.quarter

    fechas["ANIO"] = fechas["FECHA"].dt.year

    dias = {
        0: "Lunes",
        1: "Martes",
        2: "Miércoles",
        3: "Jueves",
        4: "Viernes",
        5: "Sábado",
        6: "Domingo"
    }

    fechas["DIA_SEMANA"] = (
        fechas["FECHA"]
        .dt.dayofweek
        .map(dias)
    )

    print(f"   {len(fechas)} fechas")

    return fechas


# ==================================================
# TABLA DE HECHOS
# ==================================================

def build_fact_customer_experience(

    pacientes,
    turnos,
    encuestas,
    reclamos,

    dim_patient,
    dim_plan,
    dim_service,
    dim_center,
    dim_date

):

    print("Construyendo FACT_CUSTOMER_EXPERIENCE...")

    #----------------------------------------------
    # BASE = TURNOS
    #----------------------------------------------

    fact = turnos.copy()

    #----------------------------------------------
    # Incorporar PLAN desde PACIENTES
    #----------------------------------------------

    fact = fact.merge(

        pacientes[
            [
                "id_paciente",
                "id_plan"
            ]
        ],

        on="id_paciente",

        how="left"

    )

    #----------------------------------------------
    # DATE_KEY
    #----------------------------------------------

    fact["DATE_KEY"] = (

        pd.to_datetime(
            fact["fecha_turno"]
        )

        .dt.strftime("%Y%m%d")

        .astype(int)

    )
    #----------------------------------------------
    # PATIENT_KEY
    #----------------------------------------------

    fact = fact.merge(

        dim_patient[
            [
                "PATIENT_KEY",
                "id_paciente"
            ]
        ],

        on="id_paciente",

        how="left"

    )

    #----------------------------------------------
    # PLAN_KEY
    #----------------------------------------------

    fact = fact.merge(

        dim_plan[
            [
                "PLAN_KEY",
                "id_plan"
            ]
        ],

        on="id_plan",

        how="left"

    )

    #----------------------------------------------
    # SERVICE_KEY
    #----------------------------------------------

    fact = fact.merge(

        dim_service[
            [
                "SERVICE_KEY",
                "id_servicio"
            ]
        ],

        on="id_servicio",

        how="left"

    )

    #----------------------------------------------
    # CENTER_KEY
    #----------------------------------------------

    fact = fact.merge(

        dim_center[
            [
                "CENTER_KEY",
                "id_centro"
            ]
        ],

        on="id_centro",

        how="left"

    )

    #----------------------------------------------
    # ENCUESTAS
    #----------------------------------------------

    enc = encuestas[
        [
            "id_paciente",
            "puntuacion_nps",
            "csat"
        ]
    ]

    fact = fact.merge(

        enc,

        on="id_paciente",

        how="left"

    )

    #----------------------------------------------
    # RECLAMOS
    #----------------------------------------------

    recl = (

        reclamos

        .groupby("id_paciente")

        .agg({

            "dias_resolucion": "mean",

            "id_reclamo": "count"

        })

        .reset_index()

        .rename(columns={

            "id_reclamo": "cantidad_reclamos"

        })

    )

    fact = fact.merge(

        recl,

        on="id_paciente",

        how="left"

    )

    fact["cantidad_reclamos"] = (

        fact["cantidad_reclamos"]

        .fillna(0)

        .astype(int)

    )

    fact["dias_resolucion"] = (

        fact["dias_resolucion"]

        .fillna(0)

        .round()

        .astype(int)

    )

    fact["TIENE_RECLAMO"] = (

        fact["cantidad_reclamos"] > 0

    )

    #----------------------------------------------
    # COLUMNAS FINALES
    #----------------------------------------------

    fact = fact[
        [
            "DATE_KEY",
            "PATIENT_KEY",
            "PLAN_KEY",
            "SERVICE_KEY",
            "CENTER_KEY",
            "puntuacion_nps",
            "csat",
            "tiempo_espera",
            "cancelado",
            "asistio",
            "TIENE_RECLAMO",
            "dias_resolucion"
        ]
    ]

    fact.insert(

        0,

        "EXPERIENCE_KEY",

        range(1, len(fact) + 1)

    )

    print(f"   {len(fact)} registros")

    return fact
   

# ==================================================
# VALIDACIÓN DE DIMENSIONES
# ==================================================

def validate_dimensions(dimensions):

    print()

    print("=" * 60)
    print("VALIDACIÓN DE DIMENSIONES")
    print("=" * 60)

    for name, df in dimensions.items():

        print(f"{name:<30}{len(df):>10,} registros")

    print("=" * 60)


# ==================================================
# PREPARACIÓN PARA SNOWFLAKE
# ==================================================

def prepare_for_snowflake(df):

    df = df.copy()

    # Convertir nombres de columnas a mayúsculas

    df.columns = df.columns.str.upper()

    # Convertir booleanos a TRUE/FALSE

    bool_columns = df.select_dtypes(
        include="bool"
    ).columns

    for col in bool_columns:

        df[col] = df[col].astype(bool)

    return df


# ==================================================
# PIPELINE COMPLETO
# ==================================================

def transform_complete_pipeline(data):

    print()

    print("=" * 60)
    print("INICIANDO TRANSFORMACIÓN")
    print("=" * 60)

    #---------------------------------------------
    # Construcción de dimensiones
    #---------------------------------------------

    dim_patient = build_dim_patient(
        data["pacientes"]
    )

    dim_plan = build_dim_plan(
        data["planes"]
    )

    dim_service = build_dim_service(
        data["servicios"]
    )

    dim_center = build_dim_medical_center(
        data["centros_medicos"]
    )

    dim_date = build_dim_date(
        data["turnos"]
    )

    #---------------------------------------------
    # Construcción de la Fact Table
    #---------------------------------------------

    fact = build_fact_customer_experience(

        data["pacientes"],

        data["turnos"],

        data["encuestas"],

        data["reclamos"],

        dim_patient,

        dim_plan,

        dim_service,

        dim_center,

        dim_date

    )
       #---------------------------------------------
    # Preparar tablas para Snowflake
    #---------------------------------------------

    dimensions = {

        "DIM_PATIENT":
            prepare_for_snowflake(dim_patient),

        "DIM_PLAN":
            prepare_for_snowflake(dim_plan),

        "DIM_SERVICE":
            prepare_for_snowflake(dim_service),

        "DIM_MEDICAL_CENTER":
            prepare_for_snowflake(dim_center),

        "DIM_DATE":
            prepare_for_snowflake(dim_date),

        "FACT_CUSTOMER_EXPERIENCE":
            prepare_for_snowflake(fact)

    }

    #---------------------------------------------
    # Validación
    #---------------------------------------------

    validate_dimensions(dimensions)

    print()

    print("=" * 60)
    print("TRANSFORMACIÓN FINALIZADA CORRECTAMENTE")
    print("=" * 60)

    print()

    print("Tablas preparadas:")

    for table in dimensions.keys():

        print(f"   {table}")

    print()

    return dimensions


# ==================================================
# EJECUCIÓN DEL MÓDULO
# ==================================================

if __name__ == "__main__":

    print("=" * 60)
    print("VITAHEALTH ETL - ETAPA DE TRANSFORMACIÓN")
    print("=" * 60)

    print()

    print("Este módulo forma parte del proceso ETL y")
    print("debe ejecutarse desde FL_main.py.")

    print()