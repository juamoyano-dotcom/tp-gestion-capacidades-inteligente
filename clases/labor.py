from datetime import date
from .trabajador import Trabajador
from .sectortrabajo import SectorTrabajo


class Labor:

    def __init__(self, id_labor: int, titulo: str, descripcion: str, duracion_horas: float, habilidades_requeridas: list, credenciales_requeridas: list, sector: SectorTrabajo):

        if duracion_horas <= 0:
            raise ValueError("La duración de la labor debe ser mayor a cero.")

        self.id_labor = id_labor
        self.titulo = titulo
        self.descripcion = descripcion
        self.duracion_horas = duracion_horas
        self.habilidades_requeridas = habilidades_requeridas or []
        self.credenciales_requeridas = credenciales_requeridas or []
        self.sector = sector

    def trabajador_es_apto(self, trab: Trabajador, fecha: date):
       
        return (
            trab.tiene_habilidades(self.habilidades_requeridas)
            and trab.credenciales_activas(self.credenciales_requeridas, fecha)
        )

    def __repr__(self):
        return f"Labor({self.id_labor}, {self.titulo})"