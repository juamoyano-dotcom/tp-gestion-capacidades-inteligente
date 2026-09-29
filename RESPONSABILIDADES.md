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

El archivo `clases/__init__.py` importa y expone todas las clases del paquete para facilitar su utilización desde otros módulos.

---

## Responsabilidades de las clases

### `FranjaHoraria`

Representa una franja de trabajo. La enumeración `Franja` define `MAÑANA`, `TARDE` y `NOCHE`.

Sus responsabilidades son:

- Identificar la franja horaria.
- Representar las franjas como mañana, tarde o noche.
- Permitir asociar una asignación con un período horario determinado.

No controla asignaciones ni capacidad; esos controles los realiza `SistemaGestion` mediante `CapacidadFranjaArea`.

---

### `Trabajador`

Representa a una persona disponible para realizar labores.

Sus responsabilidades son:

- Almacenar sus datos identificatorios.
- Mantener sus habilidades o competencias y sus credenciales profesionales.
- Registrar el límite máximo de horas semanales.
- Llevar el control de las horas ya asignadas.
- Permitir verificar si es apto para una labor.
- Permitir comprobar si posee las credenciales requeridas y vigentes.
- Controlar que una nueva asignación no supere su carga horaria máxima.

El trabajador no calcula ni almacena sus horas semanales. `SistemaGestion` las calcula a partir de las asignaciones del sistema para la semana consultada.

---

### `Supervisor`

Es una subclase de `Trabajador` con facultades adicionales.

Además de poseer las capacidades de un trabajador, sus responsabilidades son:

- Validar asignaciones pendientes.
- Formalizar una asignación cambiando estado de `Pendiente` a `Aprobada`.

Un supervisor puede realizar labores como cualquier otro trabajador, pero también puede aprobar asignaciones.

---

### `Credencial`

Representa una certificación o autorización profesional.

Sus responsabilidades son:

- Almacenar el nombre de la credencial.
- Registrar la fecha de obtención y la fecha de vencimiento.
- Determinar si la credencial está activa en una fecha determinada.
- Permitir validar si un trabajador puede realizar una labor o trabajar en un área.

Una credencial se considera válida únicamente cuando se encuentra vigente en la fecha de la asignación.

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
- Proporcionar la información necesaria para determinar si un trabajador es apto.

Una labor solo puede asignarse a un trabajador que cumpla todos sus requisitos.

---

### `SectorTrabajo`

Representa un área física o funcional donde se realizan labores.

Sus responsabilidades son:

- Identificar el sector de trabajo.
- Almacenar su nombre o descripción.
- Mantener las credenciales obligatorias para trabajar en el área.
- Asociar capacidades máximas de personal a sus franjas horarias.
- Permitir validar si un trabajador cumple los requisitos específicos del sector.

Además de los requisitos de una labor, el trabajador debe contar con todas las credenciales obligatorias del sector.

---

### `CapacidadFranjaArea`

Representa la capacidad máxima de trabajadores permitida para una combinación de sector y franja horaria.

Sus responsabilidades son:

- Asociar un sector con una franja horaria.
- Definir la cantidad máxima de trabajadores permitidos.
- Contabilizar las asignaciones existentes.
- Determinar si todavía hay capacidad disponible.
- Impedir nuevas asignaciones cuando la franja se encuentra completa.

`SistemaGestion` contabiliza las asignaciones existentes y utiliza esta clase para impedir superar el límite del área y la franja.

---

### `Asignacion`

Representa la propuesta o confirmación de un trabajador para realizar una labor.

Sus responsabilidades son:

- Identificar la asignación.
- Asociar un trabajador, una labor, una franja y una fecha.
- Iniciar con estado `Pendiente`.
- Obtener sus horas de la duración definida para la labor.
- Cambiar a `Aprobada` únicamente cuando la aprueba un `Supervisor`.
- Agregar la asignación aprobada a la lista del trabajador.
- Mostrar en su representación textual el trabajador, la labor, la fecha, la franja y el estado.

Mientras está pendiente, la propuesta ya forma parte de `SistemaGestion.asignaciones` y cuenta para capacidad, exclusividad y horas semanales.

---

### `SistemaGestion`

Es el componente principal de coordinación y reglas de negocio.

Sus responsabilidades son:

- Registrar trabajadores, labores y sectores, sin permitir identificadores
  duplicados.
- Registrar capacidades por sector y franja, sin duplicar una combinación.
- Validar que los objetos usados en una asignación estén registrados.
- Verificar habilidades y credenciales activas de la labor y del sector.
- Controlar la carga horaria semanal comprometida.
- Controlar la capacidad de cada sector y franja.
- Impedir que un trabajador tenga dos asignaciones en la misma fecha y franja.
- Impedir que una labor tenga dos asignaciones en la misma fecha y franja.
- Crear asignaciones en estado `Pendiente`.
- Buscar trabajadores disponibles para una labor, fecha y franja.
- Contabilizar la ocupación de un sector y franja para una fecha.
- Calcular las horas comprometidas de un trabajador en la semana de una fecha.

Los supervisores, credenciales y franjas se crean como objetos y se utilizan al registrar o validar otras entidades; no tienen registros independientes dentro del sistema.

---

## Flujo de creación de una asignación

Para proponer una asignación, el sistema realiza estas validaciones:

1. Verifica que trabajador, labor, franja y fecha sean válidos.
2. Verifica que el trabajador, la labor y el sector estén registrados.
3. Verifica que exista una capacidad configurada para el sector y la franja.
4. Comprueba que la labor no tenga otra asignación para esa fecha y franja.
5. Comprueba que el trabajador no esté ocupado en esa fecha y franja.
6. Comprueba las habilidades y credenciales activas requeridas por la labor.
7. Comprueba las credenciales obligatorias y activas del sector.
8. Verifica que no se supere el límite semanal del trabajador.
9. Verifica que la franja todavía tenga capacidad disponible.
10. Crea la asignación en estado `Pendiente` dentro del sistema.

Las horas de una propuesta pendiente ya se incluyen en el cálculo semanal. Laasignación se agrega a la lista del trabajador cuando un supervisor la aprueba.

Las horas semanales no se reinician modificando un contador: se calculan según las fechas de las asignaciones. Por eso, las asignaciones de semanas anteriores no se contabilizan al consultar una semana nueva.

---

## Relaciones principales

- Un `Trabajador` puede tener varias `Credencial` y `Asignacion` aprobadas.
- Una `Labor` pertenece a un `SectorTrabajo` y requiere habilidades y credenciales.
- `SistemaGestion` puede registrar varias `CapacidadFranjaArea`.
- Una `CapacidadFranjaArea` relaciona un `SectorTrabajo` con una `FranjaHoraria` y un límite de personal.
- Una `Asignacion` relaciona un `Trabajador`, una `Labor`, una `FranjaHoraria` y una fecha.
- Un `Supervisor` es un trabajador con permisos adicionales.
- `SistemaGestion` administra las entidades registradas y las reglas del sistema.

---

## Archivo `clases/__init__.py`

El archivo `__init__.py` permite importar las clases del paquete de forma centralizada.

En lugar de importar cada clase desde su archivo individual.

Esto mejora la organización y facilita el uso del sistema desde otros módulos.

---
