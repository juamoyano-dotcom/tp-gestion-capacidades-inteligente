from datetime import date
from typing import List
from trabajador import Trabajador

class SectorTrabajo:
    def __init__(self, id_sector: int, nombre: str, credenciales_obligatorias: List[str] = None, limite_personal: int = 0):

        if limite_personal <  0:
            raise ValueError("El límite de personal no puede ser negativo.")
    
        self.id = id_sector
        self.nombre = nombre
        self.credenciales_obligatorias = credenciales_obligatorias if credenciales_obligatorias is not None else []
        self.limite_personal = limite_personal

    def trabajador_cumple_credenciales(self, trab: Trabajador, fecha: date):

        if not self.credenciales_obligatorias:
            return True

        credenciales_activas_trabajador = [
            c.nombre for c in trab.credenciales if c.esta_activa(fecha)
        ]

        for obligatoria in self.credenciales_obligatorias:
            if obligatoria not in credenciales_activas_trabajador:
                return False  

        return True  