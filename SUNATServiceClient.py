import zeep
from zeep.wsse.username import UsernameToken


class SUNATServiceClient():
    _SUNAT_SOAP_WSDL = "https://www.sunat.gob.pe/ol-it-wsconscpegem/billConsultService?wsdl"
    client = None

    def __init__(self, empresa, tipo_doc, serie, numero):
        self._empresa = empresa
        self._tipo_doc = tipo_doc
        self._serie = serie
        self._numero = numero

    @property
    def empresa(self):
        return self._empresa
    
    @empresa.setter
    def empresa(self, value):
        self._empresa = value
    
    @property
    def tipo_doc(self):
        return self._tipo_doc
    
    @tipo_doc.setter
    def tipo_doc(self, value):
        self._tipo_doc = value

    @property
    def serie(self):
        return self._serie
    
    @serie.setter
    def serie(self, value):
        self._serie = value

    @property
    def numero(self):
        return self._numero
    
    @numero.setter
    def numero(self, value):
        self._numero = value

    def connect(self):
        token_user = "{}{}".format(self.empresa.ruc, self.empresa.clave_sol.usuario)
        token_password = self.empresa.clave_sol.contrasenha

        self.client = zeep.Client(
            self._SUNAT_SOAP_WSDL,
            wsse=UsernameToken(token_user, token_password)
        )

    def getStatus(self):
        self.connect()
        
        response = self.client.service.getStatus(
            self.empresa.ruc,
            self.tipo_doc.codigo,
            self.serie,
            self.numero
        )

        self._printResponse(response)

    def _printResponse(self, response):
        print("""\
        \nRespuesta:\
        \n  Status Code: {0}\
        \n  Status Message: {1}
        """.format(response.statusCode, response.statusMessage))