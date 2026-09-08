import pytest
from datetime import date

from clases.credencial import Credencial


def construir_credencial():
    return Credencial(
        nombre="Seguridad Eléctrica",
        fecha_obtencion=date(2024, 1, 1),
        fecha_expiracion=date(2026, 1, 1),
    )


def test_creacion_credencial_valida():
    cred = construir_credencial()

    assert cred.nombre == "Seguridad Eléctrica"
    assert cred.fecha_obtencion == date(2024, 1, 1)
    assert cred.fecha_expiracion == date(2026, 1, 1)


def test_creacion_credencial_con_fechas_invertidas_lanza_valueerror():
    with pytest.raises(ValueError, match="fecha de obtención no puede ser posterior"):
        Credencial(
            nombre="Seguridad Eléctrica",
            fecha_obtencion=date(2026, 1, 1),
            fecha_expiracion=date(2024, 1, 1),
        )


def test_credencial_esta_activa_si_fecha_esta_dentro_del_rango():
    cred = construir_credencial()

    assert cred.esta_activa(date(2025, 1, 1)) is True


def test_credencial_no_esta_activa_si_fecha_esta_fuera_del_rango():
    cred = construir_credencial()

    assert cred.esta_activa(date(2023, 1, 1)) is False
    assert cred.esta_activa(date(2027, 1, 1)) is False
