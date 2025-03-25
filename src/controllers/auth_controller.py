"""
Controlador para gestionar la autenticación de usuarios.
"""

from src.models.usuario import Usuario
from src.config.constants import ERROR_MESSAGES

class AuthController:
    """
    Controlador para gestionar la autenticación de usuarios.
    Coordina las operaciones entre la vista de autenticación y los servicios/modelos.
    """
    
    def __init__(self, auth_service):
        """
        Inicializa el controlador de autenticación.
        
        Args:
            auth_service (AuthService): Servicio de autenticación.
        """
        self.auth_service = auth_service
        self.current_user = None
    
    def login(self, username, password):
        """
        Realiza el proceso de login.
        
        Args:
            username (str): Nombre de usuario.
            password (str): Contraseña.
            
        Returns:
            dict: Resultado del proceso de login.
        """
        # Validar datos de entrada
        if not username or not password:
            return {'error': ERROR_MESSAGES['empty_fields']}
        
        # Verificar credenciales
        result = self.auth_service.verify_credentials(username, password)
        
        # Si el login es exitoso, guardar el usuario actual
        if 'success' in result and result['success']:
            user_data = result['user']
            self.current_user = Usuario.from_dict(user_data)
            return {'success': True, 'user': self.current_user}
        
        return result
    
    def logout(self):
        """
        Realiza el proceso de logout.
        
        Returns:
            bool: True si el logout fue exitoso, False en caso contrario.
        """
        self.current_user = None
        return True
    
    def register(self, user_data):
        """
        Registra un nuevo usuario.
        
        Args:
            user_data (dict): Datos del usuario a registrar.
            
        Returns:
            dict: Resultado del proceso de registro.
        """
        # Validar datos de entrada
        if not user_data.get('Nombre') or not user_data.get('Usuario') or not user_data.get('password'):
            return {'error': ERROR_MESSAGES['empty_fields']}
        
        # Verificar que las contraseñas coincidan
        if user_data.get('password') != user_data.get('confirm_password'):
            return {'error': 'Las contraseñas no coinciden'}
        
        # Eliminar campo de confirmación de contraseña
        if 'confirm_password' in user_data:
            del user_data['confirm_password']
        
        # Registrar usuario
        return self.auth_service.register_user(user_data)
    
    def update_password(self, username, new_password, confirm_password):
        """
        Actualiza la contraseña de un usuario.
        
        Args:
            username (str): Nombre de usuario.
            new_password (str): Nueva contraseña.
            confirm_password (str): Confirmación de la nueva contraseña.
            
        Returns:
            dict: Resultado del proceso de actualización.
        """
        # Validar datos de entrada
        if not username or not new_password or not confirm_password:
            return {'error': ERROR_MESSAGES['empty_fields']}
        
        # Verificar que las contraseñas coincidan
        if new_password != confirm_password:
            return {'error': 'Las contraseñas no coinciden'}
        
        # Actualizar contraseña
        return self.auth_service.update_password(username, new_password)
    
    def verify_admin(self, username, password):
        """
        Verifica si las credenciales corresponden a un administrador.
        
        Args:
            username (str): Nombre de usuario.
            password (str): Contraseña.
            
        Returns:
            bool: True si las credenciales son de administrador, False en caso contrario.
        """
        # Validar datos de entrada
        if not username or not password:
            return False
        
        return self.auth_service.verify_admin(username, password)
    
    def get_current_user(self):
        """
        Obtiene el usuario actual.
        
        Returns:
            Usuario: Usuario actual o None si no hay usuario autenticado.
        """
        return self.current_user
