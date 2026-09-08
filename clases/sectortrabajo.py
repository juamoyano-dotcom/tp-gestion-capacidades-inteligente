from datetime import date
from typing import List
from .trabajador import Trabajador


class SectorTrabajo:
    """
    Área de trabajo (Regla 10).

    El límite de personal (Regla 6) NO vive acá: depende de la combinación
    área + franja horaria (ej: Sala de Servidores puede admitir 5 personas
    a la mañana y solo 2 de noche), y ese dato es responsabilidad exclusiva
    de CapacidadFranjaArea. Tenerlo acá también sería el mismo dato en dos
    lugares, con riesgo de que se desincronicen.
    """

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