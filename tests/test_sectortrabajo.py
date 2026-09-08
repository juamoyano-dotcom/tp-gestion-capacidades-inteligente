import pytest
from datetime import date

from clases.sectortrabajo import SectorTrabajo
from clases.trabajador import Trabajador
from clases.credencial import Credencial


def construir_sector():
    return SectorTrabajo(
        id_sector=1,
        nombre="Mantenimiento",
        credenciales_obligatorias=["Seguridad Eléctrica"],
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


def test_creacion_sector_valida():
    sector = construir_sector()

    assert sector.id == 1
    assert sector.nombre == "Mantenimiento"
    assert sector.credenciales_obligatorias == ["Seguridad Eléctrica"]
    assert sector.limite_personal == 5


def test_creacion_sector_con_limite_personal_negativo_lanza_valueerror():
    with pytest.raises(ValueError, match="no puede ser negativo"):
        SectorTrabajo(
            id_sector=2,
            nombre="Electricidad",
            credenciales_obligatorias=["Seguridad Eléctrica"],
            limite_personal=-1,
        )


def test_trabajador_cumple_credenciales_true_si_todas_activas():
    sector = construir_sector()
    trabajador = construir_trabajador()
    trabajador.agregar_credencial(Credencial("Seguridad Eléctrica", date(2024, 1, 1), date(2026, 1, 1)))

    assert sector.trabajador_cumple_credenciales(trabajador, date(2025, 1, 1)) is True


def test_trabajador_cumple_credenciales_false_si_falta_credencial_activa():
    sector = construir_sector()
    trabajador = construir_trabajador()
    trabajador.agregar_credencial(Credencial("Seguridad Eléctrica", date(2024, 1, 1), date(2024, 6, 1)))

    assert sector.trabajador_cumple_credenciales(trabajador, date(2025, 1, 1)) is False


def test_trabajador_cumple_credenciales_false_si_sector_no_tiene_credenciales_obligatorias():
    sector = SectorTrabajo(
        id_sector=3,
        nombre="Limpieza",
        credenciales_obligatorias=[],
        limite_personal=2,
    )
    trabajador = construir_trabajador()

    assert sector.trabajador_cumple_credenciales(trabajador, date(2025, 1, 1)) is True
