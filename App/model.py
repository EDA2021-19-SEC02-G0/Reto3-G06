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


from os import replace
from DISClib.DataStructures.arraylist import addLast, isPresent
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.ADT import orderedmap as om
import sys
assert cf
import json

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
        "AcousticnessIn":               None,
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

    analyzer["repros"]=lt.newList('ARRAY_LIST')

    analyzer['InstrumentalnessIn']=om.newMap(omaptype='RBT')
    analyzer['AcousticnessIn']=om.newMap(omaptype='RBT')
    analyzer['LivenessIn']=om.newMap(omaptype='RBT')
    analyzer['SpeechinessIn']=om.newMap(omaptype='RBT')
    analyzer['EnergyIn']=om.newMap(omaptype='RBT')
    analyzer['DanceabilityIn']=om.newMap(omaptype='RBT')
    analyzer['ValenceIn']=om.newMap(omaptype='RBT')
    analyzer['LoudnessIn']=om.newMap(omaptype='RBT')
    analyzer['TempoIn']=om.newMap(omaptype='RBT')

    analyzer['tracks']=mp.newMap(numelements=88000,maptype='CHAINING',loadfactor=0.5)
    analyzer['artists']=mp.newMap(numelements=88000,maptype='CHAINING',loadfactor=0.5)
    
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
def playsByCharacteristics(analyzer: dict, char1: str, char1_inf: float,char1_sup: float, char2: str, char2_inf: float, char2_sup: float) -> dict:
    """
    Cuántas reproducciones (eventos de escucha) se tienen en el sistema de
    recomendación basado en la intersección de dos características de 
    contenido que se encuentran en un rango determinado

    Args
    ----

    Analyzer            -- analizador de reproducciones
    char1 : str         -- nombre de la característica 1
    char1_inf : float   -- valor mínimo de la característica 1
    char1_sup : float   -- valor máximo de la característica 1
    char2 : str         -- nombre de la característica 2
    char2_inf : float   -- valor mínimo de la característica 2
    chat2_sup : float   -- valor máximo de la característica 2

    Returns : dict[str, int] | Bool
    ------
    Diccionario ["repros": <cantidad de reproducciones>, "artists": 
    <número de artistas>] o Falso si ningún evento cumple con los
    filtros
    """
    #Obtiene el mapa de características de char1 y char2
    char1Map = analyzer.get(reprosHandler.getCharsToMapKey(char1.strip().lower()))
    char2Map = analyzer.get(reprosHandler.getCharsToMapKey(char2.strip().lower()))
   
    #Check if there are maps that match the char Name
    if char1Map is None or char2Map is None:
        #Return no events that match the filters
        #return False
        pass
      
    #Obtiene las llaves que cumplen con el filtro de char1
    char1EventsKeys = om.keys(char1Map, char1_inf, char1_sup)
    #Mapa de los eventos que cumplen con char1
    c1EventsMap = mp.newMap(100000, loadfactor=2) #TODO determinar tamaño
    #Ciclo por las llaves
    for char1EventsKey in lt.iterator(char1EventsKeys):
        char1EventsLst = getMapValue(char1Map, char1EventsKey)
        #Iterar por los eventos de cada nodo del mapa de características
        for event in lt.iterator(char1EventsLst):
            mp.put(c1EventsMap, event["id"], event)

    #Llaves que cumplen con el filtro char1 y char2
    c2EventsKeys = om.keys(char2Map, char2_inf, char2_sup)
    matchEventsCnt = 0
    #Mapa con artistas
    artistsMap = mp.newMap(100000, loadfactor=2) #TODO determinar tamaño
    #Mapa con pistas
    trackMap = mp.newMap(100000, loadfactor=2)
    #Lista de eventos que cumplen las condiciones
    eventsLst = lt.newList("ARRAY_LIST")
    #Ciclo por las llaves
    for c2EventsKey in lt.iterator(c2EventsKeys):
        c2EvetnsLst = getMapValue(char2Map, c2EventsKey)
        #Iterar por los eventos de cada nodo del mapa de caracterísricas
        for event in lt.iterator(c2EvetnsLst):
            #Si está en el mapa de eventos que cumplen char1
            if mp.contains(c1EventsMap, event["id"]):
                #Añade a la lista de eventos
                lt.addLast(eventsLst, event)
                artist = getMapValue(artistsMap, event["artist_id"], "MP")
                track = getMapValue(trackMap, event["track_id"], "MP")
                #Revisa si ya se añadió ese artista
                if artist is None:
                    #Añade el artista
                    mp.put(artistsMap, event["artist_id"], event)
                #Añade 1 a la cuenta de eventos que cumplen con los filtros
                matchEventsCnt += 1
                #Revisa si ya se añadió la pista
                if track is None:
                    mp.put(trackMap, event["track_id"], event)

    #Revisar si hay eventos que cumplen los filtros
    if lt.isEmpty(eventsLst):
        return False       

    returnDict = {
        "repros" :      eventsLst,
        "artists":      artistsMap,
        "tracks":       trackMap
    }
    
    return returnDict


