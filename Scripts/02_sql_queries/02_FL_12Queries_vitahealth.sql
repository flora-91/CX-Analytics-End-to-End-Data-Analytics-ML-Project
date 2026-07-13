/*
===========================================================
PROYECTO CUSTOMER EXPERIENCE ANALYTICS
CONSULTAS SQL - BASE OPERACIONAL
===========================================================

Autor: Florencia Lombardi
Base de datos: Customer Experience Analytics
Motor: PostgreSQL

Objetivo:
Desarrollar consultas SQL de distinta complejidad para analizar
la información operacional del sistema de atención médica,
validar la calidad de los datos y responder preguntas de negocio.

Estructura:

- 3 Consultas Básicas
- 5 Consultas Intermedias
- 4 Consultas Complejas

===========================================================
*/


/*=========================================================
QUERY 01 - PACIENTES POR PLAN
Nivel: Básico

Objetivo:
Conocer la cantidad de pacientes asociados a cada plan de salud.

Tablas utilizadas:
- pacientes
- planes
=========================================================*/

SELECT
    pl.nombre_plan,
    COUNT(p.id_paciente) AS cantidad_pacientes
FROM pacientes p
JOIN planes pl
    ON p.id_plan = pl.id_plan
GROUP BY pl.nombre_plan
ORDER BY cantidad_pacientes DESC;


/*=========================================================
QUERY 02 - TURNOS POR SERVICIO
Nivel: Básico

Objetivo:
Identificar cuáles son los servicios con mayor cantidad de turnos.

Tablas utilizadas:
- turnos
- servicios
=========================================================*/

SELECT
    s.nombre_servicio,
    COUNT(t.id_turno) AS cantidad_turnos
FROM turnos t
JOIN servicios s
    ON t.id_servicio = s.id_servicio
GROUP BY s.nombre_servicio
ORDER BY cantidad_turnos DESC;


/*=========================================================
QUERY 03 - INDICADORES GENERALES DE SATISFACCIÓN
Nivel: Básico

Objetivo:
Calcular los principales indicadores de satisfacción de los
pacientes a partir de las encuestas registradas.

La consulta obtiene:

- Cantidad total de encuestas
- Número de promotores, pasivos y detractores
- NPS (Net Promoter Score) calculado correctamente como:
  % Promotores - % Detractores
- Promedio de CSAT

Tablas utilizadas:
- encuestas
=========================================================*/

SELECT

    COUNT(*) AS total_encuestas,

    SUM(CASE
            WHEN categoria_nps = 'Promotor' THEN 1
            ELSE 0
        END) AS promotores,

    SUM(CASE
            WHEN categoria_nps = 'Pasivo' THEN 1
            ELSE 0
        END) AS pasivos,

    SUM(CASE
            WHEN categoria_nps = 'Detractor' THEN 1
            ELSE 0
        END) AS detractores,

    ROUND(
        (
            100.0 * SUM(CASE WHEN categoria_nps='Promotor' THEN 1 ELSE 0 END) / COUNT(*)
        ) -
        (
            100.0 * SUM(CASE WHEN categoria_nps='Detractor' THEN 1 ELSE 0 END) / COUNT(*)
        ),
        2
    ) AS nps,

    ROUND(AVG(csat),2) AS csat_promedio

FROM encuestas;



/*=========================================================
QUERY 04 - TIEMPO PROMEDIO DE ESPERA POR CENTRO
Nivel: Intermedio

Objetivo:
Analizar el tiempo promedio de espera de los pacientes en cada
centro médico.

Tablas utilizadas:
- turnos
- centros_medicos
=========================================================*/

SELECT
    c.nombre_centro,
    ROUND(AVG(t.tiempo_espera),2) AS tiempo_promedio_espera,
    COUNT(t.id_turno) AS total_turnos
FROM turnos t
JOIN centros_medicos c
    ON t.id_centro = c.id_centro
GROUP BY c.nombre_centro
ORDER BY tiempo_promedio_espera DESC;



/*=========================================================
QUERY 05 - SATISFACCIÓN POR SERVICIO
Nivel: Intermedio

Objetivo:
Evaluar el nivel de satisfacción de los pacientes para cada
servicio médico mediante el análisis del CSAT y del NPS,
permitiendo identificar aquellos servicios con mejor y peor
experiencia percibida.

Tablas utilizadas:
- encuestas
- servicios
=========================================================*/

