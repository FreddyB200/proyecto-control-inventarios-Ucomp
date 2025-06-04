"""
Servicio para gestionar las conexiones a la base de datos.
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Any, Optional
from config.settings import DATABASE


class DatabaseService:
    """
    Servicio para gestionar las conexiones y operaciones de la base de datos.
    """

    def __init__(self):
        """Inicializa el servicio de base de datos."""
        self.db_path = DATABASE["path"]
        self.conn = None
        self.cursor = None
        self._connect()

    def _connect(self):
        """Establece la conexión a la base de datos."""
        try:
            self.conn = psycopg2.connect(self.db_path)
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        except psycopg2.Error as e:
            raise Exception(f"Error al conectar a la base de datos: {str(e)}")

    def execute(self, query: str, params: tuple = None) -> Optional[psycopg2.extras.RealDictCursor]:
        """
        Ejecuta una consulta SQL.

        Args:
            query: Consulta SQL a ejecutar
            params: Parámetros para la consulta (opcional)

        Returns:
            Cursor de PostgreSQL o None si hay error
        """
        try:
            if params:
                return self.cursor.execute(query, params)
            return self.cursor.execute(query)
        except psycopg2.Error as e:
            raise Exception(f"Error al ejecutar consulta: {str(e)}")

    def fetch_all(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        """
        Ejecuta una consulta y retorna todos los resultados.

        Args:
            query: Consulta SQL a ejecutar
            params: Parámetros para la consulta (opcional)

        Returns:
            Lista de diccionarios con los resultados
        """
        try:
            cursor = self.execute(query, params)
            return cursor.fetchall()
        except psycopg2.Error as e:
            raise Exception(f"Error al obtener resultados: {str(e)}")

    def fetch_one(self, query: str, params: tuple = None) -> Optional[Dict[str, Any]]:
        """
        Ejecuta una consulta y retorna un resultado.

        Args:
            query: Consulta SQL a ejecutar
            params: Parámetros para la consulta (opcional)

        Returns:
            Diccionario con el resultado o None si no hay resultados
        """
        try:
            cursor = self.execute(query, params)
            return cursor.fetchone()
        except psycopg2.Error as e:
            raise Exception(f"Error al obtener resultado: {str(e)}")

    def insert(self, table: str, data: Dict[str, Any]) -> int:
        """
        Inserta datos en una tabla.

        Args:
            table: Nombre de la tabla
            data: Diccionario con los datos a insertar

        Returns:
            ID del registro insertado
        """
        try:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s' for _ in data])
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders}) RETURNING ID"

            self.execute(query, tuple(data.values()))
            self.conn.commit()

            return self.cursor.fetchone()['ID']
        except psycopg2.Error as e:
            raise Exception(f"Error al insertar datos: {str(e)}")

    def update(self, table: str, data: Dict[str, Any], condition: str, params: tuple) -> int:
        """
        Actualiza registros en una tabla.

        Args:
            table: Nombre de la tabla
            data: Diccionario con los datos a actualizar
            condition: Condición WHERE de la actualización
            params: Parámetros para la condición

        Returns:
            Número de registros actualizados
        """
        try:
            set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
            query = f"UPDATE {table} SET {set_clause} WHERE {condition}"

            self.execute(query, tuple(data.values()) + params)
            self.conn.commit()

            return self.cursor.rowcount
        except psycopg2.Error as e:
            raise Exception(f"Error al actualizar datos: {str(e)}")

    def delete(self, table: str, condition: str, params: tuple) -> int:
        """
        Elimina registros de una tabla.

        Args:
            table: Nombre de la tabla
            condition: Condición WHERE para la eliminación
            params: Parámetros para la condición

        Returns:
            Número de registros eliminados
        """
        try:
            query = f"DELETE FROM {table} WHERE {condition}"

            self.execute(query, params)
            self.conn.commit()

            return self.cursor.rowcount
        except psycopg2.Error as e:
            raise Exception(f"Error al eliminar datos: {str(e)}")

    def begin_transaction(self):
        """Inicia una transacción."""
        self.conn.execute("BEGIN TRANSACTION")

    def commit(self):
        """Confirma una transacción."""
        self.conn.commit()

    def rollback(self):
        """Revierte una transacción."""
        self.conn.rollback()

    def __del__(self):
        """Cierra la conexión cuando se destruye el objeto."""
        if self.conn:
            self.conn.close()