def songsByGender(analyzer, toStudy: list):
    """
    Retorna un diccionario con el tempo, el número de eventos de escucha, el
    número de artistas y el ID de los 10 primeros artistas 
    correspondientes a cada genero pasado en la lista de generos toStudy.

    Args
    ----
    analyzer -- analizador de eventos
    toStudy : list[str] -- lista con los nombres de los generos

    Returns : dict[str, Any]
    -------
    Diccionario con llaves correspondientes a genderName. Adicionalmente
    con llave 'total' con totales de los campos a los que aplica
    """
    genders = reprosHandler.getGenders()
    returnDict = mp.newMap(100000, loadfactor=2) #TODO determinar tamaño
    eventsCount = 0
    for genderName in toStudy:
        genderArtistsMap = mp.newMap(10, loadfactor=1) #TODO determinar tamaño
        genderArtistsLst = lt.newList()
        genderEventsCnt = 0
        genderArtistCount = 0
        genderName: str = genderName.strip().lower()
        genderTempo = genders.get(genderName)
        if genderTempo is None:
            raise Exception("Invalid gender name: " + str(genderName))
        tempoKeys = om.keys(
            analyzer[reprosHandler.getCharsToMapKey("tempo")],
            genderTempo[0],
            genderTempo[1]
        )
        for tempo in lt.iterator(tempoKeys):
            events = getMapValue(
                analyzer[reprosHandler.getCharsToMapKey("tempo")],
                tempo
            )
            genderEventsCnt += lt.size(events)
            for event in lt.iterator(events):
                if not mp.contains(genderArtistsMap, event["artist_id"]):
                    mp.put(genderArtistsMap, event["artist_id"], None)
                    genderArtistCount += 1
                    if lt.size(genderArtistsLst) < 10:
                        lt.addLast(genderArtistsLst, event["artist_id"])
        eventsCount += genderEventsCnt          
        mp.put(returnDict, genderName, {
            "tempo":        genderTempo,
            "repros":       genderEventsCnt,
            "artists":      genderArtistsLst,
            "artistCnt":    mp.size(genderArtistsMap)
        })
    
    return returnDict, eventsCount
                




def genderExists(genderName: str):
    """
    Retorna verdadero si el genero existe en el archivo .json
    de generos o Falso si no existe

    Args
    ----
    genderName: str -- nombre del género a buscar
    """
    genderName = genderName.strip().lower()
    genders = reprosHandler.getGenders()

    if genderName in genders:
        return True
    return False


def modifyGender(genderName, tempo_inf, tempo_sup):
    """
    TODO documentación
    """
    return reprosHandler.modifyGender(genderName, tempo_inf,
    tempo_sup)
        




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
        __charsToMap: dict[str, str], private -- diccionario en el que las llaves son
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
        "tempo" :               "TempoIn",
        "acousticness" :         "AcousticnessIn",
        "energy":                  "EnergyIn"
    }


    def getCharsToMapKey(charName: str) -> str:
        """
        Retorna la llave del diccionario analyzer correspondientes
        a la característica indicada por parámetro.

        Args
        ----
        charName : str      -- Nombre de la característica

        Returns : str       -- Key del dict analyzer corrrespondiente
        al mapa de la característica
        """
        mapKey = reprosHandler.charsToMap.get(charName)

        return mapKey
    

    def getGenders() -> dict:
        """
        Retorna un diccionario con los generos y los rangos de tempo
        de cada genero. Las llaves del diccionario son los nombres
        de los generos y los valores de este son listas de dos elementos.
        Los elementos de las listas son de tipo int y corresponden al
        limite inferior y superior de tempo del genero en ese orden.
        """
        with open("Data/music-genders.json", "r", encoding="utf-8") as jsonGen:
            genders = json.load(jsonGen)

        return genders


    def modifyGender(genderName: str, tempo_inf: float, tempo_sup: float):
        """
        Modifica o agrega un genero al archivo .json de generos

        Args
        ----
        genderName: str -- nombre del genero a modificar o agregar
        tempo_inf: float -- límite inferior de tempo a agregar
        tempo_sup: flaot -- límite superior de tempo a agregar
        """
        genderName = genderName.strip().lower()
        genders = reprosHandler.getGenders()
        genders[genderName] = [tempo_inf, tempo_sup]
        with open("Data/music-genders.json", "w") as jsonGen:
            json.dump(genders, jsonGen)

