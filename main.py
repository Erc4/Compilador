from Analizadorlexico import AnalizadorLexico
from AnalizadorSintactico import AnalizadorSintactico
from PilaDobleEnlazada import PilaDobleEnlazada


# Código de prueba
codigo = """
x = 5 + 3;
si x > 2 entonces {
    y = x * 2;
}
y = 3 + 1;
"""

# Analizador léxico
print("Iniciando análisis léxico...")
analizador_lexico = AnalizadorLexico(codigo)
tokens = analizador_lexico.analizar()
print("Tokens generados:")
for token in tokens:
    print(token)

# Analizador sintáctico
print("\nIniciando análisis sintáctico...")
analizador_sintactico = AnalizadorSintactico(tokens)
ast = analizador_sintactico.analizar()

# Mostrar el AST generado
def imprimir_ast(nodo, nivel=0):
    print("  " * nivel + str(nodo))
    for hijo in nodo.hijos:
        imprimir_ast(hijo, nivel + 1)

print("\nÁrbol de Sintaxis Abstracta (AST):")
imprimir_ast(ast)

