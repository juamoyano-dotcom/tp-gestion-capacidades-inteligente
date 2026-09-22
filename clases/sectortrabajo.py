from datetime import date
from typing import List
from .trabajador import Trabajador


class SectorTrabajo:

    def __init__(self, id_sector: int, nombre: str,
                 credenciales_obligatorias: List[str] = None):
        self.id = id_sector
        self.nombre = nombre
        self.credenciales_obligatorias = credenciales_obligatorias if credenciales_obligatorias is not None else []

    def trabajador_cumple_credenciales(self, trab: Trabajador, fecha: date):
        # verifica directo con el método de Trabajador --> encapsulamiento
        return trab.credenciales_activas(self.credenciales_obligatorias, fecha)

    def __repr__(self):
        return f"SectorTrabajo({self.nombre})"