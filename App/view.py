"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

from random import randint
import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import orderedmap as om

#Desactiva el seguimiento de memoria para mejorar rendimeinto
controller.mtTrace.trace_memory = False

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

# =============================
#       Output functions
# =============================
def printMenu():
    """
    Imprime el menú de opciones del programa
    """
    print("Bienvenido")
    print("1- Caracterizar reproducciones")     #REQ 1
    print("2- Encontrar música para festejar")  #REQ 2
    print("3- Encontrar música para la tusa")   #REQ 3
    print("4- Estudiar los géneros musicales")  #REQ 4
    print("0- Salir")

# =============================
#       Option functions
# =============================
def playsByCharacteristics(analyzer):
    """
    REQUERIMIENTO 1
    Pide el input del usuario, procesa e imprime cuantas
    reproducciones cumplen con dos características en un
    rango determinado.

    Args:
        catalog: catálogo
        TODO mejorar Args
    """
    char1 = input("Característica 1 (ej.: valencia, sonoridad): ")
    char1_inf = float(input("Valór mínimo para " + char1 + ": "))
    char1_sup = float(input("Valor máximo para " + char1 + ": "))
    char2 = input("Característica 1 (ej.: valencia, sonoridad): ")
    char2_inf = float(input("Valór mínimo para " + char2 + ": "))
    char2_sup = float(input("Valor máximo para " + char2 + ": "))
    ans = controller.playsByCharacteristics(analyzer, char1, char1_inf, 
    char1_sup, char2, char2_inf, char2_sup)
    print("\nTotal de eventos de reproducción:", lt.size(ans["repros"]))
    print("Total de artistas:", mp.size(ans["artists"]))
    input("\nENTER para continuar")


def celebrationMusic(analyzer):
    """
    REQUERIMIENTO 2
    TODO documentation
    """
    #Input
    liveness_inf = float(input("Valor mínimo para Liveness: "))
    liveness_sup = float(input("Valor máximo para Liveness: "))
    speechness_inf = float(input("Valor mínimo para Speechness: "))
    speechness_sup = float(input("Valor máximo para Speechness: "))
    #Process
    ans = controller.playsByCharacteristics(analyzer, "liveness", liveness_inf, 
    liveness_sup, "speechiness", speechness_inf, speechness_sup)
    trackCount = mp.size(ans["tracks"])
    tracksLst = mp.valueSet(ans["tracks"])
    #Output
    print("\nTotal de pistas:", trackCount)
    for i in range(1, 9):
        trackIndex = randint(1, trackCount)   
        track = lt.getElement(tracksLst, trackIndex)
        print("Track", i, ":", track["track_id"], "with liveness", track["liveness"],
        "and speechness", track["speechiness"])

    input("\nENTER para continuar")


def breackupMusic(analyzer):
    """
    REQUERIMIENTO 3
    TODO documentation
    """
    #INPUT
    valence_inf = float(input("Valor mínimo para Valence: "))
    valence_sup = float(input("Valor máximo para Valenve: "))
    tempo_inf = float(input("Valor mínimo para Tempo: "))
    tempo_sup = float(input("Valor máximo para Tempo: "))
    #PROCESS
    ans = controller.playsByCharacteristics(
        analyzer,
        "valence",
        valence_inf,
        valence_sup,
        "tempo",
        tempo_inf,
        tempo_sup
    )
    trackCount = mp.size(ans["tracks"])
    tracksLst = mp.valueSet(ans["tracks"])
    #Output
    print("\nTotal de pistas:", trackCount)
    for i in range(1, 9):
        trackIndex = randint(1, trackCount)   
        track = lt.getElement(tracksLst, trackIndex)
        print("Track", i, ":", track["track_id"], "with valence", track["valence"],
        "and tempo", track["tempo"])

    input("\nENTER para continuar")

# =============================
#          Main program
# =============================
def initProgram():
    """
    Inicializa el programa cargando los datos. Posteriormente llama
    al menú principal
    """
    print("Bienvenido")
    print("A continuación se procederá a cargar la información de los archivos")
    init = input("ENTER para continuar o 0 para salir\n> ")
    if init == "0":
        sys.exit(0)
    print("Cargando...")
    #Inicializa el analizador
    analyzer = controller.initAnalyzer()
    #Carga la información
    controller.loadData(analyzer)
    #Output de datos cargados
    print("Total de registros cargados:", lt.size(analyzer["repros"]))
    print("Total de artistas diferentes cargados:", mp.size(analyzer["artists"]))
    print("Total de pistas diferentes cargadas:", mp.size(analyzer["tracks"]))
    input("ENTER para continuar")
    print("** PRIMEROS 5 REGISTROS ***")
    first5Events = lt.subList(analyzer["repros"], 1, 5)
    i = 1
    for event in lt.iterator(first5Events):
        print("Event", i, "\n")
        for key in event:
            print(key, ":", event[key])
    input("ENTER para continuar")
    print("\n*** ÚLTIMOS 5 REGISTROS ***")
    last5Events = lt.subList(analyzer["repros"], lt.size(analyzer["repros"]) - 5, 5)
    i = 1
    for event in lt.iterator(last5Events):
        print("\nEvent", i, "\n")
        i += 1
        for key in event:
            print(key, ":", event[key])
    input("ENTER para continuar")
    #Main menu
    mainMenu(analyzer)


def mainMenu(analyzer):
    """
    Menú principal. Le permite al usuario ejecutar las opción
    del programa.

    Args:
        catalog -- catálogo
        TODO mejorar documentación
    """
    while True:
        print("")
        printMenu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs[0]) == 1:
            playsByCharacteristics(analyzer)

        elif int(inputs[0]) == 2:
            #REQ 2
            celebrationMusic(analyzer)
        
        elif int(inputs[0]) == 3:
            #REQ 3
            breackupMusic(analyzer)

        elif int(inputs[0]) == 4:
            #REQ 4
            pass

        else:
            sys.exit(0)


"""
Programa Principal
"""
initProgram()