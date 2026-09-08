import pytest
from datetime import date

from clases.trabajador import Trabajador
from clases.credencial import Credencial

def construir_trabajador():
    return Trabajador(
        id_trabajador=1,
        nombre="Ana",
        apellido="García",
        fecha_nacimiento=date(1990, 1, 1),
        max_horas_semanales=40,
    )


def test_creacion_trabajador_valida():
    trabajador = construir_trabajador()

    assert trabajador.id_trabajador == 1
    assert trabajador.nombre == "Ana"
    assert trabajador.apellido == "García"
    assert trabajador.fecha_nacimiento == date(1990, 1, 1)
    assert trabajador.max_horas_semanales == 40
    assert trabajador.horas_trabajadas == 0.0
    assert trabajador.habilidades == []
    assert trabajador.credenciales == []


def test_max_horas_semanales_invalido_lanza_error():
    with pytest.raises(ValueError, match="mayor a cero"):
        Trabajador(
            id_trabajador=2,
            nombre="Luis",
            apellido="Pérez",
            fecha_nacimiento=date(1995, 2, 2),
            max_horas_semanales=0,
        )


def test_agregar_habilidades_no_duplica():
    trabajador = construir_trabajador()

    trabajador.agregar_habilidades("Python")
    trabajador.agregar_habilidades("Python")

    assert trabajador.habilidades == ["Python"]


def test_agregar_credencial_agrega_credencial():
    trabajador = construir_trabajador()
    cred = Credencial("Seguridad Eléctrica", date(2024, 1, 1), date(2026, 1, 1))

    trabajador.agregar_credencial(cred)

    assert cred in trabajador.credenciales


def test_tiene_credencial_activa_retorna_true_si_esta_activa():
    trabajador = construir_trabajador()
    cred = Credencial("Seguridad Eléctrica", date(2024, 1, 1), date(2026, 1, 1))
    trabajador.agregar_credencial(cred)

    assert trabajador.tiene_credencial_activa("Seguridad Eléctrica", date(2025, 6, 1)) is True


def test_tiene_credencial_activa_retorna_false_si_esta_vencida():
    trabajador = construir_trabajador()
    cred = Credencial("Seguridad Eléctrica", date(2024, 1, 1), date(2024, 6, 1))
    trabajador.agregar_credencial(cred)

    assert trabajador.tiene_credencial_activa("Seguridad Eléctrica", date(2025, 6, 1)) is False


def test_tiene_habilidades_retorna_true_si_todas_estan():
    trabajador = construir_trabajador()
    trabajador.agregar_habilidades("Python")
    trabajador.agregar_habilidades("PLC")

    assert trabajador.tiene_habilidades(["Python", "PLC"]) is True


def test_tiene_habilidades_retorna_false_si_falta_una():
    trabajador = construir_trabajador()
    trabajador.agregar_habilidades("Python")

    assert trabajador.tiene_habilidades(["Python", "PLC"]) is False


def test_credenciales_activas_retorna_true_si_todas_estan_activas():
    trabajador = construir_trabajador()
    trabajador.agregar_credencial(Credencial("Seguridad Eléctrica", date(2024, 1, 1), date(2026, 1, 1)))
    trabajador.agregar_credencial(Credencial("Altura", date(2024, 1, 1), date(2026, 1, 1)))

    assert trabajador.credenciales_activas(["Seguridad Eléctrica", "Altura"], date(2025, 1, 1)) is True


def test_credenciales_activas_retorna_false_si_falta_una_activa():
    trabajador = construir_trabajador()
    trabajador.agregar_credencial(Credencial("Seguridad Eléctrica", date(2024, 1, 1), date(2024, 6, 1)))

    assert trabajador.credenciales_activas(["Seguridad Eléctrica"], date(2025, 1, 1)) is False


def test_agregar_horas_suma_carga_semanal():
    trabajador = construir_trabajador()

    trabajador.agregar_horas(10)
    trabajador.agregar_horas(5)

    assert trabajador.horas_trabajadas == 15


def test_resetear_horas_semanales_cambia_carga_a_cero():
    trabajador = construir_trabajador()
    trabajador.agregar_horas(12)

    trabajador.resetear_horas_semanales()

    assert trabajador.horas_trabajadas == 0.0


def test_excede_horas_retorna_true_si_sobrepasa_maximo():
    trabajador = construir_trabajador()
    trabajador.agregar_horas(35)

    assert trabajador.excede_horas(10) is True


def test_excede_horas_retorna_false_si_no_sobrepasa_maximo():
    trabajador = construir_trabajador()
    trabajador.agregar_horas(30)

    assert trabajador.excede_horas(5) is False
