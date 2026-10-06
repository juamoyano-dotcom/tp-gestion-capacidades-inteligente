from datetime import date
from typing import List
from .trabajador import Trabajador


class SectorTrabajo:
    """Área de trabajo de la planta.

    Conoce las credenciales que se exigen a cualquier trabajador que realice
    una labor en ella. El límite de personal por franja NO vive acá sino en
    CapacidadFranjaArea: ese límite depende de la combinación área + franja
    (no del área sola), y tenerlo también en el sector sería el mismo dato en
    dos lugares, con riesgo de que se desincronicen.
    """

    def __init__(self, id_sector: int, nombre: str, credenciales_obligatorias: List[str] = None) -> None:
        self.id = id_sector
        self.nombre = nombre
        self.credenciales_obligatorias = credenciales_obligatorias if credenciales_obligatorias is not None else []

    def trabajador_cumple_credenciales(self, trab: Trabajador, fecha: date) -> bool:
        """Indica si el trabajador tiene activas en `fecha` todas las credenciales del área.

        Delega en Trabajador.credenciales_activas (encapsulamiento): el sector
        no necesita conocer cómo se guardan las credenciales.
        """
        # verifica directo con el método de Trabajador --> encapsulamiento
        return trab.credenciales_activas(self.credenciales_obligatorias, fecha)

    def __repr__(self) -> str:
        return f"SectorTrabajo({self.nombre})"