from datetime import date
from enum import Enum
from .trabajador import Trabajador
from .franjahoraria import FranjaHoraria


class EstadoAsignacion(Enum):
    PENDIENTE = "Pendiente"
    APROBADA = "Aprobada"
    RECHAZADA = "Rechazada"

class Asignacion:
    """Asignación de un trabajador a una labor en una fecha y franja horaria.

    Se crea en estado Pendiente. Guarda las horas de la labor al momento de
    crearse, que SistemaGestion suma a la carga semanal del trabajador (regla 9).
    """
    def __init__(self, id_asignacion: int, trabajador: Trabajador, labor, franja: FranjaHoraria, fecha: date):
        self.id_asignacion = id_asignacion
        self.trabajador = trabajador
        self.labor = labor
        self.franja = franja
        self.fecha = fecha
        self.estado = EstadoAsignacion.PENDIENTE
        self.horas_asignadas = labor.duracion_horas
        self.motivo_rechazo = None


    def aprobar(self, supervisor) -> None:
        from .supervisor import Supervisor
        """Pasa la asignación de Pendiente a Aprobada y la registra en el trabajador.

        Lanza ValueError si quien aprueba no es un Supervisor o si la
        asignación no está Pendiente.
        """
        # Import dentro del método para evitar el import circular entre supervisor y asignacion.

        if not isinstance(supervisor, Supervisor) :
            raise ValueError("Solo un Supervisor puede aprobar una asignación.")

        if self.estado != EstadoAsignacion.PENDIENTE:
            raise ValueError(
                f"No se puede aprobar una asignación en estado '{self.estado.value}'."
            )

        self.estado = EstadoAsignacion.APROBADA
        self.trabajador.agregar_asignacion(self) 

    def rechazar(self, supervisor, motivo=""):
        from .supervisor import Supervisor

        if not isinstance(supervisor, Supervisor):
            raise ValueError("Solo un Supervisor puede rechazar una asignación.")

        if self.estado != EstadoAsignacion.PENDIENTE:
            raise ValueError(
                f"No se puede rechazar una asignación en estado '{self.estado.value}'."
            )

        self.estado = EstadoAsignacion.RECHAZADA
        self.motivo_rechazo = motivo       

    def __repr__(self) -> str:
        return (f"Asignacion({self.id_asignacion}, {self.trabajador.nombre} -> "
                f"{self.labor.titulo}, {self.fecha}, {self.franja.franja.descripcion}, {self.estado.value})")