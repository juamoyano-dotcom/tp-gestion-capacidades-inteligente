from datetime import date
from .trabajador import Trabajador
from .sectortrabajo import SectorTrabajo
from enum import Enum

class Frecuencia(Enum):
    DIARIA = "Diaria"
    SEMANAL = "Semanal"

class Labor:

    def __init__(self, id_labor: int, titulo: str, descripcion: str, duracion_horas: float, habilidades_requeridas: list, credenciales_requeridas: list, sector: SectorTrabajo, frecuencia: Frecuencia= Frecuencia.DIARIA, trabajadores_requeridos: int = 1):

        if duracion_horas <= 0:
            raise ValueError("La duración de la labor debe ser mayor a cero.")

        self.id_labor = id_labor
        self.titulo = titulo
        self.descripcion = descripcion
        self.duracion_horas = duracion_horas
        self.habilidades_requeridas = habilidades_requeridas or []
        self.credenciales_requeridas = credenciales_requeridas or []
        self.sector = sector
        self.frecuencia=frecuencia
        self.trabajadores_requeridos = trabajadores_requeridos

    def trabajador_es_apto(self, trab: Trabajador, fecha: date) -> bool:
       """Regla 4: el trabajador tiene todas las habilidades y credenciales activas (en `fecha`) que exige la labor.

        No verifica las credenciales del sector ni las horas disponibles:
        eso lo evalúa SistemaGestion.motivo_no_apto.
        """
       return (
            trab.tiene_habilidades(self.habilidades_requeridas)
            and trab.credenciales_activas(self.credenciales_requeridas, fecha)
        )

    def __repr__(self) -> str:
        return f"Labor({self.id_labor}, {self.titulo})"