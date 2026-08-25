from credencial import Credencial 
from datetime import date

class Trabajador:

    def __init__(self, id_trabajador: int, nombre: str,apellido: str, fecha_nacimiento:date,max_horas_semanales: float):
        self.id_trabajador = id_trabajador
        self.nombre = nombre
        self.apellido=apellido
        self.fecha_nacimiento=fecha_nacimiento
        self.max_horas_semanales = max_horas_semanales
        self.horas_trabajadas = 0.0
        self.habilidades = [] #tambien se entiende como 'competencias' --> es una lista str
        self.credenciales = [] #lista de objetos de la clase Credencial

    def agregar_credencial(self, credencial: Credencial): #relacion composicion --> cuando se crea la 
        self.credenciales.append(credencial)


    def agregar_habilidades(self, habilidad: str): #por ahora lo consideramos una lista de aptitudes, ingresadas por el trabajador (ej.linkedin - aptitudes)
        self.habilidades.append(habilidad)

    def tiene_credencial_activa(self, nombre_credencial: str, fecha: date):
        pass

    def agregar_horas(self, horas:float): #idea: el main una vez que se llama al metodo aprobar de la clase asignacion, y si es true consecuentemente se llama a este metodo para agregar hs
        self.horas_trabajadas +=horas   

    def resetear_horas_semanales():
        pass 

    def excede_horas(self, horas:float): #horas proviene de asignacion (atributo del objeto)
        if(self.horas_trabajadas+horas)>self.max_horas_semanales:
            return True 


    from datetime import date
from credencial import Credencial


class Trabajador:
    def __init__(self, id_trabajador: int, nombre: str, apellido: str,
                 fecha_nacimiento: date, max_horas_semanales: float):
        self.id_trabajador = id_trabajador
        self.nombre = nombre
        self.apellido = apellido
        self.fecha_nacimiento = fecha_nacimiento
        self.max_horas_semanales = max_horas_semanales
        self.horas_trabajadas = 0.0
        self.habilidades = []
        self.credenciales = []

    def agregar_credencial(self, credencial: Credencial):
        self.credenciales.append(credencial)

    def agregar_habilidad(self, habilidad: str):
        self.habilidades.append(habilidad)

    def tiene_habilidades(self, habilidades_requeridas: list):
        # recorrer habilidades_requeridas y devolver False si alguna no está en self.habilidades
        pass

    def tiene_credencial_activa(self, nombre_credencial: str, fecha: date):
        # recorrer self.credenciales buscando una con ese nombre y que credencial.esta_activa(fecha) sea True
        pass

    def credenciales_activas(self, credenciales_requeridas: list, fecha: date):
        # para cada nombre en credenciales_requeridas, usar tiene_credencial_activa(nombre, fecha); si alguno da False, devolver False
        pass

    def agregar_horas(self, horas: float):
        self.horas_trabajadas += horas

    def resetear_horas_semanales(self):
        # reestablecer self.horas_trabajadas a 0
        pass

    def excede_horas(self, horas: float):
        if (self.horas_trabajadas + horas) > self.max_horas_semanales:
            return True
        return False
        #agregar  raise_error 
        