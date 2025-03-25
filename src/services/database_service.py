import sqlite3
from contextlib import contextmanager
from src.config.constants import ERROR_MESSAGES

class DatabaseService:
    """
    Servicio para gestionar las conexiones y operaciones con la base de datos.
    Proporciona métodos para conectar, ejecutar consultas y gestionar transacciones.
    """
    def __init__(self, db_path):
        """
        Inicializa el servicio de base de datos.
        
        Args:
            db_path (str): Ruta al archivo de la base de datos.
        """
        self.db_path = db_path
        self.connection = None
        
    def connect(self):
        """
        Establece una conexión con la base de datos.
        
        Returns:
            sqlite3.Connection: Objeto de conexión a la base de datos o None si hay error.
        """
        try:
            self.connection = sqlite3.connect(self.db_path)
            # Configurar para que retorne filas como diccionarios
            self.connection.row_factory = sqlite3.Row
            return self.connection
        except sqlite3.Error as e:
            print(ERROR_MESSAGES['db_connection'].format(e))
            return None
    
    def close(self):
        """Cierra la conexión a la base de datos si está abierta."""
        if self.connection:
            try:
                self.connection.close()
                self.connection = None
            except sqlite3.Error as e:
                print(ERROR_MESSAGES['db_connection'].format(e))
    
    def get_cursor(self):
        """
        Obtiene un cursor para ejecutar consultas.
        
        Returns:
            sqlite3.Cursor: Cursor para ejecutar consultas o None si no hay conexión.
        """
        if not self.connection:
            self.connect()
        if self.connection:
            return self.connection.cursor()
        return None
    
    @contextmanager
    def transaction(self):
        """
        Contexto para ejecutar operaciones dentro de una transacción.
        Realiza commit automáticamente si no hay errores y rollback si los hay.
        
        Yields:
            sqlite3.Cursor: Cursor para ejecutar consultas dentro de la transacción.
        """
        cursor = self.get_cursor()
        if not cursor:
            raise Exception("No se pudo obtener un cursor para la transacción")
        
        try:
            yield cursor
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise e
    
    def execute_query(self, query, params=None):
        """
        Ejecuta una consulta SQL y hace commit de los cambios.
        
        Args:
            query (str): Consulta SQL a ejecutar.
            params (tuple, optional): Parámetros para la consulta. Defaults to None.
            
        Returns:
            bool: True si la consulta se ejecutó correctamente, False en caso contrario.
        """
        try:
            with self.transaction() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
            return True
        except sqlite3.Error as e:
            print(ERROR_MESSAGES['query_execution'].format(e))
            return False
    
    def fetch_one(self, query, params=None):
        """
        Ejecuta una consulta y devuelve la primera fila del resultado.
        
        Args:
            query (str): Consulta SQL a ejecutar.
            params (tuple, optional): Parámetros para la consulta. Defaults to None.
            
        Returns:
            dict: Primera fila del resultado como diccionario o None si no hay resultados.
        """
        cursor = self.get_cursor()
        if not cursor:
            return None
        
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchone()
            return dict(result) if result else None
        except sqlite3.Error as e:
            print(ERROR_MESSAGES['query_execution'].format(e))
            return None
    
    def fetch_all(self, query, params=None):
        """
        Ejecuta una consulta y devuelve todas las filas del resultado.
        
        Args:
            query (str): Consulta SQL a ejecutar.
            params (tuple, optional): Parámetros para la consulta. Defaults to None.
            
        Returns:
            list: Lista de filas como diccionarios o lista vacía si no hay resultados.
        """
        cursor = self.get_cursor()
        if not cursor:
            return []
        
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            results = cursor.fetchall()
            return [dict(row) for row in results] if results else []
        except sqlite3.Error as e:
            print(ERROR_MESSAGES['query_execution'].format(e))
            return []
    
    def insert(self, table, data):
        """
        Inserta datos en una tabla.
        
        Args:
            table (str): Nombre de la tabla.
            data (dict): Datos a insertar como diccionario {columna: valor}.
            
        Returns:
            int: ID del registro insertado o None si hay error.
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        try:
            with self.transaction() as cursor:
                cursor.execute(query, tuple(data.values()))
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(ERROR_MESSAGES['query_execution'].format(e))
            return None
    
    def update(self, table, data, condition, condition_params):
        """
        Actualiza datos en una tabla.
        
        Args:
            table (str): Nombre de la tabla.
            data (dict): Datos a actualizar como diccionario {columna: valor}.
            condition (str): Condición WHERE para la actualización.
            condition_params (tuple): Parámetros para la condición.
            
        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        set_clause = ', '.join([f"{column} = ?" for column in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {condition}"
        params = tuple(data.values()) + condition_params
        
        return self.execute_query(query, params)
    
    def delete(self, table, condition, condition_params):
        """
        Elimina registros de una tabla.
        
        Args:
            table (str): Nombre de la tabla.
            condition (str): Condición WHERE para la eliminación.
            condition_params (tuple): Parámetros para la condición.
            
        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario.
        """
        query = f"DELETE FROM {table} WHERE {condition}"
        return self.execute_query(query, condition_params)
