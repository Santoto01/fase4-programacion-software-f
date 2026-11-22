## gestor.py
"""
Controlador principal del sistema Software FJ.
Gestiona clientes, servicios y reservas en listas internas y registra todo en logs.
"""

from logging import Logger
from Cliente import Cliente
from Modelos_base import Servicio
from Reserva import Reserva
from Excepciones import (
    DatosInvalidosError,
    ReservaInvalidaError,
    SoftwareFJError,
)


class GestorSoftwareFJ:
    """Administra las operaciones del sistema en memoria."""

    def __init__(self, logger: Logger):
        self.logger = logger
        self.clientes: list[Cliente] = []
        self.servicios: list[Servicio] = []
        self.reservas: list[Reserva] = []

    def registrar_cliente(self, cliente: Cliente) -> None:
        if any(c.id == cliente.id for c in self.clientes):
            raise DatosInvalidosError(f"Ya existe un cliente registrado con documento '{cliente.id}'.")
        self.clientes.append(cliente)
        self.logger.info(f"Cliente registrado exitosamente: {cliente.obtener_resumen()}")

    def agregar_servicio(self, servicio: Servicio) -> None:
        if any(s.id == servicio.id for s in self.servicios):
            raise DatosInvalidosError(f"Ya existe un servicio registrado con código '{servicio.id}'.")
        self.servicios.append(servicio)
        self.logger.info(f"Servicio agregado al catálogo: {servicio.describir()}")

    def buscar_cliente(self, documento: str) -> Cliente:
        for cliente in self.clientes:
            if cliente.id == documento:
                return cliente
        raise LookupError(f"No se encontró ningún cliente con documento '{documento}'.")

    def buscar_servicio(self, codigo: str) -> Servicio:
        for servicio in self.servicios:
            if servicio.id == codigo:
                return servicio
        raise LookupError(f"No se encontró ningún servicio con código '{codigo}'.")

    def crear_reserva(self, codigo_reserva: str, doc_cliente: str, cod_servicio: str, horas: float) -> Reserva:
        """
        Crea una reserva buscando cliente y servicio en las listas internas.
        Demuestra encadenamiento de excepciones (raise ... from e).
        """
        try:
            cliente = self.buscar_cliente(doc_cliente)
            servicio = self.buscar_servicio(cod_servicio)
            nueva_reserva = Reserva(codigo_reserva, cliente, servicio, horas)
        except LookupError as e:
            # Encadenamiento de excepciones requerido por la guía
            raise ReservaInvalidaError(
                f"Imposible crear reserva '{codigo_reserva}': referencia inexistente."
            ) from e
        except SoftwareFJError as e:
            raise ReservaInvalidaError(
                f"Fallo al validar reglas de la reserva '{codigo_reserva}'."
            ) from e

        self.reservas.append(nueva_reserva)
        self.logger.info(f"Reserva creada: {nueva_reserva.obtener_resumen()}")
        return nueva_reserva
    