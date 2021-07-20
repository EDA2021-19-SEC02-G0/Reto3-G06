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
 """

import config as cf
import model
import csv
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
    return model.playsByCharacteristics(analyzer, char1, char1_inf,
    char1_sup, char2, char2_inf, char2_sup)