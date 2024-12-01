#PilaDobleEnlazada.py
class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None
        self.anterior = None

class PilaDobleEnlazada:
    def __init__(self):
        self.primero = None
        self.ultimo = None

    def push(self, dato):
        nuevo = Nodo(dato)
        if not self.primero:  # Si la pila está vacía
            self.primero = self.ultimo = nuevo
        else:
            self.ultimo.siguiente = nuevo
            nuevo.anterior = self.ultimo
            self.ultimo = nuevo

    def pop(self):
        if not self.ultimo:  # Si la pila está vacía
            return None
        dato = self.ultimo.dato
        if self.ultimo == self.primero:  # Si solo hay un elemento
            self.primero = self.ultimo = None
        else:
            self.ultimo = self.ultimo.anterior
            self.ultimo.siguiente = None
        return dato

    def peek(self):
        return self.ultimo.dato if self.ultimo else None

    def is_empty(self):
        return self.primero is None

    def __str__(self):
        elementos = []
        actual = self.primero
        while actual:
            elementos.append(str(actual.dato))
            actual = actual.siguiente
        return " <- ".join(elementos)
