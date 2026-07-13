"""
===========================================================
VITAHEALTH - ETL | PIPELINE PRINCIPAL
===========================================================

Proyecto:
Customer Experience Analytics

Autora:
Florencia Lombardi

Descripción:
Orquesta la ejecución completa del proceso ETL:

1. Extracción desde PostgreSQL.
2. Transformación al modelo dimensional.
3. Carga al Data Warehouse en Snowflake.

===========================================================
"""

# ==================================================
# IMPORTS
# ==================================================

import logging

from FL_extract import (
    check_connections,
    extract_tables
)

from FL_transform import (
    transform_complete_pipeline
)

from FL_load import (
    load_complete_pipeline
)

# ==================================================
# CONFIGURACIÓN DEL LOGGING
# ==================================================

logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s - %(levelname)s - %(message)s"

)

logger = logging.getLogger(__name__)


# ==================================================
# PIPELINE PRINCIPAL
# ==================================================

def main():

    logger.info("=" * 60)
    logger.info("VITAHEALTH ETL")
    logger.info("=" * 60)

    #--------------------------------------------------
    # Verificar conexiones
    #--------------------------------------------------

    logger.info("Verificando conexiones...")

    if not check_connections():

        logger.error("No fue posible establecer las conexiones.")

        return

    #--------------------------------------------------
    # EXTRACT
    #--------------------------------------------------

    logger.info("")
    logger.info("ETAPA 1 - EXTRACCIÓN")

    raw_data = extract_tables()

    #--------------------------------------------------
    # TRANSFORM
    #--------------------------------------------------

    logger.info("")
    logger.info("ETAPA 2 - TRANSFORMACIÓN")

    dimensions = transform_complete_pipeline(
        raw_data
    )

    #--------------------------------------------------
    # LOAD
    #--------------------------------------------------

    logger.info("")
    logger.info("ETAPA 3 - CARGA")

    success = load_complete_pipeline(
        dimensions
    )

    if success:

        logger.info("")
        logger.info("=" * 60)
        logger.info("PIPELINE ETL FINALIZADO CORRECTAMENTE")
        logger.info("=" * 60)

    else:

        logger.error("La carga en Snowflake falló.")


# ==================================================
# EJECUCIÓN
# ==================================================

if __name__ == "__main__":

    main()