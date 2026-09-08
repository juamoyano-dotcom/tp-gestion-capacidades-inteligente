import pytest
from datetime import date

from clases.labor import Labor
from clases.sectortrabajo import SectorTrabajo
from clases.trabajador import Trabajador
from clases.credencial import Credencial


def construir_sector():
    return SectorTrabajo(
        id_sector=1,
        nombre="Mantenimiento",
        credenciales_obligatorias=[],
        limite_personal=5,
    )


def construir_trabajador():
    return Trabajador(
        id_trabajador=1,
        nombre="Ana",
        apellido="García",
        fecha_nacimiento=date(1990, 1, 1),
        max_horas_semanales=40,
    )


def construir_labor(sector=None):
    if sector is None:
        sector = construir_sector()

    return Labor(
        id_labor=1,
        titulo="Limpieza de líneas",
        descripcion="Limpieza de una línea crítica.",
        duracion_horas=3,
        habilidades_requeridas=["Python"],
        credenciales_requeridas=["Seguridad Eléctrica"],
        sector=sector,
    )


def test_creacion_labor_valida():
    sector = construir_sector()
    labor = construir_labor(sector)

    assert labor.id_labor == 1
    assert labor.titulo == "Limpieza de líneas"
    assert labor.descripcion == "Limpieza de una línea crítica."
    assert labor.duracion_horas == 3
    assert labor.habilidades_requeridas == ["Python"]
    assert labor.credenciales_requeridas == ["Seguridad Eléctrica"]
    assert labor.sector == sector


def test_creacion_labor_con_duracion_invalida_lanza_valueerror():
    sector = construir_sector()

    with pytest.raises(ValueError, match="duración de la labor debe ser mayor a cero"):
        Labor(
            id_labor=2,
            titulo="No válida",
            descripcion="Duración negativa",
            duracion_horas=0,
            habilidades_requeridas=["Python"],
            credenciales_requeridas=[],
            sector=sector,
        )


def test_trabajador_es_apto_true_si_tiene_habilidad_y_credencial_activa():
    sector = construir_sector()
    labor = construir_labor(sector)
    trabajador = construir_trabajador()

    trabajador.agregar_habilidades("Python")
    trabajador.agregar_credencial(Credencial("Seguridad Eléctrica", date(2024, 1, 1), date(2026, 1, 1)))

    assert labor.trabajador_es_apto(trabajador, date(2025, 1, 1)) is True


def test_trabajador_es_apto_false_si_falta_habilidad():
    sector = construir_sector()
    labor = construir_labor(sector)
    trabajador = construir_trabajador()

    trabajador.agregar_credencial(Credencial("Seguridad Eléctrica", date(2024, 1, 1), date(2026, 1, 1)))

    assert labor.trabajador_es_apto(trabajador, date(2025, 1, 1)) is False


def test_trabajador_es_apto_false_si_falta_credencial_activa():
    sector = construir_sector()
    labor = construir_labor(sector)
    trabajador = construir_trabajador()

    trabajador.agregar_habilidades("Python")
    trabajador.agregar_credencial(Credencial("Seguridad Eléctrica", date(2024, 1, 1), date(2024, 6, 1)))

    assert labor.trabajador_es_apto(trabajador, date(2025, 1, 1)) is False
