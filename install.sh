#!/bin/sh

## pyinstaller how to use
# https://pyinstaller.readthedocs.io/en/stable/usage.html


## variables globales
dist_folder="dist"
config_folder="config"
cdr_folder="CDRFiles"


# creador de ejecutable
pyinstaller --distpath $dist_folder -F --clean -n sbsSOAP __main__.py


# crear carpetas necesarias para ejecutable
mkdir $dist_folder/$config_folder

mkdir $dist_folder/$cdr_folder


## copiar archivos de configuración
cp config/* ./$dist_folder/$config_folder


## copiar archivos varios
cp ./LICENSE ./$dist_folder/

cp ./README.md ./$dist_folder/


echo ""
echo "##################################################"
echo "Finalzado, presiona cualquier tecla para cerrar"
echo "##################################################"

read myothervar