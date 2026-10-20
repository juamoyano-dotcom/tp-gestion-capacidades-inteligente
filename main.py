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

    labor_2 = Labor(
        id_labor=11,
        titulo="Calibración de sensores",
        descripcion="Se deben calibrar los sensores de la línea de ensamble.",
        duracion_horas=2,
        habilidades_requeridas=["Python"],
        credenciales_requeridas=["Seguridad Eléctrica"],
        sector=sector,
    )

    sistema.registrar_area(sector)
    sistema.registrar_trabajador(trabajador_1)
    sistema.registrar_trabajador(trabajador_2)
    sistema.registrar_labor(labor)
    sistema.registrar_labor(labor_2)
    sistema.registrar_capacidad_franja(CapacidadFranjaArea(sector, franja, 2))

    return sistema, sector, franja, trabajador_1, trabajador_2, supervisor, labor, labor_2


def main():
    print("=== Sistema de Gestión de Capacidades y Asignación Inteligente ===")
    print("\nSe configura un escenario realista con trabajadores, sector, labor y capacidad por franja.")

    sistema, sector, franja, trabajador_1, trabajador_2, supervisor, labor, labor_2 = crear_demo()

    print(f"\nÁrea registrada: {sector.nombre}")
    print(f"Franja activa: {franja.franja.descripcion} ({franja.hora_inicio} a {franja.hora_fin})")
    print(f"Trabajadores registrados: {len(sistema.trabajadores)}")
    print(f"Labor disponible: {labor.titulo} ({labor.duracion_horas} hs)")

    disponibles = sistema.buscar_disponibles(labor, franja, date(2026, 10, 6))
    print(f"\nTrabajadores disponibles para la labor en esa fecha y franja: {[t.nombre for t in disponibles]}")

    print("\nPaso 1: El sistema propone dos asignaciones. Cada una entra al final de la cola de pendientes.")
    asignacion = sistema.proponer_asignacion(
        trabajador_1,
        labor,
        franja,
        date(2026, 10, 6),
    )
    asignacion_2 = sistema.proponer_asignacion(
        trabajador_1,
        labor_2,
        franja,
        date(2026, 10, 7),
    )
    print(f"Asignación creada: {asignacion}")
    print(f"Asignación creada: {asignacion_2}")
    print(f"Estado actual de la primera: {asignacion.estado.value}")
    print(f"Horas comprometidas en la semana del trabajador: {sistema.horas_comprometidas(trabajador_1, date(2026, 10, 6))}")
    print(f"Primera de la cola (la que se resolverá antes): {sistema.cola_pendientes.inicio()}")

    print("\nPaso 2: Las asignaciones quedan pendientes hasta que un supervisor las resuelve.")
    print(f"Antes de la aprobación, las asignaciones del trabajador son: {trabajador_1.asignaciones}")

    print("\nPaso 3: El supervisor procesa la cola, de la más antigua a la más nueva.")
    resuelta = sistema.procesar_siguiente(supervisor)
    while resuelta is not None:
        print(f"Resuelta: {resuelta}")
        resuelta = sistema.procesar_siguiente(supervisor)
    print(f"Trabajador luego de la aprobación: {trabajador_1.asignaciones}")

    print("\n=== Resumen final ===")
    print(f"- Estado final de las asignaciones: {asignacion.estado.value}, {asignacion_2.estado.value}")
    print(f"- Horas registradas para la semana: {sistema.horas_comprometidas(trabajador_1, date(2026, 10, 6))}")
    print(f"- Cantidad de asignaciones en el sistema: {len(sistema.asignaciones)}")


if __name__ == "__main__":
    main()