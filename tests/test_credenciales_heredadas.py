from datetime import date, time

import pytest

from clases import (
    CapacidadFranjaArea,
    Credencial,
    Franja,
    FranjaHoraria,
    Labor,
    SectorTrabajo,
    SistemaGestion,
    Trabajador,
)
from clases.excepciones import TrabajadorNoApto

FECHA = date(2026, 10, 6)


def arbol_basico():
    """01 Producción (exige 'Seguridad') -> 0101 Ensamblado (exige 'Electricidad') -> 010101 Línea A."""
    sistema = SistemaGestion()
    produccion = SectorTrabajo(1, "Producción", ["Seguridad"], codigo="01")
    ensamblado = SectorTrabajo(2, "Ensamblado", ["Electricidad"], codigo="0101")
    linea_a = SectorTrabajo(3, "Línea A", [], codigo="010101")
    for sector in (produccion, ensamblado, linea_a):
        sistema.registrar_area(sector)
    return sistema, produccion, ensamblado, linea_a


def trabajador_con(id_trabajador, *nombres_credenciales):
    t = Trabajador(id_trabajador, "Nombre", "Apellido", date(1990, 1, 1), 40)
    for nombre in nombres_credenciales:
        t.agregar_credencial(Credencial(nombre, date(2025, 1, 1), date(2027, 1, 1)))
    return t


# ---------- Estructura: el padre ----------

def test_padre_se_asigna_al_insertar_en_el_arbol():
    sistema, produccion, ensamblado, linea_a = arbol_basico()
    assert produccion.padre is sistema.organigrama
    assert ensamblado.padre is produccion
    assert linea_a.padre is ensamblado
    assert sistema.organigrama.padre is None


def test_sector_fuera_del_arbol_no_tiene_padre():
    assert SectorTrabajo(1, "Suelto", ["Seguridad"]).padre is None


# ---------- credenciales_requeridas ----------

def test_sector_sin_padre_exige_solo_las_propias():
    suelto = SectorTrabajo(1, "Suelto", ["Seguridad"])
    assert suelto.credenciales_requeridas() == ["Seguridad"]


def test_hereda_de_todos_los_ancestros_con_el_mas_alto_primero():
    _, _, ensamblado, linea_a = arbol_basico()
    assert ensamblado.credenciales_requeridas() == ["Seguridad", "Electricidad"]
    assert linea_a.credenciales_requeridas() == ["Seguridad", "Electricidad"]   # no tiene propias


def test_no_repite_credenciales_cuando_hijo_y_padre_exigen_la_misma():
    sistema, produccion, _, _ = arbol_basico()
    calidad = SectorTrabajo(4, "Calidad", ["Seguridad", "ISO 9001"], codigo="0102")
    sistema.registrar_area(calidad)
    assert calidad.credenciales_requeridas() == ["Seguridad", "ISO 9001"]


def test_el_padre_no_hereda_de_sus_hijos():
    _, produccion, _, _ = arbol_basico()
    assert produccion.credenciales_requeridas() == ["Seguridad"]


def test_una_credencial_agregada_despues_en_el_padre_llega_a_los_descendientes():
    _, produccion, _, linea_a = arbol_basico()
    produccion.credenciales_obligatorias.append("Manejo de autoelevadores")
    assert "Manejo de autoelevadores" in linea_a.credenciales_requeridas()


def test_la_raiz_puede_imponer_una_credencial_a_toda_la_empresa():
    sistema, _, _, linea_a = arbol_basico()
    sistema.organigrama.credenciales_obligatorias.append("Código de conducta")
    assert linea_a.credenciales_requeridas()[0] == "Código de conducta"


# ---------- trabajador_cumple_credenciales ----------

def test_cumple_solo_si_tiene_las_propias_y_las_heredadas():
    _, _, ensamblado, _ = arbol_basico()
    assert ensamblado.trabajador_cumple_credenciales(trabajador_con(1, "Seguridad", "Electricidad"), FECHA)
    assert not ensamblado.trabajador_cumple_credenciales(trabajador_con(2, "Electricidad"), FECHA)  # falta la heredada
    assert not ensamblado.trabajador_cumple_credenciales(trabajador_con(3, "Seguridad"), FECHA)     # falta la propia


def test_sector_sin_codigo_se_comporta_como_antes():
    suelto = SectorTrabajo(1, "Suelto", ["Seguridad"])
    assert suelto.trabajador_cumple_credenciales(trabajador_con(1, "Seguridad"), FECHA)
    assert not suelto.trabajador_cumple_credenciales(trabajador_con(2), FECHA)


# ---------- Integración con SistemaGestion ----------

def sistema_con_labor_en_linea_a():
    sistema, _, _, linea_a = arbol_basico()
    franja = FranjaHoraria(Franja.MAÑANA, time(8, 0), time(12, 0))
    labor = Labor(10, "Revisar línea", "desc", 2, [], [], linea_a)
    sistema.registrar_labor(labor)
    sistema.registrar_capacidad_franja(CapacidadFranjaArea(linea_a, franja, 5))
    return sistema, labor, franja


def test_proponer_asignacion_rechaza_si_falta_una_credencial_heredada():
    sistema, labor, franja = sistema_con_labor_en_linea_a()
    sin_seguridad = trabajador_con(1, "Electricidad")
    sistema.registrar_trabajador(sin_seguridad)
    with pytest.raises(TrabajadorNoApto):
        sistema.proponer_asignacion(sin_seguridad, labor, franja, FECHA)
    assert sistema.asignaciones == []


def test_proponer_asignacion_acepta_si_tiene_las_heredadas():
    sistema, labor, franja = sistema_con_labor_en_linea_a()
    apto = trabajador_con(1, "Seguridad", "Electricidad")
    sistema.registrar_trabajador(apto)
    asignacion = sistema.proponer_asignacion(apto, labor, franja, FECHA)
    assert asignacion in sistema.asignaciones


def test_buscar_disponibles_descarta_a_quien_no_tiene_las_heredadas():
    sistema, labor, franja = sistema_con_labor_en_linea_a()
    apto = trabajador_con(1, "Seguridad", "Electricidad")
    no_apto = trabajador_con(2, "Electricidad")
    sistema.registrar_trabajador(apto)
    sistema.registrar_trabajador(no_apto)
    assert sistema.buscar_disponibles(labor, franja, FECHA) == [apto]
