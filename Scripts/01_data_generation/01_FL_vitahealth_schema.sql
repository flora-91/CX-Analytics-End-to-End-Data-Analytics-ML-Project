-- ============================================================
-- VITAHEALTH
-- Base de Datos Operacional
-- Script: 01_vitahealth_schema.sql
-- Autor: Florencia Lombardi
-- Descripción:
-- Creación del modelo relacional de la base operacional
-- para el proyecto Customer Experience Analytics.
-- ============================================================

-- ============================================================
-- TABLA: PLANES
-- ============================================================
-- Almacena los planes de cobertura médica ofrecidos por 
-- VitaHealth y sus características principales.
-- ============================================================

CREATE TABLE planes (

    id_plan SERIAL PRIMARY KEY,

    nombre_plan VARCHAR(50) NOT NULL UNIQUE,

    categoria VARCHAR(30) NOT NULL,

    segmento VARCHAR(20) NOT NULL,

    valor_plan NUMERIC(10,2) NOT NULL,

    copago NUMERIC(10,2) NOT NULL

);

-- ============================================================
-- DATOS INICIALES: PLANES
-- ============================================================
-- Carga de los planes disponibles en VitaHealth.
-- ============================================================

INSERT INTO planes
(nombre_plan, categoria, segmento, valor_plan, copago)
VALUES
('Essential','Básico','Individual',45000,4000),
('Plus','Intermedio','Individual',70000,2500),
('Premium','Premium','Individual',110000,0),
('Corporate','Corporativo','Empresas',95000,1000);


-- ============================================================
-- TABLA: CENTROS_MEDICOS
-- ============================================================
-- Almacena los centros médicos donde se brindan las
-- prestaciones de VitaHealth.
-- ============================================================

CREATE TABLE centros_medicos (

    id_centro SERIAL PRIMARY KEY,

    nombre_centro VARCHAR(100) NOT NULL UNIQUE,

    ciudad VARCHAR(50) NOT NULL,

    zona VARCHAR(20) NOT NULL

);


-- ============================================================
-- DATOS INICIALES: CENTROS_MEDICOS
-- ============================================================
-- Carga de los centros médicos de VitaHealth.
-- ============================================================

INSERT INTO centros_medicos
(nombre_centro, ciudad, zona)
VALUES
('Centro Médico Norte','Ciudad Central','Norte'),
('Clínica del Valle','Ciudad Central','Oeste'),
('Instituto Médico Central','Ciudad Central','Centro'),
('Sanatorio Parque Salud','Ciudad Central','Sur');


-- ============================================================
-- TABLA: SERVICIOS
-- ============================================================
-- Almacena los servicios y especialidades disponibles
-- en los centros médicos.
-- ============================================================

CREATE TABLE servicios (

    id_servicio SERIAL PRIMARY KEY,

    nombre_servicio VARCHAR(100) NOT NULL UNIQUE,

    categoria VARCHAR(50) NOT NULL

);

-- ============================================================
-- DATOS INICIALES: SERVICIOS
-- ============================================================
-- Carga de los servicios disponibles en VitaHealth.
-- ============================================================

INSERT INTO servicios
(nombre_servicio, categoria)
VALUES
('Guardia','Urgencias'),
('Consultorio Clínico','Consulta'),
('Pediatría','Consulta'),
('Cardiología','Especialidad'),
('Traumatología','Especialidad'),
('Laboratorio','Diagnóstico'),
('Diagnóstico por Imágenes','Diagnóstico'),
('Vacunación','Preventivo');


-- ============================================================
-- TABLA: PACIENTES
-- ============================================================
-- Almacena la información demográfica y del plan de cada
-- paciente registrado en VitaHealth.
--
-- Los registros de esta tabla serán generados mediante el
-- script de datos sintéticos (01_data_generation.py).
-- ============================================================

CREATE TABLE pacientes (

    id_paciente INTEGER PRIMARY KEY,

    id_plan INTEGER NOT NULL,

    edad INTEGER NOT NULL CHECK (edad BETWEEN 18 AND 100),

    sexo VARCHAR(20) NOT NULL CHECK (sexo IN ('Femenino','Masculino','Otro')),

    antiguedad_meses INTEGER NOT NULL,

    zona VARCHAR(20) NOT NULL,

    CONSTRAINT fk_paciente_plan
        FOREIGN KEY (id_plan)
        REFERENCES planes(id_plan)

);

-- ============================================================
-- TABLA: TURNOS
-- ============================================================
-- Registra los turnos solicitados por los pacientes.
--
-- Los registros serán generados mediante el script de
-- datos sintéticos (01_data_generation.py).
-- ============================================================

CREATE TABLE turnos (

    id_turno SERIAL PRIMARY KEY,

    id_paciente INTEGER NOT NULL,

    id_servicio INTEGER NOT NULL,

    id_centro INTEGER NOT NULL,

    fecha_turno DATE NOT NULL,

    tiempo_espera INTEGER NOT NULL CHECK (tiempo_espera >= 0),

    cancelado BOOLEAN NOT NULL,

    asistio BOOLEAN NOT NULL,

    CONSTRAINT fk_turno_paciente
        FOREIGN KEY (id_paciente)
        REFERENCES pacientes(id_paciente),

    CONSTRAINT fk_turno_servicio
        FOREIGN KEY (id_servicio)
        REFERENCES servicios(id_servicio),

    CONSTRAINT fk_turno_centro
        FOREIGN KEY (id_centro)
        REFERENCES centros_medicos(id_centro)

);

-- ============================================================
-- TABLA: RECLAMOS
-- ============================================================
-- Registra los reclamos realizados por los pacientes.
--
-- Los registros serán generados mediante el script de
-- datos sintéticos (01_data_generation.py).
-- ============================================================

CREATE TABLE reclamos (

    id_reclamo SERIAL PRIMARY KEY,

    id_paciente INTEGER NOT NULL,

    fecha_reclamo DATE NOT NULL,

    tipo_reclamo VARCHAR(100) NOT NULL,

    criticidad VARCHAR(20) NOT NULL,

    dias_resolucion INTEGER NOT NULL CHECK (dias_resolucion >= 0),

    CONSTRAINT fk_reclamo_paciente
        FOREIGN KEY (id_paciente)
        REFERENCES pacientes(id_paciente)

);

-- ============================================================
-- TABLA: ENCUESTAS
-- ============================================================
-- Almacena las encuestas de satisfacción respondidas por los
-- pacientes. Los registros serán importados desde el dataset
-- original y posteriormente enriquecidos con el análisis NLP.
-- ============================================================

CREATE TABLE encuestas (

    id_encuesta INTEGER PRIMARY KEY,

    id_paciente INTEGER NOT NULL,

    fecha_encuesta DATE NOT NULL,

    sanatorio VARCHAR(100) NOT NULL,

    servicio VARCHAR(100) NOT NULL,

    puntuacion_nps NUMERIC(3,1) NOT NULL,

    csat INTEGER NOT NULL,

    categoria_nps VARCHAR(20) NOT NULL
    CHECK (categoria_nps IN ('Promotor','Pasivo','Detractor')),

    comentario TEXT,

    sentimiento VARCHAR(20),

    topico VARCHAR(100),

    subtopico VARCHAR(100),

    CONSTRAINT fk_encuesta_paciente
        FOREIGN KEY (id_paciente)
        REFERENCES pacientes(id_paciente),


);

