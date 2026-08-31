from datetime import date
from .asignacion import Asignacion


class SistemaGestion:
    def __init__(self):
        self.trabajadores = []
        self.labores = []
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
        # Todo lo siguiente que esta comentado es simplemente una idea en la que estuvimos trabajando pero que no logramos definir.
        # Queda comentado para no borrarlo.
        # La idea de este metodo es que agregue a la lista de 'asignaciones pendientes' a un trabajador, comprobando que sea posible, para que luego el supervisor
        # decida si asignarlo o no.

        # Regla 7: Exclusividad de la labor para esa fecha y franja
        # for asig in self.asignaciones:
        #      if asig.labor.id == labor.id and asig.fecha == fecha and asig.franja_horaria.id == franja.id:
        #         raise ValueError("La labor ya tiene una asignación comprometida para esta fecha y franja horaria.")

        # # Regla 4: Aptitud del trabajador para la labor
        # if not labor.trabajador_es_apto(trabajador, fecha):
        #     raise ValueError("El trabajador no cumple con las habilidades y credenciales activas requeridas por la labor.")

        # # Regla 10: Credenciales obligatorias del área de trabajo
        # if not labor.area.trabajador_cumple_credenciales(trabajador, fecha):
        #     raise ValueError("El trabajador no posee las credenciales obligatorias activas para esta área de trabajo.")

        # # Regla 5: Respeto por la carga horaria máxima semanal
        # if trabajador.excede_horas(labor.duracion_horas):
        #     raise ValueError("La asignación excede el límite máximo de horas semanales del trabajador.")

        # # Regla 6: Límite de personal por franja horaria y área
        # asignaciones_franja_area = [
        #     a for a in self.asignaciones
        #     if a.fecha == fecha 
        #     and a.labor.area.id == labor.area.id 
        #     and a.franja_horaria.id == franja.id
        # ]
        # capacidad = self._obtener_capacidad_franja(labor.area, franja)
        # if capacidad is not None and not capacidad.tiene_capacidad(asignaciones_franja_area):
        #     raise ValueError("La franja horaria en el área de trabajo seleccionada está completa.")

        # # Crear asignación en estado inicial 'Pendiente'
        # id_asignacion = f"ASIG-{len(self.asignaciones) + 1:04d}"
        # nueva_asignacion = Asignacion(
        #     id_asig=id_asignacion,
        #     trabajador=trabajador,
        #     labor=labor,
        #     fecha=fecha,
        #     estado="Pendiente",
        #     franja_horaria=franja
        # )

        # # Regla 9: Sumar horas asignadas al trabajador
        # trabajador.agregar_horas(labor.duracion_horas)
        # self.asignaciones.append(nueva_asignacion)
        # return nueva_asignacion
        pass

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