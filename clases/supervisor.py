from .trabajador import Trabajador
from .asignacion import Asignacion, EstadoAsignacion


class Supervisor(Trabajador):
    """Trabajador con la facultad de formalizar asignaciones (regla 8).

    Hereda de Trabajador porque también puede realizar labores como cualquier otro.
    """

    def formalizar_asignacion(self, asignacion: Asignacion) -> Asignacion:
        """Pasa la asignación de Pendiente a Aprobada y la devuelve."""
        if asignacion.estado is not EstadoAsignacion.PENDIENTE:
            raise ValueError(f"No se puede formalizar una asignación en estado '{asignacion.estado.value}' (sólo se formalizan asignaciones 'Pendiente').")

        asignacion.aprobar(self) #se pone el self porque aprobar requiere saber si el que llama al metodo es un supervisor
        return asignacion

    def __repr__(self) -> str:
        return f"Supervisor({self.id_trabajador}, {self.nombre} {self.apellido})"