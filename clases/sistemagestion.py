from datetime import date, timedelta
from .asignacion import Asignacion
from .trabajador import Trabajador
from .labor import Labor
from .sectortrabajo import SectorTrabajo
from .franjahoraria import FranjaHoraria

class SistemaGestion:
    def __init__(self):
        self.trabajadores = []
        self.labores = []
        self.areas = []
        self.asignaciones = []
        self.capacidades_franja = {}  
        self.semana_actual = None

    def registrar_trabajador(self, trabajador):
        for t in self.trabajadores:
            if t.id_trabajador == trabajador.id_trabajador:
                raise ValueError("Ya existe un trabajador con ese identificador.")
        self.trabajadores.append(trabajador)

    def registrar_labor(self, labor):
        for l in self.labores:
            if l.id_labor == labor.id_labor:
                raise ValueError("Ya existe una labor con ese identificador.")
        self.labores.append(labor)

    def registrar_area(self, area):
        for a in self.areas:
            if a.id == area.id:
                raise ValueError("Ya existe un área con ese identificador.")
        self.areas.append(area)

    def registrar_capacidad_franja(self, capacidad_franja):
        clave = (capacidad_franja.area.id, capacidad_franja.franja.franja)
        if clave in self.capacidades_franja:
            raise ValueError("Ya existe una capacidad para ese área y franja horaria.")
        self.capacidades_franja[clave] = capacidad_franja

    @staticmethod
    def misma_franja(franja_a, franja_b):
        return (
            franja_a is not None
            and franja_b is not None
            and franja_a.franja == franja_b.franja
        )

    def preparar_semana(self, fecha):
        lunes_de_la_semana = fecha - timedelta(days=fecha.weekday())

        if self.semana_actual is None:
            for trabajador in self.trabajadores:
                trabajador.resetear_horas_semanales()

            self.semana_actual = lunes_de_la_semana

        elif lunes_de_la_semana > self.semana_actual:
            for trabajador in self.trabajadores:
                trabajador.resetear_horas_semanales()

            self.semana_actual = lunes_de_la_semana

    def obtener_capacidad_franja(self, area, franja):
        return self.capacidades_franja.get((area.id, franja.franja))

    def validar_parametros_asignacion(self, trabajador, labor, franja, fecha):
        if trabajador is None or labor is None or franja is None:
            raise ValueError("El trabajador, la labor y la franja son obligatorios.")

        if not isinstance(fecha, date):
            raise TypeError("La fecha debe ser una instancia de date.")

        trabajador_registrado = False
        i = 0

        while i < len(self.trabajadores) and not trabajador_registrado:
            if self.trabajadores[i].id_trabajador == trabajador.id_trabajador:
                trabajador_registrado = True
            i += 1

        if not trabajador_registrado:
            raise ValueError("El trabajador no está registrado en el sistema.")

        labor_registrada = False
        i = 0

        while i < len(self.labores) and not labor_registrada:
            if self.labores[i].id_labor == labor.id_labor:
                labor_registrada = True
            i += 1

        if not labor_registrada:
            raise ValueError("La labor no está registrada en el sistema.")

        area_registrada = False
        i = 0

        while i < len(self.areas) and not area_registrada:
            if self.areas[i].id == labor.sector.id:
                area_registrada = True
            i += 1

        if not area_registrada:
            raise ValueError("El área de la labor no está registrada en el sistema.")




    def motivo_no_apto(self, trabajador, labor, fecha):

        if not labor.trabajador_es_apto(trabajador, fecha):
            return "El trabajador no cumple con las habilidades y credenciales activas requeridas por la labor."

        if not labor.sector.trabajador_cumple_credenciales(trabajador, fecha):
            return "El trabajador no posee las credenciales obligatorias activas para esta área de trabajo."

        if trabajador.excede_horas(labor.duracion_horas):
            return "La asignación excede el límite máximo de horas semanales del trabajador."

        return None

    def contar_ocupacion(self, area, franja, fecha):
        ocupacion_actual = 0
        for asig in self.asignaciones:
            if asig.fecha == fecha and asig.labor.sector.id == area.id and self.misma_franja(asig.franja, franja):
                ocupacion_actual += 1
        return ocupacion_actual

    def trabajador_ya_ocupado(self, trabajador, franja, fecha):
        for asig in self.asignaciones:
            if (
                asig.trabajador.id_trabajador == trabajador.id_trabajador
                and asig.fecha == fecha
                and self.misma_franja(asig.franja, franja)
            ):
                return True
        return False

    def labor_ya_asignada(self, labor, franja, fecha):
        for asig in self.asignaciones:
            if (
                asig.labor.id_labor == labor.id_labor
                and asig.fecha == fecha
                and self.misma_franja(asig.franja, franja)
            ):
                return True
        return False


    def proponer_asignacion(self, trabajador, labor, franja, fecha):
        self.validar_parametros_asignacion(trabajador, labor, franja, fecha)
        self.preparar_semana(fecha)

        capacidad = self.obtener_capacidad_franja(labor.sector, franja)
        if capacidad is None:
            raise ValueError("No existe una capacidad configurada para el área y la franja horaria.")

        if self.labor_ya_asignada(labor, franja, fecha):
            raise ValueError("La labor ya tiene una asignación comprometida para esta fecha y franja horaria.")

        if self.trabajador_ya_ocupado(trabajador, franja, fecha):
            raise ValueError("El trabajador ya tiene una asignación para esa fecha y franja horaria.")


        motivo = self.motivo_no_apto(trabajador, labor, fecha)
        if motivo is not None:
            raise ValueError(motivo)

        ocupacion_actual = self.contar_ocupacion(labor.sector, franja, fecha)
        if not capacidad.tiene_capacidad(ocupacion_actual):
            raise ValueError("La franja horaria en el área de trabajo seleccionada está completa.")

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
        if labor is None or franja is None:
            raise ValueError("La labor y la franja son obligatorias.")
        if not isinstance(fecha, date):
            raise TypeError("La fecha debe ser una instancia de date.")

        labor_registrada = False
        i = 0

        while i < len(self.labores) and not labor_registrada:
            if self.labores[i].id_labor == labor.id_labor:
                labor_registrada = True
            i += 1
            
        if not labor_registrada:
            raise ValueError("La labor no está registrada en el sistema.")

        self.preparar_semana(fecha)

        if self.labor_ya_asignada(labor, franja, fecha):
            return []

        capacidad = self.obtener_capacidad_franja(labor.sector, franja)
        if capacidad is None:
            raise ValueError("No existe una capacidad configurada para el área y la franja horaria.")

        ocupacion_actual = self.contar_ocupacion(labor.sector, franja, fecha)
        if not capacidad.tiene_capacidad(ocupacion_actual):
            return []

        disponibles = []
        for trab in self.trabajadores:
            apto = self.motivo_no_apto(trab, labor, fecha) is None
            ya_ocupado = self.trabajador_ya_ocupado(trab, franja, fecha)

            if apto and not ya_ocupado:
                disponibles.append(trab)

        return disponibles