"""
/*===========================================================
VITAHEALTH
Modelo Dimensional (Data Warehouse)
=============================================================

Proyecto:
Customer Experience Analytics

Autora:
Florencia Lombardi

Archivo:
04_dimensional_model.sql

Descripción:
Implementa el modelo dimensional (Star Schema) del Data Warehouse
de VitaHealth para el análisis de la experiencia del paciente.

El modelo está compuesto por tablas de dimensiones y una tabla
de hechos que centraliza los principales indicadores de Customer
Experience, permitiendo su posterior explotación en Snowflake,
Machine Learning y Power BI.

===========================================================*/
"""

# ==================================================
# IMPORTS
# ==================================================
# Importación de librerías necesarias para la
# generación de datos y conexión a PostgreSQL.
# ==================================================


import os
import logging
import random

import numpy as np
import pandas as pd
import psycopg2

from faker import Faker
from dotenv import load_dotenv
from datetime import datetime, timedelta


# ==================================================
# CONFIGURACIÓN GENERAL
# ==================================================
# Configuración de variables de entorno, generación
# de datos sintéticos y semilla para reproducibilidad.
# ==================================================

load_dotenv()

fake = Faker("es_ES")

random.seed(42)
np.random.seed(42)


# ==================================================
# CONFIGURACIÓN DEL LOGGING
# ==================================================
# Configuración del registro de eventos del proceso.
# ==================================================


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ==================================================
# CONEXIÓN A POSTGRESQL
# ==================================================
# Establece la conexión con la base de datos
# operacional VitaHealth.
# ==================================================


def get_db_connection():

    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )


# ==================================================
# INSERCIÓN MASIVA
# ==================================================
# Inserta múltiples registros utilizando executemany
# para mejorar el rendimiento.
# ==================================================


def insert_data_massive(cursor, query, data):

    cursor.executemany(query, data)


# ==================================================
# CARGA DEL DATASET DE ENCUESTAS
# ==================================================
# El dataset original contiene el DNI del paciente.
# Para preservar la privacidad, se reemplaza por un
# identificador interno (id_paciente), manteniendo
# la relación entre todas las encuestas del mismo
# paciente. Posteriormente se elimina el DNI.
# ==================================================

from pathlib import Path

def load_surveys():

    base_path = Path(__file__).parent
    file_path = base_path / "encuestas_cx.csv"

    df = pd.read_csv(file_path)

    # Crear identificador interno de paciente
    pacientes_unicos = df["dn_paciente"].drop_duplicates()

    mapa_pacientes = {
        dni: i + 1
        for i, dni in enumerate(pacientes_unicos)
    }

    df["id_paciente"] = df["dn_paciente"].map(mapa_pacientes)

    # Eliminar el DNI original
    df = df.drop(columns=["dn_paciente"])

    logging.info(f"Encuestas cargadas: {len(df)}")

    return df



# ==================================================
# OBTENER PACIENTES ÚNICOS
# ==================================================
# Obtiene el listado de pacientes únicos presentes
# en el dataset de encuestas.
# ==================================================

def get_unique_patients(df):

    patients = df["id_paciente"].drop_duplicates()

    logging.info(f"Pacientes únicos: {len(patients)}")

    return patients




# ==================================================
# CATÁLOGOS
# ==================================================
# Valores utilizados para la generación de datos
# sintéticos.
# ==================================================


PLANES = [1, 2, 3, 4]

PESOS_PLANES = [
    0.45,
    0.30,
    0.15,
    0.10
]

SEXOS = [
    "Femenino",
    "Masculino",
    "Otro"
]

ZONAS = [
    "Norte",
    "Centro",
    "Sur",
    "Oeste"
]

TIPOS_RECLAMO = [
    "Demora en la atención",
    "Problemas con turnos",
    "Facturación",
    "Atención administrativa",
    "Cobertura",
    "Profesionales",
    "Estudios médicos",
    "Otros"
]

CRITICIDADES = [
    "Baja",
    "Media",
    "Alta"
]

PESOS_CRITICIDAD = [
    0.50,
    0.35,
    0.15
]


# ==================================================
# REGLAS DE NEGOCIO
# ==================================================
# ==================================================
# CENTROS MÉDICOS
# ==================================================

CENTROS = {

    1: "Centro Médico Norte",
    2: "Clínica del Valle",
    3: "Instituto Médico Central",
    4: "Sanatorio Parque Salud"

}

# ==================================================
# SERVICIOS
# ==================================================

