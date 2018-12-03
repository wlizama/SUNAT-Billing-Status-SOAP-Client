"""Clase para consultas a SOAP a SUNAT
"""

import zeep
from zeep.wsse.username import UsernameToken
from halo import Halo

class SUNATServiceClient():
    # Direccion de servicio SUNAT
    _SUNAT_SOAP_WSDL = "https://www.sunat.gob.pe/ol-it-wsconscpegem/billConsultService?wsdl"
    client = None

    def __init__(self, empresa, tipo_doc, serie, numero):
        """
        Parameters
        ----------
        empresa: DAO.Empresa
            Empresa con la que se realiza la consulta
        tipo_doc: DAO.TipoDocumento
            Tipo de documento a consultar
        serie: str
            serie de documento a consultar. Ejm: F033
        numero: int
            número de documento documento a consultar
        """
        self._empresa = empresa
        self._tipo_doc = tipo_doc
        self._serie = serie
        self._numero = numero

    # setters y getters
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
        """Establecer conección al servicio con las credenciales de acceso.
        Lanza una excepcion en caso de error
        """
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


    @Halo(text="Consultando status ...", spinner="dots3")
    def getStatus(self):
        """Metódo para consultar estado de documento
        Lanza excepción por error en consulta
        """
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


    @Halo(text="Consultando CDR ...", spinner="dots9")
    def getStatusCdr(self):
        """Metódo para consultar CDR de documento
        Lanza excepción por error en consulta
        """
        self.connect()
        
        response = None
        try:
            response = self.client.service.getStatusCdr(
                self.empresa.ruc,
                self.tipo_doc.codigo,
                self.serie,
                self.numero
            )
        except (ConnectionResetError, ConnectionError):
            print("Sucedió un error en método getStatus")
            raise
        
        return response