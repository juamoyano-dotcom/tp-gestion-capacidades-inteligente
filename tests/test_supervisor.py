import pytest
from datetime import date, time

from clases.supervisor import Supervisor
from clases.asignacion import Asignacion
from clases.trabajador import Trabajador
from clases.labor import Labor
from clases.sectortrabajo import SectorTrabajo
from clases.franjahoraria import FranjaHoraria, Franja


def construir_supervisor():
    return Supervisor(
        id_trabajador=1,
        nombre="Juan",
        apellido="Pérez",
        fecha_nacimiento=date(1990, 1, 1),
        max_horas_semanales=40,
    )


def construir_trabajador():
    return Trabajador(
        id_trabajador=2,
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
        descripcion="Limpieza de una línea crítica.",
        duracion_horas=3,
        habilidades_requeridas=[],
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

    return Asignacion(
        id_asignacion=1,
        trabajador=trabajador,
        labor=labor,
        franja=franja,
        fecha=date(2025, 1, 1),
    )


def test_creacion_supervisor_valida():
    supervisor = construir_supervisor()

    assert supervisor.id_trabajador == 1
    assert supervisor.nombre == "Juan"
    assert supervisor.apellido == "Pérez"
    assert supervisor.max_horas_semanales == 40


def test_formalizar_asignacion_pendiente_cambia_estado_a_aprobada():
    supervisor = construir_supervisor()
    asignacion = construir_asignacion()

    resultado = supervisor.formalizar_asignacion(asignacion)

    assert resultado is asignacion
    assert asignacion.estado == "Aprobada"


def test_formalizar_asignacion_ya_aprobada_lanza_valueerror():
    supervisor = construir_supervisor()
    asignacion = construir_asignacion()
    asignacion.aprobar()

    with pytest.raises(ValueError, match="sólo se formalizan asignaciones 'Pendiente'"):
        supervisor.formalizar_asignacion(asignacion)
