# Sistema de Gestión de Capacidades y Asignación Inteligente

## Descripción general

Este proyecto implementa un sistema para gestionar trabajadores, habilidades, credenciales, labores y asignaciones dentro de distintas áreas de trabajo.

El sistema permite:

- Registrar trabajadores y sus capacidades.
- Gestionar credenciales profesionales y su vigencia.
- Definir labores con requisitos específicos.
- Controlar la disponibilidad y capacidad de las áreas.
- Crear asignaciones de trabajadores a labores.
- Controlar la carga horaria semanal.
- Validar y aprobar asignaciones mediante supervisores.

No se utiliza pandas; la información se administra mediante clases, listas y diccionarios de Python.

---

## Estructura del proyecto

Las clases principales se encuentran dentro del paquete `clases`:

- `FranjaHoraria`
- `Trabajador`
- `Asignacion`
- `CapacidadFranjaArea`
- `Credencial`
- `Labor`
- `SectorTrabajo`
- `SistemaGestion`
- `Supervisor`
- `Excepciones`

El archivo `clases/__init__.py` importa y expone todas las clases del paquete para facilitar su utilización desde otros módulos.

---

## Responsabilidades de las clases

### `FranjaHoraria`

Representa una franja de trabajo. La enumeración `Franja` define `MAÑANA`, `TARDE` y `NOCHE`.

Sus responsabilidades son:

- Identificar la categoría de franja (`MAÑANA`, `TARDE` o `NOCHE`).
- Guardar su hora de inicio y fin y rechazar franjas con la misma hora de inicio y fin.
- Considerar iguales dos objetos `FranjaHoraria` si tienen la misma categoría, independientemente de sus horas.
- Permitir asociar una asignación con una franja horaria.

---

### `Trabajador`

Representa a una persona disponible para realizar labores.

Sus responsabilidades son:

- Almacenar sus datos identificatorios.
- Mantener sus habilidades o competencias, credenciales profesionales y asignaciones aprobadas.
- Registrar el límite máximo de horas semanales.
- Permitir consultar si posee las habilidades y las credenciales requeridas y vigentes en una fecha.
- Permitir agregar y consultar atributos adicionales sin sobrescribir nombres de atributos o métodos propios.
- Validar que el máximo de horas semanales sea mayor que cero al crear o modificar el límite.

El trabajador no calcula ni almacena las horas semanales ya comprometidas. `SistemaGestion` las calcula a partir de las asignaciones aprobadas para la semana consultada.

---

### `Supervisor`

Es una subclase de `Trabajador` con facultades adicionales.

Además de poseer las capacidades de un trabajador, sus responsabilidades son:

- Formalizar asignaciones pendientes, cambiándolas a `Aprobada`.
- Rechazar asignaciones pendientes, guardando el motivo del rechazo.

Un supervisor puede realizar labores como cualquier otro trabajador. Para la aprobación con revalidación y limpieza en cascada de propuestas conflictivas, debe usarse `SistemaGestion.aprobar_asignacion`; llamar directamente a `formalizar_asignacion` solo cambia el estado y registra la asignación en el trabajador.

---

### `Credencial`

Representa una certificación o autorización profesional.

Sus responsabilidades son:

- Almacenar el nombre de la credencial.
- Registrar la fecha de obtención y la fecha de vencimiento.
- Rechazar fechas de obtención posteriores a la fecha de vencimiento.
- Determinar si está activa en una fecha determinada, considerando inclusivas ambas fechas.

`Trabajador` utiliza esta información para validar las credenciales requeridas por una labor o por un sector en la fecha de la asignación.

---

### `Labor`

Representa una tarea que debe ser realizada por un trabajador.

Sus responsabilidades son:

- Identificar la labor.
- Almacenar su título y descripción.
- Registrar su duración estimada en horas.
- Definir las habilidades necesarias.
- Definir las credenciales requeridas.
- Asociar la labor con un sector o área de trabajo.
- Indicar su frecuencia (`DIARIA` o `SEMANAL`)
- Proporcionar la validación de habilidades y credenciales propias de la labor.

La duración debe ser mayor que cero. La labor comprueba los requisitos que le corresponden; `SistemaGestion` coordina además la validación de credenciales del sector, disponibilidad y carga.

---

### `SectorTrabajo`

Representa un área física o funcional donde se realizan labores.

Sus responsabilidades son:

- Identificar el sector de trabajo.
- Almacenar su nombre o descripción.
- Mantener las credenciales obligatorias para trabajar en el área.
- Delegar la validación de sus credenciales obligatorias a `Trabajador`.

Además de los requisitos de una labor, el trabajador debe contar con todas las credenciales obligatorias del sector.

---

### `CapacidadFranjaArea`

Representa la capacidad máxima de trabajadores permitida para una combinación de sector y franja horaria.

Sus responsabilidades son:

- Asociar un sector con una franja horaria.
- Definir un límite de personal mayor que cero para esa combinación.
- Indicar si la ocupación actual está por debajo del límite.

No almacena ni contabiliza la ocupación. `SistemaGestion` cuenta las asignaciones aprobadas del sector, franja y fecha, y utiliza esta clase para comprobar si queda capacidad.

---

### `Asignacion`

Representa la propuesta o confirmación de un trabajador para realizar una labor.

Sus responsabilidades son:

