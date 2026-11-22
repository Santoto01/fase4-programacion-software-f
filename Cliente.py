"""
Modelo de Cliente con encapsulación estricta y validaciones de datos personales.
"""

from Modelos_base import EntidadBase
from Excepciones import DatosInvalidosError, ParametroFaltanteError


class Cliente(EntidadBase):
    """Representa a un cliente registrado en Software FJ."""

    def __init__(self, documento: str, nombre: str, correo: str, telefono: str):
        super().__init__(documento)
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not str(valor).strip():
            raise ParametroFaltanteError("El nombre del cliente es obligatorio.")
        if len(str(valor).strip()) < 3:
            raise DatosInvalidosError("El nombre del cliente debe tener al menos 3 caracteres.")
        self._nombre = str(valor).strip()

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str):
        if not valor or not str(valor).strip():
            raise ParametroFaltanteError("El correo electrónico es obligatorio.")
        correo_limpio = str(valor).strip()
        if "@" not in correo_limpio or "." not in correo_limpio.split("@")[-1]:
            raise DatosInvalidosError(f"Formato de correo inválido: '{correo_limpio}'.")
        self._correo = correo_limpio

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str):
        if not valor or not str(valor).strip():
            raise ParametroFaltanteError("El teléfono del cliente es obligatorio.")
        tel_limpio = str(valor).strip()
        if not tel_limpio.isdigit() or len(tel_limpio) < 7:
            raise DatosInvalidosError("El teléfono debe contener solo números y mínimo 7 dígitos.")
        self._telefono = tel_limpio

    def obtener_resumen(self) -> str:
        return f"Cliente {self.id}: {self.nombre} | Correo: {self.correo} | Tel: {self.telefono}"