class NodoAST:
    def __init__(self, tipo, valor=None, linea=None, columna=None):
        self.tipo = tipo
        self.valor = valor
        self.hijos = []
        self.linea = linea
        self.columna = columna

    def agregar_hijo(self, nodo):
        self.hijos.append(nodo)

    def __str__(self):
        return f"{self.tipo}({self.valor if self.valor else ''})"

class AnalizadorSintacticoCompleto:
    def __init__(self, tokens):
        self.tokens = tokens
        self.posicion_actual = 0
        self.token_actual = None
        self.siguiente_token()

    def peek_next_token(self):
        """Mira el siguiente token sin consumirlo"""
        if self.posicion_actual < len(self.tokens):
            return self.tokens[self.posicion_actual]
        return None

    def siguiente_token(self):
        if self.posicion_actual < len(self.tokens):
            self.token_actual = self.tokens[self.posicion_actual]
            self.posicion_actual += 1
        else:
            self.token_actual = None
        return self.token_actual

    def match(self, lexema_esperado):
        if self.token_actual and self.token_actual[1] == lexema_esperado:
            token = self.token_actual
            self.siguiente_token()
            return token
        else:
            self.error_sintaxis(f"Se esperaba '{lexema_esperado}'", 
                              f"se encontró '{self.token_actual[1] if self.token_actual else 'fin de archivo'}'")

    def match_tipo(self, tipo_esperado):
        if self.token_actual and self.token_actual[2] == tipo_esperado:
            token = self.token_actual
            self.siguiente_token()
            return token
        else:
            tipo_encontrado = self.token_actual[2] if self.token_actual else 'fin de archivo'
            self.error_sintaxis(f"Se esperaba un token de tipo {tipo_esperado}", 
                              f"se encontró {tipo_encontrado}")

    def error_sintaxis(self, esperado, encontrado):
        linea = self.token_actual[4] if self.token_actual else "desconocida"
        columna = self.token_actual[5] if self.token_actual else "desconocida"
        raise SyntaxError(f"Error de sintaxis en línea {linea}, columna {columna}: {esperado}, pero {encontrado}")

    def analizar(self):
        programa = NodoAST("PROGRAMA")
        self.match("inicio")
        
        while self.token_actual and self.token_actual[1] != "fin":
            try:
                sentencia = self.analizar_sentencia()
                if sentencia:
                    programa.agregar_hijo(sentencia)
            except SyntaxError as e:
                print(f"Error: {str(e)}")
                self.recuperar_error()
        
        self.match("fin")
        return programa

    def recuperar_error(self):
        while self.token_actual and self.token_actual[1] not in [';', '}', 'fin']:
            self.siguiente_token()
        if self.token_actual and self.token_actual[1] in [';', '}']:
            self.siguiente_token()

    def analizar_sentencia(self):
        if not self.token_actual:
            return None

        if self.token_actual[1] == "leer":
            return self.analizar_leer()
        elif self.token_actual[1] == "escribir":
            return self.analizar_escribir()
        elif self.token_actual[1] == "si":
            return self.analizar_si()
        elif self.token_actual[1] == "mientras":
            return self.analizar_mientras()
        elif self.token_actual[1] == "para":
            return self.analizar_para()
        elif self.token_actual[2] == "ID":
            return self.analizar_asignacion()
        elif self.token_actual[1] == "si no":  # Añadimos manejo explícito de "si no"
            return None  # El "si no" se maneja dentro de analizar_si()
        elif self.token_actual[1] in ['}', '{']:
            self.siguiente_token()
            return None
        else:
            self.error_sintaxis("una sentencia válida", 
                            f"token inesperado '{self.token_actual[1]}'")


    def analizar_si(self):
        nodo = NodoAST("SI", linea=self.token_actual[4], columna=self.token_actual[5])
        self.match("si")
        nodo.agregar_hijo(self.analizar_condicion())
        self.match("entonces")
        self.match("{")
        
        # Bloque principal del si
        nodo_bloque = NodoAST("BLOQUE")
        while self.token_actual and self.token_actual[1] != "}":
            sentencia = self.analizar_sentencia()
            if sentencia:
                nodo_bloque.agregar_hijo(sentencia)
        self.match("}")
        nodo.agregar_hijo(nodo_bloque)
        
        # Verificar si hay un "si no"
        if self.token_actual and self.token_actual[1] == "si no":
            self.match("si no")  # Consumir el token "si no"
            self.match("{")
            nodo_sino = NodoAST("BLOQUE_SINO")
            while self.token_actual and self.token_actual[1] != "}":
                sentencia = self.analizar_sentencia()
                if sentencia:
                    nodo_sino.agregar_hijo(sentencia)
            self.match("}")
            nodo.agregar_hijo(nodo_sino)
        
        return nodo


    def analizar_mientras(self):
        nodo = NodoAST("MIENTRAS", linea=self.token_actual[4], columna=self.token_actual[5])
        self.match("mientras")
        nodo.agregar_hijo(self.analizar_condicion())
        self.match("{")
        
        nodo_bloque = NodoAST("BLOQUE")
        while self.token_actual and self.token_actual[1] != "}":
            sentencia = self.analizar_sentencia()
            if sentencia:
                nodo_bloque.agregar_hijo(sentencia)
        self.match("}")
        nodo.agregar_hijo(nodo_bloque)
        return nodo

    def analizar_para(self):
        nodo = NodoAST("PARA", linea=self.token_actual[4], columna=self.token_actual[5])
        self.match("para")
        self.match("(")
        
        # Inicialización
        inicializacion = self.analizar_asignacion_simple()
        nodo.agregar_hijo(inicializacion)
        self.match(";")
        
        # Condición
        condicion = self.analizar_condicion()
        nodo.agregar_hijo(condicion)
        self.match(";")
        
        # Incremento
        incremento = self.analizar_asignacion_simple()
        nodo.agregar_hijo(incremento)
        self.match(")")
        
        # Bloque del para
        self.match("{")
        nodo_bloque = NodoAST("BLOQUE")
        while self.token_actual and self.token_actual[1] != "}":
            sentencia = self.analizar_sentencia()
            if sentencia:
                nodo_bloque.agregar_hijo(sentencia)
        self.match("}")
        nodo.agregar_hijo(nodo_bloque)
        
        return nodo

    def analizar_leer(self):
        nodo = NodoAST("LEER", linea=self.token_actual[4], columna=self.token_actual[5])
        self.match("leer")
        self.match("(")
        id_token = self.match_tipo("ID")
        nodo.agregar_hijo(NodoAST("ID", id_token[1]))
        self.match(")")
        self.match(";")
        return nodo

    def analizar_escribir(self):
        nodo = NodoAST("ESCRIBIR", linea=self.token_actual[4], columna=self.token_actual[5])
        self.match("escribir")
        self.match("(")
        nodo.agregar_hijo(self.analizar_expresion())
        self.match(")")
        self.match(";")
        return nodo

    def analizar_asignacion(self):
        nodo = NodoAST("ASIGNACION", linea=self.token_actual[4], columna=self.token_actual[5])
        id_token = self.match_tipo("ID")
        nodo.agregar_hijo(NodoAST("ID", id_token[1]))
        self.match("=")
        nodo.agregar_hijo(self.analizar_expresion())
        self.match(";")
        return nodo

    def analizar_asignacion_simple(self):
        """Versión de asignación sin punto y coma para usar en el bucle para"""
        nodo = NodoAST("ASIGNACION", linea=self.token_actual[4], columna=self.token_actual[5])
        id_token = self.match_tipo("ID")
        nodo.agregar_hijo(NodoAST("ID", id_token[1]))
        self.match("=")
        nodo.agregar_hijo(self.analizar_expresion())
        return nodo

    def analizar_expresion(self):
        return self.analizar_expresion_aditiva()

    def analizar_expresion_aditiva(self):
        nodo = self.analizar_expresion_multiplicativa()
        
        while self.token_actual and self.token_actual[1] in ['+', '-']:
            operador = self.token_actual[1]
            self.siguiente_token()
            nodo_temp = NodoAST("OPERACION", operador)
            nodo_temp.agregar_hijo(nodo)
            nodo_temp.agregar_hijo(self.analizar_expresion_multiplicativa())
            nodo = nodo_temp
            
        return nodo

    def analizar_expresion_multiplicativa(self):
        nodo = self.analizar_factor()
        
        while self.token_actual and self.token_actual[1] in ['*', '/']:
            operador = self.token_actual[1]
            self.siguiente_token()
            nodo_temp = NodoAST("OPERACION", operador)
            nodo_temp.agregar_hijo(nodo)
            nodo_temp.agregar_hijo(self.analizar_factor())
            nodo = nodo_temp
            
        return nodo

    def analizar_factor(self):
        if not self.token_actual:
            self.error_sintaxis("un factor", "fin de archivo")

        if self.token_actual[2] == "ID":
            token = self.match_tipo("ID")
            return NodoAST("ID", token[1])
        elif self.token_actual[2] == "NUMERICO":
            token = self.match_tipo("NUMERICO")
            return NodoAST("NUMERO", token[1])
        elif self.token_actual[1] == "(":
            self.match("(")
            expr = self.analizar_expresion()
            self.match(")")
            return expr
        else:
            self.error_sintaxis("un identificador o número", 
                              f"token '{self.token_actual[1]}'")

    def analizar_condicion(self):
        nodo = NodoAST("CONDICION")
        expr_izq = self.analizar_expresion()
        if self.token_actual and self.token_actual[2] == "OPERADORES_REL":
            operador = self.token_actual[1]
            self.match_tipo("OPERADORES_REL")
            nodo_rel = NodoAST("OPERACION_REL", operador)
            nodo_rel.agregar_hijo(expr_izq)
            nodo_rel.agregar_hijo(self.analizar_expresion())
            return nodo_rel
        return expr_izq
    
def imprimir_ast(nodo, nivel=0):
    """Versión mejorada de la impresión del AST"""
    indentacion = "  " * nivel
    if nodo.valor:
        print(f"{indentacion}{nodo.tipo}({nodo.valor})")
    else:
        print(f"{indentacion}{nodo.tipo}")
        
    for hijo in nodo.hijos:
        imprimir_ast(hijo, nivel + 1)