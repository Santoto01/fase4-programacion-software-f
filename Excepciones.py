# excepciones.py
"""
Módulo de excepciones personalizadas para el sistema de Software FJ.
"""


class SoftwareFJError(Exception):
    """Excepción base para todos los errores controlados del sistema."""

    def __init__(self, message: str, codigo_error: str = None):
        self.message = message
        self.codigo_error = codigo_error
        if codigo_error is not None:
            super().__init__(f"[{codigo_error}] {self.message}")
        else:
            super().__init__(self.message)


class DatosInvalidosError(SoftwareFJError):
    """Se lanza cuando los datos ingresados tienen formato o valores erroneos."""

    def __init__(self, message: str):
        super().__init__(message, codigo_error="ERR-101")


class ParametroFaltanteError(SoftwareFJError):
    """Se lanza cuando falta un dato obligatorio que crea un objeto."""

    def __init__(self, message: str):
        super().__init__(message, codigo_error="ERR-102")


class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando el servicio está inactivo o no tiene cupo/stock."""

    def __init__(self, message: str):
        super().__init__(message, codigo_error="ERR-201")


class ReservaInvalidaError(SoftwareFJError):
    """Se lanza cuando hay fallos al crear o procesar una reserva."""

    def __init__(self, message: str):
        super().__init__(message, codigo_error="ERR-301")


class OperacionNoPermitidaError(SoftwareFJError):
    """Se lanza cuando se intenta realizar una transición de estado ilegal."""

    def __init__(self, message: str):
        super().__init__(message, codigo_error="ERR-401")


class CalculoInconsistenteError(SoftwareFJError):
    """Se lanza cuando el cálculo de costos arroja un valor negativo o incoherente."""

    def __init__(self, message: str):
        super().__init__(message, codigo_error="ERR-501")
