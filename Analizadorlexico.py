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
                if caracter.isalpha():
                    self.estado = 1
                else:
                    return False
            elif self.estado == 1:  # q1 - Los caracteres restantes pueden ser letras, dígitos o '_'
                if not (caracter.isalnum() or caracter == '_'):
                    return False
        return self.estado == 1


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
                    self.estado = 1
                else:
                    return False
            elif self.estado == 1:  # q1 - Si encuentra un punto, pasa al estado decimal
                if caracter == '.':
                    self.estado = 2  # Estado decimal
                elif not caracter.isdigit():
                    return False
            elif self.estado == 2:  # q2 - Después del punto, debe haber dígitos
                if not caracter.isdigit():
                    return False
        return self.estado == 1 or self.estado == 2


class AutomataSimbolo:
    def __init__(self, simbolos_especiales):
        self.simbolos_especiales = simbolos_especiales

    def procesarcadena(self, cadena):
        return cadena in self.simbolos_especiales


class AnalizadorLexico:
    def __init__(self, codigo_fuente):
        self.codigo_fuente = codigo_fuente
        self.token_table = []
        self.id_counter = 1
        self.operadoresAritmeticos = {'=': 'ASIGNACION', '+': 'SUMA', '-': 'RESTA', '*': 'MULTIPLICACION', '/': 'DIVISION'}
        self.operadoresRelacionales = {'!=': 'DESIGUALDAD', '==': 'IGUALDAD', '<': 'MENORQUE', '>': 'MAYORQUE', '<=': 'MENOROIGUAL', '>=': 'MAYOROIGUAL'}
        self.simbolos_especiales = {"(": "parentesisa", ")": "parentesisc", "[": "corchetea", "]": "corchetec", "{": "llavea", "}": "llavec", ":": "dospuntos", ";": "puntoycoma"}
        self.palabras_reservadas = ["inicio", "fin", "si", "entonces", "si no", "funcion", "escribir", "mientras", "repetir", "para", "caso", "var", "const", "entero", "decimal", "booleano", "nulo", "verdadero", "falso", "cadena", "arreglo", "hacer", "flotante"]
        self.automata_identificador = AutomataIdentificador()
        self.automata_numerico = AutomataNumerico()
        self.automata_simbolo = AutomataSimbolo(self.simbolos_especiales)

    def analizar(self):
        program = self.codigo_fuente.split("\n")
        for line_num, line in enumerate(program, start=1):
            tokens = re.findall(r'!=|==|<=|>=|[<>]|[=+\-*/]|\d+\.\d+|\d+|\w+|[^\s\w]', line)
            col = 1

            for token in tokens:
                lexema = token
                tipo = None
                valor = '-'

                if token in self.palabras_reservadas:
                    tipo = "PALABRA_RESERVADA"
                elif token in self.operadoresAritmeticos:
                    tipo = "OPERADORES_ARIT"
                elif token in self.operadoresRelacionales:
                    tipo = "OPERADORES_REL"
                elif self.automata_simbolo.procesarcadena(token):
                    tipo = "SIMBOLO_ESPECIAL"
                elif self.automata_numerico.procesarcadena(token):
                    tipo = "NUMERICO"
                    valor = token
                elif self.automata_identificador.procesarcadena(token):
                    tipo = "ID"
                if tipo is None:
                    tipo = "DESCONOCIDO"

                self.token_table.append([self.id_counter, lexema, tipo, valor, line_num, col])
                self.id_counter += 1
                col += len(token) + 1

        return self.token_table
