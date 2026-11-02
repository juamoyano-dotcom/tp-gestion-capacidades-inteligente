from datetime import date
from typing import List
from .trabajador import Trabajador
from .cola import Cola

# Cada nivel de la jerarquía ocupa 2 dígitos del código: "01" -> "0101" -> "010102"
LARGO_SEGMENTO = 2


class SectorTrabajo:
    """Área de trabajo de la planta y, a la vez, nodo del organigrama de IIT.

    Conoce las credenciales que se exigen a cualquier trabajador que realice
    una labor en ella. El límite de personal por franja NO vive acá sino en
    CapacidadFranjaArea: ese límite depende de la combinación área + franja
    (no del área sola), y tenerlo también en el sector sería el mismo dato en
    dos lugares, con riesgo de que se desincronicen.

    Organigrama: los sectores forman un árbol general (cada nodo puede tener
    cualquier cantidad de hijos). El `codigo` de un sector es el camino desde
    la raíz: el de un subsector empieza con el de su padre ("01" Producción,
    "0101" Ensamblado). La raíz de la empresa tiene código "" (vacío).
    `codigo=None` significa que el sector todavía no forma parte del árbol.

    `padre` apunta al sector del nivel superior (None en la raíz y en los
    sectores que todavía no están en el árbol). Lo asigna agregar_subsector al
    insertar el sector; no hay que tocarlo a mano. Gracias a él un sector
    "hereda" las credenciales obligatorias de todos sus ancestros (ver
    `credenciales_requeridas`): una norma cargada en "Producción" rige también
    para "Ensamblado" y "Calidad" sin repetirla en cada sector.

    Los trabajadores asignados a un sector se guardan SOLO acá (`trabajadores`),
    no en Trabajador: así hay una única fuente de verdad de a qué sector
    pertenece cada uno, y se evita el import circular con trabajador.py.
    """

    def __init__(self, id_sector: int, nombre: str, credenciales_obligatorias: List[str] = None, codigo: str = None) -> None:
        if codigo is not None and codigo != "":
            self._validar_codigo(codigo)

        self.id = id_sector
        self.nombre = nombre
        self.credenciales_obligatorias = credenciales_obligatorias if credenciales_obligatorias is not None else []
        self.codigo = codigo
        self.padre = None          # lo asigna agregar_subsector al insertar el sector en el árbol
        self.subsectores = {}      # segmento (str de 2 dígitos) -> SectorTrabajo hijo
        self.trabajadores = []     # trabajadores asignados DIRECTAMENTE a este sector

    @staticmethod
    def _validar_codigo(codigo: str) -> None:
        """El código debe ser solo dígitos y tener una cantidad de dígitos múltiplo de LARGO_SEGMENTO."""
        if not isinstance(codigo, str) or not codigo.isdigit() or len(codigo) % LARGO_SEGMENTO != 0:
            raise ValueError(
                f"Código de sector inválido: '{codigo}'. Debe tener solo dígitos, "
                f"en grupos de {LARGO_SEGMENTO} (ej: '01', '0102')."
            )

    # ---------- Reglas de credenciales ----------

    def credenciales_requeridas(self) -> list:
        """Credenciales que se exigen en este sector: las propias más las heredadas de todos sus ancestros.

        Recursivo hacia arriba. Caso base: sin padre (raíz o sector fuera del
        árbol) solo cuentan las propias, que es el comportamiento de siempre.
        Se calcula cada vez (no se guarda), así que si se agrega una
        credencial a un sector, sus descendientes la heredan automáticamente.
        Primero van las del ancestro más alto, sin repetidos.
        """
        heredadas = self.padre.credenciales_requeridas() if self.padre is not None else []
        propias = [c for c in self.credenciales_obligatorias if c not in heredadas]
        return heredadas + propias

    def trabajador_cumple_credenciales(self, trab: Trabajador, fecha: date) -> bool:
        """Indica si el trabajador tiene activas en `fecha` todas las credenciales exigidas en el área.

        Incluye las heredadas de los sectores superiores (ver credenciales_requeridas).
        Delega en Trabajador.credenciales_activas (encapsulamiento): el sector
        no necesita conocer cómo se guardan las credenciales.
        """
        # verifica directo con el método de Trabajador --> encapsulamiento
        return trab.credenciales_activas(self.credenciales_requeridas(), fecha)

    # ---------- Árbol: estructura ----------

    def agregar_subsector(self, sector: "SectorTrabajo") -> None:
        """Inserta `sector` en el lugar que le corresponde según su código (recursivo).

        Caso base: el código es de un hijo directo de este nodo -> se guarda acá.
        Caso recursivo: es de un descendiente más profundo -> se delega en el
        hijo que corresponde al siguiente segmento del código.
        El padre debe existir antes que el hijo.
        """
        codigo = sector.codigo
        if codigo is None or not codigo.startswith(self.codigo) or len(codigo) <= len(self.codigo):
            raise ValueError(f"El código '{codigo}' no corresponde a un descendiente del sector '{self.codigo}'.")

        inicio = len(self.codigo)
        segmento = codigo[inicio:inicio + LARGO_SEGMENTO]

        if len(codigo) == inicio + LARGO_SEGMENTO:      # caso base: hijo directo
            if segmento in self.subsectores:
                raise ValueError(f"Ya existe un sector con el código '{codigo}'.")
            self.subsectores[segmento] = sector
            sector.padre = self
        else:                                           # caso recursivo: bajar un nivel
            hijo = self.subsectores.get(segmento)
            if hijo is None:
                raise ValueError(
                    f"No existe el sector padre '{codigo[:inicio + LARGO_SEGMENTO]}'. Hay que crearlo antes."
                )
            hijo.agregar_subsector(sector)

    def buscar(self, codigo: str):
        """Devuelve el sector con ese código dentro de esta rama, o None si no existe (recursivo)."""
        if codigo == self.codigo:                       # caso base: lo encontré
            return self
        if not codigo.startswith(self.codigo):          # caso base: no puede estar en esta rama
            return None
        inicio = len(self.codigo)
        hijo = self.subsectores.get(codigo[inicio:inicio + LARGO_SEGMENTO])
        if hijo is None:                                # caso base: se acaba el camino
            return None
        return hijo.buscar(codigo)

    # ---------- Árbol: trabajadores ----------

    def agregar_trabajador(self, trab: Trabajador) -> None:
        for t in self.trabajadores:
            if t.id_trabajador == trab.id_trabajador:
                raise ValueError("El trabajador ya está asignado a este sector.")
        self.trabajadores.append(trab)

    def quitar_trabajador(self, trab: Trabajador) -> None:
        for t in self.trabajadores:
            if t.id_trabajador == trab.id_trabajador:
                self.trabajadores.remove(t)
                return
        raise ValueError("El trabajador no está asignado a este sector.")

    def sector_de(self, trab: Trabajador):
        """Devuelve el sector (de esta rama) al que pertenece el trabajador, o None (recursivo)."""
        for t in self.trabajadores:
            if t.id_trabajador == trab.id_trabajador:
                return self
        for hijo in self.subsectores.values():
            encontrado = hijo.sector_de(trab)
            if encontrado is not None:
                return encontrado
        return None

    # ---------- Árbol: consultas recursivas sobre la rama ----------

    def contar_trabajadores(self) -> int:
        """Trabajadores de este sector más los de todos sus subsectores."""
        total = len(self.trabajadores)
        for hijo in self.subsectores.values():
            total += hijo.contar_trabajadores()
        return total          # sin hijos el for no corre: ese es el caso base

    def trabajadores_de_rama(self) -> list:
        """Lista de todos los trabajadores de esta rama (este sector y sus descendientes)."""
        resultado = list(self.trabajadores)
        for hijo in self.subsectores.values():
            resultado.extend(hijo.trabajadores_de_rama())
        return resultado

    def organigrama(self, nivel: int = 0) -> str:
        """Texto del organigrama de esta rama, con sangría según el nivel (recorrido en pre-orden)."""
        codigo = self.codigo if self.codigo else "--"
        texto = "    " * nivel + f"[{codigo}] {self.nombre} ({len(self.trabajadores)} trab.)\n"
        for segmento in sorted(self.subsectores):
            texto += self.subsectores[segmento].organigrama(nivel + 1)
        return texto

    def recorrido_por_niveles(self) -> list:
        """Sectores de la rama, nivel por nivel (BFS), usando la Cola propia del TP."""
        resultado = []
        cola = Cola()
        cola.encolar(self)
        while not cola.esta_vacia():
            sector = cola.desencolar()
            resultado.append(sector)
            for segmento in sorted(sector.subsectores):
                cola.encolar(sector.subsectores[segmento])
        return resultado

    def __repr__(self) -> str:
        return f"SectorTrabajo({self.nombre})"
