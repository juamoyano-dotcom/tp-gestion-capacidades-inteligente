from datetime import time

class franjahoraria:

    FRANJAS_VALIDAS = {
        1: "Mañana",
        2: "Tarde",
        3: "Noche"
    }

    def __init__(self, id_franja: int, descripcion:str, hora_inicio: time, hora_fin: time):
        self.id_franja = id_franja
        self.descripcion = descripcion
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin 

    def validar_hora(self):
        if self.hora_inicio == self.hora_fin:
            raise ValueError("La hora de inicio debe ser distinta a la hora de fin.")

    def validar_franja(self):
        if self.id_franja not in self.FRANJAS_VALIDAS:
            raise ValueError("El id de la franja horaria debe ser 1, 2 o 3.")
        if self.FRANJAS_VALIDAS[self.id_franja] != self.descripcion:
            raise ValueError(f"Para el id {self.id_franja}, la descripción debe ser '{self.FRANJAS_VALIDAS[self.id_franja]}'.")

        
    
        