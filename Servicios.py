#Servicios.py

"""
modulo con los tres servios especializados de software FJ.
muestra que la herencia y polimorfismo al sobreescribir validacion, calculo descriptivo 
"""

from Modelos_base import Servicio
from Excepciones import DatosInvalidosError, ServicioNoDisponibleError

class ReservaSala(Servicio):
    """Servicio de reserva de salas de reuniones o capacitación."""

    def __init__(self, codigo: str, nombre: str, tarifa_hora: float, capacidad: int, disponible: bool = True):
        super().__init__(codigo, nombre, tarifa_hora, disponible)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise DatosInvalidosError("La capacidad de la sala debe ser un entero positivo.")
        self.capacidad = capacidad

    def validar_parametros(self, horas: float) -> None:
        if not self.disponible:
            raise ServicioNoDisponibleError(f"La sala '{self.nombre}' no se encuentra disponible.")
        if horas < 1 or horas > 12:
            raise DatosInvalidosError("La reserva de sala debe ser entre 1 y 12 horas.")

    def calcular_costo(self, horas: float) -> float:
        self.validar_parametros(horas)
        subtotal = self.tarifa_hora * horas
        return subtotal * 1.10 if horas > 4 else subtotal

    def describir(self) -> str:
        return f"Sala '{self.nombre}' (Capacidad: {self.capacidad} personas) - ${self.tarifa_hora:,.2f}/h"
     
class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos de cómputo o audiovisuales."""

    def __init__(self, codigo: str, nombre: str, tarifa_hora: float, stock: int, deposito: float = 50000.0):
        super().__init__(codigo, nombre, tarifa_hora, disponible=(stock > 0))
        if not isinstance(stock, int) or stock < 0:
            raise DatosInvalidosError("El stock de equipos no puede ser negativo.")
        if deposito < 0:
            raise DatosInvalidosError("El depósito de garantía no puede ser negativo.")
        self.stock = stock
        self.deposito = float(deposito)

    def validar_parametros(self, horas: float) -> None:
        if not self.disponible or self.stock <= 0:
            raise ServicioNoDisponibleError(f"No hay unidades disponibles del equipo '{self.nombre}'.")
        if horas < 2:
            raise DatosInvalidosError("El alquiler de equipos requiere un mínimo de 2 horas.")

    def calcular_costo(self, horas: float) -> float:
        self.validar_parametros(horas)
        return (self.tarifa_hora * horas) + self.deposito

    def describir(self) -> str:
        return f"Equipo '{self.nombre}' (Stock: {self.stock}, Depósito: ${self.deposito:,.2f}) - ${self.tarifa_hora:,.2f}/h" 

class AsesoriaEspecializada(Servicio):
    """Servicio de consultoria y soporte tecnico especializado"""

    def __init__(self, codigo: str, nombre: str, tarifa_hora: float, especialidad: str, disponible: bool = True):
        super().__init__(codigo, nombre, tarifa_hora, disponible)
        if not especialidad or not str(especialidad).strip():
            raise DatosInvalidosError("Debe especificar el área de especialidad de la asesoría.")
        self.especialidad = str(especialidad).strip()

    def validar_parametros(self, horas: float) -> None:
        if not self.disponible:
            raise ServicioNoDisponibleError(f"La asesoría '{self.nombre}' no está disponible actualmente.")
        if horas <= 0 or horas > 8:
            raise DatosInvalidosError("Las asesorías deben durar entre 0.5 y 8 horas por sesión.")

    def calcular_costo(self, horas: float) -> float:
        self.validar_parametros(horas)
        # Descuento del 5% si contrata 5 o más horas de asesoría
        subtotal = self.tarifa_hora * horas
        return subtotal * 0.95 if horas >= 5 else subtotal

    def describir(self) -> str:
        return f"Asesoría '{self.nombre}' [Área: {self.especialidad}] - ${self.tarifa_hora:,.2f}/h"