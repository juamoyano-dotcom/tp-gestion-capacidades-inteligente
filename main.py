from datetime import date, time

from clases import (
    CapacidadFranjaArea,
    Credencial,
    Franja,
    FranjaHoraria,
    Labor,
    SectorTrabajo,
    SistemaGestion,
    Supervisor,
    Trabajador,
)


def crear_demo():
    sistema = SistemaGestion()

    sector = SectorTrabajo(
        id_sector=1,
        nombre="Planta de Ensamble Robótico",
        credenciales_obligatorias=["Seguridad Eléctrica"],
    )

    franja = FranjaHoraria(
        franja=Franja.MAÑANA,
        hora_inicio=time(8, 0),
        hora_fin=time(12, 0),
    )

    trabajador_1 = Trabajador(
        id_trabajador=1,
        nombre="Ana",
        apellido="García",
        fecha_nacimiento=date(1990, 1, 15),
        max_horas_semanales=40,
    )
    trabajador_1.agregar_habilidades("Python")
    trabajador_1.agregar_habilidades("Mantenimiento eléctrico")
    trabajador_1.agregar_credencial(
        Credencial("Seguridad Eléctrica", date(2024, 1, 1), date(2027, 1, 1))
    )

    trabajador_2 = Trabajador(
        id_trabajador=2,
        nombre="Luis",
        apellido="Pérez",
        fecha_nacimiento=date(1993, 5, 10),
        max_horas_semanales=30,
    )
    trabajador_2.agregar_habilidades("Python")
    trabajador_2.agregar_habilidades("Control de procesos")
    trabajador_2.agregar_credencial(
        Credencial("Seguridad Eléctrica", date(2023, 6, 1), date(2026, 6, 1))
    )

    supervisor = Supervisor(
        id_trabajador=99,
        nombre="María",
        apellido="López",
        fecha_nacimiento=date(1986, 3, 20),
        max_horas_semanales=45,
    )

    labor = Labor(
        id_labor=10,
        titulo="Revisión de tablero eléctrico",
        descripcion="Se debe validar el estado físico y eléctrico del tablero principal.",
        duracion_horas=3,
        habilidades_requeridas=["Python", "Mantenimiento eléctrico"],
        credenciales_requeridas=["Seguridad Eléctrica"],
        sector=sector,
    )

    sistema.registrar_area(sector)
    sistema.registrar_trabajador(trabajador_1)
    sistema.registrar_trabajador(trabajador_2)
    sistema.registrar_labor(labor)
    sistema.registrar_capacidad_franja(CapacidadFranjaArea(sector, franja, 2))

    return sistema, sector, franja, trabajador_1, trabajador_2, supervisor, labor


def main():
    print("=== Sistema de Gestión de Capacidades y Asignación Inteligente ===")
    print("\nSe configura un escenario realista con trabajadores, sector, labor y capacidad por franja.")

    sistema, sector, franja, trabajador_1, trabajador_2, supervisor, labor = crear_demo()

    print(f"\nÁrea registrada: {sector.nombre}")
    print(f"Franja activa: {franja.franja.descripcion} ({franja.hora_inicio} a {franja.hora_fin})")
    print(f"Trabajadores registrados: {len(sistema.trabajadores)}")
    print(f"Labor disponible: {labor.titulo} ({labor.duracion_horas} hs)")

    disponibles = sistema.buscar_disponibles(labor, franja, date(2026, 10, 6))
    print(f"\nTrabajadores disponibles para la labor en esa fecha y franja: {[t.nombre for t in disponibles]}")

    print("\nPaso 1: El sistema propone la asignación.")
    asignacion = sistema.proponer_asignacion(
        trabajador_1,
        labor,
        franja,
        date(2026, 10, 6),
    )
    print(f"Asignación creada: {asignacion}")
    print(f"Estado actual: {asignacion.estado.value}")
    print(f"Horas comprometidas en la semana del trabajador: {sistema.horas_comprometidas(trabajador_1, date(2026, 10, 6))}")

    print("\nPaso 2: La asignación queda pendiente hasta que un supervisor la formaliza.")
    print(f"Antes de la aprobación, las asignaciones del trabajador son: {trabajador_1.asignaciones}")

    print("\nPaso 3: El supervisor aprueba la asignación.")
    supervisor.formalizar_asignacion(asignacion)
    print(f"Asignación final: {asignacion}")
    print(f"Trabajador luego de la aprobación: {trabajador_1.asignaciones}")

    print("\n=== Resumen final ===")
    print(f"- Estado final de la asignación: {asignacion.estado.value}")
    print(f"- Horas registradas para la semana: {sistema.horas_comprometidas(trabajador_1, date(2026, 10, 6))}")
    print(f"- Cantidad de asignaciones en el sistema: {len(sistema.asignaciones)}")


if __name__ == "__main__":
    main()