from datetime import time
from enum import Enum


class Franja(Enum): 
#el dominio esta definido directamente, python se encarga de validarlo

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

        #si llamas a este metodo, cuando creas el objeto se verifica automaticamente la hora 
        self.validar_hora()


    def validar_hora(self): 
        if self.hora_inicio == self.hora_fin: 
            raise ValueError( "La hora de inicio debe ser distinta a la hora de fin." )



