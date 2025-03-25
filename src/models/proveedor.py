"""
Modelo para representar un proveedor en el sistema.
"""

class Proveedor:
    """
    Clase que representa un proveedor en el sistema.
    Encapsula los datos y la lógica de negocio relacionada con los proveedores.
    """
    
    def __init__(self, nit=None, razon_social="", direccion="", telefono="", email=""):
        """
        Inicializa un nuevo proveedor.
        
        Args:
            nit (str, optional): NIT del proveedor. Defaults to None.
            razon_social (str, optional): Razón social del proveedor. Defaults to "".
            direccion (str, optional): Dirección del proveedor. Defaults to "".
            telefono (str, optional): Teléfono del proveedor. Defaults to "".
            email (str, optional): Email del proveedor. Defaults to "".
        """
        self.nit = nit
        self.razon_social = razon_social
        self.direccion = direccion
        self.telefono = telefono
        self.email = email
    
    @classmethod
    def from_dict(cls, data):
        """
        Crea una instancia de Proveedor a partir de un diccionario.
        
        Args:
            data (dict): Diccionario con los datos del proveedor.
            
        Returns:
            Proveedor: Instancia de Proveedor.
        """
        return cls(
            nit=data.get('NIT'),
            razon_social=data.get('razon_social', ""),
            direccion=data.get('direccion', ""),
            telefono=data.get('telefono', ""),
            email=data.get('email', "")
        )
    
    def to_dict(self):
        """
        Convierte la instancia de Proveedor a un diccionario.
        
        Returns:
            dict: Diccionario con los datos del proveedor.
        """
        data = {
            'razon_social': self.razon_social
        }
        
        if self.nit is not None:
            data['NIT'] = self.nit
        
        if self.direccion:
            data['direccion'] = self.direccion
        
        if self.telefono:
            data['telefono'] = self.telefono
        
        if self.email:
            data['email'] = self.email
        
        return data
    
    def __str__(self):
        """
        Representación en string del proveedor.
        
        Returns:
            str: Representación en string.
        """
        return f"{self.razon_social} (NIT: {self.nit})"
