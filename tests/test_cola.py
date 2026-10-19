from datetime import date, time

import pytest

from clases import (
    Cola, ColaVacia, ErrorAsignacion, SistemaGestion, Trabajador, Supervisor,
    Labor, SectorTrabajo, FranjaHoraria, Franja, CapacidadFranjaArea,
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
# Una propuesta Pendiente reserva trabajador, labor, cupo y horas, así que las
# propuestas de estos tests usan trabajadores y labores distintos.

@pytest.fixture
def escenario():
    sistema = SistemaGestion()
    area = SectorTrabajo(1, "Mantenimiento")
    franja = FranjaHoraria(Franja.MAÑANA, time(8), time(14))
    labor1 = Labor(1, "Revisión", "Revisar equipos", 4, [], [], area)
    labor2 = Labor(2, "Limpieza", "Limpiar el sector", 4, [], [], area)
    sistema.registrar_area(area)
    sistema.registrar_labor(labor1)
    sistema.registrar_labor(labor2)
    sistema.registrar_capacidad_franja(CapacidadFranjaArea(area, franja, 5))
    ana = Trabajador(1, "Ana", "Pérez", date(1990, 1, 1), 40)
    beto = Trabajador(2, "Beto", "Gómez", date(1991, 1, 1), 40)
    sistema.registrar_trabajador(ana)
    sistema.registrar_trabajador(beto)
    sup = Supervisor(99, "Sofía", "Ruiz", date(1985, 1, 1), 40)
    return sistema, labor1, labor2, franja, ana, beto, sup


def test_proponer_encola_en_orden_de_llegada(escenario):
    sistema, labor1, labor2, franja, ana, beto, _ = escenario
    a1 = sistema.proponer_asignacion(ana, labor1, franja, LUNES)
    a2 = sistema.proponer_asignacion(beto, labor2, franja, LUNES)
    assert sistema.cola_pendientes.desencolar() is a1
    assert sistema.cola_pendientes.desencolar() is a2
    assert sistema.cola_pendientes.esta_vacia()


def test_propuesta_rechazada_al_proponer_no_se_encola(escenario):
    sistema, labor1, _, franja, ana, beto, _ = escenario
    a1 = sistema.proponer_asignacion(ana, labor1, franja, LUNES)
    with pytest.raises(ErrorAsignacion):
        sistema.proponer_asignacion(beto, labor1, franja, LUNES)  # labor ya reservada
    assert sistema.cola_pendientes.desencolar() is a1
    assert sistema.cola_pendientes.esta_vacia()


def test_procesar_siguiente_resuelve_en_orden_de_llegada(escenario):
    sistema, labor1, labor2, franja, ana, beto, sup = escenario
    a1 = sistema.proponer_asignacion(ana, labor1, franja, LUNES)
    a2 = sistema.proponer_asignacion(beto, labor2, franja, LUNES)

    assert sistema.procesar_siguiente(sup) is a1
    assert a1.estado == EstadoAsignacion.APROBADA
    assert a2.estado == EstadoAsignacion.PENDIENTE   # todavía no le toca

    assert sistema.procesar_siguiente(sup) is a2
    assert a2.estado == EstadoAsignacion.APROBADA
    assert sistema.procesar_siguiente(sup) is None


def test_procesar_siguiente_saltea_las_aprobadas_a_mano(escenario):
    sistema, labor1, labor2, franja, ana, beto, sup = escenario
    a1 = sistema.proponer_asignacion(ana, labor1, franja, LUNES)
    a2 = sistema.proponer_asignacion(beto, labor2, franja, LUNES)

    sistema.aprobar_asignacion(sup, a1)   # el supervisor eligió a mano la más antigua

    assert sistema.procesar_siguiente(sup) is a2   # a1 se saltea, se resuelve a2
    assert sistema.procesar_siguiente(sup) is None


def test_procesar_siguiente_saltea_las_rechazadas_a_mano(escenario):
    sistema, labor1, labor2, franja, ana, beto, sup = escenario
    a1 = sistema.proponer_asignacion(ana, labor1, franja, LUNES)
    a2 = sistema.proponer_asignacion(beto, labor2, franja, LUNES)

    sup.rechazar_asignacion(a1, "ya no hace falta")

    assert sistema.procesar_siguiente(sup) is a2
    assert a1.estado == EstadoAsignacion.RECHAZADA
    assert a2.estado == EstadoAsignacion.APROBADA


def test_procesar_siguiente_rechaza_si_al_procesarla_ya_no_se_puede_aprobar(escenario):
    sistema, labor1, _, franja, ana, _, sup = escenario
    a1 = sistema.proponer_asignacion(ana, labor1, franja, LUNES)   # 4 hs

    ana.max_horas_semanales = 2   # el contrato cambió mientras esperaba en la cola

    assert sistema.procesar_siguiente(sup) is a1
    assert a1.estado == EstadoAsignacion.RECHAZADA
    assert "Rechazada al procesar la cola" in a1.motivo_rechazo


def test_procesar_siguiente_sin_propuestas_devuelve_none(escenario):
    sistema, *_, sup = escenario
    assert sistema.procesar_siguiente(sup) is None
