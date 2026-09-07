from datetime import date
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
        self.capacidades_franja = []  # Instancias de CapacidadFranjaArea
        self.semana_actual = None

    def registrar_trabajador(self, trabajador):
        if any(t.id_trabajador == trabajador.id_trabajador for t in self.trabajadores):
            raise ValueError("Ya existe un trabajador con ese identificador.")
        self.trabajadores.append(trabajador)

    def registrar_labor(self, labor):
        if any(l.id_labor == labor.id_labor for l in self.labores):
            raise ValueError("Ya existe una labor con ese identificador.")
        self.labores.append(labor)

    def registrar_area(self, area):
        if any(a.id == area.id for a in self.areas):
            raise ValueError("Ya existe un área con ese identificador.")
        self.areas.append(area)

    def registrar_capacidad_franja(self, capacidad_franja):
        for capacidad in self.capacidades_franja:
            if (
                capacidad.area.id == capacidad_franja.area.id
                and self._misma_franja(capacidad.franja, capacidad_franja.franja)
            ):
                raise ValueError("Ya existe una capacidad para ese área y franja horaria.")
        self.capacidades_franja.append(capacidad_franja)

    @staticmethod
    def _misma_franja(franja_a, franja_b):
        return (
            franja_a is not None
            and franja_b is not None
            and franja_a.franja == franja_b.franja
        )

    def _preparar_semana(self, fecha):
        semana = (fecha.isocalendar().year, fecha.isocalendar().week)
        if self.semana_actual != semana:
            for trabajador in self.trabajadores:
                trabajador.resetear_horas_semanales()
            self.semana_actual = semana

    def _obtener_capacidad_franja(self, area, franja):
        for capacidad in self.capacidades_franja:
            if capacidad.area.id == area.id and self._misma_franja(capacidad.franja, franja):
                return capacidad
        return None

    def _validar_parametros_asignacion(self, trabajador, labor, franja, fecha):
        if trabajador is None or labor is None or franja is None:
            raise ValueError("El trabajador, la labor y la franja son obligatorios.")
        if not isinstance(fecha, date):
            raise TypeError("La fecha debe ser una instancia de date.")
        if not any(t.id_trabajador == trabajador.id_trabajador for t in self.trabajadores):
            raise ValueError("El trabajador no está registrado en el sistema.")
        if not any(l.id_labor == labor.id_labor for l in self.labores):
            raise ValueError("La labor no está registrada en el sistema.")
        if not any(a.id == labor.sector.id for a in self.areas):
            raise ValueError("El área de la labor no está registrada en el sistema.")

    def proponer_asignacion(self, trabajador, labor, franja, fecha):
        self._validar_parametros_asignacion(trabajador, labor, franja, fecha)
        self._preparar_semana(fecha)

        capacidad = self._obtener_capacidad_franja(labor.sector, franja)
        if capacidad is None:
            raise ValueError("No existe una capacidad configurada para el área y la franja horaria.")

        # Regla 7: exclusividad de asignación
        for asig in self.asignaciones:
            if (
                asig.labor.id_labor == labor.id_labor
                and asig.fecha == fecha
                and self._misma_franja(asig.franja, franja)
            ):
                raise ValueError(
                    "La labor ya tiene una asignación comprometida para esta fecha y franja horaria."
                )

            if (
                asig.trabajador.id_trabajador == trabajador.id_trabajador
                and asig.fecha == fecha
                and self._misma_franja(asig.franja, franja)
            ):
                raise ValueError("El trabajador ya tiene una asignación para esa fecha y franja horaria.")

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
        ocupacion_actual = sum(
            1
            for asig in self.asignaciones
            if (
                asig.fecha == fecha
                and asig.labor.sector.id == labor.sector.id
                and self._misma_franja(asig.franja, franja)
            )
        )

        if not capacidad.tiene_capacidad(ocupacion_actual):
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
        if labor is None or franja is None:
            raise ValueError("La labor y la franja son obligatorias.")
        if not isinstance(fecha, date):
            raise TypeError("La fecha debe ser una instancia de date.")
        if not any(l.id_labor == labor.id_labor for l in self.labores):
            raise ValueError("La labor no está registrada en el sistema.")

        self._preparar_semana(fecha)

        # Regla 7: si la labor ya fue asignada para esa fecha y franja, no hay disponibles.
        for asignacion in self.asignaciones:
            if (
                asignacion.labor.id_labor == labor.id_labor
                and asignacion.fecha == fecha
                and self._misma_franja(asignacion.franja, franja)
            ):
                return []

        # Regla 6: comprobar la capacidad del sector para esa fecha y franja.
        ocupacion_actual = sum(
            1
            for asignacion in self.asignaciones
            if (
                asignacion.fecha == fecha
                and asignacion.labor.sector.id == labor.sector.id
                and self._misma_franja(asignacion.franja, franja)
            )
        )

        capacidad = self._obtener_capacidad_franja(labor.sector, franja)

        if capacidad is None or not capacidad.tiene_capacidad(ocupacion_actual):
            return []

        # Regla 11: filtrar trabajadores aptos y dentro del límite horario.
        disponibles = []
        for trab in self.trabajadores:
            if (
                labor.trabajador_es_apto(trab, fecha)
                and labor.sector.trabajador_cumple_credenciales(trab, fecha)
                and not trab.excede_horas(labor.duracion_horas)
                and not any(
                    asignacion.trabajador.id_trabajador == trab.id_trabajador
                    and asignacion.fecha == fecha
                    and self._misma_franja(asignacion.franja, franja)
                    for asignacion in self.asignaciones
                )
            ):
                disponibles.append(trab)
        return disponibles
        
