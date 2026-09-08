from .sectortrabajo import SectorTrabajo
from .franjahoraria import FranjaHoraria
 
 
class CapacidadFranjaArea:
    """
    Regla 6: límite de personal para una combinación (área, franja horaria).
    SistemaGestion mantiene una lista de estas y calcula la ocupación real
    contando asignaciones existentes para esa área+franja+fecha.
    """
 
    def __init__(self, area: SectorTrabajo, franja: FranjaHoraria, limite_personal: int):
        if limite_personal <= 0:
            raise ValueError("El límite de personal por franja debe ser mayor a cero.")
 
        self.area = area
        self.franja = franja
        self.limite_personal = limite_personal
 
    def tiene_capacidad(self, ocupacion_actual: int):  # ocupación actual se calcula en SistemaGestion
        return ocupacion_actual < self.limite_personal
 
    def __repr__(self):
        return f"CapacidadFranjaArea({self.area.nombre}/{self.franja}, max={self.limite_personal})"