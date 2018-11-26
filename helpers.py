"""Funciones de ayuda al programa principal

Funciones independientes de la aplicación
"""
import json
import os
import platform
import re
from terminaltables import SingleTable
from colorama import init
from termcolor import colored

# Inicializar colorama para compatibilidad en windows
init()

# VARIABLES GLOBALES #########

# Objeto que almacena las rutas de archivos de configuración
_CONFIG_FILES = {
    "empresas": "./config/empresas.json",
    "tipos_docs": "./config/tipos_docs.json",
    "paths": "./config/paths.json"
}

_LINE_SEPARADOR = "-"

_str_inputs = []

_opts_continuar = ["s", "n"]  # SI, NO


# DEFINICIÓN DE MÉTODOS #########

def lineSeparator(len):
    return _LINE_SEPARADOR * len


# @Decorador
# Imprimir valores solicitados al usuario
def printInputValues(func):
    def wrapper(*args, **kwargs):
        value = func(*args, **kwargs)
        clearConsole()
        str = "{}{}".format(args[0], value)
        _str_inputs.append(str)
        print("\n".join(_str_inputs))
        return value

    return wrapper


# Verificar si existen archivos de configuración
def checkIfConfigFilesExists():
    """Recorrer objeto que almacena rutas de configuración.

    Si no los encuentra imprime en consola el archivo no encontrado  y
    finaliza el programa
    """
    for ind, val in _CONFIG_FILES.items():
        if not os.path.exists(val):
            print("ERROR. No se ha podido encontrar el archivo {}"
                  .format(val))
            exit()


# Retornar data de archivo configuración
def getConfigData(str_key):
    """Obtiene data de archivo configuración por clave.

    Si sucede una excepción al abrir archivo imprime error y 
    finaliza el programa
    
    Parameters
    ----------
    str_key: str
        clave para reconocer archivo dentro de carpeta ./config
    
    Returns
    -------
    dict
        data obtenida de archivo
    """
    data = []
    try:
        data = json.loads(open(_CONFIG_FILES[str_key]).read())    
    except:
        print("Sucedió un error obteniendo data de archivos.")
        exit()
    
    return data


# Evaluar cadena completa por expresion regular
def fullMatchRExp(pattern, str):
    """
    Parameters
    ----------
    pattern: reg_exp
        Expresion regular a cumplir
    str: str
        Cadena a evaluar

    Returns
    -------
    bool
        evaluación de la expresión regular
    """
    return re.fullmatch(pattern, str)


# Limpiar consola según sistema operativo
def clearConsole():
    """Verifica el Sistema operativo usado para ejecutar comando de limpieza"""
    clear_command = "clear"
    if platform.system().lower() == "windows":
        clear_command = "cls"
    
    os.system(clear_command)


# Mostrar datos en formato de tabla
def printSingleTable(data, title, heading_row=True):
    """Imprimir datos en formato de tabla con título

    Parameters
    ----------
    data: array
        Datos a imprimir
    title: str
        titulo de tabla
    heading_row: bool
        (Default: True) Si es verdadero se considera la primera fila como el
        encabezado de la tabla

    """
    try:
        table = SingleTable(data)
        table.title = title
        table.inner_heading_row_border = heading_row
        print(table.table)
    except:
        print("Sucedió un error imprimiendo datos en tabla.")
        exit()


# Imprimir en consola un mensaje a color según tipo
def printOnConsole(str, type=""):
    """Muestra en consola un mensaje de diferente color segun el tipo

    Parameters
    ----------
    str: str
        mensaje a mostrar
    type: str
        define el tipo de mensaje
        "" : (Default) color blanco
        "w": warnining color amarillo
        "i": info color azul
        "e": error color rojo
    """
    color = "white"
    if type.lower() == "w":
        color = "yellow"
    elif type.lower() == "i":
        color = "blue"
    elif type.lower() == "e":
        color = "red"

    print(colored(str, color))


# guardar archivo desde datos binarios
def saveBinaryFile(bin_source, path, name):
    """Recibe datos binarios y los guarda como archivo

    Parameters
    ----------
    bin_source: bin
        Datos en binario a guardar
    path: str
        Ruta para ubicación de archivo
    name: str
        nombre de archivo a guardar

    Returns
    -------
    str
        ruta de ubicación final de archivo
    """
    full_path = ""
    try:
        full_path = os.path.join(path, name)

        with open(full_path, "wb") as file:
            file.write(bin_source)
    except:
        print("Sucedió un error al crear el archivo CDR")
        exit()
    
    return full_path


# acciones antes de ejecutar
def preInit():
    """Ejecuta tareas antes de iniciar programa"""
    clearConsole()
    checkIfConfigFilesExists()


# @Decorador
# Ejecutar funcion en bucle segun peticion de confirmacion
def executeOnBucle(func):
    """Ejecuta función en un ciclo preguntando si desea seguir ejecutando"""

    # funcion que pregunta se desea seguir ejecutando
    # controla excepción si es interrumpida por usuario
    def preguntar():
        try:
            rpt = str(input("Desea realizar otra consulta? [ {} ]: "
                            .format(" / ".join(_opts_continuar)))).lower()
            return rpt
        except(KeyboardInterrupt, EOFError, AttributeError):
            printOnConsole("\n[  PROGRAMA FINALIZADO POR EL USUARIO  ]")
            exit()

    # ejecutar ciclo y limpiar cadena inputs
    def wrapper():
        respuesta = "s"
        while respuesta == _opts_continuar[0]:
            func()

            respuesta = preguntar()
            while respuesta not in _opts_continuar:
                respuesta = preguntar()

            _str_inputs.clear()

    return wrapper