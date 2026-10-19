from datetime import date, time

import pytest

from clases import (
    Cola, ColaVacia, SistemaGestion, Trabajador, Supervisor, Labor,
    SectorTrabajo, FranjaHoraria, Franja, CapacidadFranjaArea,
)
from clases.asignacion import EstadoAsignacion

LUNES = date(2026, 10, 12)


# ---------- Cola ----------

def test_cola_nueva_esta_vacia():
    assert Cola().esta_vacia()


def test_fifo_el_primero_en_entrar_es_el_primero_en_salir():
    cola = Cola()
    for dato in ("A", "B", "C"):
        cola.encolar(dato)
    assert [cola.desencolar(), cola.desencolar(), cola.desencolar()] == ["A", "B", "C"]


def test_inicio_no_quita_el_elemento():
    cola = Cola()
    cola.encolar("A")
    cola.encolar("B")
    assert cola.inicio() == "A"
    assert cola.inicio() == "A"
    assert cola.desencolar() == "A"


def test_desencolar_el_unico_elemento_deja_la_cola_consistente():
    cola = Cola()
    cola.encolar("A")
    cola.desencolar()
    assert cola.esta_vacia()
    # si `final` quedara colgado, este encolar engancharía el nodo al viejo
    cola.encolar("B")
    assert cola.inicio() == "B"
    assert cola.desencolar() == "B"
    assert cola.esta_vacia()


def test_desencolar_cola_vacia_lanza_colavacia():
    with pytest.raises(ColaVacia):
        Cola().desencolar()


def test_inicio_cola_vacia_lanza_colavacia():
    with pytest.raises(ColaVacia):
        Cola().inicio()


# ---------- SistemaGestion + Cola ----------

@pytest.fixture
def escenario():
    sistema = SistemaGestion()
    area = SectorTrabajo(1, "Mantenimiento")
    franja = FranjaHoraria(Franja.MAÑANA, time(8), time(14))
    labor = Labor(1, "Revisión", "Revisar equipos", 4, [], [], area)  # requiere 1 trabajador
    sistema.registrar_area(area)
    sistema.registrar_labor(labor)
    sistema.registrar_capacidad_franja(CapacidadFranjaArea(area, franja, 5))
    ana = Trabajador(1, "Ana", "Pérez", date(1990, 1, 1), 40)
    beto = Trabajador(2, "Beto", "Gómez", date(1991, 1, 1), 40)
    sistema.registrar_trabajador(ana)
    sistema.registrar_trabajador(beto)
    sup = Supervisor(99, "Sofía", "Ruiz", date(1985, 1, 1), 40)
    return sistema, labor, franja, ana, beto, sup


def test_proponer_encola_en_orden_de_llegada(escenario):
    sistema, labor, franja, ana, beto, _ = escenario
    a1 = sistema.proponer_asignacion(ana, labor, franja, LUNES)
    a2 = sistema.proponer_asignacion(beto, labor, franja, LUNES)
    assert sistema.cola_pendientes.desencolar() is a1
    assert sistema.cola_pendientes.desencolar() is a2


def test_propuesta_invalida_no_se_encola(escenario):
    sistema, labor, franja, ana, _, _ = escenario
    sistema.proponer_asignacion(ana, labor, franja, LUNES)
    with pytest.raises(Exception):
        sistema.proponer_asignacion(ana, labor, franja, LUNES)  # duplicada
    sistema.cola_pendientes.desencolar()
    assert sistema.cola_pendientes.esta_vacia()


def test_procesar_siguiente_aprueba_la_mas_antigua_y_la_cascada_descarta_la_otra(escenario):
    sistema, labor, franja, ana, beto, sup = escenario
    a1 = sistema.proponer_asignacion(ana, labor, franja, LUNES)
    a2 = sistema.proponer_asignacion(beto, labor, franja, LUNES)

    resuelta = sistema.procesar_siguiente(sup)

    assert resuelta is a1
    assert a1.estado == EstadoAsignacion.APROBADA
    assert a2.estado == EstadoAsignacion.RECHAZADA   # la cascada la descartó
    # a2 sigue en la cola pero ya no está pendiente: se saltea
    assert sistema.procesar_siguiente(sup) is None
    assert sistema.cola_pendientes.esta_vacia()


def test_procesar_siguiente_saltea_las_aprobadas_a_mano(escenario):
    sistema, labor, franja, ana, beto, sup = escenario
    sistema.proponer_asignacion(ana, labor, franja, LUNES)
    a2 = sistema.proponer_asignacion(beto, labor, franja, LUNES)

    sistema.aprobar_asignacion(sup, a2)   # el supervisor elige a Beto a mano

    assert sistema.procesar_siguiente(sup) is None
    assert a2.estado == EstadoAsignacion.APROBADA


def test_procesar_siguiente_rechaza_si_al_procesarla_ya_choca(escenario):
    sistema, labor, franja, ana, beto, sup = escenario
    a1 = sistema.proponer_asignacion(ana, labor, franja, LUNES)
    a2 = sistema.proponer_asignacion(beto, labor, franja, LUNES)

    sup.formalizar_asignacion(a1)   # aprobada salteando la cascada a propósito

    resuelta = sistema.procesar_siguiente(sup)

    assert resuelta is a2
    assert a2.estado == EstadoAsignacion.RECHAZADA
    assert "Rechazada al procesar la cola" in a2.motivo_rechazo


def test_procesar_siguiente_sin_propuestas_devuelve_none(escenario):
    sistema, _, _, _, _, sup = escenario
    assert sistema.procesar_siguiente(sup) is None
