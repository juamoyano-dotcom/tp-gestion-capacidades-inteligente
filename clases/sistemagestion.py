from datetime import date, timedelta
from .trabajador import Trabajador
from .asignacion import Asignacion, EstadoAsignacion
from .labor import Labor, Frecuencia
from .sectortrabajo import SectorTrabajo
from .franjahoraria import FranjaHoraria
from .excepciones import (
    ErrorAsignacion,
    CapacidadNoConfigurada,
    LaborYaAsignada,
    TrabajadorOcupado,
    TrabajadorNoApto,
    CargaHorariaExcedida,
    FranjaCompleta,
)

class SistemaGestion:
    """Núcleo del sistema: registra entidades, propone asignaciones y busca personal disponible.

    Concentra las reglas que involucran a varias clases a la vez (aptitud,
    horas semanales, capacidad de franja, exclusividad). Las asignaciones son
    la única fuente de verdad: horas comprometidas y ocupación se calculan a
    partir de ellas, no se guardan en contadores.

    Una propuesta Pendiente reserva trabajador, labor, cupo de franja y horas.
    Si se rechaza, deja de contar para esos recursos.
    """  # ~ CAMBIADO: antes la docstring no aclaraba este criterio

    def __init__(self):
        self.trabajadores = []
        self.labores = []
        self.areas = []
        self.asignaciones = []
        self.capacidades_franja = {}


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
    def misma_franja(franja_a, franja_b) -> bool:
        return (
            franja_a is not None
            and franja_b is not None
            and franja_a.franja == franja_b.franja
        )


    def obtener_capacidad_franja(self, area, franja):
        return self.capacidades_franja.get((area.id, franja.franja))

    def validar_parametros_asignacion(self, trabajador, labor, franja, fecha) -> None:
        """Valida los datos de entrada de una asignación.

        Lanza ValueError si falta algún dato o si el trabajador, la labor o el
        área de la labor no están registrados; TypeError si `fecha` no es date.
        """
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

    def verificar_apto(self, trabajador, labor, fecha):
        """Valida habilidades y credenciales requeridas por la labor y el área."""
        if not labor.trabajador_es_apto(trabajador, fecha):
            raise TrabajadorNoApto(
                "El trabajador no cumple con las habilidades y credenciales activas requeridas por la labor."
            )

        if not labor.sector.trabajador_cumple_credenciales(trabajador, fecha):
            raise TrabajadorNoApto(
                "El trabajador no posee las credenciales obligatorias activas para esta área de trabajo."
            )

    def verificar_conflictos(self, asig) -> None:                      # + NUEVO (método completo)
        """Lanza la excepción que corresponda si la asignación `asig` (pendiente o candidata)
        choca con otras propuestas o asignaciones aprobadas: trabajador ocupado, labor cubierta en su período,
        horas semanales excedidas o franja sin cupo.

        Por qué existe: estas validaciones se necesitan en tres momentos (proponer,
        aprobar y limpiar pendientes en cascada). Con un solo método los tres usan
        exactamente el mismo criterio.
        """
        if self.labor_completa_en_periodo(asig.labor, asig.fecha, excluir=asig):
            raise LaborYaAsignada("La labor ya tiene una asignación en este período.")

        if self.trabajador_ya_ocupado(asig.trabajador, asig.franja, asig.fecha, excluir=asig):
            raise TrabajadorOcupado("El trabajador ya tiene otra asignación pendiente o aprobada en esa fecha y franja horaria.")

        if self.horas_comprometidas(asig.trabajador, asig.fecha, excluir=asig) + asig.horas_asignadas > asig.trabajador.max_horas_semanales:
            raise CargaHorariaExcedida("La asignación excede el límite máximo de horas semanales del trabajador.")

        capacidad = self.obtener_capacidad_franja(asig.labor.sector, asig.franja)
        if capacidad is None:
            raise CapacidadNoConfigurada("No existe una capacidad configurada para el área y la franja horaria.")

        if not capacidad.tiene_capacidad(self.contar_ocupacion(asig.labor.sector, asig.franja, asig.fecha, excluir=asig)):
            raise FranjaCompleta("La franja horaria en el área de trabajo seleccionada está completa.")

    def contar_ocupacion(self, area, franja, fecha, excluir=None) -> int:
        ocupacion_actual = 0
        for asig in self.asignaciones:
            if (
                asig is not excluir
                and asig.estado in (EstadoAsignacion.PENDIENTE, EstadoAsignacion.APROBADA)
                and asig.fecha == fecha
                and asig.labor.sector.id == area.id
                and self.misma_franja(asig.franja, franja)
            ):
                ocupacion_actual += 1
        return ocupacion_actual

    def trabajador_ya_ocupado(self, trabajador, franja, fecha, excluir=None) -> bool:
        for asig in self.asignaciones:
            if (
                asig is not excluir
                and asig.estado in (EstadoAsignacion.PENDIENTE, EstadoAsignacion.APROBADA)
                and asig.trabajador.id_trabajador == trabajador.id_trabajador
                and asig.fecha == fecha
                and self.misma_franja(asig.franja, franja)
            ):
                return True
        return False

    # borre labor_ya_asignada. La reemplaza labor_completa_en_periodo
    # mira el período de la labor (día o semana) y cuántos trabajadores necesita

    def asignaciones_aprobadas(self):
        return [a for a in self.asignaciones if a.estado == EstadoAsignacion.APROBADA]

    def asignaciones_pendientes(self):
        return [a for a in self.asignaciones if a.estado == EstadoAsignacion.PENDIENTE]

    def rango_periodo(self, labor, fecha):
        if labor.frecuencia == Frecuencia.DIARIA:
            return fecha, fecha
        lunes = fecha - timedelta(days=fecha.weekday())
        return lunes, lunes + timedelta(days=6)

    def labor_completa_en_periodo(self, labor, fecha, excluir=None):
        inicio, fin = self.rango_periodo(labor, fecha)

        for a in self.asignaciones:
            if (
                a is not excluir
                and a.estado in (EstadoAsignacion.PENDIENTE, EstadoAsignacion.APROBADA)
                and a.labor.id_labor == labor.id_labor
                and inicio <= a.fecha <= fin
            ):
                return True

        return False

    def labores_a_cubrir(self, fecha):
        return [l for l in self.labores if not self.labor_completa_en_periodo(l, fecha)]

    def trabajadores_con_horas(self, fecha):
        return [t for t in self.trabajadores
                if self.horas_comprometidas(t, fecha) < t.max_horas_semanales]

    def proponer_asignacion(self, trabajador, labor, franja, fecha) -> Asignacion:
        """Propone una asignación y la deja en estado Pendiente.

        Valida parámetros, aptitud y conflictos con otras asignaciones pendientes
        o aprobadas. La propuesta reserva recursos hasta que se aprueba o rechaza.
        """  
        self.validar_parametros_asignacion(trabajador, labor, franja, fecha)

        self.verificar_apto(trabajador, labor, fecha)

        # cambio --> se crea ANTES de validar, porque verificar_conflictos recibe una Asignacion
        nueva_asignacion = Asignacion(
            id_asignacion=len(self.asignaciones) + 1,
            trabajador=trabajador,
            labor=labor,
            franja=franja,
            fecha=fecha
        )

        # nuevo --> reemplaza los chequeos sueltos de capacidad, trabajador ocupado y franja completa.
        # si falla, no se agregó nada a la lista, así que no queda informacion basura
        self.verificar_conflictos(nueva_asignacion)

        self.asignaciones.append(nueva_asignacion)
        return nueva_asignacion

    def aprobar_asignacion(self, supervisor, asignacion):   # + NUEVO (método completo)
        """Aprueba una pendiente y descarta automáticamente las pendientes que quedan en conflicto.

        Usar siempre este método (y no supervisor.formalizar_asignacion directo),
        porque acá se revalida y se hace la cascada.
        """
        # se chequea el estado primero para que el error sea claro si ya estaba aprobada/rechazada
        if asignacion.estado != EstadoAsignacion.PENDIENTE:
            raise ValueError(f"No se puede aprobar una asignación en estado '{asignacion.estado.value}'.")

        # Revalida excluyendo la propia propuesta, que ya está reservando sus recursos.
        self.verificar_conflictos(asignacion)

        # aprueba formalizar_asignacion sin modificarlo
        supervisor.formalizar_asignacion(asignacion)

        # cascada --> rechaza las pendientes que ahora chocan (mismo trabajador/franja, labor cubierta, horas insuficientes o franja llena)
        for pendiente in self.asignaciones_pendientes():
            try:
                self.verificar_conflictos(pendiente)
            except ErrorAsignacion as e:
                supervisor.rechazar_asignacion(pendiente, f"Descartada automáticamente: {e}")

    def buscar_disponibles(self, labor, franja, fecha) -> list:
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

        # cambio --> solo se deja el chequeo de capacidad configurada, para que siga LANZANDO la excepción
        # si lo dejáramos al verificar_conflictos por trabajador, el except lo taparía y devolvería [] sin avisar que falta configurar.
        if self.obtener_capacidad_franja(labor.sector, franja) is None:
            raise CapacidadNoConfigurada("No existe una capacidad configurada para el área y la franja horaria.")

        # borre el `return []` por franja llena
        # ahora lo decide verificar_conflictos por candidato

        disponibles = []
        for trab in self.trabajadores:
            candidata = Asignacion(0, trab, labor, franja, fecha)   # temporal, NO se guarda en self.asignaciones
            try:
                self.verificar_apto(trab, labor, fecha)
                self.verificar_conflictos(candidata) # cambio --> reemplaza trabajador_ya_ocupado
            except ErrorAsignacion:
                continue
            disponibles.append(trab)

        return disponibles
        # buscar_disponibles y proponer_asignacion usan los mismos criterios
        # nunca devuelve como "disponible" a alguien que proponer_asignacion luego rechace

    def horas_comprometidas(self, trabajador, fecha, excluir=None) -> int:
        """
        Horas pendientes o aprobadas del trabajador en la semana (lunes a domingo) de `fecha`.

        Decisión de diseño: no se guarda un contador. Se calcula desde
        self.asignaciones, que es la única fuente de verdad. Así, las consultas no
        modifican el estado y no hay desincronización.
        """  

        lunes = fecha - timedelta(days=fecha.weekday())
        domingo = lunes + timedelta(days=6)
        return sum(
            a.horas_asignadas
            for a in self.asignaciones
            if a.estado in (EstadoAsignacion.PENDIENTE, EstadoAsignacion.APROBADA)
            and a is not excluir
            and a.trabajador.id_trabajador == trabajador.id_trabajador
            and lunes <= a.fecha <= domingo
        )