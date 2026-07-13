# Business Rules

## Pacientes

- Los pacientes con planes **Premium** presentan menores tiempos de espera promedio que los pacientes con planes **Básicos**.
- Los pacientes con mayor antigüedad presentan una menor probabilidad de generar reclamos, aunque pueden hacerlo ocasionalmente.
- La edad y el sexo no determinan directamente el nivel de satisfacción del paciente, pero forman parte del perfil utilizado para los análisis y modelos predictivos.

---

## Turnos

- Los tiempos de espera dependen principalmente del tipo de servicio y del plan contratado.
- **Guardia** presenta los mayores tiempos de espera promedio.
- **Vacunación** y **Laboratorio** presentan tiempos de espera bajos.
- **Diagnóstico por Imágenes** presenta tiempos de espera intermedios.
- La probabilidad de cancelación aumenta cuando el tiempo de espera esperado es elevado.
- La asistencia al turno disminuye levemente cuando existen cancelaciones previas o demoras prolongadas.

---

## Reclamos

- La probabilidad de registrar un reclamo aumenta cuando los tiempos de espera son elevados.
- **Guardia** presenta una mayor frecuencia de reclamos que otros servicios.
- Los pacientes con planes Premium presentan una menor frecuencia de reclamos.
- Los reclamos críticos requieren más días de resolución que los reclamos administrativos.
- Los reclamos administrativos suelen resolverse en menor tiempo.
- No todos los pacientes que presentan un reclamo generan posteriormente una mala evaluación de la experiencia.

---

## Encuestas

- La puntuación **NPS** depende principalmente de la experiencia del paciente durante la atención.
- Los tiempos de espera elevados incrementan la probabilidad de obtener puntuaciones bajas de NPS.
- Los pacientes que realizaron reclamos presentan una mayor probabilidad de convertirse en detractores.
- Los pacientes cuyo turno fue cancelado presentan una mayor probabilidad de otorgar bajas calificaciones.
- Los pacientes con planes Premium presentan una mayor probabilidad de otorgar puntuaciones altas.
- La satisfacción (**CSAT**) mantiene una fuerte relación con el NPS, aunque incorpora variabilidad para reflejar diferencias individuales.
- Las variables sintéticas deberán ser consistentes con la información del dataset de encuestas, sin determinar directamente la categoría NPS.

---

# Variabilidad de los Datos

El conjunto de datos sintético fue diseñado para representar un escenario realista de Customer Experience en una organización de salud.

Para lograrlo, las reglas de negocio siguen los siguientes principios:

- Las reglas representan **tendencias generales** y no relaciones determinísticas.
- Ninguna condición garantiza por sí sola un resultado específico.
- Las relaciones entre variables se implementan mediante probabilidades, permitiendo excepciones y comportamientos atípicos.
- Se incorpora un componente aleatorio para representar factores no observables propios de la experiencia del paciente.
- Algunas variables permanecen completamente aleatorias con el objetivo de reflejar la variabilidad natural presente en escenarios reales.

---

# Objetivo del Dataset Sintético

El objetivo de la generación de datos sintéticos es construir un conjunto de información que permita:

- Simular un escenario realista de Customer Experience en una organización de salud.
- Implementar un proceso ETL completo desde PostgreSQL hacia Snowflake.
- Construir un Data Warehouse bajo un modelo dimensional.
- Realizar análisis exploratorios de datos (EDA).
- Aplicar técnicas de Procesamiento de Lenguaje Natural (NLP) sobre los comentarios de las encuestas.
- Entrenar y comparar modelos de Machine Learning (**Random Forest** y **XGBoost**) para la predicción de pacientes detractores.
- Desarrollar dashboards analíticos en Power BI.

El conjunto de datos busca mantener un equilibrio entre **realismo**, **variabilidad** y **consistencia**, evitando tanto relaciones completamente aleatorias como dependencias totalmente determinísticas, permitiendo que los modelos analíticos identifiquen patrones de forma autónoma.