from trabajador import Trabajador
from asignacion import Asignacion


class Supervisor(Trabajador):
    #hereda todos los atributos y métodos de Trabajador (id, nombre, habilidades,
    #credenciales, horas trabajadas, etc.) -- un supervisor puede hacer labores
    #como cualquier otro trabajador, por eso no le agregamos atributos propios

    def formalizar_asignacion(self, asignacion: Asignacion):
        #Regla 8: solo se puede formalizar una asignación que esté 'Pendiente'
        if asignacion.estado != "Pendiente":
            raise ValueError(f"No se puede formalizar una asignación en estado '{asignacion.estado}' (sólo se formalizan asignaciones 'Pendiente').")

        asignacion.aprobar()
        return asignacion
