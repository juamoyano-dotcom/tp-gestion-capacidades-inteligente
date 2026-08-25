from credencial import Credencial 
from datetime import date

class Trabajador:

    def _init_(self, id_trabajador: int, nombre: str,apellido: str, fecha_nacimiento:date,max_horas_semanales: float):
        self.id_trabajador = id_trabajador
        self.nombre = nombre
        self.apellido=apellido
        self.fecha_nacimiento=fecha_nacimiento
        self.max_horas_semanales = max_horas_semanales
        self.horas_asignadas = 0.0
        self.habilidades = [] #tambien se entiende como 'competencias' --> es una lista str
        self.credenciales = [] #lista de objetos de la clase Credencial

    def agregar_credencial(self, credencial: Credencial): #relacion composicion --> cuando se crea la 
        self.credenciales.append(credencial)


    def agregar_habilidades(self, habilidad: str): #por ahora lo consideramos una lista de aptitudes, ingresadas por el trabajador (ej.linkedin - aptitudes)
        self.habilidades.append(habilidad)

    def tiene_credencial_activa(self, nombre_credencial: str, fecha: date) -> bool:
       
        pass

    

    