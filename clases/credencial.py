from datetime import date

class Credencial:
    """Credencial profesional con nombre y período de vigencia.

    Permite saber si está activa o vencida en una fecha dada."""
    def __init__(self, nombre: str, fecha_obtencion: date, fecha_expiracion: date):

        if fecha_obtencion > fecha_expiracion:
            raise ValueError("La fecha de obtención no puede ser posterior a la fecha de expiración.")
            #Agrego esto del issue4, para que no se acepten fechas invertidas. 

        self.nombre = nombre
        self.fecha_obtencion = fecha_obtencion
        self.fecha_expiracion = fecha_expiracion

    def esta_activa(self, fecha_consulta: date) -> bool:
        """Indica si la credencial está vigente en `fecha_consulta` (límites inclusivos).

        Recibe la fecha por parámetro, en vez de usar date.today(), para poder
        validar asignaciones a futuro y para que los tests sean deterministas.
        """
        return self.fecha_obtencion <= fecha_consulta <= self.fecha_expiracion #idea en vez de usar fecha_consulta --> date.today()

    def __repr__(self) ->str:
        return f"Credencial({self.nombre}, obtenida={self.fecha_obtencion}, vence={self.fecha_expiracion})"      