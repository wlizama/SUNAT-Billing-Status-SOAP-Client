import json
import os
from DAO import Empresa, ClaveSol, TipoDocumento
from SUNATServiceClient import SUNATServiceClient

LINE_SEPARADOR = "-"

str_inputs = []

# Helpers

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

    is_error = True
    empresa_seleccionada = None
            
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

    while is_error:
        is_error = True
        try:
            indx_empresa_seleccionada = int(input(str_msg))
            if indx_empresa_seleccionada > 0:
                empresa_seleccionada = empresas[indx_empresa_seleccionada - 1]
                is_error = False
            else:
                print("‼ El valor debe ser mayor a Cero ( 0 ).")
        except ValueError as verr:
            print("‼ El valor ingresado no es númerico.")
        except IndexError as ierr:
            print("‼ Debe seleccionar una de las empresas en la lista.")

    return empresa_seleccionada

@printInputValues
def getInputTipoDoc(str_msg):

    is_error = True
    tipo_doc_seleccionado = None

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

    while is_error:
        is_error = True
        try:
            indx_tipo_doc_seleccionado = int(input(str_msg))
            if indx_tipo_doc_seleccionado > 0:
                tipo_doc_seleccionado = tipos_docs[indx_tipo_doc_seleccionado - 1]
                is_error = False
            else:
                print("‼ El valor debe ser mayor a Cero ( 0 ).")
        except ValueError as verr:
            print("‼ El valor ingresado no es númerico.")
        except IndexError as ierr:
            print("‼ Debe seleccionar uno de los documentos en la lista.")

    return tipo_doc_seleccionado


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