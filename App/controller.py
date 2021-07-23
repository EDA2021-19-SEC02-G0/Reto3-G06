﻿"""
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
 """

import config as cf
import model
import csv
import time
import tracemalloc
from mtTrace import mtTrace #Memory and time trace


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de reproducciones
def initAnalyzer():
    """
    Inicializa el analizador

    Crea una lista vacia para guardar todas las reproducciones
    Se crean indices (Maps ordenado) por todas las características
    de contenido

    Retorna el analizador inicializado.
    """
    analyzer = model.newAnalizer()

    return analyzer


def loadData(analyzer) -> None:
    """
    Carga la información de los archivos al analizador.

    Args
    ----
        analyzer: Analizador inicializado
    """
    loadListenEvents(analyzer)
    #TODO load other files

def loadListenEvents(analyzer):
    reprosFile = cf.data_dir + "context_content_features-small.csv" #TODO remove '-small' for production
    listen_input_file = csv.DictReader(open(reprosFile, encoding="utf-8"),
                                delimiter=",")
    for listenEvent in listen_input_file:
        model.addEvent(analyzer, listenEvent)

# Funciones para la carga de datos

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def  playsByCharacteristics(analyzer, char1, char1_inf, char1_sup, char2, char2_inf, char2_sup):
    """
    TODO documentación
    """
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    ans = model.playsByCharacteristics(analyzer, char1, char1_inf,
    char1_sup, char2, char2_inf, char2_sup)
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()
    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    return ans,delta_time,delta_memory


def genderExists(genderName):
    """
    TODO documentación
    """
    return model.genderExists(genderName)


def modifyGender(genderName, tempo_inf, tempo_sup):
    """
    TODO documentación
    """
    return model.modifyGender(genderName, tempo_inf, tempo_sup)


def getGenders():
    """
    TODO documentación
    """
    return model.reprosHandler.getGenders()


def songsByGender(analyzer, toStudy: list):
    """
    TODO documentación 
    """
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    ans=model.songsByGender(analyzer, toStudy)
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()
    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    return ans,delta_time,delta_memory

def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(start_memory, stop_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory
