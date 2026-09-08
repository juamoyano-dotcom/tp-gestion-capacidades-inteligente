import pytest

from clases.capacidadfranja import CapacidadFranjaArea
from clases.sectortrabajo import SectorTrabajo
from clases.franjahoraria import FranjaHoraria, Franja
from datetime import time


def construir_sector():
    return SectorTrabajo(
        id_sector=1,
        nombre="Mantenimiento",
        credenciales_obligatorias=[],
        limite_personal=5,
    )


def construir_franja():
    return FranjaHoraria(
        franja=Franja.MAÑANA,
        hora_inicio=time(8, 0),
        hora_fin=time(12, 0),
    )


def construir_capacidad():
    sector = construir_sector()
    franja = construir_franja()
    return CapacidadFranjaArea(
        area=sector,
        franja=franja,
        limite_personal=3,
    )


def test_creacion_capacidad_valida():
    capacidad = construir_capacidad()

    assert capacidad.area.nombre == "Mantenimiento"
    assert capacidad.franja.franja == Franja.MAÑANA
    assert capacidad.limite_personal == 3


def test_creacion_capacidad_con_limite_personal_cero_o_negativo_lanza_valueerror():
    sector = construir_sector()
    franja = construir_franja()

    with pytest.raises(ValueError, match="mayor a cero"):
        CapacidadFranjaArea(
            area=sector,
            franja=franja,
            limite_personal=0,
        )


def test_tiene_capacidad_true_si_ocupacion_es_menor_al_limite():
    capacidad = construir_capacidad()

    assert capacidad.tiene_capacidad(2) is True


def test_tiene_capacidad_false_si_ocupacion_alcanza_el_limite():
    capacidad = construir_capacidad()

    assert capacidad.tiene_capacidad(3) is False
