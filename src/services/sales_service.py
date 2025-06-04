"""
Servicio para gestionar las ventas.
"""

from datetime import datetime
from typing import List, Dict, Optional
from config.constants import ERROR_MESSAGES, SUCCESS_MESSAGES, SQL_QUERIES, DB_TABLES
from services.database_service import DatabaseService
from services.inventory_service import InventoryService


class SalesService:
    """
    Servicio para gestionar operaciones relacionadas con ventas.
    Proporciona métodos para registrar ventas, obtener historial de ventas,
    calcular totales y generar reportes.
    """

    def __init__(self):
        """
        Inicializa el servicio de ventas.
        """
        self.db_service = DatabaseService()
        self.inventory_service = InventoryService()

    def register_sale(self, sale_data: Dict) -> int:
        """
        Registra una nueva venta.

        Args:
            sale_data: Diccionario con los datos de la venta

        Returns:
            int: ID de la venta registrada
        """
        try:
            # Iniciar transacción
            self.db_service.begin_transaction()

            # Insertar la venta
            sale_id = self.db_service.insert('Ventas', {
                'Fecha': datetime.now(),
                'ID_usuario': sale_data['ID_usuario'],
                'Total': sale_data['Total']
            })

            # Insertar detalles de la venta
            for detail in sale_data['detalles']:
                self.db_service.insert('DetallesVenta', {
                    'ID_venta': sale_id,
                    'ID_producto': detail['ID_producto'],
                    'Cantidad': detail['Cantidad'],
                    'Precio_unitario': detail['Precio_unitario'],
                    'Subtotal': detail['Subtotal']
                })

                # Actualizar stock
                product = self.inventory_service.get_product_by_id(
                    detail['ID_producto'])
                new_stock = product['stock'] - detail['Cantidad']
                self.inventory_service.update_product_stock(
                    detail['ID_producto'], new_stock)

            # Registrar movimiento de stock
            self.db_service.insert('MovimientosStock', {
                'Fecha': datetime.now(),
                'ID_producto': detail['ID_producto'],
                'Cantidad': -detail['Cantidad'],
                'Tipo': 'Venta',
                'ID_usuario': sale_data['ID_usuario']
            })

            # Confirmar transacción
            self.db_service.commit()
            return sale_id

        except Exception as e:
            # Revertir cambios en caso de error
            self.db_service.rollback()
            raise Exception(f"{ERROR_MESSAGES['db_error']}: {str(e)}")

    def get_sale_by_id(self, sale_id: int) -> Optional[Dict]:
        """
        Obtiene una venta por su ID.

        Args:
            sale_id: ID de la venta

        Returns:
            Dict: Datos de la venta o None si no existe
        """
        try:
            query = """
                SELECT v.ID, v.Fecha, v.Total, u.Usuario as vendedor,
                       COUNT(d.ID) as total_productos
                FROM Ventas v
                LEFT JOIN Usuarios u ON v.ID_usuario = u.ID
                LEFT JOIN DetallesVenta d ON v.ID = d.ID_venta
                WHERE v.ID = %s
                GROUP BY v.ID, v.Fecha, v.Total, u.Usuario
            """
            return self.db_service.fetch_one(query, (sale_id,))
        except Exception as e:
            raise Exception(f"{ERROR_MESSAGES['db_error']}: {str(e)}")

    def get_sale_details(self, sale_id: int) -> List[Dict]:
        """
        Obtiene los detalles de una venta.

        Args:
            sale_id: ID de la venta

        Returns:
            List[Dict]: Lista de detalles de la venta
        """
        try:
            query = """
                SELECT d.ID, p.Nombre as producto, d.Cantidad,
                       d.Precio_unitario, d.Subtotal
                FROM DetallesVenta d
                JOIN Productos p ON d.ID_producto = p.ID
                WHERE d.ID_venta = %s
                ORDER BY d.ID
            """
            return self.db_service.fetch_all(query, (sale_id,))
        except Exception as e:
            raise Exception(f"{ERROR_MESSAGES['db_error']}: {str(e)}")

    def get_sales_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Dict]:
        """
        Obtiene las ventas en un rango de fechas.

        Args:
            start_date: Fecha inicial
            end_date: Fecha final

        Returns:
            List[Dict]: Lista de ventas en el rango de fechas
        """
        try:
            query = """
                SELECT v.ID, v.Fecha, v.Total, u.Usuario as vendedor,
                       COUNT(d.ID) as total_productos
                FROM Ventas v
                LEFT JOIN Usuarios u ON v.ID_usuario = u.ID
                LEFT JOIN DetallesVenta d ON v.ID = d.ID_venta
                WHERE v.Fecha BETWEEN %s AND %s
                GROUP BY v.ID, v.Fecha, v.Total, u.Usuario
                ORDER BY v.Fecha DESC
            """
            return self.db_service.fetch_all(query, (start_date, end_date))
        except Exception as e:
            raise Exception(f"{ERROR_MESSAGES['db_error']}: {str(e)}")

    def get_sales_by_user(self, user_id: int) -> List[Dict]:
        """
        Obtiene las ventas realizadas por un usuario.

        Args:
            user_id: ID del usuario

        Returns:
            List[Dict]: Lista de ventas del usuario
        """
        try:
            query = """
                SELECT v.ID, v.Fecha, v.Total,
                       COUNT(d.ID) as total_productos
                FROM Ventas v
                LEFT JOIN DetallesVenta d ON v.ID = d.ID_venta
                WHERE v.ID_usuario = %s
                GROUP BY v.ID, v.Fecha, v.Total
                ORDER BY v.Fecha DESC
            """
            return self.db_service.fetch_all(query, (user_id,))
        except Exception as e:
            raise Exception(f"{ERROR_MESSAGES['db_error']}: {str(e)}")

    def get_sales_summary(self) -> Dict:
        """
        Obtiene un resumen de las ventas.

        Returns:
            Dict: Resumen de ventas con totales y estadísticas
        """
        try:
            query = """
                SELECT 
                    COUNT(*) as total_ventas,
                    SUM(Total) as monto_total,
                    AVG(Total) as promedio_venta,
                    MAX(Total) as venta_maxima,
                    MIN(Total) as venta_minima
                FROM Ventas
            """
            return self.db_service.fetch_one(query)
        except Exception as e:
            raise Exception(f"{ERROR_MESSAGES['db_error']}: {str(e)}")

    def get_top_products(self, limit: int = 10) -> List[Dict]:
        """
        Obtiene los productos más vendidos.

        Args:
            limit: Número máximo de productos a retornar

        Returns:
            List[Dict]: Lista de productos más vendidos
        """
        try:
            query = """
                SELECT p.ID, p.Nombre, p.Categoria,
                       SUM(d.Cantidad) as total_vendido,
                       SUM(d.Subtotal) as monto_total
                FROM Productos p
                JOIN DetallesVenta d ON p.ID = d.ID_producto
                GROUP BY p.ID, p.Nombre, p.Categoria
                ORDER BY total_vendido DESC
                LIMIT %s
            """
            return self.db_service.fetch_all(query, (limit,))
        except Exception as e:
            raise Exception(f"{ERROR_MESSAGES['db_error']}: {str(e)}")

    def get_sales_by_category(self) -> List[Dict]:
        """
        Obtiene las ventas agrupadas por categoría.

        Returns:
            List[Dict]: Lista de ventas por categoría
        """
        try:
            query = """
                SELECT p.Categoria,
                       COUNT(DISTINCT v.ID) as total_ventas,
                       SUM(d.Cantidad) as total_productos,
                       SUM(d.Subtotal) as monto_total
                FROM Ventas v
                JOIN DetallesVenta d ON v.ID = d.ID_venta
                JOIN Productos p ON d.ID_producto = p.ID
                GROUP BY p.Categoria
                ORDER BY monto_total DESC
            """
            return self.db_service.fetch_all(query)
        except Exception as e:
            raise Exception(f"{ERROR_MESSAGES['db_error']}: {str(e)}")
