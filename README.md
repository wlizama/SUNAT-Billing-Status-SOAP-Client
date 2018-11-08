# SUNAT Billing Status SOAP Client

Cliente para consultar estado de documentos electrónicos declarados a [SUNAT](http://www.sunat.gob.pe/)


## Modo de uso
Se debe crear el archivo ``empresas.json`` de acuerdo a la estructura de ``empresas.sample.json`` dentro de la carpeta ``config/``, este archivo es importante porque es de alli de donde se sacan los datos para la consulta SOAP, esto le permite tener una lista de empresas emisoras y poder consultar en cualquiera de ellas.


El archivo ``tipo_docs.json`` dentro de la carpeta ``config/`` contiene la lista de tipos de documentos a consultar según el [Catálogo No. 01](http://www.sunat.gob.pe/legislacion/superin/2017/anexoVII-117-2017.pdf) - Códigos Tipos de documentos