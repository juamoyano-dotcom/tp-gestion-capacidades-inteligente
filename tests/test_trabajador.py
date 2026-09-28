import pytest
from datetime import date, time

from clases.trabajador import Trabajador
from clases.credencial import Credencial
from clases.asignacion import Asignacion
from clases.labor import Labor
from clases.sectortrabajo import SectorTrabajo
from clases.franjahoraria import FranjaHoraria, Franja

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
    assert trabajador.horas_de_trabajo == 0.0
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

    assert trabajador.horas_de_trabajo == 15


def test_resetear_horas_semanales_cambia_carga_a_cero():
    trabajador = construir_trabajador()
    trabajador.agregar_horas(12)

    trabajador.resetear_horas_semanales()

    assert trabajador.horas_de_trabajo == 0.0


def test_excede_horas_retorna_true_si_sobrepasa_maximo():
    trabajador = construir_trabajador()
    trabajador.agregar_horas(35)

    assert trabajador.excede_horas(10) is True


def test_excede_horas_retorna_false_si_no_sobrepasa_maximo():
    trabajador = construir_trabajador()
    trabajador.agregar_horas(30)

    assert trabajador.excede_horas(5) is False


def test_creacion_con_atributos_adicionales_los_guarda():
    trabajador = Trabajador(
        id_trabajador=3,
        nombre="Luis",
        apellido="Pérez",
        fecha_nacimiento=date(1995, 2, 2),
        max_horas_semanales=40,
        idioma="Portugués",
    )

    assert trabajador.obtener_atributo("idioma") == "Portugués"


def test_obtener_atributo_inexistente_devuelve_none_o_el_default():
    trabajador = construir_trabajador()

    assert trabajador.obtener_atributo("idioma") is None
    assert trabajador.obtener_atributo("idioma", "Español") == "Español"


def test_agregar_atributo_guarda_el_valor():
    trabajador = construir_trabajador()

    trabajador.agregar_atributo("idioma", "Portugués")

    assert trabajador.obtener_atributo("idioma") == "Portugués"


def test_agregar_atributo_sobrescribe_por_defecto():
    trabajador = construir_trabajador()
    trabajador.agregar_atributo("idioma", "Portugués")

    trabajador.agregar_atributo("idioma", "Inglés")

    assert trabajador.obtener_atributo("idioma") == "Inglés"


def test_agregar_atributo_sin_sobrescribir_lanza_valueerror_si_ya_existe():
    trabajador = construir_trabajador()
    trabajador.agregar_atributo("idioma", "Portugués")

    with pytest.raises(ValueError, match="ya existe"):
        trabajador.agregar_atributo("idioma", "Inglés", sobrescribir=False)

    assert trabajador.obtener_atributo("idioma") == "Portugués"


@pytest.mark.parametrize("clave", ["habilidades", "credenciales", "asignaciones", "max_horas_semanales"])
def test_agregar_atributo_con_clave_reservada_lanza_valueerror(clave):
    trabajador = construir_trabajador()

    with pytest.raises(ValueError, match="ya es un atributo o método"):
        trabajador.agregar_atributo(clave, "valor")


def test_creacion_con_kwarg_que_pisa_un_atributo_real_lanza_valueerror():
    with pytest.raises(ValueError, match="ya es un atributo o método"):
        Trabajador(
            id_trabajador=4,
            nombre="Ana",
            apellido="Gómez",
            fecha_nacimiento=date(1990, 1, 1),
            max_horas_semanales=40,
            habilidades=["Soldadura"],
        )


def test_agregar_asignacion_agrega_y_no_duplica():
    trabajador = construir_trabajador()
    sector = SectorTrabajo(id_sector=1, nombre="Mantenimiento", credenciales_obligatorias=[])
    labor = Labor(1, "Limpieza", "Limpieza de línea.", 3, [], [], sector)
    franja = FranjaHoraria(Franja.MAÑANA, time(8, 0), time(12, 0))
    asignacion = Asignacion(1, trabajador, labor, franja, date(2025, 1, 1))

    trabajador.agregar_asignacion(asignacion)
    trabajador.agregar_asignacion(asignacion)

    assert trabajador.asignaciones == [asignacion]
