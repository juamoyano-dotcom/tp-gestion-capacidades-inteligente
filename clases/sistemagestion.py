from datetime import date
from .asignacion import Asignacion
from .trabajador import Trabajador
from .labor import Labor
from .sectortrabajo import SectorTrabajo
from .franjahoraria import FranjaHoraria

class SistemaGestion:
    def __init__(self):
        self.trabajadores = []
        self.labores = [] # tiene que tener historial o se va borrando?
        self.areas = []
        self.asignaciones = []
        self.capacidades_franja = []  # Instancias de CapacidadFranjaArea

    def registrar_trabajador(self, trabajador):
        self.trabajadores.append(trabajador)

    def registrar_labor(self, labor):
        self.labores.append(labor)

    def registrar_area(self, area):
        self.areas.append(area)

    def registrar_capacidad_franja(self, capacidad_franja):
        self.capacidades_franja.append(capacidad_franja)

    def proponer_asignacion(self, trabajador, labor, franja, fecha):
        # Validación básica de existencia
        if trabajador is None:
            raise ValueError("Debe indicarse un trabajador.")
        if labor is None:
            raise ValueError("Debe indicarse una labor.")
        if franja is None:
            raise ValueError("Debe indicarse una franja horaria.")

        # Regla 7: exclusividad de asignación
        for asig in self.asignaciones:
            if (
                asig.labor.id_labor == labor.id_labor
                and asig.fecha == fecha
                and asig.franja == franja
            ):
                raise ValueError(
                    "La labor ya tiene una asignación comprometida para esta fecha y franja horaria."
                )

        # Regla 4: aptitud del trabajador para la labor
        if not labor.trabajador_es_apto(trabajador, fecha):
            raise ValueError(
                "El trabajador no cumple con las habilidades y credenciales activas requeridas por la labor."
            )

        # Regla 10: credenciales obligatorias del área
        if not labor.sector.trabajador_cumple_credenciales(trabajador, fecha):
            raise ValueError(
                "El trabajador no posee las credenciales obligatorias activas para esta área de trabajo."
            )

        # Regla 5: carga horaria semanal máxima
        if trabajador.excede_horas(labor.duracion_horas):
            raise ValueError(
                "La asignación excede el límite máximo de horas semanales del trabajador."
            )

        # Regla 6: capacidad por franja horaria y área
        ocupacion_actual = 0
        for asig in self.asignaciones:
            if (
                asig.fecha == fecha
                and asig.labor.sector.id == labor.sector.id
                and asig.franja == franja
            ):
                ocupacion_actual += 1

        capacidad = None
        for cap in self.capacidades_franja:
            if cap.area.id == labor.sector.id and cap.franja == franja:
                capacidad = cap
                break

        if capacidad is not None and not capacidad.tiene_capacidad(ocupacion_actual):
            raise ValueError("La franja horaria en el área de trabajo seleccionada está completa.")

        # Regla 9: suma horas propuestas
        # Crear la asignación pendiente
        nueva_asignacion = Asignacion(
            id_asignacion=len(self.asignaciones) + 1,
            trabajador=trabajador,
            labor=labor,
            franja=franja,
            fecha=fecha
        )

        trabajador.agregar_horas(labor.duracion_horas)
        self.asignaciones.append(nueva_asignacion)
        return nueva_asignacion

    def buscar_disponibles(self, labor, franja, fecha):
        # #  Identifica que trabajadores cumplen con todos los requisitos para ser asignados.
        # # Verificar primero si el área/franja aún tiene cupo de personal (Regla 6)
        # asignaciones_franja_area = [
        #     a for a in self.asignaciones
        #     if a.fecha == fecha 
        #     and a.labor.area.id == labor.area.id 
        #     and a.franja_horaria.id == franja.id
        # ]
        # capacidad = self._obtener_capacidad_franja(labor.area, franja)
        # if capacidad is not None and not capacidad.tiene_capacidad(asignaciones_franja_area):
        #     return []

        # Regla 11: Filtrar trabajadores aptos
        # disponibles = []
        # for trab in self.trabajadores:
        #     if (labor.trabajador_es_apto(trab, fecha) and
        #         labor.area.trabajador_cumple_credenciales(trab, fecha) and
        #         not trab.excede_horas(labor.duracion_horas)):
        #         disponibles.append(trab)

        # return disponibles
        pass

    # def _obtener_capacidad_franja(self, area, franja):
        # # Calcula la capacidad del sector de trabajo segun la franja horaria. Existe la posibilidad de que se elimine.
        # for cap in self.capacidades_franja:
        #     if cap.area.id == area.id and cap.franja.id == franja.id:
        #         return cap
        # return None