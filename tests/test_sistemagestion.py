import pytest
from datetime import date, time

from clases.sistemagestion import SistemaGestion
from clases.trabajador import Trabajador
from clases.supervisor import Supervisor
from clases.labor import Labor
from clases.sectortrabajo import SectorTrabajo
from clases.credencial import Credencial
from clases.asignacion import Asignacion, EstadoAsignacion
from clases.franjahoraria import FranjaHoraria, Franja
from clases.capacidadfranja import CapacidadFranjaArea


def construir_sector():
    return SectorTrabajo(
        id_sector=1,
        nombre="Mantenimiento",
        credenciales_obligatorias=["Seguridad Eléctrica"],
    )


def construir_trabajador():
    return Trabajador(
        id_trabajador=1,
        nombre="Ana",
        apellido="García",
        fecha_nacimiento=date(1990, 1, 1),
        max_horas_semanales=40,
    )


def construir_labor(sector):
    return Labor(
        id_labor=1,
        titulo="Limpieza de líneas",
        descripcion="Limpieza de una línea crítica.",
        duracion_horas=3,
        habilidades_requeridas=["Python"],
        credenciales_requeridas=["Seguridad Eléctrica"],
        sector=sector,
    )


def construir_franja():
    return FranjaHoraria(
        franja=Franja.MAÑANA,
        hora_inicio=time(8, 0),
        hora_fin=time(12, 0),
    )


def construir_sistema_base():
    sistema = SistemaGestion()
    sector = construir_sector()
    trabajador = construir_trabajador()
    labor = construir_labor(sector)
    franja = construir_franja()

    trabajador.agregar_habilidades("Python")
    trabajador.agregar_credencial(Credencial("Seguridad Eléctrica", date(2024, 1, 1), date(2026, 1, 1)))

    sistema.registrar_area(sector)
    sistema.registrar_trabajador(trabajador)
    sistema.registrar_labor(labor)
    sistema.registrar_capacidad_franja(CapacidadFranjaArea(sector, franja, 5))

    return sistema, trabajador, labor, franja


def test_creacion_sistema_valida():
    sistema = SistemaGestion()

    assert sistema.trabajadores == []
    assert sistema.labores == []
    assert sistema.areas == []
    assert sistema.asignaciones == []
    assert sistema.capacidades_franja == {}


def test_registrar_trabajador_y_area_y_labor_y_capacidad():
    sistema, trabajador, labor, franja = construir_sistema_base()

    assert trabajador in sistema.trabajadores
    assert labor in sistema.labores
    assert labor.sector in sistema.areas
    assert sistema.obtener_capacidad_franja(labor.sector, franja) is not None


def test_proponer_asignacion_valida_cambia_estado_a_pendiente_y_suma_horas():
    sistema, trabajador, labor, franja = construir_sistema_base()

    asignacion = sistema.proponer_asignacion(trabajador, labor, franja, date(2025, 1, 1))

    assert isinstance(asignacion, Asignacion)
    assert asignacion.estado is EstadoAsignacion.PENDIENTE
    assert sistema.horas_comprometidas(trabajador, date(2025, 1, 1)) == labor.duracion_horas
    assert asignacion in sistema.asignaciones


def test_proponer_asignacion_lanza_error_si_labor_ya_tiene_asignacion_para_esa_fecha_y_franja():
    sistema, trabajador, labor, franja = construir_sistema_base()
    sistema.proponer_asignacion(trabajador, labor, franja, date(2025, 1, 1))

    with pytest.raises(ValueError, match="labor ya tiene una asignación"):
        sistema.proponer_asignacion(trabajador, labor, franja, date(2025, 1, 1))


def test_proponer_asignacion_lanza_error_si_trabajador_excede_horas_semanales():
    sistema, trabajador, labor, franja = construir_sistema_base()
    trabajador.max_horas_semanales = 2

    with pytest.raises(ValueError, match="excede el límite máximo de horas semanales"):
        sistema.proponer_asignacion(trabajador, labor, franja, date(2025, 1, 1))


