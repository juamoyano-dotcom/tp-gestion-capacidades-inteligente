from datetime import date
from typing import List
from trabajador import Trabajador

class SectorTrabajo:
    def __init__(self, id_sector: int, nombre: str, credenciales_obligatorias: List[str] = None, limite_personal: int = 0):
        self.id = id_sector
        self.nombre = nombre
        self.credenciales_obligatorias = credenciales_obligatorias if credenciales_obligatorias is not None else []
        self.limite_personal = limite_personal

    def trabajador_cumple_credenciales(self, trab, fecha: date) -> bool:
        """
        Verifica si el trabajador posee todas las credenciales obligatorias 
        del sector activas a la fecha indicada.
        """
        # Si el área no exige credenciales, cumple automáticamente
        if not self.credenciales_obligatorias:
            return True
        
        # Se apoya en el método 'credenciales_activas' de la clase Trabajador
        return trab.credenciales_activas(self.credenciales_obligatorias, fecha)