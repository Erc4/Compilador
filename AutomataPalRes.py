#AutomataPasRes
class AutomataPalRes:
    def __init__(self,lista_palres):
        self.lista_palres = lista_palres
        self.estado=0

    def procesarcadena(self,cadena):
        if cadena in self.lista_palres:
            return True
        else:
            return False
        
lista_palres = ["inicio","fin","si","entonces","si no","funcion","escribir","mientras","repetir",
                        "para","caso","var","const","entero","decimal","booleano","nulo","verdadero","falso",
                        "real","    cadena","arreglo","hacer", "hacer mientras", "retornar"]

automata = AutomataPalRes(lista_palres)
cadenas = ["entonces","decimales","hacer","arreglos","cadena","nulo","mientras","hacer mientras"]

for cadena in cadenas:
    if automata.procesarcadena(cadena):
        print(f"cadena {cadena} valida")
    else:
        print(f"cadena {cadena} no valida")


    