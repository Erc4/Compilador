class AutomataIdentificador:
    def __init__(self):
        self.estado = 0

    def procesarcadena(self, cadena):
        # El identificador no puede estar vacío
        if len(cadena) == 0:
            return False

        for caracter in cadena:
            if self.estado == 0:  # q0 - El primer carácter debe ser una letra
                if caracter.isalpha():  # Verifica si es una letra
                    self.estado = 1     # Pasa al estado de aceptación
                else:
                    return False  # Si no es letra, no es válido
            elif self.estado == 1:  # q1 - Restantes caracteres pueden ser letras, dígitos o '_'
                if not (caracter.isalnum() or caracter == '_'):
                    return False  # Si encuentra algo distinto a letras, dígitos o '_', no es válido

        return self.estado == 1  # La cadena es aceptada si está en el estado de aceptación

# Instanciamos el autómata
automata = AutomataIdentificador()

# Prueba con identificadores válidos e inválidos
cadenas = ["_variable", "asda", "juan_123", "juan123_"]
for cadena in cadenas:
    if automata.procesarcadena(cadena):
        print(f"Cadena '{cadena}' aceptada")
    else:
        print(f"Cadena '{cadena}' no aceptada")
