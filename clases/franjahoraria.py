from datetime import time
from enum import Enum


class Franja(Enum):
    
    MAÑANA = (1, "Mañana")
    TARDE = (2, "Tarde")
    NOCHE = (3, "Noche")

    def __init__(self, id_franja, descripcion):
        self.id_franja = id_franja
        self.descripcion = descripcion


class FranjaHoraria:
    """Franja de la jornada con su horario de inicio y fin.

    Dos FranjaHoraria se consideran iguales si tienen la misma `Franja`, sin
    importar el horario. Así se pueden usar como clave de diccionario o en
    comparaciones sin depender de la identidad del objeto.
    """
    def __init__(self, franja: Franja, hora_inicio: time, hora_fin: time):
        self.franja = franja
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin

        self.validar_hora()

    def validar_hora(self):
        if self.hora_inicio == self.hora_fin:
            raise ValueError("La hora de inicio debe ser distinta a la hora de fin.")

    def __eq__(self, other) -> bool:
        return isinstance(other, FranjaHoraria) and self.franja == other.franja

    def __hash__(self) -> int:
        return hash(self.franja)

    def __repr__(self) -> str:
        return f"FranjaHoraria({self.franja.descripcion})"