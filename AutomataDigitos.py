class AutomataDigitos:
    def __init__(self):
        self.estado = 0

    def procesarcadena(self, cadena):
        if len(cadena) != 1:  
            return False

        #| q0 | --- {0..9} --- || q1 ||

        for caracter in cadena:
            if self.estado == 0:              # q0
                if caracter.isdigit():
                    self.estado = 1           # q1
                else:
                    self.estado = -1
        return self.estado == 1

automata = AutomataDigitos()

cadena = "s"
if automata.procesarcadena(cadena):
    print("Cadena aceptada")
else:
    print("Cadena no aceptada")


                    

