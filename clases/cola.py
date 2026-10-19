from .nodo import Nodo
from .excepciones import ColaVacia


class Cola:
    """Cola FIFO (el primero en entrar es el primero en salir) armada con nodos.

    Mantiene dos referencias: `_inicio` (frente, de donde se saca) y `_final`
    (último nodo, donde se agrega). Con `_final` encolar no tiene que recorrer
    toda la cadena para encontrar el último nodo.

    Los atributos llevan guion bajo porque quien use la cola no debería tocar
    los nodos: solo encolar, desencolar, mirar el inicio y preguntar si está vacía.
    """

    def __init__(self) -> None:
        self._inicio = None
        self._final = None

    def esta_vacia(self) -> bool:
        return self._inicio is None

    def encolar(self, dato) -> None:
        """Agrega `dato` al final de la cola."""
        nuevo = Nodo(dato)
        if self.esta_vacia():
            # Cola vacía: el nuevo nodo es a la vez el primero y el último.
            self._inicio = nuevo
        else:
            # El último nodo actual apunta al nuevo, y recién después se
            # actualiza `_final` (al revés se perdería la referencia al viejo último).
            self._final.siguiente = nuevo
        self._final = nuevo

    def desencolar(self):
        """Quita y devuelve el dato del inicio. Lanza ColaVacia si no hay elementos."""
        if self.esta_vacia():
            raise ColaVacia("No se puede desencolar de una cola vacía.")
        dato = self._inicio.dato
        self._inicio = self._inicio.siguiente
        if self._inicio is None:
            # Se sacó el único elemento: si no se limpia `_final`, quedaría
            # apuntando a un nodo que ya no pertenece a la cola.
            self._final = None
        return dato

    def inicio(self):
        """Devuelve el dato del inicio sin quitarlo. Lanza ColaVacia si no hay elementos."""
        if self.esta_vacia():
            raise ColaVacia("La cola está vacía: no hay inicio.")
        return self._inicio.dato
