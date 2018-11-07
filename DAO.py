class Empresa():
    
    def __init__(self, razon_social, ruc, clave_sol):
        self._razon_social = razon_social
        self._ruc = ruc
        self._clave_sol = clave_sol

    @property
    def razon_social(self):
        return self._razon_social
    
    @razon_social.setter
    def razon_social(self, value):
        self._razon_social = value

    @property
    def ruc(self):
        return self._ruc
    
    @ruc.setter
    def ruc(self, value):
        self._ruc = value

    @property
    def clave_sol(self):
        return self._clave_sol
    
    @clave_sol.setter
    def clave_sol(self, value):
        self._clave_sol = value

    def __str__(self):
        return "{0} {1}".format(self.ruc, self.razon_social)


class ClaveSol():

    def __init__(self, usuario, contrasenha):
        self._usuario = usuario
        self._contrasenha = contrasenha

    @property
    def usuario(self):
        return self._usuario
    
    @usuario.setter
    def usuario(self, value):
        self._usuario = value

    @property
    def contrasenha(self):
        return self._contrasenha
    
    @contrasenha.setter
    def contrasenha(self, value):
        self._contrasenha = value


class TipoDocumento():
    def __init__(self, codigo, descripcion):
        self._codigo = codigo
        self._descripcion = descripcion

    @property
    def codigo(self):
        return self._codigo
    
    @codigo.setter
    def codigo(self, value):
        self._codigo = value

    @property
    def descripcion(self):
        return self._descripcion
    
    @descripcion.setter
    def descripcion(self, value):
        self._descripcion = value

    def __str__(self):
        return "{0} {1}".format(self.codigo, self.descripcion)