"""
Modelo para representar un usuario del sistema.
"""

class Usuario:
    """
    Clase que representa un usuario del sistema.
    Encapsula los datos y la lógica de negocio relacionada con los usuarios.
    """
    
    def __init__(self, id=None, nombre="", usuario="", password=""):
        """
        Inicializa un nuevo usuario.
        
        Args:
            id (int, optional): ID del usuario. Defaults to None.
            nombre (str, optional): Nombre completo del usuario. Defaults to "".
            usuario (str, optional): Nombre de usuario para login. Defaults to "".
            password (str, optional): Contraseña del usuario. Defaults to "".
        """
        self.id = id
        self.nombre = nombre
        self.usuario = usuario
        self.password = password
    
    @classmethod
    def from_dict(cls, data):
        """
        Crea una instancia de Usuario a partir de un diccionario.
        
        Args:
            data (dict): Diccionario con los datos del usuario.
            
        Returns:
            Usuario: Instancia de Usuario.
        """
        return cls(
            id=data.get('ID'),
            nombre=data.get('Nombre', ""),
            usuario=data.get('Usuario', ""),
            password=data.get('password', "")
        )
    
    def to_dict(self):
        """
        Convierte la instancia de Usuario a un diccionario.
        
        Returns:
            dict: Diccionario con los datos del usuario.
        """
        data = {
            'Nombre': self.nombre,
            'Usuario': self.usuario,
            'password': self.password
        }
        
        if self.id is not None:
            data['ID'] = self.id
        
        return data
    
    def validate_password(self, password):
        """
        Valida si la contraseña proporcionada coincide con la del usuario.
        
        Args:
            password (str): Contraseña a validar.
            
        Returns:
            bool: True si la contraseña es correcta, False en caso contrario.
        """
        # En una implementación real, se debería comparar con un hash
        return self.password == password
    
    def change_password(self, new_password):
        """
        Cambia la contraseña del usuario.
        
        Args:
            new_password (str): Nueva contraseña.
            
        Returns:
            bool: True si se cambió la contraseña, False en caso contrario.
        """
        if not new_password:
            return False
        
        # En una implementación real, se debería almacenar un hash
        self.password = new_password
        return True
    
    def __str__(self):
        """
        Representación en string del usuario.
        
        Returns:
            str: Representación en string.
        """
        return f"{self.nombre} ({self.usuario})"
