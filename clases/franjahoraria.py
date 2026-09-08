from datetime import time
from enum import Enum


class Franja(Enum):
    # El dominio está definido directamente en el Enum; Python se encarga
    # de validarlo (no se puede construir un id_franja que no sea 1, 2 o 3).
    MAÑANA = (1, "Mañana")
    TARDE = (2, "Tarde")
    NOCHE = (3, "Noche")

    def __init__(self, id_franja, descripcion):
        self.id_franja = id_franja
        self.descripcion = descripcion


class FranjaHoraria:
    def __init__(self, franja: Franja, hora_inicio: time, hora_fin: time):
        self.franja = franja
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin

        # Si llamás a este método, cuando creás el objeto se verifica
        # automáticamente la hora.
        self.validar_hora()

    def validar_hora(self):
        if self.hora_inicio == self.hora_fin:
            raise ValueError("La hora de inicio debe ser distinta a la hora de fin.")

    def __eq__(self, other):
        return isinstance(other, FranjaHoraria) and self.franja == other.franja

    def __hash__(self):
        return hash(self.franja)

    def __repr__(self):
        return f"FranjaHoraria({self.franja.descripcion})"