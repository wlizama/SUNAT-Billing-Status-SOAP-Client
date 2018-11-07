import json
from DAO import Empresa, ClaveSol, TipoDocumento
import os

LINE_SEPARADOR = "-"

def lineSeparator(len):
    return LINE_SEPARADOR * len


def getListaEmpresas():
    lista_empresas = []

    data = json.loads(open("config/empresas.json").read())
    for empresa in data["empresas"]:
        emp = Empresa(
            empresa["razon_social"],
            empresa["ruc"],
            ClaveSol(
                empresa["clave_sol"]["usuario"],
                empresa["clave_sol"]["contrasenha"]
            )
        )

        lista_empresas.append(emp)
    
    return lista_empresas


def getListaTiposDocs():
    lista_tipos_docs = []

    data = json.loads(open("config/tipos_docs.json").read())
    for tipo_doc in data["tipos_docs"]:
        tdoc = TipoDocumento(
            tipo_doc["codigo"],
            tipo_doc["descripcion"]
        )

        lista_tipos_docs.append(tdoc)
    
    return lista_tipos_docs


def getEmpresaSeleccionada():
    print("""\
    \nLISTA DE EMPRESAS\
    \n{0}\
    \n # | RUC         | Empresa\
    \n{0}\
    """.format(lineSeparator(50)))

    empresas = getListaEmpresas()
    for empresa in empresas:
        print(" {} | {} | {}".format(
            empresas.index(empresa) + 1,
            empresa.ruc,
            empresa.razon_social))

    indx_empresa_seleccionada = int(input("Empresa: ")) - 1

    return empresas[indx_empresa_seleccionada]


def getTipoDocSeleccionado():
    print("""\
    \nLISTA TIPOS DE DOCUMENTOS\
    \n{0}\
    \n # |  Cod  | Descripción\
    \n{0}\
    """.format(lineSeparator(80)))

    tipos_docs = getListaTiposDocs()
    for tipo_doc in tipos_docs:
        print(" {} |  {}   | {}".format(
            tipos_docs.index(tipo_doc) + 1,
            tipo_doc.codigo,
            tipo_doc.descripcion))

    indx_tipos_doc_seleccionado = int(input("Tipo documento: ")) - 1

    return tipos_docs[indx_tipos_doc_seleccionado]


def main():
    empresa_seleccionada = getEmpresaSeleccionada()
    
    os.system('cls')  # windows OS
    
    print("Empresa: {0}".format(empresa_seleccionada))

    tipo_doc_seleccionado = getTipoDocSeleccionado()

    os.system('cls')  # windows OS

    print("Empresa: {0}".format(empresa_seleccionada))
    print("Tipo Documento: {0}".format(tipo_doc_seleccionado))

    serie = input("Serie: ")

    os.system('cls')  # windows OS

    print("Empresa: {0}".format(empresa_seleccionada))
    print("Tipo Documento: {0}".format(tipo_doc_seleccionado))
    print("Serie: {0}".format(serie))

    numero = int(input("Número: "))

    os.system('cls')  # windows OS

    print("Empresa: {0}".format(empresa_seleccionada))
    print("Tipo Documento: {0}".format(tipo_doc_seleccionado))
    print("Serie: {0}".format(serie))
    print("Número: {0}".format(numero))


    # print(empresa_seleccionada.clave_sol.usuario)
    # print(empresa_seleccionada.clave_sol.contrasenha)

if __name__ == '__main__':
    main()