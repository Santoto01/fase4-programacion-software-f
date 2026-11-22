#reserva.py
"""
Modulo de gestion de reservas.
Implimenta control de estados y metodos sobrecargados para el calculo de los costos.
"""
from Modelos_base import EntidadBase, Servicio
from Cliente import Cliente
from Excepciones import(
    CalculoInconsistenteError,
    OperacionNoPermitidaError,
    ReservaInvalidaError,
)

class Reserva(EntidadBase):
    """Representa una reserva que vincula un cliente con un servicio por un tiempo dado."""

    ESTADOS_VALIDOS = ("PENDIENTE," "CONFIRMADA", "CANCELADA", "PROCESADA")

    def __init__(self, codigo_reserva: str, cliente: Cliente, servicio: Servicio, duracion_horas: float):

        super().__init__(codigo_reserva)

        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva requiere un objeto Cliente valido")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere un objeto Servicio valido")
        if not isinstance(duracion_horas,(int, float)) or duracion_horas <=0:
            raise ReservaInvalidaError("La duracion de las reservas tiene que ser mayor a 0 horasw ")

        #Valida las reglas propias del servicio seleccionado
        servicio.validar_parametros(duracion_horas)

        self.cliente = cliente
        self.servicio = servicio
        self.duracion_horas= float(duracion_horas)
        self._estado = "PENDIENTE"

    @property
    def estado(self) -> str:
        return self._estado

    def calcular_total(
        self,
        porcentaje_iva: float = 0.19,
        descuento: float = 0.0,
        recargo_urgencia: float = 0.0
    ) -> float:
        """
        Método sobrecargado mediante parámetros opcionales:
        1. calcular_total() -> Aplica IVA estándar del 19% sin descuentos.
        2. calcular_total(0.19, 15000) -> Aplica descuento fijo.
        3. calcular_total(0.0, 0.0, 25000) -> Exento de IVA con recargo por urgencia.
        """
        if porcentaje_iva < 0 or descuento < 0 or recargo_urgencia < 0:
            raise CalculoInconsistenteError("Los impuestos, descuentos y recargos no pueden ser negativos.")
        costo_base = self.servicio.calcular_costo(self.duracion_horas)
        subtotal = costo_base - descuento + recargo_urgencia

        if subtotal < 0:

            raise CalculoInconsistenteError(
               f" El descuento (${descuento:,.2f}) supera el costo del servicio (${costo_base:,.2f})."
            )
        total = subtotal * (1 + porcentaje_iva)
        return round(total, 2)

    def confirmar(self) ->None:
        if self._estado != "PENDIENTE":
            raise OperacionNoPermitidaError(
                f"No se puede confirmar la reserva {self.id} porque su estado es '{self._estado}'."
            )
        self._estado= "CONFIRMADA"

    def cancelar(self) -> None:
        if self._estado in ("CANCELA", "PROCESADA"):
            raise OperacionNoPermitidaError(
              f"No se puede cancelar la reserva {self.id} en estado '{self._estado}'."
            )
        self._estado="CANCELADA"

    def procesar(self) -> float:
        if self._estado !="CONFIRMADA":
            raise OperacionNoPermitidaError(
                f"Solo se pueden procesar reservas CONFIRMADAS (estado actual: '{self._estado}')."
            )
        total = self.calcular_total()
        self._estado= "PROCESADA"
        return total

    def obtener_resumen(self) -> str:
        return (
            f"Reserva [{self.id}] | Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} ({self.duracion_horas}h) | Estado: {self._estado}"
        )
        
        

