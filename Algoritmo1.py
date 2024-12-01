#Algoritmo1.py
def Preprocesar_archivo(nombre_archivo_entrada, nombre_archivo_salida):

    try:
        with open(nombre_archivo_entrada, 'r') as archivo_entrada:
            lineas_procesadas = []

            for linea in archivo_entrada:
                # Eliminar espacios en blanco al inicio y al final de la línea
                linea = linea.strip()

                # Ignorar líneas vacías
                if not linea:
                    continue

                # Ignorar comentarios (suponiendo que los comentarios comienzan con '#')
                if linea.startswith('#'):
                    continue

                # Agregar línea procesada a la lista
                linea = linea.replace(' ', '').replace('\t', '')

                lineas_procesadas.append(linea)

        # Guardar las líneas procesadas en un nuevo archivo
        with open(nombre_archivo_salida, 'w') as archivo_salida:
            for linea in lineas_procesadas:
                archivo_salida.write(linea + '\n')

        print(f"El archivo ha sido procesado y guardado como '{nombre_archivo_salida}'.")

    except FileNotFoundError:
        print("El archivo de entrada no fue encontrado.")
    except Exception as e:
        print(f"Ha ocurrido un error: {e}")

def Recorrer_archivo_(archivo_procesado):
    try:
        with open (archivo_procesado, 'r') as archivo:
            contenido = archivo.read()
            print ("Contenido del archivo:\n")
            for caracter in contenido:
                print(caracter, end='')
    except FileNotFoundError:
        print("El archivo no fue encontrado.")
    except Exception as e:
        print (f"Ha ocurrido un error: {e}")


# Uso de la función
Preprocesar_archivo('pruebatexto.txt', 'Posprocesado.txt')
Recorrer_archivo_('Posprocesado.txt')

