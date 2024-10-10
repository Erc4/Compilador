import re

class Token:
    def __init__(self, lexema, col, ren, valor, tipo):
        self.lexema = lexema
        self.col = col
        self.ren = ren
        self.valor = valor
        self.tipo = tipo

    def __repr__(self):
        return f"Token({self.lexema}, {self.col}, {self.ren}, {self.valor}, {self.tipo})"

class Pila:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop() if not self.empty() else None

    def empty(self):
        return len(self.items) == 0

    #def mostrar_pila(self):
    #   print("Pila actual (desde la base hasta el tope):")
    #    for item in reversed(self.items):
    #        print(item)

# Autómata para reconocer identificadores
class AutomataIdentificador:
    def __init__(self):
        self.estado = 0

    def procesarcadena(self, cadena):
        self.estado = 0  # Reiniciar el estado
        if len(cadena) == 0:
            return False

        for caracter in cadena:
            if self.estado == 0:  # q0 - El primer carácter debe ser una letra
                if caracter.isalpha():  # Verifica si es una letra
                    self.estado = 1  # Pasa al estado de aceptación
                else:
                    return False  # Si no es letra, no es válido
            elif self.estado == 1:  # q1 - Los caracteres restantes pueden ser letras, dígitos o '_'
                if not (caracter.isalnum() or caracter == '_'):
                    return False  # Si encuentra algo distinto a letras, dígitos o '_', no es válido
        return self.estado == 1  # La cadena es aceptada si termina en el estado de aceptación

# Autómata para reconocer números
class AutomataNumerico:
    def __init__(self):
        self.estado = 0

    def procesarcadena(self, cadena):
        self.estado = 0  # Reiniciar el estado
        if len(cadena) == 0:
            return False

        for caracter in cadena:
            if self.estado == 0:  # q0 - El primer carácter debe ser un dígito
                if caracter.isdigit():
                    self.estado = 1  # Pasa al estado q1 (entero)
                else:
                    return False
            elif self.estado == 1:  # q1 - Si encuentra un punto, pasa al estado decimal
                if caracter == '.':
                    self.estado = 2  # q2 - En el estado decimal
                elif not caracter.isdigit():  # Si no es dígito ni punto, es inválido
                    return False
            elif self.estado == 2:  # q2 - Después del punto, debe haber dígitos
                if not caracter.isdigit():
                    return False  # Si no hay dígitos después del punto, es inválido
        return self.estado == 1 or self.estado == 2  # Se acepta tanto el entero como el decimal

# Autómata para reconocer símbolos especiales
class AutomataSimbolo:
    def __init__(self, simbolos_especiales):
        self.simbolos_especiales = simbolos_especiales

    def procesarcadena(self, cadena):
        return cadena in self.simbolos_especiales

# Definiciones de operadores, tipos de datos, símbolos especiales y palabras reservadas
operadoresAritmeticos = {
    '=': 'ASIGNACION',
    '+': 'SUMA',
    '-': 'RESTA',
    '*': 'MULTIPLICACION',
    '/': 'DIVISION'
}

operadoresRelacionales = {
    '!=': 'DESIGUALDAD',
    '==': 'IGUALDAD',
    '<': 'MENORQUE',
    '>': 'MAYORQUE',
    '<=': 'MENOROIGUAL',
    '>=': 'MAYOROIGUAL'
}

simbolos_especiales = {"(":"parentesisa", ")":"parentesisc", "[":"corchetea", "]":"corchetec", "{":"llavea", "}":"llavec" ,":":"dospuntos", ";":"puntoycoma"}

palabras_reservadas = [
    "inicio", "fin", "si", "entonces", "si no", "funcion", "escribir", "mientras",
    "repetir", "para", "caso", "var", "const", "entero", "decimal", "booleano",
    "nulo", "verdadero", "falso", "cadena", "arreglo", "hacer", "flotante"
]

# Lectura del archivo
file = open("read.py")
a = file.read()
file.close()

program = a.split("\n")
pila_tokens = Pila() 
id_counter = 1

automata_identificador = AutomataIdentificador()
automata_numerico = AutomataNumerico()
automata_simbolo = AutomataSimbolo(simbolos_especiales)

# Procesamiento de cada línea
for line_num, line in enumerate(program, start=1):
    # Ajustar la expresión regular para manejar operadores relacionales y otros tokens
    tokens = re.findall(r'!=|==|<=|>=|[<>]|[=+\-*/]|\d+\.\d+|\d+|\w+|[^\s\w]', line)  # Detecta números decimales, operadores y demás
    col = 1

    for token in tokens:
        lexema = token
        tipo = None
        valor = '-'

        if token in palabras_reservadas:
            tipo = "PALABRA_RESERVADA"

        elif token in operadoresAritmeticos:
            tipo = "OPERADORES_ARIT"
        
        elif token in operadoresRelacionales:
            tipo = "OPERADORES_REL"

        elif automata_simbolo.procesarcadena(token):
            tipo = "SIMBOLO_ESPECIAL"

        elif automata_numerico.procesarcadena(token):
            tipo = "NUMERICO"
            valor = token

        elif automata_identificador.procesarcadena(token):
            tipo = "ID"

        if tipo is None:
            tipo = "DESCONOCIDO"

        nuevo_token = Token(lexema, col, line_num, valor, tipo)
        pila_tokens.push(nuevo_token)
        
        id_counter += 1
        col += len(token) + 1 

#pila_tokens.mostrar_pila()

print("\nTabla de tokens (desapilando de la pila):")
print(f"{'LEXEMA':<10} {'COLUMNA':<10} {'RENGLON':<10} {'VALOR':<10} {'TIPO':<20}")
while not pila_tokens.empty():
    token = pila_tokens.pop()
    print(f"{token.lexema:<10} {token.col:<10} {token.ren:<10} {token.valor:<10} {token.tipo:<20}")