SELECT

    s.nombre_servicio,

    COUNT(e.id_encuesta) AS total_encuestas,

    ROUND(AVG(e.csat),2) AS csat_promedio,

    ROUND(
        (
            100.0 * SUM(CASE WHEN e.categoria_nps = 'Promotor' THEN 1 ELSE 0 END)
            / COUNT(e.id_encuesta)
        ) -
        (
            100.0 * SUM(CASE WHEN e.categoria_nps = 'Detractor' THEN 1 ELSE 0 END)
            / COUNT(e.id_encuesta)
        ),
        2
    ) AS nps

FROM servicios s

LEFT JOIN encuestas e
    ON s.nombre_servicio = e.servicio

GROUP BY s.nombre_servicio

ORDER BY nps DESC, csat_promedio DESC;


/*=========================================================
QUERY 06 - PACIENTES CON MAYOR CANTIDAD DE RECLAMOS
Nivel: Intermedio

Objetivo:
Identificar los pacientes con mayor cantidad de reclamos
registrados.

Tablas utilizadas:
- pacientes
- reclamos
=========================================================*/

SELECT

    p.id_paciente,

    pl.nombre_plan,

    COUNT(r.id_reclamo) AS cantidad_reclamos

FROM pacientes p

JOIN planes pl
    ON p.id_plan = pl.id_plan

JOIN reclamos r
    ON p.id_paciente = r.id_paciente

GROUP BY
    p.id_paciente,
    pl.nombre_plan

ORDER BY cantidad_reclamos DESC

LIMIT 10;



/*=========================================================
QUERY 07 - TURNOS CANCELADOS POR SERVICIO
Nivel: Intermedio

Objetivo:
Analizar la cantidad de turnos cancelados por cada servicio.

Tablas utilizadas:
- turnos
- servicios
=========================================================*/

SELECT

    s.nombre_servicio,

    COUNT(*) AS total_turnos,

    SUM(
        CASE
            WHEN t.cancelado = TRUE THEN 1
            ELSE 0
        END
    ) AS turnos_cancelados,

    ROUND(
        100.0 *
        SUM(CASE WHEN t.cancelado = TRUE THEN 1 ELSE 0 END)
        / COUNT(*),
        2
    ) AS porcentaje_cancelacion

FROM turnos t

JOIN servicios s
    ON t.id_servicio = s.id_servicio

GROUP BY s.nombre_servicio

ORDER BY porcentaje_cancelacion DESC;



/*=========================================================
QUERY 08 - RELACIÓN ENTRE TIEMPO DE ESPERA Y SATISFACIÓN
Nivel: Intermedio

Objetivo:
Analizar la relación entre el tiempo promedio de espera de los
pacientes y su nivel de satisfacción, agrupando la información
por paciente.

Tablas utilizadas:
- pacientes
- turnos
- encuestas
=========================================================*/

SELECT

    p.id_paciente,

    ROUND(AVG(t.tiempo_espera),2) AS espera_promedio,

    ROUND(AVG(e.csat),2) AS csat_promedio,

    ROUND(
        (
            100.0 * SUM(CASE WHEN e.categoria_nps = 'Promotor' THEN 1 ELSE 0 END)
            / COUNT(e.id_encuesta)
        ) -
        (
            100.0 * SUM(CASE WHEN e.categoria_nps = 'Detractor' THEN 1 ELSE 0 END)
            / COUNT(e.id_encuesta)
        ),
        2
    ) AS nps

FROM pacientes p

LEFT JOIN turnos t
    ON p.id_paciente = t.id_paciente

LEFT JOIN encuestas e
    ON p.id_paciente = e.id_paciente

GROUP BY p.id_paciente

HAVING COUNT(e.id_encuesta) > 0

ORDER BY espera_promedio DESC;


/*=========================================================
QUERY 09 - RANKING DE CENTROS MÉDICOS
Nivel: Complejo

Objetivo:
Evaluar el desempeño de cada centro médico considerando el
volumen de atención, el tiempo promedio de espera y la cantidad
de cancelaciones de turnos.

Tablas utilizadas:
- centros_medicos
- turnos
=========================================================*/

