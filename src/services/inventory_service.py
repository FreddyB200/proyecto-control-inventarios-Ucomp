"""
Servicio para gestionar el inventario de productos.
"""

from datetime import datetime, timedelta
from config.constants import ERROR_MESSAGES, SUCCESS_MESSAGES, SQL_QUERIES, DB_TABLES
from config.settings import ALERTS, DATABASE, STOCK
from typing import List, Dict, Optional
from services.database_service import DatabaseService


class InventoryService:
    """
    Servicio para gestionar operaciones relacionadas con el inventario.
    Proporciona métodos para agregar, actualizar, eliminar y buscar productos,
    así como para obtener alertas sobre stock bajo y productos próximos a vencer.
    """

    def __init__(self):
        """
        Inicializa el servicio de inventario.
        """
        self.db_service = DatabaseService()

    def get_all_products(self) -> List[Dict]:
        """
        Obtiene todos los productos del inventario.

        Returns:
            List[Dict]: Lista de productos con sus detalles
        """
        try:
            query = """
                SELECT p.ID as id, p.Nombre as nombre, c.Nombre as categoria,
                       p.Cantidad_en_stock as stock, p.Precio as precio, 
                       p.Fecha_vencimiento as fecha_vencimiento, 
                       p.Fecha_registro as fecha_registro 
                FROM Productos p
                LEFT JOIN Categorias c ON p.categoria_id = c.ID
                ORDER BY p.Nombre
            """
            return self.db_service.fetch_all(query)
        except Exception as e:
            raise Exception(f"{ERROR_MESSAGES['db_error']}: {str(e)}")

    def get_product_by_id(self, product_id: int) -> Optional[Dict]:
        """
        Obtiene un producto por su ID.

        Args:
            product_id: ID del producto

        Returns:
            Dict: Datos del producto o None si no existe
        """
        try:
            query = """
                SELECT p.ID as id, p.Nombre as nombre, c.Nombre as categoria,
                       p.Cantidad_en_stock as stock, p.Precio as precio, 
                       p.Fecha_vencimiento as fecha_vencimiento, 
                       p.Fecha_registro as fecha_registro 
                FROM Productos p
                LEFT JOIN Categorias c ON p.categoria_id = c.ID
                WHERE p.ID = %s
            """
            return self.db_service.fetch_one(query, (product_id,))
        except Exception as e:
            raise Exception(f"{ERROR_MESSAGES['db_error']}: {str(e)}")

    def add_product(self, product: Dict) -> int:
        """
        Agrega un nuevo producto al inventario.

        Args:
            product: Diccionario con los datos del producto

        Returns:
            int: ID del producto agregado
        """
        try:
            return self.db_service.insert('Productos', product)
        except Exception as e:
            raise Exception(f"{ERROR_MESSAGES['db_error']}: {str(e)}")

    def update_product(self, product_id: int, data: Dict) -> None:
        """
        Actualiza los datos de un producto.

        Args:
            product_id: ID del producto a actualizar
            data: Diccionario con los datos a actualizar
        """
        try:
            self.db_service.update('Productos', data, 'ID = %s', (product_id,))
        except Exception as e:
            raise Exception(f"{ERROR_MESSAGES['db_error']}: {str(e)}")

    def update_product_stock(self, product_id: int, new_stock: int) -> None:
        """
        Actualiza el stock de un producto.

        Args:
            product_id: ID del producto
            new_stock: Nueva cantidad en stock
        """
        try:
            self.update_product(product_id, {'Cantidad_en_stock': new_stock})
        except Exception as e:
            raise Exception(f"{ERROR_MESSAGES['db_error']}: {str(e)}")

    def delete_product(self, product_id: int) -> None:
        """
        Elimina un producto del inventario.

        Args:
            product_id: ID del producto a eliminar
        """
        try:
            self.db_service.delete('Productos', 'ID = %s', (product_id,))
        except Exception as e:
            raise Exception(f"{ERROR_MESSAGES['db_error']}: {str(e)}")

    def get_low_stock_products(self) -> List[Dict]:
        """
        Obtiene los productos con stock bajo.

        Returns:
            List[Dict]: Lista de productos con stock bajo
        """
        try:
            query = """
                SELECT ID, Nombre, Categoria, Cantidad_en_stock, Precio
                FROM Productos
                WHERE Cantidad_en_stock <= %s
                ORDER BY Cantidad_en_stock
            """
            return self.db_service.fetch_all(query, (STOCK['low_stock_threshold'],))
        except Exception as e:
            raise Exception(f"{ERROR_MESSAGES['db_error']}: {str(e)}")

    def get_products_by_category(self, category: str) -> List[Dict]:
        """
        Obtiene los productos de una categoría.

        Args:
            category: Nombre de la categoría

        Returns:
            List[Dict]: Lista de productos de la categoría
        """
        try:
            query = """
                SELECT p.ID, p.Nombre, c.Nombre as categoria, p.Cantidad_en_stock, p.Precio
                FROM Productos p
                LEFT JOIN Categorias c ON p.categoria_id = c.ID
                WHERE c.Nombre = %s
                ORDER BY p.Nombre
            """
            return self.db_service.fetch_all(query, (category,))
        except Exception as e:
            raise Exception(f"{ERROR_MESSAGES['db_error']}: {str(e)}")

    def get_expiring_products(self, days: int = 30) -> List[Dict]:
        """
        Obtiene los productos próximos a vencer.

        Args:
            days: Número de días para considerar próximos a vencer

        Returns:
            List[Dict]: Lista de productos próximos a vencer
        """
        try:
            expiry_date = (datetime.now() + timedelta(days=days)
                           ).strftime('%Y-%m-%d')
            query = """
                SELECT ID, Nombre, Categoria, Cantidad_en_stock, Precio, Fecha_vencimiento
                FROM Productos
                WHERE Fecha_vencimiento <= %s
                  AND Fecha_vencimiento >= CURRENT_DATE
                ORDER BY Fecha_vencimiento
            """
            return self.db_service.fetch_all(query, (expiry_date,))
        except Exception as e:
            raise Exception(f"{ERROR_MESSAGES['db_error']}: {str(e)}")

    def search_products(self, search_term: str) -> List[Dict]:
        """
        Busca productos por nombre o categoría.

        Args:
            search_term: Término de búsqueda

        Returns:
            List[Dict]: Lista de productos que coinciden con la búsqueda
        """
        try:
            query = """
                SELECT p.ID, p.Nombre, c.Nombre as categoria, p.Cantidad_en_stock, p.Precio
                FROM Productos p
                LEFT JOIN Categorias c ON p.categoria_id = c.ID
                WHERE p.Nombre ILIKE %s OR c.Nombre ILIKE %s
                ORDER BY p.Nombre
            """
            search_pattern = f"%{search_term}%"
            return self.db_service.fetch_all(query, (search_pattern, search_pattern))
        except Exception as e:
            raise Exception(f"{ERROR_MESSAGES['db_error']}: {str(e)}")

    def get_stock_value(self) -> float:
        """
        Calcula el valor total del inventario.

        Returns:
            float: Valor total del inventario
        """
        try:
            query = """
                SELECT SUM(Cantidad_en_stock * Precio) as valor_total
                FROM Productos
            """
            result = self.db_service.fetch_one(query)
            return float(result['valor_total'] if result and result['valor_total'] else 0)
        except Exception as e:
            raise Exception(f"{ERROR_MESSAGES['db_error']}: {str(e)}")

    def get_stock_value_by_category(self) -> List[Dict]:
        """
        Calcula el valor del inventario por categoría.

        Returns:
            List[Dict]: Lista de valores por categoría
        """
        try:
            query = """
                SELECT Categoria,
                       COUNT(*) as total_productos,
                       SUM(Cantidad_en_stock) as total_stock,
                       SUM(Cantidad_en_stock * Precio) as valor_total
                FROM Productos
                GROUP BY Categoria
                ORDER BY valor_total DESC
            """
            return self.db_service.fetch_all(query)
        except Exception as e:
            raise Exception(f"{ERROR_MESSAGES['db_error']}: {str(e)}")
