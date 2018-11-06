import json
from DAO import Empresa, ClaveSol

def getListaEmpresas():
    lista_empresas = []

    data = json.loads(open("empresas.json").read())
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


def getEmpresaSeleccionada():
    line_separador = "-" * 50

    print("""\
    \nSELECCIONE LA EMPRESA\
    \n{0}\
    \n # | Empresa\
    \n{0}\
    """.format(line_separador))

    empresas = getListaEmpresas()
    for empresa in empresas:
        print(" {} | {}".format(empresas.index(empresa) + 1, empresa))

    indx_empresa_seleccionada = int(input("Ingrese el número: ")) - 1

    return empresas[indx_empresa_seleccionada]


def main():
    empresa_seleccionada = getEmpresaSeleccionada()

    print(empresa_seleccionada.clave_sol.usuario)
    print(empresa_seleccionada.clave_sol.contrasenha)

if __name__ == '__main__':
    main()