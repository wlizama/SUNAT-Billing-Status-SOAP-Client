import zeep
from zeep.wsse.username import UsernameToken
from halo import Halo

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
        try:
            token_user = "{}{}".format(self.empresa.ruc, self.empresa.clave_sol.usuario)
            token_password = self.empresa.clave_sol.contrasenha

            self.client = zeep.Client(
                self._SUNAT_SOAP_WSDL,
                wsse=UsernameToken(token_user, token_password)
            )
        except (ConnectionResetError, ConnectionError):
            print("Error al establecer la conección")
            raise

    @Halo(text="Consultando ando ...", spinner="dots")
    def getStatus(self):
        self.connect()
        
        response = None
        try:
            response = self.client.service.getStatus(
                self.empresa.ruc,
                self.tipo_doc.codigo,
                self.serie,
                self.numero
            )
        except (ConnectionResetError, ConnectionError):
            print("Sucedió un error en método getStatus")
            raise
        
        return response