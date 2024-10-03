# Nodo para la pila doblemente enlazada
class Nodo:
    def __init__(self, token):
        self.token = token
        self.anterior = None
        self.siguiente = None

# Pila doblemente enlazada
class PilaDobleEnlazada:
    def __init__(self):
        self.cabeza = None
        self.cola = None

    # Empujar un token a la pila
    def push(self, token):
        nuevo_nodo = Nodo(token)
        if self.cabeza is None:
            self.cabeza = self.cola = nuevo_nodo
        else:
            nuevo_nodo.anterior = self.cola
            self.cola.siguiente = nuevo_nodo
            self.cola = nuevo_nodo

    # Extraer el último token de la pila
    def pop(self):
        if self.cola is None:
            return None
        token = self.cola.token
        if self.cola == self.cabeza:  # Si solo hay un nodo
            self.cabeza = self.cola = None
        else:
            self.cola = self.cola.anterior
            self.cola.siguiente = None
        return token

    # Mostrar la pila completa desde el principio hasta el final
    def mostrar_pila(self):
        nodo_actual = self.cabeza
        while nodo_actual:
            print(nodo_actual.token)
            nodo_actual = nodo_actual.siguiente

# Modificar la función AnalizadorLexico para utilizar la pila
def AnalizadorLexico(nombre_archivo):
    try:
        # Crear una pila doblemente enlazada para almacenar los tokens
        pila_tokens = PilaDobleEnlazada()

        # Leer el archivo preprocesado
        with open(nombre_archivo, 'r') as archivo:
            program = archivo.readlines()

        token_table = []
        id_counter = 1

        # Instancias de autómatas
        automata_identificador = AutomataIdentificador()
        automata_numerico = AutomataNumerico()
        automata_simbolo = AutomataSimbolo(simbolos_especiales)

        # Procesamiento línea por línea
        for line_num, line in enumerate(program, start=1):
            tokens = re.findall(r'!=|==|<=|>=|[<>]|[=+\-*/]|\d+\.\d+|\d+|\w+|[^\s\w]', line)
            col = 1

            for token in tokens:
                lexema = token
                tipo = None
                valor = '-'

                # Verificar si es una palabra reservada
                if token in palabras_reservadas:
                    tipo = "PALABRA_RESERVADA"

                # Verificar si es un operador
                elif token in operadoresAritmeticos:
                    tipo = "OPERADOR_ARITMETICO"
                elif token in operadoresRelacionales:
                    tipo = "OPERADOR_RELACIONAL"

                # Verificar si es un símbolo especial
                elif automata_simbolo.procesarcadena(token):
                    tipo = "SIMBOLO_ESPECIAL"

                # Verificar si es un número
                elif automata_numerico.procesarcadena(token):
                    tipo = "NUMERO"
                    valor = token

                # Verificar si es un identificador
                elif automata_identificador.procesarcadena(token):
                    tipo = "IDENTIFICADOR"

                # Si no se encontró un tipo, se clasifica como desconocido
                if tipo is None:
                    tipo = "DESCONOCIDO"

                # Crear el token y empujarlo a la pila
                token_data = [id_counter, lexema, tipo, valor, line_num, col]
                pila_tokens.push(token_data)

                # Agregar el token a la tabla
                token_table.append(token_data)
                id_counter += 1

                # Actualizar columna
                col += len(token) + 1

        # Imprimir la tabla de tokens
        print(f"{'ID':<5} {'LEXEMA':<10} {'TIPO':<20} {'VALOR':<10} {'LINEA':<10} {'COLUMNA':<10}")
        for row in token_table:
            print(f"{row[0]:<5} {row[1]:<10} {row[2]:<20} {row[3]:<10} {row[4]:<10} {row[5]:<10}")

        # Mostrar los tokens en la pila (opcional)
        print("\nTokens almacenados en la pila (en orden):")
        pila_tokens.mostrar_pila()

    except FileNotFoundError:
        print("El archivo no fue encontrado.")
    except Exception as e:
        print(f"Ha ocurrido un error: {e}")

# Uso de las funciones
Preprocesar_archivo('pruebatexto.txt', 'Posprocesado.txt')
AnalizadorLexico('Posprocesado.txt')
