import pytest
from datetime import date, time

from clases.asignacion import Asignacion
from clases.trabajador import Trabajador
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


def construir_sector():
    return SectorTrabajo(
        id_sector=1,
        nombre="Mantenimiento",
        credenciales_obligatorias=[],
        limite_personal=5,
    )


def construir_labor(sector):
    return Labor(
        id_labor=1,
        titulo="Limpieza de líneas",
        descripcion="Se limpia una línea crítica.",
        duracion_horas=3,
        habilidades_requeridas=["Python"],
        credenciales_requeridas=[],
        sector=sector,
    )


def construir_franja():
    return FranjaHoraria(
        franja=Franja.MAÑANA,
        hora_inicio=time(8, 0),
        hora_fin=time(12, 0),
    )


def construir_asignacion():
    trabajador = construir_trabajador()
    sector = construir_sector()
    labor = construir_labor(sector)
    franja = construir_franja()

    trabajador.agregar_habilidades("Python")

    return Asignacion(
        id_asignacion=1,
        trabajador=trabajador,
        labor=labor,
        franja=franja,
        fecha=date(2025, 1, 1),
    )


def test_creacion_asignacion_valida():
    asignacion = construir_asignacion()

    assert asignacion.id_asignacion == 1
    assert asignacion.trabajador.nombre == "Ana"
    assert asignacion.labor.titulo == "Limpieza de líneas"
    assert asignacion.franja.franja == Franja.MAÑANA
    assert asignacion.fecha == date(2025, 1, 1)
    assert asignacion.estado == "Pendiente"
    assert asignacion.horas_asignadas == 3


def test_aprobar_asignacion_cambia_estado_a_aprobada():
    asignacion = construir_asignacion()

    asignacion.aprobar()

    assert asignacion.estado == "Aprobada"


def test_formalizar_asignacion_solo_puede_hacerse_si_esta_pendiente():
    asignacion = construir_asignacion()
    asignacion.aprobar()

    with pytest.raises(ValueError, match="sólo se formalizan asignaciones 'Pendiente'"):
        from clases.supervisor import Supervisor
        supervisor = Supervisor(
            id_trabajador=2,
            nombre="José",
            apellido="López",
            fecha_nacimiento=date(1991, 1, 1),
            max_horas_semanales=40,
        )
        supervisor.formalizar_asignacion(asignacion)
