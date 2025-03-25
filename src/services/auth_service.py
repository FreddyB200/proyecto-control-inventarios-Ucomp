"""
Servicio de autenticación para gestionar usuarios, login y registro.
"""

from typing import Optional
import sqlite3
from src.config.constants import ERROR_MESSAGES, SUCCESS_MESSAGES, SQL_QUERIES, DB_TABLES
from src.config.settings import SECURITY
from utils.security import hash_password, verify_password

class AuthService:
    """
    Servicio para gestionar la autenticación de usuarios.
    Proporciona métodos para verificar credenciales, registrar usuarios y recuperar contraseñas.
    """
    
    def __init__(self, db_path: str):
        """
        Inicializa el servicio de autenticación.
        
        Args:
            db_path (str): Ruta a la base de datos.
        """
        self.db_path = db_path
        self.login_attempts = {}  # Diccionario para controlar intentos de login por usuario
    
    def _get_connection(self):
        """
        Obtiene una conexión a la base de datos.
        
        Returns:
            sqlite3.Connection: Conexión a la base de datos.
        """
        return sqlite3.connect(self.db_path)
    
    def _hash_password(self, password):
        """
        Genera un hash seguro para la contraseña.
        
        Args:
            password (str): Contraseña en texto plano.
            
        Returns:
            str: Hash de la contraseña.
        """
        # En una implementación real, se debería usar un salt único por usuario
        # y un algoritmo más seguro como bcrypt
        return hash_password(password)
    
    def verify_credentials(self, username, password):
        """
        Verifica las credenciales de un usuario.
        
        Args:
            username (str): Nombre de usuario.
            password (str): Contraseña.
            
        Returns:
            dict: Información del usuario si las credenciales son correctas, None en caso contrario.
        """
        # Verificar si el usuario ha excedido el número máximo de intentos
        if username in self.login_attempts and self.login_attempts[username] >= SECURITY['max_login_attempts']:
            return {'error': ERROR_MESSAGES['login_blocked']}
        
        # Incrementar contador de intentos
        if username not in self.login_attempts:
            self.login_attempts[username] = 0
        
        # En una implementación real, se debería verificar el hash de la contraseña
        # password_hash = self._hash_password(password)
        
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT password FROM Usuarios WHERE Usuario = ?",
                    (username,)
                )
                result = cursor.fetchone()
                
                if result and verify_password(password, result[0]):
                    # Reiniciar contador de intentos
                    self.login_attempts[username] = 0
                    return {'success': True, 'user': username}
                else:
                    # Incrementar contador de intentos
                    self.login_attempts[username] += 1
                    attempts_left = SECURITY['max_login_attempts'] - self.login_attempts[username]
                    return {'error': ERROR_MESSAGES['login_failed'].format(attempts_left)}
        except sqlite3.Error as e:
            raise Exception(f"Error en la base de datos: {str(e)}")
    
    def verify_admin(self, username, password):
        """
        Verifica si las credenciales corresponden a un administrador.
        
        Args:
            username (str): Nombre de usuario.
            password (str): Contraseña.
            
        Returns:
            bool: True si las credenciales son de administrador, False en caso contrario.
        """
        return (username == SECURITY['admin_credentials']['username'] and 
                password == SECURITY['admin_credentials']['password'])
    
    def register_user(self, username: str, password: str, nombre: str, apellido: str) -> bool:
        """
        Registra un nuevo usuario en la base de datos.
        
        Args:
            username: The username for the new user
            password: The password for the new user
            nombre: The user's first name
            apellido: The user's last name
            
        Returns:
            bool: True if registration successful, False otherwise
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Check if username already exists
                cursor.execute(
                    "SELECT Usuario FROM Usuarios WHERE Usuario = ?",
                    (username,)
                )
                if cursor.fetchone():
                    raise Exception("El usuario ya existe")
                    
                # Hash password and insert new user
                hashed_password = hash_password(password)
                cursor.execute(
                    """
                    INSERT INTO Usuarios (Usuario, password, Nombre, Apellido)
                    VALUES (?, ?, ?, ?)
                    """,
                    (username, hashed_password, nombre, apellido)
                )
                conn.commit()
                return True
        except sqlite3.Error as e:
            raise Exception(f"Error en la base de datos: {str(e)}")
    
    def update_password(self, username, new_password):
        """
        Actualiza la contraseña de un usuario.
        
        Args:
            username (str): Nombre de usuario.
            new_password (str): Nueva contraseña.
            
        Returns:
            dict: Resultado de la operación.
        """
        # En una implementación real, se debería almacenar el hash de la contraseña
        # password_hash = self._hash_password(new_password)
        
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Check if user exists
                cursor.execute(
                    "SELECT Usuario FROM Usuarios WHERE Usuario = ?",
                    (username,)
                )
                if not cursor.fetchone():
                    raise Exception("Usuario no encontrado")
                    
                # Update password
                hashed_password = hash_password(new_password)
                cursor.execute(
                    "UPDATE Usuarios SET password = ? WHERE Usuario = ?",
                    (hashed_password, username)
                )
                conn.commit()
                return {'success': True, 'message': SUCCESS_MESSAGES['password_updated']}
        except sqlite3.Error as e:
            raise Exception(f"Error en la base de datos: {str(e)}")
    
    def reset_login_attempts(self, username):
        """
        Reinicia el contador de intentos de login para un usuario.
        
        Args:
            username (str): Nombre de usuario.
        """
        if username in self.login_attempts:
            self.login_attempts[username] = 0

    def reset_password(self, username: str, new_password: str) -> bool:
        """
        Reset a user's password.
        
        Args:
            username: The username whose password to reset
            new_password: The new password to set
            
        Returns:
            bool: True if password reset successful, False otherwise
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Check if user exists
                cursor.execute(
                    "SELECT Usuario FROM Usuarios WHERE Usuario = ?",
                    (username,)
                )
                if not cursor.fetchone():
                    raise Exception("Usuario no encontrado")
                    
                # Update password
                hashed_password = hash_password(new_password)
                cursor.execute(
                    "UPDATE Usuarios SET password = ? WHERE Usuario = ?",
                    (hashed_password, username)
                )
                conn.commit()
                return True
        except sqlite3.Error as e:
            raise Exception(f"Error en la base de datos: {str(e)}")
