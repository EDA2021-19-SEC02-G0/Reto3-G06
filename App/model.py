"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.ADT import orderedmap as om
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newAnalizer():
    """
    Inicializa el analizador

    Crea una lista vacia para guardar todas las reproducciones
    Se crean indices (Maps ordenado) por todas las características
    de contenido

    Retorna el analizador inicializado.
    """
    #TODO determinar el tipo de mapa ordenado y asignar funciones de comparación
    analyzer = {"repros":               None,
        "InstrumentalnessIn":           None,
        "Acousticnessin":               None,
        "LivenessIn":                   None,
        "SpeechinessIn":                None,       
        "EnergyIn":                     None,
        "DanceabilityIn":               None,
        "ValenceIn":                    None,
        "LoudnessIn":                   None,
        "TempoIn":                      None,
        "tracks":                       None,
        "artists":                      None
                }
    analyzer["repros"]=lt.newList('ARRAY_LIST',compareRepros)

    analyzer['InstrumentalnessIn']=om.newMap(omaptype='RBT',comparefunction=compareInstrumental)

    analyzer['Acousticnessin']=om.newMap(omaptype='RBT',comparefunction=compareAcoustic)

    analyzer['LivenessIn']=om.newMap(omaptype='RBT',comparefunction=compareLiveness)

    analyzer['SpeechinessIn']=om.newMap(omaptype='RBT',comparefunction=compareSpeech)

    analyzer['EnergyIn']=om.newMap(omaptype='RBT',comparefunction=compareEnergy)

    analyzer['DanceabilityIn']=om.newMap(omaptype='RBT',comparefunction=compareDance)

    analyzer['ValenceIn']=om.newMap(omaptype='RBT',comparefunction=compareValance)

    analyzer['LoudnessIn']=om.newMap(omaptype='RBT',comparefunction=compareLoud)

    analyzer['TempoIn']=om.newMap(omaptype='RBT',comparefunction=compareTempo)

    analyzer['tracks']=mp.newMap()

    analyzer['artists']=mp.newMap()
    

    return analyzer


def addEvent(analyzer, listenEvent):
    """
    Carga 1 enento de escucha al analizador

    Args
    ----
        listenEvent: dict -- Evento de escucha obtenido del archivo 
        context_content_features-small.csv
    """
    # Añade evento a la lista de reproducciones
    lt.addLast(analyzer["repros"], listenEvent)
    # Añade evento a los mapas ordenados de características
    addToCharMaps(analyzer, listenEvent)
    # Añade la pista al mapa de pistas
    addEventsTrack(analyzer, listenEvent)
    # Añade el artista al mapa de artistas
    addEventsArtist(analyzer, listenEvent)


def addToCharMaps(analyzer, listenEvent):
    """
    Añade un evento de escucha a los mapas ordenados de características
    del evento de escucha

    Args
    ----
        analyzer -- analizador de reproducciones
        listenEvent: dict -- diccionario con información del evento de escucha
    """
    #Ciclo por todas las características de un evento de escucha
    for charName in reprosHandler.charsToMap:
        #Obtener el mapa correspondiente a la característica
        charMap = analyzer[reprosHandler.charsToMap[charName]]
        #Obtiene el valor correspondiente a la catacterística
        charVal = float(listenEvent[charName])
        #Obtiene la lista con eventos que tienen ese valor en esa característica
        charList = getMapValue(charMap, charVal)
        if charList is None:
            #Si el valor para la característica no estaba en el mapa
            #Crea una lista
            charList = lt.newList("ARRAY_LIST")
            #Añade el evento a la lista de eventos
            lt.addLast(charList, listenEvent)
            #Añade charVal como llave y charList como valor al mapa de características
            om.put(charMap, charVal, charList)
        else:
            #Añade el evento a la lista de eventos
            lt.addLast(charList, listenEvent)


def addEventsTrack(analyzer, listenEvent):
    """
    Añade la pista presente en un evento de escucha al mapa de pistas
    si no se ha añadido antes.

    Args
    ----
    analyzer -- analizador de eventos
    listenEvent -- evento de escucha
    """
    tracksMap = analyzer["tracks"]
    trackEvent = getMapValue(tracksMap, listenEvent["track_id"], "MP")
    if trackEvent is None:
        mp.put(tracksMap, listenEvent["track_id"], listenEvent)


def addEventsArtist(analyzer, listenEvent):
    artistsMap = analyzer["artists"]
    artistEvent = getMapValue(artistsMap, listenEvent["artist_id"], "MP")
    if artistEvent is None:
        mp.put(artistsMap, listenEvent["artist_id"], listenEvent)


# Funciones para agregar informacion al catalogo
# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento


# =========================
# Otras funciones y clases
# =========================


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


class reprosHandler:
    """
    Contiene variables estáticas con información
    de los eventos de escucha y los mapas
    en los que se almacenan

    Atributes
    ---------
        keysToMap: dict[str, str] -- diccionario en el que las llaves son
        las llaves en un diccionario de evento de escucha, correspondientes
        a las características . Los valores son las llaves del diccionario analyzer,
        que corresponden a los mapas ordenados de cada característica de un evento
        de escucha

    """

    charsToMap : dict = {
        "instrumentalness" :    "InstrumentalnessIn",
        "liveness" :            "LivenessIn",
        "speechiness" :         "SpeechinessIn",
        "danceability" :        "DanceabilityIn",
        "valence" :             "ValenceIn",
        "loudness" :            "LoudnessIn",
        "tempo" :               "TempoIn"
    }

def compareRepros(repro1,repro2):
    if (repro1 == repro2):
        return 0
    elif repro1 > repro2:
        return 1
    else:
        return -1

def compareInstrumental(instrumental1,instrumental2):
    if (instrumental1 == instrumental2):
        return 0
    elif instrumental1 > instrumental2:
        return 1
    else:
        return -1
def compareAcoustic(acoustic1,acoustic2):
    if (acoustic1 == acoustic2):
        return 0
    elif acoustic1 > acoustic2:
        return 1
    else:
        return -1
def compareLiveness(liveness1,liveness2):
    if ( liveness1 == liveness2) :
        return 0
    elif liveness1 > liveness2 :
        return 1
    else:
        return -1
def compareSpeech(speech1,speech2):
    if ( speech1 == speech2) :
        return 0
    elif speech1 > speech2 :
        return 1
    else:
        return -1
def compareEnergy(energy1,energy2):
    if ( energy1 == energy2) :
        return 0
    elif energy1 > energy2:
        return 1
    else:
        return -1
def compareDance(dance1,dance2):
    if ( dance1 == dance2) :
        return 0
    elif dance1 > dance2 :
        return 1
    else:
        return -1
def compareValance(valance1,valance2):
    if ( valance1 == valance2) :
        return 0
    elif valance1 > valance2 :
        return 1
    else:
        return -1
def compareLoud(loud1,loud2):
    if ( loud1 == loud2) :
        return 0
    elif loud1 > loud2 :
        return 1
    else:
        return -1

def compareTempo(tempo1,tempo2):
    if ( tempo1 == tempo2) :
        return 0
    elif tempo1 > tempo2 :
        return 1
    else:
        return -1