def test_proponer_asignacion_lanza_error_si_no_existe_capacidad_para_franja_y_area():
    sistema = SistemaGestion()
    sector = construir_sector()
    trabajador = construir_trabajador()
    labor = construir_labor(sector)
    franja = construir_franja()

    trabajador.agregar_habilidades("Python")
    trabajador.agregar_credencial(Credencial("Seguridad Eléctrica", date(2024, 1, 1), date(2026, 1, 1)))

    sistema.registrar_area(sector)
    sistema.registrar_trabajador(trabajador)
    sistema.registrar_labor(labor)

    with pytest.raises(ValueError, match="capacidad configurada"):
        sistema.proponer_asignacion(trabajador, labor, franja, date(2025, 1, 1))


def test_buscar_disponibles_filtra_aptos_y_no_excede_horas():
    sistema, trabajador, labor, franja = construir_sistema_base()

    disponibles = sistema.buscar_disponibles(labor, franja, date(2025, 1, 1))

    assert trabajador in disponibles


def test_proponer_asignacion_no_la_agrega_al_trabajador_hasta_que_el_supervisor_la_formaliza():
    sistema, trabajador, labor, franja = construir_sistema_base()
    supervisor = Supervisor(
        id_trabajador=99,
        nombre="José",
        apellido="López",
        fecha_nacimiento=date(1991, 1, 1),
        max_horas_semanales=40,
    )

    asignacion = sistema.proponer_asignacion(trabajador, labor, franja, date(2025, 1, 1))
    assert trabajador.asignaciones == []

    supervisor.formalizar_asignacion(asignacion)
    assert trabajador.asignaciones == [asignacion]

def test_horas_comprometidas_es_cero_para_trabajador_sin_asignaciones():
    sistema, trabajador, labor, franja = construir_sistema_base()

    assert sistema.horas_comprometidas(trabajador, date(2025, 1, 1)) == 0


def test_horas_comprometidas_suma_asignaciones_de_la_misma_semana():
    sistema, trabajador, labor, franja = construir_sistema_base()

    sistema.proponer_asignacion(trabajador, labor, franja, date(2025, 1, 1))
    sistema.proponer_asignacion(trabajador, labor, franja, date(2025, 1, 2))

    assert sistema.horas_comprometidas(trabajador, date(2025, 1, 3)) == 6


def test_horas_comprometidas_no_cuenta_asignaciones_de_otra_semana():
    sistema, trabajador, labor, franja = construir_sistema_base()
    sistema.proponer_asignacion(trabajador, labor, franja, date(2025, 1, 1))

    assert sistema.horas_comprometidas(trabajador, date(2025, 1, 5)) == 3  # domingo: misma semana
    assert sistema.horas_comprometidas(trabajador, date(2025, 1, 6)) == 0  # lunes: semana nueva


def test_proponer_asignacion_lanza_error_si_las_horas_acumuladas_superan_el_maximo():
    sistema, trabajador, labor, franja = construir_sistema_base()
    trabajador.setter_max_horas_semanales(5)
    sistema.proponer_asignacion(trabajador, labor, franja, date(2025, 1, 1))  # 3 h, entra

    with pytest.raises(ValueError, match="excede el límite máximo de horas semanales"):
        sistema.proponer_asignacion(trabajador, labor, franja, date(2025, 1, 2))  # 3 + 3 = 6 > 5


def test_proponer_asignacion_permite_llegar_justo_al_maximo_de_horas():
    sistema, trabajador, labor, franja = construir_sistema_base()
    trabajador.setter_max_horas_semanales(6)
    sistema.proponer_asignacion(trabajador, labor, franja, date(2025, 1, 1))

    asignacion = sistema.proponer_asignacion(trabajador, labor, franja, date(2025, 1, 2))  # 3 + 3 = 6, no supera

    assert asignacion in sistema.asignaciones