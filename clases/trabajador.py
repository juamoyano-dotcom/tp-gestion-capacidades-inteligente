from .credencial import Credencial 
from datetime import date

class Trabajador:

    def __init__(self, id_trabajador: int, nombre: str, apellido: str, fecha_nacimiento: date, max_horas_semanales: float):

        if max_horas_semanales <= 0:
            raise ValueError("El máximo de horas semanales debe ser mayor a cero.")

        self.id_trabajador = id_trabajador
        self.nombre = nombre
        self.apellido = apellido
        self.fecha_nacimiento = fecha_nacimiento
        self.max_horas_semanales = max_horas_semanales
        self.horas_trabajadas = 0.0
        self.habilidades = []       #tambien se entiende como 'competencias' --> es una lista str
        self.credenciales = []      #lista de objetos de la clase Credencial

    def agregar_credencial(self, credencial: Credencial): #relacion composicion --> cuando se crea la 
        self.credenciales.append(credencial)

    def agregar_habilidades(self, habilidad: str): #por ahora lo consideramos una lista de aptitudes, ingresadas por el trabajador (ej.linkedin - aptitudes)
        if habilidad not in self.habilidades:
            self.habilidades.append(habilidad)

    def tiene_credencial_activa(self, nombre_credencial: str, fecha: date):
    
        for credencial in self.credenciales:
            if credencial.nombre == nombre_credencial: #credencial es un elemento de una lista, que a su vez es un objeto de la clase credenciales
                if credencial.esta_activa(fecha):
                    return True
        return False

    def tiene_habilidades(self, habilidades_requeridas: list):
        for habilidad in habilidades_requeridas:
            if habilidad not in self.habilidades:
                return False

        return True

    def credenciales_activas(self, credenciales_requeridas: list, fecha: date):
            
        for nombre in credenciales_requeridas:
            if not self.tiene_credencial_activa(nombre, fecha):
                return False
        return True
    
    def agregar_horas(self, horas:float): #idea: el main una vez que se llama al metodo aprobar de la clase asignacion, y si es true consecuentemente se llama a este metodo para agregar hs
        self.horas_trabajadas +=horas   

    def resetear_horas_semanales(self):
        self.horas_trabajadas = 0.0 

    def excede_horas(self, horas:float): #horas proviene de asignacion (atributo del objeto)

        total_horas = self.horas_trabajadas + horas
        if total_horas > self.max_horas_semanales:
            return True

        return False

