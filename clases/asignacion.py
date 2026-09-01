from datetime import date
from .trabajador import Trabajador
from .franjahoraria import FranjaHoraria


class Asignacion:
    def __init__(self, id_asignacion: int, trabajador: Trabajador, labor, franja: FranjaHoraria, fecha: date):
        self.id_asignacion = id_asignacion
        self.trabajador = trabajador
        self.labor = labor
        self.franja = franja
        self.fecha = fecha
        self.estado = "Pendiente"
        self.horas_asignadas = labor.duracion_horas

    def aprobar(self):
        self.estado = "Aprobada"

    def __repr__(self):
        return (f"Asignacion({self.id_asignacion}, {self.trabajador.nombre} -> "
                f"{self.labor.titulo}, {self.fecha}, {self.franja.descripcion}, {self.estado})")