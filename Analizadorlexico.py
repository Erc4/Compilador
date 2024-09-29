import re

file = open("read.py")

operadores = {'=' : 'igual op','+' : 'suma op','-' : 'resta op','/' : 'division op','*' : 'multiplicacion op','<' : 'menorque op','>' : 'mayorque op','<=' : 'menorigual op','>=' : 'mayorigual op',}
operadores_key = operadores.keys()

tipo_dato = {'entero' : 'tipo entero', 'flotante': 'tipo flotante' , 'caracter' : 'tipo caracter', 'booleano' : 'tipo boleano', 'cadena': 'tipo cadena' }
tipo_dato_key = tipo_dato.keys()

punctuation_symbol = { ':' : 'dospuntos', ';' : 'puntoycoma', '.' : 'punto' , ',' : 'coma' }
punctuation_symbol_key = punctuation_symbol.keys()

identifier = { 'a' : 'id', 'b' : 'id', 'c' : 'id' , 'd' : 'id' }
identifier_key = identifier.keys()

dataFlag = False

a=file.read()

count=0
program = a.split("\n")
for line in program:
    count = count + 1
    print("line#" , count, "\n" , line)

    tokens=line.split(' ')
    print("Tokens are " , tokens)
    print("Line#", count, "properties \n")
    for token in tokens:
        if token in operadores_key:
            print("operator is ", operadores[token])
        if token in tipo_dato_key:
            print("datatype is", tipo_dato[token])
        if token in punctuation_symbol_key:
            print (token, "Punctuation symbol is" , punctuation_symbol[token])
        if token in identifier_key:
            print (token, "Identifier is" , identifier[token])

    dataFlag=False
    print("_ _ _ _ _ _ _ _ _ _ _ _ _ _ _  _") 