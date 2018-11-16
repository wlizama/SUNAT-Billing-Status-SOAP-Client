import json
import os
import platform
import re
from terminaltables import SingleTable
from colorama import init
from termcolor import colored


init()


_CONFIG_FILES = {
    "empresas": "./config/empresas.json",
    "tipos_docs": "./config/tipos_docs.json",
    "paths": "./config/paths.json"
}

_LINE_SEPARADOR = "-"

_str_inputs = []


def lineSeparator(len):
    return _LINE_SEPARADOR * len


def printInputValues(func):
    def wrapper(*args, **kwargs):
        value = func(*args, **kwargs)
        clearConsole()
        str = "{}{}".format(args[0], value)
        _str_inputs.append(str)
        print("\n".join(_str_inputs))
        return value

    return wrapper


def checkIfConfigFilesExists():
    for ind, val in _CONFIG_FILES.items():
        if not os.path.exists(val):
            print("ERROR. No se ha podido encontrar el archivo {}"
                  .format(val))
            exit()


def getConfigData(str_key):
    data = []
    try:
        data = json.loads(open(_CONFIG_FILES[str_key]).read())    
    except:
        print("Sucedió un error obteniendo data de archivos.")
        exit()
    
    return data


def fullMatchRExp(regex, str):
    return re.fullmatch(regex, str)


def clearConsole():
    clear_command = "clear"
    if platform.system().lower() == "windows":
        clear_command = "cls"
    
    os.system(clear_command)


def printSingleTable(data, title, heading_row=True):
    try:
        table = SingleTable(data)
        table.title = title
        table.inner_heading_row_border = heading_row
        print(table.table)
    except:
        print("Sucedió un error imprimiendo datos en tabla.")
        exit()


def printOnConsole(str, type=""):
    color = "white"
    if type.lower() == "w":
        color = "yellow"
    elif type.lower() == "i":
        color = "blue"
    elif type.lower() == "e":
        color = "red"

    print(colored(str, color))


def saveBinaryFile(bin_source, path, name):
    full_path = ""
    try:
        full_path = os.path.join(path, name)

        with open(full_path, "wb") as file:
            file.write(bin_source)
    except:
        print("Sucedió un error al crear el archivo CDR")
        exit()
    
    return full_path


def preInit():
    clearConsole()
    checkIfConfigFilesExists()