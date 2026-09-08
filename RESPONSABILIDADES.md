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

Representa una franja de trabajo dentro de la jornada operativa.

Sus responsabilidades son:

- Identificar la franja horaria.
- Representar las franjas como mañana, tarde o noche.
- Permitir asociar una asignación con un período horario determinado.

Las franjas horarias son utilizadas junto con un área de trabajo para controlar la capacidad máxima de personal permitida.

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

Al comenzar una nueva semana, las horas asignadas deben restablecerse a cero.

---

### `Supervisor`

Representa a un trabajador con facultades adicionales de supervisión.

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

Esta clase permite cumplir la regla de límite de personal por área y franja horaria.

---

### `Asignacion`

Representa la propuesta o confirmación de un trabajador para realizar una labor.

Sus responsabilidades son:

- Identificar la asignación.
- Asociar un trabajador con una labor.
- Asociar una franja horaria y una fecha.
- Registrar el estado de la asignación.
- Registrar las horas asignadas.
- Permitir aprobar la asignación.

Una asignación comienza con estado `Pendiente`. Cuando un supervisor la valida, pasa a estado `Aprobada`.

La duración de la asignación se obtiene de la duración definida para la labor.

La representación textual de la clase permite visualizar rápidamente el trabajador, la labor, la fecha, la franja horaria y el estado.

---

### `SistemaGestion`

Representa el componente principal de coordinación del sistema.

Sus responsabilidades son:

- Registrar trabajadores.
- Registrar supervisores.
- Registrar labores.
- Registrar sectores de trabajo.
- Registrar franjas horarias.
- Registrar credenciales.
- Crear asignaciones.
- Validar la aptitud de los trabajadores.
- Verificar la vigencia de las credenciales.
- Controlar la carga horaria semanal.
- Controlar la capacidad de cada área y franja.
- Impedir asignaciones duplicadas.
- Buscar trabajadores disponibles.
- Reiniciar las horas al comenzar una nueva semana.
- Administrar y consultar las asignaciones existentes.

Esta clase concentra las reglas de negocio y coordina la interacción entre las demás clases.

---

## Flujo de creación de una asignación

Para proponer una asignación, el sistema debe realizar las siguientes validaciones:

1. Verificar que la labor exista.
2. Verificar que el trabajador exista.
3. Verificar que el sector de trabajo corresponda a la labor.
4. Comprobar que el trabajador posea todas las habilidades requeridas.
5. Comprobar que posea las credenciales requeridas por la labor.
6. Comprobar que dichas credenciales estén activas en la fecha indicada.
7. Comprobar las credenciales obligatorias del sector.
8. Verificar que no supere su límite de horas semanales.
9. Verificar que la franja horaria tenga capacidad disponible.
10. Verificar que la labor no tenga otra asignación para esa fecha y franja.
11. Crear la asignación en estado `Pendiente`.
12. Sumar las horas de la labor a la carga semanal del trabajador.

Posteriormente, un supervisor puede aprobar la asignación.

---

## Relaciones principales

Las relaciones entre las clases son las siguientes:

- Un `Trabajador` puede tener varias `Credencial`.
- Un `Trabajador` puede tener varias `Asignacion`.
- Una `Labor` pertenece a un `SectorTrabajo`.
- Una `Labor` requiere habilidades y credenciales.
- Un `SectorTrabajo` puede tener varias `CapacidadFranjaArea`.
- Una `CapacidadFranjaArea` relaciona un `SectorTrabajo` con una `FranjaHoraria`.
- Una `Asignacion` relaciona un `Trabajador`, una `Labor`, una `FranjaHoraria` y una fecha.
- Un `Supervisor` es un trabajador con permisos adicionales.
- `SistemaGestion` administra todas las entidades y reglas del sistema.

---

## Archivo `clases/__init__.py`

El archivo `__init__.py` permite importar las clases del paquete de forma centralizada.

En lugar de importar cada clase desde su archivo individual.

Esto mejora la organización y facilita el uso del sistema desde otros módulos.

---
