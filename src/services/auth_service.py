"""
Servicio de autenticación para gestionar usuarios, login y registro.
"""

from typing import Optional, Tuple, Dict
import sqlite3
import bcrypt
from config.constants import ERROR_MESSAGES, SUCCESS_MESSAGES, SQL_QUERIES, DB_TABLES
from config.settings import SECURITY
from utils.security import hash_password, verify_password


class AuthService:
    """
    Servicio para gestionar la autenticación de usuarios.
    Proporciona métodos para verificar credenciales, registrar usuarios y recuperar contraseñas.
    """

    def __init__(self):
        """
        Inicializa el servicio de autenticación.
        """
        self.login_attempts = {}  # Diccionario para controlar intentos de login por usuario

    def _get_connection(self):
        """
        Obtiene una conexión a la base de datos.

        Returns:
            sqlite3.Connection: Conexión a la base de datos.
        """
        return sqlite3.connect("src/inventario.db")

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

        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT ID, Usuario, password, Rol FROM Usuarios WHERE Usuario = ?",
                    (username,)
                )
                result = cursor.fetchone()

                if result and verify_password(password, result[2]):
                    # Reiniciar contador de intentos
                    self.login_attempts[username] = 0
                    return {
                        'success': True,
                        'user': {
                            'id': result[0],
                            'username': result[1],
                            'rol': result[3]
                        }
                    }
                else:
                    # Incrementar contador de intentos
                    self.login_attempts[username] += 1
                    attempts_left = SECURITY['max_login_attempts'] - \
                        self.login_attempts[username]
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
                    INSERT INTO Usuarios (Usuario, password, Nombre, Apellido, Rol)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (username, hashed_password, nombre, apellido, 'user')
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

    def login(self, username: str, password: str) -> Tuple[bool, str]:
        """
        Authenticate a user.

        Args:
            username: The username to authenticate
            password: The password to verify

        Returns:
            Tuple containing:
                - bool: Whether authentication was successful
                - str: Success/error message
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(SQL_QUERIES["get_user"], (username,))
                user = cursor.fetchone()

                if not user:
                    return False, ERROR_MESSAGES["invalid_credentials"]

                stored_password = user[2]  # password is in third column

                if not bcrypt.checkpw(password.encode(), stored_password.encode()):
                    return False, ERROR_MESSAGES["invalid_credentials"]

                return True, SUCCESS_MESSAGES["login_success"]

        except sqlite3.Error as e:
            return False, f"{ERROR_MESSAGES['db_error']}: {str(e)}"

    def register(self, username: str, password: str, rol: str = "user") -> Tuple[bool, str]:
        """
        Register a new user.

        Args:
            username: The username to register
            password: The password to hash and store
            rol: The role to assign to the user (default: "user")

        Returns:
            Tuple containing:
                - bool: Whether registration was successful
                - str: Success/error message
        """
        try:
            # Check if username already exists
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(SQL_QUERIES["get_user"], (username,))
                if cursor.fetchone():
                    return False, ERROR_MESSAGES["user_exists"]

            # Hash password
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

            # Insert new user
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    SQL_QUERIES["create_user"], (username, hashed.decode(), rol))
                conn.commit()

            return True, SUCCESS_MESSAGES["register_success"]

        except sqlite3.Error as e:
            return False, f"{ERROR_MESSAGES['db_error']}: {str(e)}"

    def change_password(self, username: str, old_password: str, new_password: str) -> Tuple[bool, str]:
        """
        Change a user's password.

        Args:
            username: The username whose password to change
            old_password: The current password
            new_password: The new password to set

        Returns:
            Tuple containing:
                - bool: Whether password change was successful
                - str: Success/error message
        """
        try:
            # Verify current credentials
            success, message = self.login(username, old_password)
            if not success:
                return False, message

            # Hash new password
            hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())

            # Update password
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    SQL_QUERIES["update_password"], (hashed.decode(), username))
                conn.commit()

            return True, SUCCESS_MESSAGES["password_changed"]

        except sqlite3.Error as e:
            return False, f"{ERROR_MESSAGES['db_error']}: {str(e)}"

    def __del__(self):
        """Close database connection when object is destroyed."""
        self.conn.close()
