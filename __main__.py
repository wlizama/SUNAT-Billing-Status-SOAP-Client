from DAO import Empresa, ClaveSol, TipoDocumento
from SUNATServiceClient import SUNATServiceClient
from helpers import (preInit,
                     printInputValues,
                     getConfigData,
                     checkIfConfigFilesExists,
                     fullMatchRExp,
                     printSingleTable,
                     printOnConsole,
                     saveBinaryFile,
                     executeOnBucle)
import argparse

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
        printOnConsole("No existen empresas configuradas.", "e")
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
        printOnConsole("No existen Tipos de documentos configurados.", "e")
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
                    printOnConsole("El valor debe ser mayor a Cero ( 0 ).", "w")
            else:
                empresa_seleccionada = empresas[0]
                is_error = False
        except ValueError as verr:
            printOnConsole("El valor ingresado no es númerico.", "w")
        except IndexError as ierr:
            printOnConsole("Debe seleccionar una de las empresas en la lista.", "w")

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
                    printOnConsole("El valor debe ser mayor a Cero ( 0 ).", "w")
            else:
                tipo_doc_seleccionado = tipos_docs[0]
                is_error = False
        except ValueError as verr:
            printOnConsole("El valor ingresado no es númerico.", "w")
        except IndexError as ierr:
            printOnConsole("Debe seleccionar uno de los documentos en la lista.", "w")

    return tipo_doc_seleccionado


@printInputValues
def getInputSerieDoc(str_msg):
    
    is_error = True
    while is_error:
        is_error = True
        str_input = input(str_msg)
        match = fullMatchRExp(r"[a-zA-Z]\d{3}", str_input)

        if match == None:
            printOnConsole("La serie no es correcta", "w")
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
                printOnConsole("El valor debe ser mayor a Cero ( 0 ).", "w")
            else:
                is_error = False
        except ValueError as verr:
            printOnConsole("El valor ingresado no es númerico.", "w")

    return num


def getStatus(service):
    rpt = service.getStatus()
    data = [
        ["Code", rpt.statusCode],
        ["Message", rpt.statusMessage]
    ]
    printSingleTable(data, " Respuesta Status: ", False)


def getStatusCDR(service):

    cdr_name_file = "R-{}-{}-{}-{:08d}.zip".format(
        service.empresa.ruc,
        service.tipo_doc.codigo,
        service.serie,
        service.numero,
    )

    rpt = service.getStatusCdr()
    paths = getConfigData("paths")["paths"]
    full_path = ""

    if rpt.content:
        full_path = saveBinaryFile(
            rpt.content, paths["destino_CDR_file"],
            cdr_name_file)

    data = [
        ["Code", rpt.statusCode],
        ["Message", rpt.statusMessage],
    ]

    if rpt.content:
        data.append(["Ubicación", full_path])

    printSingleTable(data, " Respuesta CDR: ", False)


@executeOnBucle
def main():

    preInit()

    parser = argparse.ArgumentParser(
        description="Consulta status de documento en SUNAT y obtiene archivo CDR")
    parser.add_argument(
        '--status',
        "-s",
        action='store_true',
        help="Solo consultar estado de documento")
    parser.add_argument(
        '--cdr',
        "-c",
        action='store_true',
        help="Solo consultar archivo CDR y almacenarlo según configuración")
    args = parser.parse_args()

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

    if not args.status and not args.cdr:
        getStatus(service)
        getStatusCDR(service)
    else:
        if args.status:
            getStatus(service)
        
        if args.cdr:
            getStatusCDR(service)


if __name__ == '__main__':

    try:
        main()
    except(KeyboardInterrupt, EOFError, AttributeError):
        printOnConsole("\n[  PROGRAMA FINALIZADO POR EL USUARIO  ]")