SERVICIOS = {

    1: "Guardia",
    2: "Consultorio Clínico",
    3: "Pediatría",
    4: "Cardiología",
    5: "Traumatología",
    6: "Laboratorio",
    7: "Diagnóstico por Imágenes",
    8: "Vacunación"

}

ESPERA_SERVICIO = {

    # Guardia
    1: (75,20),

    # Consultorio
    2: (30,8),

    # Pediatría
    3: (28,8),

    # Cardiología
    4: (35,10),

    # Traumatología
    5: (50,12),

    # Laboratorio
    6: (15,5),

    # Diagnóstico por Imágenes
    7: (45,12),

    # Vacunación
    8: (10,4)

}

AJUSTE_PLAN = {

    1: 8,
    2: 4,
    3: 0,
    4: -8

}

# ==================================================
# GENERACIÓN DE PACIENTES
# ==================================================
# Genera un registro sintético por cada paciente
# único presente en el dataset de encuestas,
# asignando atributos demográficos de forma
# aleatoria mediante distribuciones predefinidas.
# ==================================================

def generate_patients(patient_ids):

    patients = []

    for patient_id in patient_ids:

        id_plan = random.choices(

            PLANES,

            weights=PESOS_PLANES,

            k=1

        )[0]

        # -------------------------
        # Edad
        # -------------------------

        edad = int(

            np.clip(

                np.random.normal(47,18),

                18,

                90

            )

        )

        sexo = random.choices(

            SEXOS,

            weights=[0.52,0.47,0.01],

            k=1

        )[0]

        # -------------------------
        # Antigüedad
        # -------------------------

        if id_plan == 4:

            antiguedad = random.randint(36,120)

        elif id_plan == 3:

            antiguedad = random.randint(18,96)

        else:

            antiguedad = random.randint(1,72)

        zona = random.choice(ZONAS)

        patients.append((

            int(patient_id),

            id_plan,

            edad,

            sexo,

            antiguedad,

            zona

        ))

    logging.info(

        f"Pacientes generados: {len(patients)}"

    )

    return patients

# ==================================================
# INSERCIÓN DE PACIENTES
# ==================================================
# Inserta los pacientes generados en la base de datos
# operacional VitaHealth.
# ==================================================

