from .sectortrabajo import SectorTrabajo
from .franjahoraria import FranjaHoraria
 
class CapacidadFranjaArea:
    
    def __init__(self, area: SectorTrabajo, franja: FranjaHoraria, limite_personal: int) -> None:
        if limite_personal <= 0:
            raise ValueError("El límite de personal por franja debe ser mayor a cero.")
 
        self.area = area
        self.franja = franja
        self.limite_personal = limite_personal
 
    def tiene_capacidad(self, ocupacion_actual: int) -> bool:  # ocupación actual se calcula en SistemaGestion
        return ocupacion_actual < self.limite_personal
 
    def __repr__(self) -> str:
        return f"CapacidadFranjaArea({self.area.nombre}/{self.franja}, max={self.limite_personal})"