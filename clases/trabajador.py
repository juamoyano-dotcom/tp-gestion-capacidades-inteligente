from .credencial import Credencial 
from datetime import date

class Trabajador:
    """Miembro del personal técnico.

    Guarda sus datos personales, habilidades, credenciales profesionales, el
    máximo de horas semanales de su contrato y las asignaciones aprobadas.
    Las horas ya comprometidas no se guardan acá: las calcula SistemaGestion.
    """
    def __init__(self, id_trabajador: int, nombre: str, apellido: str, fecha_nacimiento: date, max_horas_semanales: float, **atributos):
        """Crea el trabajador sin habilidades, credenciales ni asignaciones.

        Los `**atributos` extra se guardan como atributos adicionales (ver
        `agregar_atributo`). """
        if max_horas_semanales <= 0:
            raise ValueError("El máximo de horas semanales debe ser mayor a cero.")

        self.id_trabajador = id_trabajador
        self.nombre = nombre
        self.apellido = apellido
        self.fecha_nacimiento = fecha_nacimiento
        self.max_horas_semanales = max_horas_semanales
        self.habilidades = []       #tambien se entiende como 'competencias' --> es una lista str
        self.credenciales = []      #lista de objetos de la clase Credencial
        self.asignaciones = []

        self._atributos = {} #_atributos representa un atributo interno de la clase (no encapsulamiento fuerte)
        #intención: el acceso y modificación de los atributos adicionales se haga mediante obtener_atributo() y agregar_atributo()
        for clave, valor in atributos.items():
            self.agregar_atributo(clave, valor)  
        
    def agregar_credencial(self, credencial: Credencial):
        self.credenciales.append(credencial)

    def obtener_atributo(self, clave, default=None) :
        return self._atributos.get(clave, default)

    def agregar_atributo(self, clave, valor, sobrescribir=True):
        if hasattr(self, clave):
            raise ValueError(
                f"'{clave}' ya es un atributo o método de Trabajador, "
                "no un atributo adicional."
            )

        if not sobrescribir and clave in self._atributos:
            raise ValueError(f"El atributo '{clave}' ya existe.")

        self._atributos[clave] = valor

    def agregar_habilidades (self, habilidad: str): #por ahora lo consideramos una lista de aptitudes, ingresadas por el trabajador (ej.linkedin - aptitudes)
        if habilidad not in self.habilidades:
            self.habilidades.append(habilidad)

    def agregar_asignacion(self, asignacion): #asignacion es un objeto de la clase Asignacion --> no pongo el tipo de dato porque sino hay un ciclo infinito de imports
        if asignacion not in self.asignaciones:
            self.asignaciones.append(asignacion)

    def setter_max_horas_semanales(self, max_horas_semanales: float):
        if max_horas_semanales <= 0:
            raise ValueError("El máximo de horas semanales debe ser mayor a cero.")
        self.max_horas_semanales = max_horas_semanales

    def tiene_credencial_activa(self, nombre_credencial: str, fecha: date) -> bool:
    
        for credencial in self.credenciales:
            if credencial.nombre == nombre_credencial: #credencial es un elemento de una lista, que a su vez es un objeto de la clase credenciales
                if credencial.esta_activa(fecha):
                    return True
        return False

    def tiene_habilidades(self, habilidades_requeridas: list) -> bool:
        for habilidad in habilidades_requeridas:
            if habilidad not in self.habilidades:
                return False

        return True

    def credenciales_activas(self, credenciales_requeridas: list, fecha: date) -> bool:
            
        for nombre in credenciales_requeridas:
            if not self.tiene_credencial_activa(nombre, fecha):
                return False
        return True
    
    def __repr__(self) -> str:
        return f"Trabajador ({self.id_trabajador}, {self.nombre} {self.apellido})"
