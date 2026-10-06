from datetime import date
from enum import Enum
from .trabajador import Trabajador
from .franjahoraria import FranjaHoraria


class EstadoAsignacion(Enum):
    PENDIENTE = "Pendiente"
    APROBADA = "Aprobada"


class Asignacion:
    def __init__(self, id_asignacion: int, trabajador: Trabajador, labor, franja: FranjaHoraria, fecha: date):
        self.id_asignacion = id_asignacion
        self.trabajador = trabajador
        self.labor = labor
        self.franja = franja
        self.fecha = fecha
        self.estado = EstadoAsignacion.PENDIENTE
        self.horas_asignadas = labor.duracion_horas


    def aprobar(self, supervisor) -> None:
        from .supervisor import Supervisor
        # Import dentro del método para evitar el import circular entre supervisor y asignacion.

        if not isinstance(supervisor, Supervisor) :
            raise ValueError("Solo un Supervisor puede aprobar una asignación.")

        if self.estado != EstadoAsignacion.PENDIENTE:
            raise ValueError(
                f"No se puede aprobar una asignación en estado '{self.estado.value}'."
            )

        self.estado = EstadoAsignacion.APROBADA
        self.trabajador.agregar_asignacion(self)        

    def __repr__(self) -> str:
        return (f"Asignacion({self.id_asignacion}, {self.trabajador.nombre} -> "
                f"{self.labor.titulo}, {self.fecha}, {self.franja.franja.descripcion}, {self.estado.value})")