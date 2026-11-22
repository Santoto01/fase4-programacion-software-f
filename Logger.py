# logger.py
"""
Configuración del sistema de registro (logs) en archivo y consola.
"""

import logging


def configurar_logger(nombre_archivo: str = "sistema_fj.log") -> logging.Logger:
    """Crea y retorna el logger principal del sistema."""
    logger = logging.getLogger("SoftwareFJ")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formato = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Guarda los eventos y errores en sistema_fj.log
        archivo_handler = logging.FileHandler(nombre_archivo, mode="a", encoding="utf-8")
        archivo_handler.setLevel(logging.INFO)
        archivo_handler.setFormatter(formato)

        # Muestra también en consola para seguir la ejecución
        consola_handler = logging.StreamHandler()
        consola_handler.setLevel(logging.INFO)
        consola_handler.setFormatter(formato)

        logger.addHandler(archivo_handler)
        logger.addHandler(consola_handler)

    return logger
