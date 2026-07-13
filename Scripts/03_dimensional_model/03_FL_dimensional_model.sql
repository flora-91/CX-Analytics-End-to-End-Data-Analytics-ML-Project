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

----------------------------------------------------------
-- ETAPA 1
-- CREACIÓN DEL ESQUEMA
----------------------------------------------------------

CREATE SCHEMA IF NOT EXISTS DW_CX;

USE SCHEMA DW_CX;

----------------------------------------------------------
-- ETAPA 2
-- DIMENSIONES
----------------------------------------------------------

----------------------------------------------------------
-- DIM_PACIENTE
----------------------------------------------------------

CREATE OR REPLACE TABLE DIM_PATIENT (

    PATIENT_KEY INTEGER AUTOINCREMENT PRIMARY KEY,

    ID_PACIENTE INTEGER,

    EDAD INTEGER,

    SEXO VARCHAR(20),

    ZONA VARCHAR(100),

    ANTIGUEDAD_MESES INTEGER

);

----------------------------------------------------------
-- DIM_PLAN
----------------------------------------------------------

CREATE OR REPLACE TABLE DIM_PLAN (

    PLAN_KEY INTEGER AUTOINCREMENT PRIMARY KEY,

    ID_PLAN INTEGER,

    NOMBRE_PLAN VARCHAR(100),

    CATEGORIA VARCHAR(100),

    SEGMENTO VARCHAR(100),

    VALOR_PLAN DECIMAL(12,2),

    COPAGO DECIMAL(12,2)

);

----------------------------------------------------------
-- DIM_SERVICIO
----------------------------------------------------------

CREATE OR REPLACE TABLE DIM_SERVICE (

    SERVICE_KEY INTEGER AUTOINCREMENT PRIMARY KEY,

    ID_SERVICIO INTEGER,

    NOMBRE_SERVICIO VARCHAR(100),

    CATEGORIA VARCHAR(100)

);

----------------------------------------------------------
-- DIM_CENTRO_MEDICO
----------------------------------------------------------

CREATE OR REPLACE TABLE DIM_MEDICAL_CENTER (

    CENTER_KEY INTEGER AUTOINCREMENT PRIMARY KEY,

    ID_CENTRO INTEGER,

    NOMBRE_CENTRO VARCHAR(100),

    CIUDAD VARCHAR(100),

    ZONA VARCHAR(100)

);

----------------------------------------------------------
-- DIM_FECHA
----------------------------------------------------------

CREATE OR REPLACE TABLE DIM_DATE (

    DATE_KEY INTEGER PRIMARY KEY,

    FECHA DATE,

    DIA INTEGER,

    MES INTEGER,

    NOMBRE_MES VARCHAR(20),

    TRIMESTRE INTEGER,

    ANIO INTEGER,

    DIA_SEMANA VARCHAR(20)

);

----------------------------------------------------------
-- ETAPA 3
-- TABLA DE HECHOS
----------------------------------------------------------

CREATE OR REPLACE TABLE FACT_CUSTOMER_EXPERIENCE (

    EXPERIENCE_KEY INTEGER AUTOINCREMENT PRIMARY KEY,

    DATE_KEY INTEGER,

    PATIENT_KEY INTEGER,

    PLAN_KEY INTEGER,

    SERVICE_KEY INTEGER,

    CENTER_KEY INTEGER,

    PUNTUACION_NPS INTEGER,

    CSAT INTEGER,

    TIEMPO_ESPERA INTEGER,

    CANCELADO BOOLEAN,

    ASISTIO BOOLEAN,

    TIENE_RECLAMO BOOLEAN,

    DIAS_RESOLUCION INTEGER

);

----------------------------------------------------------
-- ETAPA 4
-- CLAVES FORÁNEAS
----------------------------------------------------------

ALTER TABLE FACT_CUSTOMER_EXPERIENCE
ADD CONSTRAINT FK_DATE
FOREIGN KEY (DATE_KEY)
REFERENCES DIM_DATE(DATE_KEY);

ALTER TABLE FACT_CUSTOMER_EXPERIENCE
ADD CONSTRAINT FK_PATIENT
FOREIGN KEY (PATIENT_KEY)
REFERENCES DIM_PATIENT(PATIENT_KEY);

ALTER TABLE FACT_CUSTOMER_EXPERIENCE
ADD CONSTRAINT FK_PLAN
FOREIGN KEY (PLAN_KEY)
REFERENCES DIM_PLAN(PLAN_KEY);

ALTER TABLE FACT_CUSTOMER_EXPERIENCE
ADD CONSTRAINT FK_SERVICE
FOREIGN KEY (SERVICE_KEY)
REFERENCES DIM_SERVICE(SERVICE_KEY);

ALTER TABLE FACT_CUSTOMER_EXPERIENCE
ADD CONSTRAINT FK_CENTER
FOREIGN KEY (CENTER_KEY)
REFERENCES DIM_MEDICAL_CENTER(CENTER_KEY);

----------------------------------------------------------
-- FIN DEL MODELO DIMENSIONAL
----------------------------------------------------------