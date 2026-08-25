
from datetime import date

class Credencial:
    def __init__(self, nombre: str, fecha_obtencion: date, fecha_expiracion: date):
        self.nombre = nombre
        self.fecha_obtencion = fecha_obtencion
        self.fecha_expiracion = fecha_expiracion

    def esta_activa(self, fecha_consulta: date):
        return self.fecha_obtencion <= fecha_consulta <= self.fecha_expiracion
