from DAO import Empresa, ClaveSol, TipoDocumento
from SUNATServiceClient import SUNATServiceClient
from helpers import (clearConsole,
                     lineSeparator,
                     printInputValues,
                     getConfigData,
                     checkIfConfigFilesExists,
                     fullMatchRExp,
                     printSingleTable)


def getListaEmpresas():

    lista_empresas = []
    data = getConfigData("empresas")
    
    if len(data["empresas"]) > 0:
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
    else:
        print("‼ No existen empresas configuradas.")
        exit()

    return lista_empresas


def getListaTiposDocs():

    lista_tipos_docs = []
    data = getConfigData("tipos_docs")

    if len(data["tipos_docs"]) > 0:
        for tipo_doc in data["tipos_docs"]:
            tdoc = TipoDocumento(
                tipo_doc["codigo"],
                tipo_doc["descripcion"]
            )

            lista_tipos_docs.append(tdoc)
    else:
        print("‼ No existen Tipos de documentos configurados.")
        exit()

    return lista_tipos_docs


@printInputValues
def getInputEmpresa(str_msg):

    is_error = True
    empresa_seleccionada = None
    empresas = getListaEmpresas()

    if len(empresas) > 1:
        data_table = []
        data_table.append(["#", "RUC", "Razón Social"])
        for empresa in empresas:
            data_table.append([
                empresas.index(empresa) + 1,
                empresa.ruc,
                empresa.razon_social
            ])
        printSingleTable(data_table, " LISTA DE EMPRESAS ")

    while is_error:
        is_error = True
        try:
            if len(empresas) > 1:
                indx_empresa_seleccionada = int(input(str_msg))
                if indx_empresa_seleccionada > 0:
                    empresa_seleccionada = empresas[indx_empresa_seleccionada - 1]
                    is_error = False
                else:
                    print("‼ El valor debe ser mayor a Cero ( 0 ).")
            else:
                empresa_seleccionada = empresas[0]
                is_error = False
        except ValueError as verr:
            print("‼ El valor ingresado no es númerico.")
        except IndexError as ierr:
            print("‼ Debe seleccionar una de las empresas en la lista.")

    return empresa_seleccionada

@printInputValues
def getInputTipoDoc(str_msg):

    is_error = True
    tipo_doc_seleccionado = None
    tipos_docs = getListaTiposDocs()

    if len(tipos_docs) > 1:
        data_table = []
        data_table.append(["#", "Cod", "Descripción"])
        for tipo_doc in tipos_docs:
            data_table.append([
                tipos_docs.index(tipo_doc) + 1,
                tipo_doc.codigo,
                tipo_doc.descripcion
            ])
        printSingleTable(data_table, " LISTA TIPOS DE DOCUMENTOS ")

    while is_error:
        is_error = True
        try:
            if len(tipos_docs) > 1:
                indx_tipo_doc_seleccionado = int(input(str_msg))
                if indx_tipo_doc_seleccionado > 0:
                    tipo_doc_seleccionado = tipos_docs[indx_tipo_doc_seleccionado - 1]
                    is_error = False
                else:
                    print("‼ El valor debe ser mayor a Cero ( 0 ).")
            else:
                tipo_doc_seleccionado = tipos_docs[0]
                is_error = False
        except ValueError as verr:
            print("‼ El valor ingresado no es númerico.")
        except IndexError as ierr:
            print("‼ Debe seleccionar uno de los documentos en la lista.")

    return tipo_doc_seleccionado


@printInputValues
def getInputSerieDoc(str_msg):
    
    is_error = True
    while is_error:
        is_error = True
        str_input = input(str_msg)
        match = fullMatchRExp(r"[a-zA-Z]\d{3}", str_input)

        if match == None:
            print("‼ La serie no es correcta")
        else:
            is_error = False
    
    return str_input.upper()


@printInputValues
def getInputNumeroDoc(str_msg):
    is_error = True
    num = 0
    while is_error:
        is_error = True
        try:
            num = int(input(str_msg))
            if num <= 0:
                print("‼ El valor debe ser mayor a Cero ( 0 ).")
            else:
                is_error = False
        except ValueError as verr:
            print("‼ El valor ingresado no es númerico.")

    return num


def printStatusResponse(data_rpt):
    data = [
        ["Status Code", data_rpt.statusCode],
        ["Status Message", data_rpt.statusMessage]
    ]
    printSingleTable(data, " Respuesta: ", False)


def main():

    try:
        clearConsole()
        checkIfConfigFilesExists()

        empresa = getInputEmpresa("Empresa: ")
        tipo_doc = getInputTipoDoc("Tipo de Documento: ")
        serie = getInputSerieDoc("Serie: ")
        numero = getInputNumeroDoc("Número: ")

        service = SUNATServiceClient(
            empresa,
            tipo_doc,
            serie,
            numero
        )
        
        rpt = service.getStatus()
        printStatusResponse(rpt)
    except(KeyboardInterrupt, EOFError):
        print("\n[  PROGRAMA FINALIZADO POR EL USUARIO  ]")


if __name__ == '__main__':
    main()