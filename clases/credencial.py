from datetime import date

class Credencial:
    def __init__(self, nombre: str, fecha_obtencion: date, fecha_expiracion: date):

        if fecha_obtencion > fecha_expiracion:
            raise ValueError("La fecha de obtención no puede ser posterior a la fecha de expiración.")
            #Agrego esto del issue4, para que no se acepten fechas invertidas. 

        self.nombre = nombre
        self.fecha_obtencion = fecha_obtencion
        self.fecha_expiracion = fecha_expiracion

    def esta_activa(self, fecha_consulta: date):
        return self.fecha_obtencion <= fecha_consulta <= self.fecha_expiracion
    