- Identificar la asignación.
- Asociar un trabajador, una labor, una franja y una fecha.
- Iniciar con estado `Pendiente`.
- Guardar las horas asignadas con la duración de la labor al momento de crearla.
- Permitir la aprobación o el rechazo por un `Supervisor` solo mientras esté pendiente.
- Guardar el motivo cuando se rechaza.
- Agregar la asignación al historial del trabajador cuando se aprueba.
- Mostrar en su representación textual el trabajador, la labor, la fecha, la franja y el estado.

Una asignación puede estar `Pendiente`, `Aprobada` o `Rechazada`. Mientras está pendiente forma parte de `SistemaGestion.asignaciones`, pero no reserva recursos ni se agrega a la lista del trabajador.

---

### `EstadoAsignacion`

Enumera los estados posibles de una asignación: `PENDIENTE`, `APROBADA` y `RECHAZADA`. `Asignacion` y `SistemaGestion` utilizan estos estados para controlar las transiciones y determinar qué asignaciones ocupan recursos.

---

### `Frecuencia`

Enumera las frecuencias admitidas para una labor: `DIARIA` y `SEMANAL`. La frecuencia determina el período en que `SistemaGestion` contabiliza cuántos trabajadores ya fueron asignados a esa labor.

---

### `ErrorAsignacion` y excepciones derivadas

Representan rechazos de reglas de negocio al proponer, comprobar o aprobar asignaciones. `ErrorAsignacion` es la excepción base; sus especializaciones identifican falta de capacidad configurada, labor cubierta, trabajador ocupado o no apto, exceso de horas y franja completa. Así, `buscar_disponibles` puede excluir candidatos que incumplen estas reglas sin ocultar errores ajenos a ellas.

---

### `SistemaGestion`

Es el componente principal de coordinación y reglas de negocio.

Sus responsabilidades son:

- Registrar trabajadores, labores y sectores, sin permitir identificadores
  duplicados.
- Registrar capacidades por sector y franja, sin duplicar una combinación.
- Validar que los objetos usados en una asignación estén registrados.
- Verificar las habilidades y credenciales vigentes requeridas por la labor y el sector.
- Comprobar conflictos contra las asignaciones aprobadas: trabajador ocupado en la fecha y franja, labor ya cubierta en su período, límite semanal de horas y capacidad del sector/franja/fecha.
- Proponer asignaciones en estado `Pendiente`, evitando duplicar una propuesta pendiente idéntica.
- Revalidar una propuesta pendiente al aprobarla, porque el sistema puede haber cambiado desde que se creó.
- Después de una aprobación, rechazar automáticamente las propuestas pendientes que hayan quedado en conflicto, guardando el motivo.
- Buscar trabajadores disponibles aplicando los mismos requisitos y conflictos de una propuesta.
- Consultar asignaciones aprobadas o pendientes, labores aún por cubrir y trabajadores con horas disponibles.
- Calcular la ocupación y las horas comprometidas a partir de las asignaciones aprobadas, sin mantener contadores duplicados.

Las horas se calculan por semana calendario, de lunes a domingo. Para cubrir una labor, el sistema cuenta las asignaciones aprobadas de esa labor dentro del período: el día de la fecha para frecuencia diaria y la semana de lunes a domingo para frecuencia semanal. La ocupación de capacidad, en cambio, se calcula para una fecha concreta y una categoría de franja.

Los supervisores, credenciales y franjas se crean como objetos y se utilizan al registrar o validar otras entidades; no tienen registros independientes dentro del sistema.

---

## Flujo de creación de una asignación

Al proponer una asignación, el sistema:

1. Valida los parámetros y que el trabajador, la labor y el sector estén registrados.
2. Rechaza una propuesta pendiente idéntica para el mismo trabajador, labor, fecha y franja.
3. Comprueba las habilidades y credenciales vigentes exigidas por la labor y el sector.
4. Crea una asignación candidata y verifica que no entre en conflicto con lo ya aprobado: ocupación del trabajador, cobertura de la labor en su período, máximo semanal de horas y capacidad configurada/disponible.
5. Si pasa las validaciones, la agrega a `SistemaGestion.asignaciones` en estado `Pendiente`.

Las propuestas pendientes no reservan horas, cupos ni exclusividad y no bloquean otras propuestas. Por eso pueden coexistir alternativas; solo las asignaciones aprobadas cuentan para los límites y la ocupación.

Al aprobar, se usa `SistemaGestion.aprobar_asignacion`: este vuelve a comprobar los conflictos contra las aprobadas, formaliza la asignación y luego revisa las propuestas pendientes restantes. Las que ya no son válidas se rechazan automáticamente con el motivo correspondiente. Las horas y la ocupación se calculan desde las aprobadas, por lo que las rechazadas y las pendientes no se contabilizan.

---

## Relaciones principales

- Un `Trabajador` puede tener varias `Credencial` y `Asignacion` aprobadas.
- Una `Labor` pertenece a un `SectorTrabajo`, requiere habilidades y credenciales, tiene una frecuencia y define cuántos trabajadores requiere.
- `SistemaGestion` puede registrar varias `CapacidadFranjaArea`.
- Una `CapacidadFranjaArea` relaciona un `SectorTrabajo` con una `FranjaHoraria` y un límite de personal.
- Una `Asignacion` relaciona un `Trabajador`, una `Labor`, una `FranjaHoraria` y una fecha; su estado determina si participa en los cálculos de recursos.
- Un `Supervisor` es un trabajador con permisos adicionales.
- `SistemaGestion` administra las entidades registradas y las reglas del sistema.

---

## Archivo `clases/__init__.py`

El archivo `__init__.py` expone las clases, enumeraciones y excepciones del paquete para permitir importarlas de forma centralizada desde otros módulos.

---
