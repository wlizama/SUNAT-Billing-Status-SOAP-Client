import json
import os
from DAO import Empresa, ClaveSol, TipoDocumento
from SUNATServiceClient import SUNATServiceClient

LINE_SEPARADOR = "-"

str_inputs = []


def lineSeparator(len):
    return LINE_SEPARADOR * len


def printInputValues(func):
    def wrapper(*args, **kwargs):
        value = func(*args, **kwargs)
        os.system('cls')
        str = "{}{}".format(args[0], value)
        str_inputs.append(str)
        print("\n".join(str_inputs))
        return value

    return wrapper


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


@printInputValues
def getInputEmpresa(str_msg):
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

    indx_empresa_seleccionada = int(input(str_msg)) - 1

    return empresas[indx_empresa_seleccionada]


@printInputValues
def getInputTipoDoc(str_msg):
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

    indx_tipos_doc_seleccionado = int(input(str_msg)) - 1

    return tipos_docs[indx_tipos_doc_seleccionado]


@printInputValues
def getInputSerieDoc(str_msg):
    return input(str_msg)


@printInputValues
def getInputNumeroDoc(str_msg):
    return int(input(str_msg))


def main():
    # os.system('cls')

    empresa = getInputEmpresa("Empresa: ")
    tipo_doc = getInputTipoDoc("Tipo de Documento: ")
    serie = getInputSerieDoc("Serie: ").upper()
    numero = getInputNumeroDoc("Número: ")

    service = SUNATServiceClient(
        empresa,
        tipo_doc,
        serie,
        numero
    )
    
    service.getStatus()


if __name__ == '__main__':
    main()