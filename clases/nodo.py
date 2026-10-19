class Nodo:
    """Eslabón de una cadena enlazada: guarda un dato y la referencia al siguiente nodo.

    Es el bloque con el que se construye Cola. `siguiente` vale None cuando el
    nodo es el último de la cadena.
    """

    def __init__(self, dato, siguiente=None) -> None:
        self.dato = dato
        self.siguiente = siguiente

    def __repr__(self) -> str:
        return f"Nodo({self.dato!r})"
