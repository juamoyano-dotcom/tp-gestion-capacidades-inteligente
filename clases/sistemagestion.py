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

    Una propuesta (Pendiente) NO reserva recursos: solo las asignaciones
    Aprobadas ocupan trabajador, labor, cupo de franja y horas.
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
        """Reglas 4 y 5: lanza TrabajadorNoApto si el trabajador no cumple habilidades o credenciales.

        Solo mira condiciones estáticas del trabajador. Las que dependen de lo
        aprobado (horas, ocupación, cupo) están en verificar_conflictos.
        """  # ~ CAMBIADO: docstring (ya no incluye la regla de horas)
        if not labor.trabajador_es_apto(trabajador, fecha):
            raise TrabajadorNoApto(
                "El trabajador no cumple con las habilidades y credenciales activas requeridas por la labor."
            )

        if not labor.sector.trabajador_cumple_credenciales(trabajador, fecha):
            raise TrabajadorNoApto(
                "El trabajador no posee las credenciales obligatorias activas para esta área de trabajo."
            )

        # borre el chequeo de CargaHorariaExcedida que estaba aca
        # las horas dependen de qué se aprobó, igual que el resto de los conflictos
        # Ahora lo valida verificar_conflictos, para no duplicar la regla.

    def verificar_conflictos(self, asig) -> None:                      # + NUEVO (método completo)
        """Lanza la excepción que corresponda si la asignación `asig` (pendiente o candidata)
        choca con lo ya aprobado: trabajador ocupado, labor cubierta en su período,
        horas semanales excedidas o franja sin cupo.

        Por qué existe: estas validaciones se necesitan en tres momentos (proponer,
        aprobar y limpiar pendientes en cascada). Con un solo método los tres usan
        exactamente el mismo criterio.
        """
        if self.trabajador_ya_ocupado(asig.trabajador, asig.franja, asig.fecha):
            raise TrabajadorOcupado("El trabajador ya tiene otra asignación aprobada en esa fecha y franja horaria.")

        if self.labor_completa_en_periodo(asig.labor, asig.fecha):
            raise LaborYaAsignada("La labor ya tiene todos los trabajadores requeridos en este período.")

        if self.horas_comprometidas(asig.trabajador, asig.fecha) + asig.horas_asignadas > asig.trabajador.max_horas_semanales:
            raise CargaHorariaExcedida("La asignación excede el límite máximo de horas semanales del trabajador.")

        capacidad = self.obtener_capacidad_franja(asig.labor.sector, asig.franja)
        if capacidad is None:
            raise CapacidadNoConfigurada("No existe una capacidad configurada para el área y la franja horaria.")

        if not capacidad.tiene_capacidad(self.contar_ocupacion(asig.labor.sector, asig.franja, asig.fecha)):
            raise FranjaCompleta("La franja horaria en el área de trabajo seleccionada está completa.")

    def contar_ocupacion(self, area, franja, fecha) -> int:
        ocupacion_actual = 0
        for asig in self.asignaciones_aprobadas():   # ~ CAMBIADO (antes: self.asignaciones). Solo las aprobadas ocupan cupo.
            if asig.fecha == fecha and asig.labor.sector.id == area.id and self.misma_franja(asig.franja, franja):
                ocupacion_actual += 1
        return ocupacion_actual

    def trabajador_ya_ocupado(self, trabajador, franja, fecha) -> bool:
        for asig in self.asignaciones_aprobadas():   # ~ CAMBIADO. Solo una aprobada bloquea al trabajador.
            if (
                asig.trabajador.id_trabajador == trabajador.id_trabajador
                and asig.fecha == fecha
                and self.misma_franja(asig.franja, franja)
            ):
                return True
        return False

    # borre labor_ya_asignada. La reemplaza labor_completa_en_periodo
    # mira el período de la labor (día o semana) y cuántos trabajadores necesita

    def asignaciones_aprobadas(self):                # + NUEVO: lo que realmente ocupa recursos
        return [a for a in self.asignaciones if a.estado == EstadoAsignacion.APROBADA]

    def asignaciones_pendientes(self):               # + NUEVO: lo que el supervisor decide y se revalida en cascada
        return [a for a in self.asignaciones if a.estado == EstadoAsignacion.PENDIENTE]

    def rango_periodo(self, labor, fecha):           # + NUEVO: diaria = ese día; semanal = lunes a domingo
        if labor.frecuencia == Frecuencia.DIARIA:
            return fecha, fecha
        lunes = fecha - timedelta(days=fecha.weekday())
        return lunes, lunes + timedelta(days=6)

    def labor_completa_en_periodo(self, labor, fecha):   # + NUEVO: ¿ya hay aprobadas suficientes en el período?
        inicio, fin = self.rango_periodo(labor, fecha)
        asignados = sum(
            1 for a in self.asignaciones_aprobadas()
            if a.labor.id_labor == labor.id_labor and inicio <= a.fecha <= fin
        )
        return asignados >= labor.trabajadores_requeridos

    def labores_a_cubrir(self, fecha):               # + NUEVO: el "plan del día"
        return [l for l in self.labores if not self.labor_completa_en_periodo(l, fecha)]

    def trabajadores_con_horas(self, fecha):         # + NUEVO: quiénes no llegaron a su máximo semanal
        return [t for t in self.trabajadores
                if self.horas_comprometidas(t, fecha) < t.max_horas_semanales]

    def proponer_asignacion(self, trabajador, labor, franja, fecha) -> Asignacion:
        """Propone una asignación y la deja en estado Pendiente.

        Valida parámetros, propuesta duplicada, aptitud y conflictos con lo ya
        aprobado. Una propuesta no reserva recursos: pueden coexistir varias
        alternativas pendientes, y el supervisor elige con aprobar_asignacion.
        """  
        self.validar_parametros_asignacion(trabajador, labor, franja, fecha)

        # nuevo --> evita proponer exactamente lo mismo dos veces (al no haber reserva, nada lo impedía)
        for a in self.asignaciones_pendientes():
            if (a.trabajador.id_trabajador == trabajador.id_trabajador
                    and a.labor.id_labor == labor.id_labor
                    and a.fecha == fecha
                    and self.misma_franja(a.franja, franja)):
                raise ErrorAsignacion("Ya existe una propuesta pendiente igual.")

        self.verificar_apto(trabajador, labor, fecha)   # igual que antes (ahora sin el chequeo de horas)

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

        # revalida: pudo quedar inválida desde que se propuso
        # las propuestas pendientes no reservan nada, y entre el momento en que se propone y el momento en que el supervisor decide, el estado del sistema puede cambiar
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

    def horas_comprometidas(self, trabajador, fecha) -> int:
        """
        Horas ya aprobadas del trabajador en la semana (lunes a domingo) de `fecha`.

        Decisión de diseño: no se guarda un contador. Se calcula desde
        self.asignaciones, que es la única fuente de verdad. Así, las consultas no
        modifican el estado y no hay desincronización.
        """  

        lunes = fecha - timedelta(days=fecha.weekday())
        domingo = lunes + timedelta(days=6)
        return sum(a.horas_asignadas
        for a in self.asignaciones_aprobadas()   
            if a.trabajador.id_trabajador == trabajador.id_trabajador
            and lunes <= a.fecha <= domingo
        )