def insert_patients(cursor, patients):

    query = """
        INSERT INTO pacientes
        (
            id_paciente,
            id_plan,
            edad,
            sexo,
            antiguedad_meses,
            zona
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    insert_data_massive(cursor, query, patients)

    logging.info(f"Pacientes insertados: {len(patients)}")


# ==================================================
# GENERACIÓN DE TURNOS
# ==================================================

def generate_turns(patient_ids, patients):

    turns = []

    fecha_actual = datetime.now()

    # ---------------------------------------------
    # MAPA DE PLANES
    # ---------------------------------------------

    mapa_planes = {

        p[0]: p[1]

        for p in patients

    }

    for patient_id in patient_ids:

        id_plan = mapa_planes[int(patient_id)]

        # Pacientes Premium usan más el sistema
        if id_plan == 4:

            cantidad_turnos = random.randint(3,8)

        elif id_plan == 3:

            cantidad_turnos = random.randint(2,7)

        else:

            cantidad_turnos = random.randint(1,6)

        for _ in range(cantidad_turnos):

            # ---------------------------------------------
            # Servicio
            # ---------------------------------------------

            id_servicio = random.choices(

                population=[1,2,3,4,5,6,7,8],

                weights=[

                            0.20,   # Guardia
                            0.28,   # Consultorio
                            0.12,   # Pediatría
                            0.10,   # Cardiología
                            0.08,   # Traumatología
                            0.10,   # Laboratorio
                            0.07,   # Diagnóstico
                            0.05    # Vacunación

                ],

                k=1

            )[0]

            media, desvio = ESPERA_SERVICIO[id_servicio]

            espera = np.random.normal(

                media,

                desvio

            )

            espera += AJUSTE_PLAN[id_plan]

            espera = max(

                5,

                int(round(espera))

            )

            # ---------------------------------------------
            # Centro Médico
            # ---------------------------------------------

            if id_servicio == 1:

                id_centro = random.choices(

                    [1,2,3,4],

                    weights=[0.35,0.35,0.20,0.10],

                    k=1

                )[0]

            else:

                id_centro = random.randint(1,4)

            # ---------------------------------------------
            # Fecha
            # ---------------------------------------------

            fecha_turno = fecha_actual - timedelta(

                days=random.randint(0,730)

            )

            # ---------------------------------------------
            # Cancelación
            # ---------------------------------------------

            prob_cancelacion = 0.04

            if espera > 60:

                prob_cancelacion += 0.18

            elif espera > 40:

                prob_cancelacion += 0.10

            # Guardia tiene más cancelaciones

            if id_servicio == 1:

                prob_cancelacion += 0.05

            # Premium cancela menos

            if id_plan == 4:

                prob_cancelacion -= 0.03

            prob_cancelacion = max(

                0.01,

                min(prob_cancelacion,0.40)

            )

            cancelado = (

                random.random()

                < prob_cancelacion

            )

            # ---------------------------------------------
            # Asistencia
            # ---------------------------------------------

            if cancelado:

                asistio = False

            else:

                prob_asistencia = 0.96

                if espera > 70:

                    prob_asistencia -= 0.04

                asistio = (

                    random.random()

                    < prob_asistencia

                )

            turns.append(

                (

                    int(patient_id),

                    id_servicio,

                    id_centro,

                    fecha_turno.date(),

                    espera,

                    cancelado,

                    asistio

                )

            )

    logging.info(

        f"Turnos generados: {len(turns)}"

    )

    return turns

# ==================================================
# INSERCIÓN DE TURNOS
# ==================================================
# Inserta los turnos generados en la base de datos
# operacional VitaHealth.
# ==================================================

def insert_turns(cursor, turns):

    query = """
        INSERT INTO turnos
        (
            id_paciente,
            id_servicio,
            id_centro,
            fecha_turno,
            tiempo_espera,
            cancelado,
            asistio
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    insert_data_massive(cursor, query, turns)

    logging.info(f"Turnos insertados: {len(turns)}")

# ==================================================
# GENERACIÓN DE RECLAMOS
# ==================================================
# Genera reclamos sintéticos asociados a los pacientes.
# ==================================================

# ==================================================
# GENERACIÓN DE RECLAMOS
# ==================================================

def generate_claims(patient_ids, patients, turns):

    claims = []

    fecha_actual = datetime.now()

    # ---------------------------------------------
    # MAPA DE PACIENTES
    # ---------------------------------------------

    mapa_pacientes = {

        p[0]: {

            "plan": p[1],
            "edad": p[2],
            "sexo": p[3],
            "antiguedad": p[4],
            "zona": p[5]

        }

        for p in patients

    }

    # ---------------------------------------------
    # TURNOS POR PACIENTE
    # ---------------------------------------------

    turnos_paciente = {}

    for turno in turns:

        turnos_paciente.setdefault(

            turno[0],

            []

        ).append(turno)

    # ---------------------------------------------
    # GENERACIÓN
    # ---------------------------------------------

    for patient_id in patient_ids:

        paciente = mapa_pacientes[int(patient_id)]

        turnos = turnos_paciente.get(

            int(patient_id),

            []

        )

        if len(turnos) == 0:

            continue

        espera_promedio = np.mean(

            [t[4] for t in turnos]

        )

        cantidad_turnos = len(turnos)

        servicios = [

            t[1]

            for t in turnos

        ]

        # ---------------------------------------------
        # Probabilidad base
        # ---------------------------------------------

        prob = 0.05

        # Espera

        if espera_promedio > 70:

            prob += 0.25

        elif espera_promedio > 50:

            prob += 0.15

        elif espera_promedio > 35:

            prob += 0.08

        # Guardia

        if 1 in servicios:

            prob += 0.08

        # Muchos turnos → más oportunidades de reclamar

        if cantidad_turnos >= 5:

            prob += 0.05

        # Premium reclama menos

        if paciente["plan"] == 4:

            prob -= 0.03

        # Mucha antigüedad → menor probabilidad

        if paciente["antiguedad"] > 60:

            prob -= 0.04

        # Ruido

        prob += np.random.normal(0,0.02)

        prob = max(

            0.02,

            min(prob,0.60)

        )

        # ---------------------------------------------
        # ¿Tiene reclamo?
        # ---------------------------------------------

        if random.random() < prob:

            cantidad = random.choices(

                [1,2],

                weights=[0.82,0.18],

                k=1

            )[0]

            for _ in range(cantidad):

                tipo = random.choice(

                    TIPOS_RECLAMO

                )

                criticidad = random.choices(

                    CRITICIDADES,

                    weights=PESOS_CRITICIDAD,

                    k=1

                )[0]

                # ---------------------------------------------
                # Días resolución
                # ---------------------------------------------

                if criticidad == "Alta":

                    dias = random.randint(20,45)

                elif criticidad == "Media":

                    dias = random.randint(8,20)

                else:

                    dias = random.randint(1,8)

                # Guardia demora un poco más

                if 1 in servicios:

                    dias += random.randint(0,5)

                # Premium se resuelve antes

                if paciente["plan"] == 4:

                    dias = max(

                        1,

                        dias - random.randint(1,4)

                    )

                claims.append(

                    (

                        int(patient_id),

                        fecha_actual - timedelta(

                            days=random.randint(0,730)

                        ),

                        tipo,

                        criticidad,

                        dias

                    )

                )

    logging.info(

        f"Reclamos generados: {len(claims)}"

    )

    return claims

# ==================================================
# INSERCIÓN DE RECLAMOS
# ==================================================
# Inserta los reclamos generados en la base de datos
# operacional VitaHealth.
# ==================================================

def insert_claims(cursor, claims):

    query = """
        INSERT INTO reclamos
        (
            id_paciente,
            fecha_reclamo,
            tipo_reclamo,
            criticidad,
            dias_resolucion
        )
        VALUES (%s, %s, %s, %s, %s)
    """

    insert_data_massive(cursor, query, claims)

    logging.info(f"Reclamos insertados: {len(claims)}")


# ==================================================
# PREPARACIÓN DE ENCUESTAS
# ==================================================
# Prepara las encuestas para su inserción en
# PostgreSQL utilizando los valores originales
# del dataset.
# ==================================================

# ==================================================
# GENERACIÓN DE ENCUESTAS
# ==================================================

def generate_surveys(df_original, patients, turns, claims):

    logging.info("Generando encuestas sintéticas...")

    # ---------------------------------------------
    # MAPAS
    # ---------------------------------------------

    mapa_pacientes = {

        p[0]: {

            "plan": p[1],
            "edad": p[2],
            "sexo": p[3],
            "antiguedad": p[4],
            "zona": p[5]

        }

        for p in patients

    }

    mapa_turnos = {}

    for turno in turns:

        mapa_turnos.setdefault(

            turno[0],

            []

        ).append(turno)

    mapa_reclamos = {}

    for reclamo in claims:

        mapa_reclamos.setdefault(

            reclamo[0],

            []

        ).append(reclamo)

    surveys = []

    # =====================================================
    # GENERACIÓN
    # =====================================================

    for fila in df_original.itertuples():

        id_paciente = fila.id_paciente

        paciente = mapa_pacientes[id_paciente]

        turnos_paciente = mapa_turnos[id_paciente]

        reclamos = mapa_reclamos.get(

            id_paciente,

            []

        )
        # ---------------------------------------------
        # EXPERIENCIA DEL PACIENTE
        # ---------------------------------------------

        espera = np.mean(

            [t[4] for t in turnos_paciente]

        )

        # Elegimos uno de los turnos del paciente para asociar la encuesta
        turno = random.choice(

            turnos_paciente

        )

        id_servicio = turno[1]

        id_centro = turno[2]

        # Convertimos IDs a nombres para insertar en la tabla encuestas
        nombre_servicio = SERVICIOS[id_servicio]

        nombre_centro = CENTROS[id_centro]

        cantidad_reclamos = len(reclamos)

        if cantidad_reclamos > 0:

            dias_resolucion = np.mean(

                [r[4] for r in reclamos]

            )

        else:

            dias_resolucion = 0
        
        # ==========================================
        # PROBABILIDADES
        # ==========================================

        promotor = 0.55

        pasivo = 0.25

        detractor = 0.20

        # ------------------------------------------
        # Espera
        # ------------------------------------------

        if espera > 70:

            detractor += 0.25

            promotor -= 0.18

        elif espera > 45:

            detractor += 0.12

            promotor -= 0.08

        # ------------------------------------------
        # Reclamos
        # ------------------------------------------

        if cantidad_reclamos > 0:

            detractor += 0.15

            promotor -= 0.08

        # ------------------------------------------
        # Días resolución
        # ------------------------------------------

        if dias_resolucion > 20:

            detractor += 0.08

        # ------------------------------------------
        # Premium
        # ------------------------------------------

        if paciente["plan"] == 4:

            promotor += 0.05

            # Premium es más exigente
            if espera > 40:

                detractor += 0.06

        # ------------------------------------------
        # Guardia
        # ------------------------------------------

        if id_servicio == 1:

            detractor += 0.05

        # ------------------------------------------
        # Antigüedad
        # ------------------------------------------

        if paciente["antiguedad"] > 60:

            promotor += 0.04

            if dias_resolucion > 20:

                detractor += 0.08

        # ------------------------------------------
        # Ruido
        # ------------------------------------------

        ruido = np.random.normal(

            0,

            0.05

        )

        promotor += ruido

        detractor -= ruido

        total = promotor + pasivo + detractor

        promotor /= total

        pasivo /= total

        detractor /= total

        categoria = random.choices(

            [

                "Promotor",

                "Pasivo",

                "Detractor"

            ],

            weights=[

                promotor,

                pasivo,

                detractor

            ],

            k=1

        )[0]

        # ------------------------------------------
        # NPS
        # ------------------------------------------

        if categoria == "Promotor":

            nps = random.choice(

                [9,10]

            )

        elif categoria == "Pasivo":

            nps = random.choice(

                [7,8]

            )

        else:

            nps = random.randint(

                0,

                6

            )

        # ------------------------------------------
        # CSAT
        # ------------------------------------------

        csat = nps + random.choice(

            [

                -1,

                0,

                0,

                1

            ]

        )

        csat = max(

            0,

            min(

                csat,

                10

            )

        )
        surveys.append(

            (

                fila.id_encuesta,

                id_paciente,

                fila.fecha_encuesta,

                nombre_centro,

                nombre_servicio,

                nps,

                csat,   

                categoria,

                fila.comentario

            )

        )

    logging.info(

        f"Encuestas generadas: {len(surveys)}"

    )

    return surveys

    

# ==================================================
# INSERCIÓN DE ENCUESTAS
# ==================================================
# Inserta las encuestas en la base de datos
# operacional VitaHealth.
# ==================================================

def insert_surveys(cursor, surveys):

    query = """
        INSERT INTO encuestas
        (
            id_encuesta,
            id_paciente,
            fecha_encuesta,
            sanatorio,
            servicio,
            puntuacion_nps,
            csat,
            categoria_nps,
            comentario
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    insert_data_massive(cursor, query, surveys)

    logging.info(f"Encuestas insertadas: {len(surveys)}")

# ==================================================
# EJECUCIÓN PRINCIPAL
# ==================================================

def main():

    logging.info("==========================================")
    logging.info("INICIO DEL PROCESO DE GENERACIÓN DE DATOS")
    logging.info("==========================================")

    # ==========================================
    # Cargar encuestas
    # ==========================================

    df = load_surveys()

    # ==========================================
    # Obtener pacientes únicos
    # ==========================================

    pacientes = get_unique_patients(df)

    logging.info(f"Cantidad de pacientes únicos: {len(pacientes)}")

    print("\nPrimeros pacientes encontrados:")
    print(pacientes.head())

    # ==========================================
    # Generar datos sintéticos de pacientes
    # ==========================================

    patients_data = generate_patients(pacientes)

    print("\nPrimeros pacientes generados:")

    for paciente in patients_data[:5]:
        print(paciente)

    # ==========================================
    # Generar datos sintéticos de turnos
    # ==========================================

    turns_data = generate_turns(

    pacientes,

    patients_data

    )

    print("\nPrimeros turnos generados:")

    for turno in turns_data[:5]:
        print(turno)
    
    # ==========================================
    # Generar datos sintéticos de reclamos
    # ==========================================

    claims_data = generate_claims(

    pacientes,

    patients_data,

    turns_data

    )


    print("\nPrimeras reclamos generados:")
    for reclamo in claims_data[:5]:
        print(reclamo)

    # ==========================================
    # Preparar encuestas
    # ==========================================

    surveys_data = generate_surveys(

    df,

    patients_data,

    turns_data,

    claims_data

)

    print("\nPrimeras encuestas preparadas:")

    for encuesta in surveys_data[:5]:
        print(encuesta)
    # ==========================================
    # Conexión a PostgreSQL
    # ==========================================

    conn = get_db_connection()
    cursor = conn.cursor()

    # ==========================================
    # Insertar pacientes 
    # ==========================================

    insert_patients(cursor, patients_data)
    # Ya fueron insertados previamente.
    # Descomentar únicamente si se recrea la base
    # de datos desde cero.
    # ==========================================
    # Insertar turnos
    # ==========================================

    insert_turns(cursor, turns_data)

    # ==========================================
    # Insertar reclamos
    # ==========================================

    insert_claims(cursor, claims_data)

    # ==========================================
    # Insertar encuestas
    # ==========================================

    insert_surveys(cursor, surveys_data)

    # ==========================================
    # Confirmar cambios
    # ==========================================

    conn.commit()

    # ==========================================
    # Cerrar conexión
    # ==========================================

    cursor.close()
    conn.close()

    logging.info("Proceso finalizado correctamente.")

# ==================================================
# EJECUCIÓN DEL SCRIPT
# ==================================================

if __name__ == "__main__":
    main()