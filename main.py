# main.py
from Analizadorlexico import AnalizadorLexico, Preprocesador
from AnalizadorSintactico import AnalizadorSintacticoCompleto, imprimir_ast
from colorama import init, Fore, Style

def main():
    init()  # Inicializar colorama
    
    # Archivos de entrada y salida
    archivo_entrada = "pruebatexto.txt"
    archivo_preprocesado = "Posprocesado.txt"
    
    print(f"\n{Fore.YELLOW}Iniciando compilación...{Style.RESET_ALL}")
    
    # Paso 1: Preprocesamiento
    print(f"\n{Fore.CYAN}Fase de preprocesamiento...{Style.RESET_ALL}")
    preprocesador = Preprocesador()
    if not preprocesador.preprocesar_archivo(archivo_entrada, archivo_preprocesado):
        return

    # Mostrar contenido del archivo original
    codigo_original = preprocesador.leer_archivo_procesado(archivo_entrada)
    print(f"\n{Fore.YELLOW}Código fuente original:{Style.RESET_ALL}")
    print("-" * 80)
    print(codigo_original)
    print("-" * 80)

    # Mostrar contenido del archivo preprocesado
    codigo_preprocesado = preprocesador.leer_archivo_procesado(archivo_preprocesado)
    print(f"\n{Fore.YELLOW}Código preprocesado:{Style.RESET_ALL}")
    print("-" * 80)
    print(codigo_preprocesado)
    print("-" * 80)

    if codigo_preprocesado is None:
        return

    try:
        # Paso 2: Análisis léxico
        print(f"\n{Fore.CYAN}Iniciando análisis léxico...{Style.RESET_ALL}")
        analizador_lexico = AnalizadorLexico(codigo_preprocesado)
        tokens = analizador_lexico.analizar()
        
        print("\n" + "=" * 80)
        print(f"{Fore.CYAN}ANÁLISIS LÉXICO - TOKENS GENERADOS{Style.RESET_ALL}")
        print("=" * 80)
        print(f"{'ID':<5} {'LEXEMA':<15} {'TIPO':<20} {'VALOR':<10} {'LÍNEA':<8} {'COLUMNA':<8}")
        print("-" * 80)
        for token in tokens:
            id_token, lexema, tipo, valor, linea, columna = token
            print(f"{id_token:<5} {lexema:<15} {tipo:<20} {valor:<10} {linea:<8} {columna:<8}")

        # Paso 3: Análisis sintáctico
        print(f"\n{Fore.GREEN}Iniciando análisis sintáctico...{Style.RESET_ALL}")
        analizador_sintactico = AnalizadorSintacticoCompleto(tokens)
        ast = analizador_sintactico.analizar()
        
        print("\n" + "=" * 80)
        print(f"{Fore.GREEN}ANÁLISIS SINTÁCTICO - ÁRBOL DE SINTAXIS ABSTRACTA (AST){Style.RESET_ALL}")
        print("=" * 80)
        imprimir_ast(ast)

        print(f"\n{Fore.WHITE}Compilación completada exitosamente.{Style.RESET_ALL}")

    except Exception as e:
        print(f"\n{Fore.RED}Error durante la compilación:{Style.RESET_ALL}")
        print(str(e))

if __name__ == "__main__":
    main()