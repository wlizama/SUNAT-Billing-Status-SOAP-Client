import json
import os
from DAO import Empresa, ClaveSol, TipoDocumento
import zeep
from zeep.wsse.username import UsernameToken


LINE_SEPARADOR = "-"
SUNAT_SOAT_WSDL = "https://www.sunat.gob.pe/ol-it-wsconscpegem/billConsultService?wsdl"

str_inputs = []


def lineSeparator(len):
    return LINE_SEPARADOR * len


def printValues(func):
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


@printValues
def getEmpresaSeleccionada(str_msg):
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


@printValues
def getTipoDocSeleccionado(str_msg):
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


@printValues
def getSerieDoc(str_msg):
    return input(str_msg)


@printValues
def getNumeroDoc(str_msg):
    return int(input(str_msg))


def main():
    # os.system('cls')

    empresa = getEmpresaSeleccionada("Empresa: ")
    tipo_doc = getTipoDocSeleccionado("Tipo de Documento: ")
    serie = getSerieDoc("Serie: ").upper()
    numero = getNumeroDoc("Número: ")

    token_user = "{}{}".format(empresa.ruc, empresa.clave_sol.usuario)
    token_password = empresa.clave_sol.contrasenha

    client = zeep.Client(
    SUNAT_SOAT_WSDL,
        wsse=UsernameToken(token_user, token_password)
    )

    response = client.service.getStatus(
        empresa.ruc,
        tipo_doc.codigo,
        serie,
        numero
    )

    print(response)


if __name__ == '__main__':
    main()