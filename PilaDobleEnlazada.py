class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None
        self.anterior = None

class PilaDobleEnlazada:
    def __init__(self):
        self.cabeza = None
        self.cola = None

    def esta_vacia(self):
        return self.cabeza is None

    def apilar(self, valor):
        nuevo_nodo = Nodo(valor)
        if self.esta_vacia():
            self.cabeza = self.cola = nuevo_nodo
        else:
            nuevo_nodo.anterior = self.cola
            self.cola.siguiente = nuevo_nodo
            self.cola = nuevo_nodo

    def desapilar(self):
        if self.esta_vacia():
            raise IndexError("La pila está vacía")
        valor = self.cola.valor
        if self.cabeza == self.cola:
            self.cabeza = self.cola = None
        else:
            self.cola = self.cola.anterior
            self.cola.siguiente = None
        return valor

    def obtener_ultimo(self):
        if self.esta_vacia():
            raise IndexError("La pila está vacía")
        return self.cola.valor

    def mostrar(self):
        actual = self.cabeza
        while actual:
            print(actual.valor, end=' ')
            actual = actual.siguiente
        print()

# Uso de la pila doblemente enlazada
pila = PilaDobleEnlazada()
pila.apilar('token1')
pila.apilar('token2')
pila.apilar('token3')
pila.mostrar()  # Imprimirá: token1 token2 token3
print("Desapilar:", pila.desapilar())  # Imprimirá: token3
pila.mostrar()  # Imprimirá: token1 token2



