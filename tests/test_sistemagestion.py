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
from clases.excepciones import (
    ErrorAsignacion,
    CapacidadNoConfigurada,
    LaborYaAsignada,
    TrabajadorOcupado,
    TrabajadorNoApto,
    CargaHorariaExcedida,
    FranjaCompleta,
)


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

    with pytest.raises(LaborYaAsignada):
        sistema.proponer_asignacion(trabajador, labor, franja, date(2025, 1, 1))


def test_proponer_asignacion_lanza_error_si_trabajador_excede_horas_semanales():
    sistema, trabajador, labor, franja = construir_sistema_base()
    trabajador.max_horas_semanales = 2

    with pytest.raises(CargaHorariaExcedida):
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

    with pytest.raises(CapacidadNoConfigurada):
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

    with pytest.raises(CargaHorariaExcedida):
        sistema.proponer_asignacion(trabajador, labor, franja, date(2025, 1, 2))  # 3 + 3 = 6 > 5


def test_proponer_asignacion_permite_llegar_justo_al_maximo_de_horas():
    sistema, trabajador, labor, franja = construir_sistema_base()
    trabajador.setter_max_horas_semanales(6)
    sistema.proponer_asignacion(trabajador, labor, franja, date(2025, 1, 1))

    asignacion = sistema.proponer_asignacion(trabajador, labor, franja, date(2025, 1, 2))  # 3 + 3 = 6, no supera

    assert asignacion in sistema.asignaciones


# ---------------------------------------------------------------------------
# Issue #14: excepciones propias del dominio
# ---------------------------------------------------------------------------

def construir_trabajador_apto(id_trabajador):
    t = Trabajador(id_trabajador, "Ana", "García", date(1990, 1, 1), 40)
    t.agregar_habilidades("Python")
    t.agregar_credencial(Credencial("Seguridad Eléctrica", date(2024, 1, 1), date(2026, 1, 1)))
    return t


def construir_labor_n(id_labor, sector):
    return Labor(id_labor, f"Labor {id_labor}", "desc", 3, ["Python"], ["Seguridad Eléctrica"], sector)


def construir_sistema_con_limite(limite):
    sistema = SistemaGestion()
    sector = construir_sector()
    franja = construir_franja()
    sistema.registrar_area(sector)
    sistema.registrar_capacidad_franja(CapacidadFranjaArea(sector, franja, limite))
    return sistema, sector, franja


def test_proponer_asignacion_lanza_franja_completa_si_se_alcanza_el_limite():
    sistema, sector, franja = construir_sistema_con_limite(1)
    t1, t2 = construir_trabajador_apto(1), construir_trabajador_apto(2)
    l1, l2 = construir_labor_n(1, sector), construir_labor_n(2, sector)
    sistema.registrar_trabajador(t1)
    sistema.registrar_trabajador(t2)
    sistema.registrar_labor(l1)
    sistema.registrar_labor(l2)

    sistema.proponer_asignacion(t1, l1, franja, date(2025, 1, 1))

    with pytest.raises(FranjaCompleta):
        sistema.proponer_asignacion(t2, l2, franja, date(2025, 1, 1))


def test_proponer_asignacion_lanza_trabajador_ocupado_si_ya_tiene_esa_franja():
    sistema, sector, franja = construir_sistema_con_limite(5)
    t = construir_trabajador_apto(1)
    l1, l2 = construir_labor_n(1, sector), construir_labor_n(2, sector)
    sistema.registrar_trabajador(t)
    sistema.registrar_labor(l1)
    sistema.registrar_labor(l2)

    sistema.proponer_asignacion(t, l1, franja, date(2025, 1, 1))

    with pytest.raises(TrabajadorOcupado):
        sistema.proponer_asignacion(t, l2, franja, date(2025, 1, 1))


def test_proponer_asignacion_lanza_trabajador_no_apto_si_falta_habilidad():
    sistema, sector, franja = construir_sistema_con_limite(5)
    t = Trabajador(1, "Luis", "Pérez", date(1990, 1, 1), 40)  # sin habilidades
    labor = construir_labor_n(1, sector)
    sistema.registrar_trabajador(t)
    sistema.registrar_labor(labor)

    with pytest.raises(TrabajadorNoApto):
        sistema.proponer_asignacion(t, labor, franja, date(2025, 1, 1))


def test_proponer_asignacion_lanza_trabajador_no_apto_si_falta_credencial_del_area():
    sistema, sector, franja = construir_sistema_con_limite(5)  # el sector exige Seguridad Eléctrica
    t = Trabajador(1, "Luis", "Pérez", date(1990, 1, 1), 40)
    t.agregar_habilidades("Python")  # tiene la habilidad pero no la credencial
    labor = Labor(1, "Labor", "desc", 3, ["Python"], [], sector)
    sistema.registrar_trabajador(t)
    sistema.registrar_labor(labor)

    with pytest.raises(TrabajadorNoApto):
        sistema.proponer_asignacion(t, labor, franja, date(2025, 1, 1))


def test_buscar_disponibles_excluye_al_no_apto_sin_lanzar_excepcion():
    sistema, sector, franja = construir_sistema_con_limite(5)
    apto = construir_trabajador_apto(1)
    no_apto = Trabajador(2, "Luis", "Pérez", date(1990, 1, 1), 40)
    labor = construir_labor_n(1, sector)
    sistema.registrar_trabajador(apto)
    sistema.registrar_trabajador(no_apto)
    sistema.registrar_labor(labor)

    assert sistema.buscar_disponibles(labor, franja, date(2025, 1, 1)) == [apto]


@pytest.mark.parametrize("excepcion", [
    CapacidadNoConfigurada, LaborYaAsignada, TrabajadorOcupado,
    TrabajadorNoApto, CargaHorariaExcedida, FranjaCompleta,
])
def test_las_excepciones_de_dominio_heredan_de_error_asignacion(excepcion):
    assert issubclass(excepcion, ErrorAsignacion)
    assert not issubclass(excepcion, ValueError)