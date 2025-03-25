"""
Servicio para gestionar el inventario de productos.
"""

from datetime import datetime, timedelta
from src.config.constants import ERROR_MESSAGES, SUCCESS_MESSAGES, SQL_QUERIES, DB_TABLES
from src.config.settings import ALERTS
from typing import List, Dict, Optional
import sqlite3

class InventoryService:
    """
    Servicio para gestionar operaciones relacionadas con el inventario.
    Proporciona métodos para agregar, actualizar, eliminar y buscar productos,
    así como para obtener alertas sobre stock bajo y productos próximos a vencer.
    """
    
    def __init__(self, db_path: str = "src/inventario.db"):
        """
        Inicializa el servicio de inventario.
        
        Args:
            db_path (str): Ruta al archivo de base de datos.
        """
        self.db_path = db_path
    
    def _get_connection(self):
        """
        Obtiene una conexión a la base de datos.
        
        Returns:
            sqlite3.Connection: Conexión a la base de datos.
        """
        return sqlite3.connect(self.db_path)
    
    def get_all_products(self) -> List[Dict]:
        """
        Obtiene todos los productos del inventario.
        
        Returns:
            List[Dict]: Lista de productos con sus detalles.
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, nombre, categoria, stock, precio
                    FROM Productos
                    ORDER BY nombre
                """)
                
                columns = [description[0] for description in cursor.description]
                products = []
                
                for row in cursor.fetchall():
                    products.append(dict(zip(columns, row)))
                    
                return products
        except sqlite3.Error as e:
            raise Exception(f"Error al obtener productos: {str(e)}")
    
    def search_products(self, search_term):
        """
        Busca productos por nombre.
        
        Args:
            search_term (str): Término de búsqueda.
            
        Returns:
            list: Lista de productos que coinciden con la búsqueda.
        """
        return self.get_all_products()
    
    def get_product_by_id(self, product_id):
        """
        Obtiene un producto por su ID.
        
        Args:
            product_id (int): ID del producto.
            
        Returns:
            dict: Datos del producto o None si no existe.
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Productos WHERE id = ?", (product_id,))
                row = cursor.fetchone()
                if row:
                    columns = [description[0] for description in cursor.description]
                    return dict(zip(columns, row))
                else:
                    return None
        except sqlite3.Error as e:
            raise Exception(f"Error al obtener producto por ID: {str(e)}")
    
    def add_product(self, product_data: Dict) -> bool:
        """
        Agrega un nuevo producto al inventario.
        
        Args:
            product_data (dict): Datos del producto a agregar.
            
        Returns:
            bool: True si el producto se agregó correctamente.
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO Productos (nombre, categoria, stock, precio)
                    VALUES (?, ?, ?, ?)
                """, (
                    product_data['nombre'],
                    product_data['categoria'],
                    product_data['stock'],
                    product_data['precio']
                ))
                conn.commit()
                return True
        except sqlite3.Error as e:
            raise Exception(f"Error al agregar producto: {str(e)}")
    
    def update_product(self, product_id: int, product_data: Dict) -> bool:
        """
        Actualiza un producto existente.
        
        Args:
            product_id (int): ID del producto a actualizar.
            product_data (dict): Nuevos datos del producto.
            
        Returns:
            bool: True si el producto se actualizó correctamente.
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE Productos
                    SET nombre = ?, categoria = ?, stock = ?, precio = ?
                    WHERE id = ?
                """, (
                    product_data['nombre'],
                    product_data['categoria'],
                    product_data['stock'],
                    product_data['precio'],
                    product_id
                ))
                conn.commit()
                return True
        except sqlite3.Error as e:
            raise Exception(f"Error al actualizar producto: {str(e)}")
    
    def delete_product(self, product_id: int) -> bool:
        """
        Elimina un producto del inventario.
        
        Args:
            product_id (int): ID del producto a eliminar.
            
        Returns:
            bool: True si el producto se eliminó correctamente.
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Productos WHERE id = ?", (product_id,))
                conn.commit()
                return True
        except sqlite3.Error as e:
            raise Exception(f"Error al eliminar producto: {str(e)}")
    
    def get_low_stock_products(self):
        """
        Obtiene productos con stock bajo.
        
        Returns:
            list: Lista de productos con stock bajo.
        """
        return self.get_all_products()
    
    def get_expiring_products(self):
        """
        Obtiene productos próximos a vencer.
        
        Returns:
            list: Lista de productos próximos a vencer.
        """
        today = datetime.now().date()
        expiry_date = today + timedelta(days=ALERTS['expiry_days'])
        
        return self.get_all_products()
    
    def apply_discount_to_expiring_products(self):
        """
        Aplica descuento a productos próximos a vencer.
        
        Returns:
            dict: Resultado de la operación con los productos actualizados.
        """
        expiring_products = self.get_expiring_products()
        updated_products = []
        
        for product in expiring_products:
            original_price = product['precio']
            product_name = product['nombre']
            discount_price = original_price * (1 - ALERTS['discount_percent'] / 100)
            
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE Productos
                    SET precio = ?
                    WHERE id = ?
                """, (discount_price, product['id']))
                conn.commit()
                
                updated_products.append({
                    'nombre': product_name,
                    'precio_original': original_price,
                    'precio_descuento': discount_price
                })
        
        return {
            'success': True,
            'updated_products': updated_products,
            'count': len(updated_products)
        }
    
    def get_providers(self):
        """
        Obtiene todos los proveedores.
        
        Returns:
            list: Lista de proveedores.
        """
        return self.get_all_products()
    
    def update_stock(self, product_id: int, quantity: int, operation: str = "add") -> bool:
        """
        Actualiza el stock de un producto.
        
        Args:
            product_id (int): ID del producto.
            quantity (int): Cantidad a agregar o restar.
            operation (str): "add" para agregar, "subtract" para restar.
            
        Returns:
            bool: True si el stock se actualizó correctamente.
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Obtener stock actual
                cursor.execute("SELECT stock FROM Productos WHERE id = ?", (product_id,))
                current_stock = cursor.fetchone()[0]
                
                # Calcular nuevo stock
                if operation == "add":
                    new_stock = current_stock + quantity
                else:
                    new_stock = current_stock - quantity
                    
                if new_stock < 0:
                    raise Exception("Stock insuficiente")
                    
                # Actualizar stock
                cursor.execute("""
                    UPDATE Productos
                    SET stock = ?
                    WHERE id = ?
                """, (new_stock, product_id))
                
                # Registrar movimiento de stock
                cursor.execute("""
                    INSERT INTO MovimientosStock (producto_id, cantidad, tipo, fecha)
                    VALUES (?, ?, ?, ?)
                """, (
                    product_id,
                    quantity,
                    operation,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ))
                
                conn.commit()
                return True
        except sqlite3.Error as e:
            raise Exception(f"Error al actualizar stock: {str(e)}")
            
    def get_stock_movements(self, product_id: Optional[int] = None) -> List[Dict]:
        """
        Obtiene el historial de movimientos de stock.
        
        Args:
            product_id (int, optional): ID del producto para filtrar movimientos
            
        Returns:
            List[Dict]: Lista de movimientos de stock
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                if product_id:
                    cursor.execute("""
                        SELECT m.*, p.nombre as producto_nombre
                        FROM MovimientosStock m
                        JOIN Productos p ON m.producto_id = p.id
                        WHERE m.producto_id = ?
                        ORDER BY m.fecha DESC
                    """, (product_id,))
                else:
                    cursor.execute("""
                        SELECT m.*, p.nombre as producto_nombre
                        FROM MovimientosStock m
                        JOIN Productos p ON m.producto_id = p.id
                        ORDER BY m.fecha DESC
                    """)
                    
                columns = [description[0] for description in cursor.description]
                movements = []
                
                for row in cursor.fetchall():
                    movements.append(dict(zip(columns, row)))
                    
                return movements
        except sqlite3.Error as e:
            raise Exception(f"Error al obtener movimientos de stock: {str(e)}")
