class NodoAST:
    def __init__(self, tipo, valor=None):
        self.tipo = tipo  # Tipo de nodo (ej. "ASIGNACION", "OPERACION", "CONSTANTE", "VARIABLE")
        self.valor = valor  # Valor del nodo (ej. el operador "+", el identificador "x")
        self.hijos = []  # Lista de hijos (para operaciones o estructuras compuestas)

    def agregar_hijo(self, nodo):
        self.hijos.append(nodo)

    def __str__(self):
        return f"({self.tipo}: {self.valor}, hijos: {len(self.hijos)})"


class AnalizadorSintactico:
    def __init__(self, tokens):
        self.tokens = tokens  # Lista de tokens del analizador léxico
        self.posicion = 0  # Posición actual en la lista de tokens

    def obtener_token_actual(self):
        if self.posicion < len(self.tokens):
            return self.tokens[self.posicion]
        return None

    def avanzar(self):
        self.posicion += 1

    def consumir(self, tipo_esperado):
        token = self.tokens[self.posicion]
        if token[2] == tipo_esperado:  # El tipo está en el índice 2 de la lista
            self.posicion += 1
            return token
        raise SyntaxError(f"Se esperaba un token de tipo {tipo_esperado}, pero se encontró {token}.")

    def analizar(self):
        """
        Punto de entrada del análisis sintáctico.
        """
        ast_raiz = NodoAST("PROGRAMA")
        while self.posicion < len(self.tokens):
            ast_raiz.agregar_hijo(self.sentencia())
        return ast_raiz

    def sentencia(self):
        """
        Analiza una sentencia y retorna el nodo correspondiente.
        """
        token_actual = self.obtener_token_actual()
        if token_actual and token_actual[2] == "ID":
            return self.asignacion()
        elif token_actual and token_actual[1] == "si":
            return self.condicional()
        else:
            raise SyntaxError(f"Sentencia inesperada: {token_actual}")

    def asignacion(self):
        """
        Analiza una asignación: ID '=' expresion ';'
        """
        nodo = NodoAST("ASIGNACION")
        id_token = self.consumir("ID")
        nodo.agregar_hijo(NodoAST("VARIABLE", id_token[1]))
        self.consumir("OPERADORES_ARIT")  # Consume '='
        nodo.agregar_hijo(self.expresion())
        self.consumir("SIMBOLO_ESPECIAL")  # Consume ';'
        return nodo

    def condicional(self):
        """
        Analiza una estructura condicional: si expresion_relacional 'entonces' bloque
        """
        nodo = NodoAST("CONDICIONAL")
        self.consumir("PALABRA_RESERVADA")  # Consume 'si'
        nodo.agregar_hijo(self.expresion_relacional())  # Cambiar a expresion_relacional
        self.consumir("PALABRA_RESERVADA")  # Consume 'entonces'
        nodo.agregar_hijo(self.bloque())
        return nodo


    def bloque(self):
        """
        Analiza un bloque de sentencias entre llaves.
        """
        nodo = NodoAST("BLOQUE")
        self.consumir("SIMBOLO_ESPECIAL")  # Consume '{'
        while self.obtener_token_actual() and self.obtener_token_actual()[1] != "}":
            nodo.agregar_hijo(self.sentencia())
        self.consumir("SIMBOLO_ESPECIAL")  # Consume '}'
        return nodo

    def expresion(self):
        """
        Analiza una expresión aritmética simple (por ahora sin jerarquía de operadores).
        """
        nodo = self.termino()
        while self.obtener_token_actual() and self.obtener_token_actual()[2] == "OPERADORES_ARIT":
            operador = self.consumir("OPERADORES_ARIT")
            nodo_operacion = NodoAST("OPERACION", operador[1])
            nodo_operacion.agregar_hijo(nodo)
            nodo_operacion.agregar_hijo(self.termino())
            nodo = nodo_operacion
        return nodo
    
    def expresion_relacional(self):
        """
        Analiza una expresión relacional: término operador_relacional término.
        """
        nodo = self.expresion()  # Obtiene el lado izquierdo (puede ser una expresión aritmética)
        token_actual = self.obtener_token_actual()
        if token_actual and token_actual[2] == "OPERADORES_REL":
            operador = self.consumir("OPERADORES_REL")  # Consume el operador relacional
            nodo_relacional = NodoAST("RELACIONAL", operador[1])
            nodo_relacional.agregar_hijo(nodo)
            nodo_relacional.agregar_hijo(self.expresion())  # Obtiene el lado derecho
            return nodo_relacional
        return nodo  # Si no hay operador relacional, retorna la expresión original

    def termino(self):
        """
        Analiza un término: un número, variable o expresión entre paréntesis.
        """
        token_actual = self.obtener_token_actual()
        if token_actual[2] == "NUMERICO":
            self.consumir("NUMERICO")
            return NodoAST("CONSTANTE", token_actual[1])
        elif token_actual[2] == "ID":
            self.consumir("ID")
            return NodoAST("VARIABLE", token_actual[1])
        elif token_actual[1] == "(":
            self.consumir("SIMBOLO_ESPECIAL")  # Consume '('
            nodo = self.expresion()
            self.consumir("SIMBOLO_ESPECIAL")  # Consume ')'
            return nodo
        else:
            raise SyntaxError(f"Término inesperado: {token_actual}")
