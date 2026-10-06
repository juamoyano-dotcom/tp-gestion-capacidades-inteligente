class ErrorAsignacion(Exception):
    """Base de los rechazos de negocio al proponer una asignación."""


class CapacidadNoConfigurada(ErrorAsignacion):
    """No hay CapacidadFranjaArea registrada para el área y la franja (regla 6)."""


class LaborYaAsignada(ErrorAsignacion):
    """La labor ya tiene una asignación en esa fecha y franja (regla 7)."""


class TrabajadorOcupado(ErrorAsignacion):
    """El trabajador ya tiene otra asignación en esa fecha y franja."""


class TrabajadorNoApto(ErrorAsignacion):
    """Faltan habilidades o credenciales activas, de la labor o del área (reglas 4 y 10)."""


class CargaHorariaExcedida(ErrorAsignacion):
    """La labor haría superar el máximo de horas semanales (regla 5)."""


class FranjaCompleta(ErrorAsignacion):
    """El área ya alcanzó su límite de personal en esa franja (regla 6)."""