SELECT

    c.nombre_centro,

    COUNT(t.id_turno) AS total_turnos,

    ROUND(AVG(t.tiempo_espera),2) AS espera_promedio,

    SUM(CASE WHEN t.cancelado THEN 1 ELSE 0 END) AS cancelaciones,

    ROUND(
        100.0 *
        SUM(CASE WHEN t.cancelado THEN 1 ELSE 0 END)
        / COUNT(*),
        2
    ) AS porcentaje_cancelacion

FROM centros_medicos c

JOIN turnos t
ON c.id_centro=t.id_centro

GROUP BY c.nombre_centro

ORDER BY espera_promedio ASC;



/*=========================================================
QUERY 10 - INDICADORES POR SERVICIO
Nivel: Complejo

Objetivo:
Obtener un resumen operativo por servicio incluyendo:

- Cantidad de turnos
- Tiempo promedio de espera
- Cancelaciones
- NPS promedio
- CSAT promedio

Tablas utilizadas:
- servicios
- turnos
- encuestas
=========================================================*/

SELECT

    s.nombre_servicio,

    COUNT(t.id_turno) AS total_turnos,

    ROUND(AVG(t.tiempo_espera),2) AS espera_promedio,

    SUM(CASE WHEN t.cancelado THEN 1 ELSE 0 END) AS cancelaciones,

    ROUND(
        100.0 *
        SUM(CASE WHEN t.cancelado THEN 1 ELSE 0 END)
        / COUNT(*),
        2
    ) AS porcentaje_cancelacion

FROM servicios s

LEFT JOIN turnos t
ON s.id_servicio=t.id_servicio

GROUP BY s.nombre_servicio

ORDER BY total_turnos DESC;



/*=========================================================
QUERY 11 - PERFIL DE PACIENTES
Nivel: Complejo

Objetivo:
Analizar el comportamiento de los pacientes según:

- Plan
- Edad
- Antigüedad
- Reclamos
- Nivel de satisfacción

Tablas utilizadas:
- pacientes
- planes
- reclamos
- encuestas
=========================================================*/

SELECT

    pl.nombre_plan,

    p.zona,

    COUNT(DISTINCT p.id_paciente) AS pacientes,

    ROUND(AVG(p.edad),1) AS edad_promedio,

    ROUND(AVG(p.antiguedad_meses),1) AS antiguedad_promedio,

    COUNT(DISTINCT r.id_reclamo) AS reclamos,

    ROUND(AVG(e.csat),2) AS csat_promedio

FROM pacientes p

LEFT JOIN planes pl
ON p.id_plan=pl.id_plan

LEFT JOIN reclamos r
ON p.id_paciente=r.id_paciente

LEFT JOIN encuestas e
ON p.id_paciente=e.id_paciente

GROUP BY
pl.nombre_plan,
p.zona

ORDER BY pacientes DESC;



/*=========================================================
QUERY 12 - ÍNDICE DE EXPERIENCIA DEL PACIENTE
Nivel: Complejo

Objetivo:
Construir un indicador compuesto que integre:

- Tiempo de espera
- NPS
- CSAT
- Reclamos

Este indicador servirá posteriormente como base para el modelo
analítico del Data Warehouse y los dashboards en Power BI.

Tablas utilizadas:
- pacientes
- turnos
- encuestas
- reclamos
=========================================================*/

SELECT

    p.id_paciente,

    pl.nombre_plan,

    ROUND(AVG(t.tiempo_espera),2) AS espera_promedio,

    ROUND(AVG(e.csat),2) AS csat_promedio,

    COUNT(DISTINCT r.id_reclamo) AS reclamos,

    ROUND(
        (
            AVG(e.csat) * 20
            -
            AVG(t.tiempo_espera)
            -
            COUNT(DISTINCT r.id_reclamo) * 5
        ),
        2
    ) AS indice_experiencia

FROM pacientes p

JOIN planes pl
ON p.id_plan=pl.id_plan

LEFT JOIN turnos t
ON p.id_paciente=t.id_paciente

LEFT JOIN encuestas e
ON p.id_paciente=e.id_paciente

LEFT JOIN reclamos r
ON p.id_paciente=r.id_paciente

GROUP BY
p.id_paciente,
pl.nombre_plan

ORDER BY indice_experiencia DESC;