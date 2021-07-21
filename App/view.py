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
    print("1- Caracterizar reproducciones")             #REQ 1
    print("2- Encontrar música para festejar")          #REQ 2
    print("3- Encontrar música para la tusa")           #REQ 3
    print("4- Estudiar los géneros musicales")          #REQ 4
    print("5- Consultar / modificar generos musicales") #REQ 4
    print("0- Salir")


def printRow(row: list) -> None:
    """
    Imprime la fila de una tabla. Si el largo de los datos supera el ancho de la columna,
    imprime el dato incompleto con ...
    Args:
        row: Lista de listas. Row debe ser de la forma [<lens>, <data>]
            <lens>: (list) Lista con ancho de las columnas
            <data>: (list) Lista con datos de las columnas
    TODO Manejo de ancho y caracteres asiaticos
    """
    rowFormat = ""
    for i in range(0, len(row[0])):
        colWidth = row[0][i]
        cell = str(row[1][i])
        #Añade la columna al formato
        rowFormat += "{:<" + str(colWidth) + "}"
        #Revisa y corrige si el tamaño de los datos es más grande que la columna
        if len(cell) > colWidth:
            row[1][i] = cell[0:colWidth - 3] + "..."
    
    #Imrpime la fila
    print(rowFormat.format(*row[1]))


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
    if ans == False:
        print("No hay eventos que cumplan con los filtros")
    else:
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

    if ans == False:
        print("Ningún evento cumple los filtros")
        input("\nENTER para continuar")
        return ...
    
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

    if ans == False:
        print("Ningún evento cumple con los filtros")
        input("\nENTER para continuar")
        return ...
    
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


def lstMusicGenders():
    genders = controller.getGenders()
    printRow([
            [20, 10, 10],
            [
                "Nombre",
                "BPM inf",
                "BPM sup"
            ]
    ])
    for genderName in genders:
        printRow([
            [20, 10, 10],
            [
                genderName,
                genders[genderName][0],
                genders[genderName][1]
            ]
        ])
    input("\nENTER para continuar")


def modifyMusicGenders():
    print("Ingrese el nombre de el genero que desea modificar o agregar")
    genderName = input("> ")
    if controller.genderExists(genderName):
        print("MODIFICANDO genero", genderName)
    else:
        print("AGREGANDO genero", genderName)
    
    tempo_inf = float(input("Límite inferior de tempo: "))
    tempo_sup = float(input("Límite superior de tempo: "))

    controller.modifyGender(genderName, tempo_inf, tempo_sup)
    print("Genero modificado exitosamente")
    input("\nENTER para continuar")


def studyMusicGenders(analyzer):
    """
    TODO documentación
    """
    #INPUT
    toStudy = input("Ingrese lista de generos a estudiar separada por ',': ").split(",")
    ans = controller.songsByGender(analyzer, toStudy)
    genderNames = mp.keySet(ans[0])
    for genderName in lt.iterator(genderNames):
        tempo = getMapValue(ans[0], genderName, "MP")["tempo"]
        genderEventCount = getMapValue(ans[0], genderName, "MP")["repros"]
        genderArtistCount = getMapValue(ans[0], genderName, "MP")["artistCnt"]
        genderArtists = getMapValue(ans[0], genderName, "MP")["artists"]
        print("\n\n====", genderName, "====")
        print("Para", genderName, "el tempo está entre", tempo[0], "y", tempo[1])
        print(genderName, "tiene", genderEventCount, "reproducciones y",
        genderArtistCount, "artistas")
        i = 1
        for artist in lt.iterator(genderArtists):
            print("Artista", i, ":", artist)
            i += 1
    print("\nTotal de eventos:", ans[1])
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
            #REQ 1
            playsByCharacteristics(analyzer)

        elif int(inputs[0]) == 2:
            #REQ 2
            celebrationMusic(analyzer)
        
        elif int(inputs[0]) == 3:
            #REQ 3
            breackupMusic(analyzer)

        elif int(inputs[0]) == 4:
            #REQ 4
            studyMusicGenders(analyzer)
        
        elif int(inputs[0]) == 5:
            print("Seleccione una opción")
            print("1- Consultar generos")
            print("2- Modificar generos")
            option = int(input("> ")[0])
            if option == 1:
                lstMusicGenders()
            elif option == 2:
                modifyMusicGenders()
            else:
                print("Opción invalida")
        else:
            sys.exit(0)


def getMapValue(map, key, type = "OM"):
    """
    Devuelve el valor correspondiente a la llave pasada por
    parámetro en el mapa pasado por parámetro
    
    Args
    ----
        map -- Mapa
        key -- llave
        type: str -- tipo de mapa. 'OM' para ordered map y 'MP'
        para mapa normal
    
    Returns
    -------
    Valor correspondiente a la llave o None si no se encuentra la llave
    en el mapa
    """
    if type == "OM":
        entry = om.get(map, key)
    elif type == "MP":
        entry = mp.get(map, key)
    else:
        raise Exception("Invalid map type. Type param must be 'OM' or 'MP'")
    
    if entry is None:
        return None

    val = me.getValue(entry)
    return val

"""
Programa Principal
"""
initProgram()