from datetime import date
from typing import List
from .trabajador import Trabajador

class SectorTrabajo:

    def __init__(self, id_sector: int, nombre: str, credenciales_obligatorias: List[str] = None, limite_personal: int = 0):

        if limite_personal <  0:
            raise ValueError("El límite de personal no puede ser negativo.")
    
        self.id = id_sector
        self.nombre = nombre
        self.credenciales_obligatorias = credenciales_obligatorias if credenciales_obligatorias is not None else []
        self.limite_personal = limite_personal

    def trabajador_cumple_credenciales(self, trab: Trabajador, fecha: date):

        return trab.credenciales_activas(self.credenciales_obligatorias, fecha) #verifica directo con el metodo de trabajador --> encapsulamiento