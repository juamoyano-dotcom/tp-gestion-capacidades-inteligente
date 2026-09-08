import pytest
from datetime import time

from clases.franjahoraria import FranjaHoraria, Franja


def construir_franja_horaria():
    return FranjaHoraria(
        franja=Franja.MAÑANA,
        hora_inicio=time(8, 0),
        hora_fin=time(12, 0),
    )


def test_creacion_franja_horaria_valida():
    franja_horaria = construir_franja_horaria()

    assert franja_horaria.franja == Franja.MAÑANA
    assert franja_horaria.hora_inicio == time(8, 0)
    assert franja_horaria.hora_fin == time(12, 0)


def test_hora_inicio_igual_hora_fin_lanza_error():
    with pytest.raises(ValueError, match="debe ser distinta"):
        FranjaHoraria(
            franja=Franja.MAÑANA,
            hora_inicio=time(8, 0),
            hora_fin=time(8, 0),
        )


def test_eq_retorna_true_si_franjas_son_iguales():
    franja_1 = FranjaHoraria(
        franja=Franja.MAÑANA,
        hora_inicio=time(8, 0),
        hora_fin=time(12, 0),
    )

    franja_2 = FranjaHoraria(
        franja=Franja.MAÑANA,
        hora_inicio=time(8, 0),
        hora_fin=time(12, 0),
    )

    assert franja_1 == franja_2


def test_eq_retorna_false_si_franjas_son_distintas():
    franja_1 = FranjaHoraria(
        franja=Franja.MAÑANA,
        hora_inicio=time(8, 0),
        hora_fin=time(12, 0),
    )

    franja_2 = FranjaHoraria(
        franja=Franja.TARDE,
        hora_inicio=time(13, 0),
        hora_fin=time(17, 0),
    )

    assert franja_1 != franja_2


def test_hash_retorna_mismo_valor_si_franjas_son_iguales():
    franja_1 = FranjaHoraria(
        franja=Franja.MAÑANA,
        hora_inicio=time(8, 0),
        hora_fin=time(12, 0),
    )

    franja_2 = FranjaHoraria(
        franja=Franja.MAÑANA,
        hora_inicio=time(8, 0),
        hora_fin=time(12, 0),
    )

    assert hash(franja_1) == hash(franja_2)


def test_repr_retorna_descripcion_de_franja():
    franja_horaria = construir_franja_horaria()

    assert repr(franja_horaria) == "FranjaHoraria(Mañana)"