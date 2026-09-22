from .trabajador import Trabajador
from .asignacion import Asignacion


class Supervisor(Trabajador):

    def formalizar_asignacion(self, asignacion: Asignacion):
    
        if asignacion.estado != "Pendiente":
            raise ValueError(f"No se puede formalizar una asignación en estado '{asignacion.estado}' (sólo se formalizan asignaciones 'Pendiente').")

        asignacion.aprobar()
        return asignacion

    def __repr__(self):
        return f"Supervisor({self.id_trabajador}, {self.nombre} {self.apellido})"