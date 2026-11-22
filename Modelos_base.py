"""
Clases abstractas base que definen la estructura mínima de las entidades y servicios.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from Excepciones import DatosInvalidosError, ParametroFaltanteError


class EntidadBase(ABC):
    """Clase abstracta que representa cualquier entidad del sistema."""

    def __init__(self, identificador: str):
        if not identificador or not str(identificador).strip():
            raise ParametroFaltanteError("El identificador de la entidad es obligatorio.")
        self._id = str(identificador).strip()
        self._fecha_creacion = datetime.now()

    @property
    def id(self) -> str:
        return self._id

    @property
    def fecha_creacion(self) -> datetime:
        return self._fecha_creacion

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Cada entidad hija debe tener su propia representación resumida."""
        pass


class Servicio(EntidadBase, ABC):
    """Clase abstracta base para los servicios ofrecidos por Software FJ."""

    def __init__(self, codigo: str, nombre: str, tarifa_hora: float, disponible: bool = True):
        super().__init__(codigo)
        self.nombre = nombre
        self.tarifa_hora = tarifa_hora
        self.disponible = disponible

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not str(valor).strip():
            raise ParametroFaltanteError("El nombre del servicio no puede estar vacío.")
        self._nombre = str(valor).strip()

    @property
    def tarifa_hora(self) -> float:
        return self._tarifa_hora

    @tarifa_hora.setter
    def tarifa_hora(self, valor: float):
        if not isinstance(valor, (int, float)) or valor <= 0:
            raise DatosInvalidosError("La tarifa por hora debe ser un número mayor a cero.")
        self._tarifa_hora = float(valor)

    @abstractmethod
    def validar_parametros(self, horas: float) -> None:
        """Valida reglas específicas de cada tipo de servicio."""
        pass

    @abstractmethod
    def calcular_costo(self, horas: float) -> float:
        """Calcula el costo base del servicio según su lógica particular."""
        pass

    @abstractmethod
    def describir(self) -> str:
        """Retorna la descripción detallada del servicio."""
        pass

    def obtener_resumen(self) -> str:
        estado = "Disponible" if self.disponible else "No disponible"
        return f"[{self.id}] {self.nombre} (${self.tarifa_hora:,.2f}/h) - {estado}"
    