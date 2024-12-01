# Analizadorlexico.py
import re

class AutomataIdentificador:
    def __init__(self):
        self.estado = 0

    def procesarcadena(self, cadena):
        self.estado = 0
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
        self.estado = 0
        if len(cadena) == 0:
            return False

        for caracter in cadena:
            if self.estado == 0:
                if caracter.isdigit():
                    self.estado = 1
                else:
                    return False
            elif self.estado == 1:
                if caracter == '.':
                    self.estado = 2
                elif not caracter.isdigit():
                    return False
            elif self.estado == 2:
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
        self.simbolos_especiales = {"(": "parentesisa", ")": "parentesisc", "[": "corchetea", "]": "corchetec", "{": "llavea", "}" : "llavec", ":" : "dospuntos", ";" : "puntoycoma"}
        self.palabras_reservadas = ["inicio", "fin", "si", "entonces", "si no", "funcion", "escribir", "mientras", "repetir", "para", "caso", "var", "const", "entero", "decimal", "booleano", "nulo", "verdadero", "falso", "cadena", "arreglo", "hacer", "flotante", "leer"]
        self.automata_identificador = AutomataIdentificador()
        self.automata_numerico = AutomataNumerico()
        self.automata_simbolo = AutomataSimbolo(self.simbolos_especiales)

    def analizar(self):
        program = self.codigo_fuente.split("\n")
        for line_num, line in enumerate(program, start=1):
            # Ignorar líneas vacías
            if not line.strip():
                continue
                
            # Eliminar comentarios
            if '#' in line:
                line = line[:line.index('#')].strip()
                if not line:  # Si la línea solo tenía un comentario, saltarla
                    continue

            tokens = re.findall(r'!=|==|<=|>=|[<>]|[=+\-*/]|\d+\.\d+|\d+|\w+|[^\s\w]', line)
            col = 1

            for token in tokens:
                lexema = token
                tipo = None
                valor = '-'

                # Verificar si es una palabra reservada compuesta (si no)
                if lexema == "si" and tokens[tokens.index(token)+1:] and tokens[tokens.index(token)+1] == "no":
                    lexema = "si no"
                    tipo = "PALABRA_RESERVADA"
                    tokens.pop(tokens.index(token)+1)  # Eliminar el "no" del siguiente token
                elif token in self.palabras_reservadas:
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
                
                if tipo is not None:  # Solo agregar tokens válidos
                    self.token_table.append([self.id_counter, lexema, tipo, valor, line_num, col])
                    self.id_counter += 1
                    col += len(token) + 1

        return self.token_table
    # Preprocesador.py
class Preprocesador:
    @staticmethod
    def preprocesar_archivo(nombre_archivo_entrada, nombre_archivo_salida):
        try:
            with open(nombre_archivo_entrada, 'r', encoding='utf-8') as archivo_entrada:
                lineas_procesadas = []
                
                for linea in archivo_entrada:
                    # Eliminar espacios en blanco al inicio y al final
                    linea = linea.strip()
                    
                    # Ignorar líneas vacías
                    if not linea:
                        continue
                    
                    # Manejar comentarios
                    if '#' in linea:
                        linea = linea[:linea.index('#')].strip()
                        if not linea:  # Si la línea solo tenía un comentario
                            continue
                    
                    # Normalizar espacios
                    palabras = linea.split()
                    linea_procesada = ' '.join(palabras)
                    
                    lineas_procesadas.append(linea_procesada)
            
            # Guardar archivo procesado
            with open(nombre_archivo_salida, 'w', encoding='utf-8') as archivo_salida:
                for linea in lineas_procesadas:
                    archivo_salida.write(linea + '\n')
                    
            print(f"Archivo preprocesado guardado como '{nombre_archivo_salida}'")
            return True
            
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo '{nombre_archivo_entrada}'")
            return False
        except Exception as e:
            print(f"Error durante el preprocesamiento: {str(e)}")
            return False

    @staticmethod
    def leer_archivo_procesado(nombre_archivo):
        try:
            with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
                return archivo.read()
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo '{nombre_archivo}'")
            return None
        except Exception as e:
            print(f"Error al leer el archivo: {str(e)}")
            return None