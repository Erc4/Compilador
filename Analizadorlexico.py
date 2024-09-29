import re

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
token_table = []
id_counter = 1

# Instancias de los autómatas
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

        # Verificar si es una palabra reservada
        if token in palabras_reservadas:
            tipo = "PALABRA_RESERVADA"

        # Verificar si es un operador
        elif token in operadoresAritmeticos:
            tipo = "OPERADORES_ARIT"
        
        elif token in operadoresRelacionales:
            tipo = "OPERADORES_REL"

        # Verificar si es un símbolo especial
        elif automata_simbolo.procesarcadena(token):
            tipo = "SIMBOLO_ESPECIAL"

        # Verificar si es un número (entero o decimal)
        elif automata_numerico.procesarcadena(token):
            tipo = "NUMERICO"
            valor = token

        # Verificar si es un identificador
        elif automata_identificador.procesarcadena(token):
            tipo = "ID"

        # Si no se encontró un tipo, se clasifica como desconocido
        if tipo is None:
            tipo = "DESCONOCIDO"

        # Agregar el token a la tabla
        token_table.append([id_counter, lexema, tipo, valor, line_num, col])
        id_counter += 1

        # Actualizar la columna
        col += len(token) + 1  # Se asume que los tokens están separados por un espacio

# Imprimir la tabla de tokens
print(f"{'ID':<5} {'LEXEMA':<10} {'TIPO':<20} {'VALOR':<10} {'LINEA':<10} {'COLUMNA':<10}")
for row in token_table:
    print(f"{row[0]:<5} {row[1]:<10} {row[2]:<20} {row[3]:<10} {row[4]:<10} {row[5]:<10}")
