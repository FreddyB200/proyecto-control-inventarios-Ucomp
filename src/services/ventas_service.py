"""
Servicio para gestionar las ventas de productos.
"""

from datetime import datetime
from config.constants import DB_TABLES, SQL_QUERIES, ERROR_MESSAGES, SUCCESS_MESSAGES
from services.database_service import DatabaseService
from services.inventory_service import InventoryService


class VentasService:
    """
    Servicio para gestionar las ventas de productos.
    Proporciona métodos para registrar ventas, consultar historial y generar reportes.
    """

    def __init__(self):
        """
        Inicializa el servicio de ventas.
        """
        self.db_service = DatabaseService()
        self.inventory_service = InventoryService()

    def register_sale(self, sale_data):
        """
        Registra una nueva venta en el sistema.

        Args:
            sale_data (dict): Datos de la venta a registrar.

        Returns:
            dict: Resultado de la operación.
        """
        try:
            # Validar datos de entrada
            if not sale_data.get('ID_producto') or not sale_data.get('Cantidad'):
                return {'error': ERROR_MESSAGES['empty_fields']}

            # Obtener producto
            product_id = sale_data['ID_producto']
            cantidad = int(sale_data['Cantidad'])

            product = self.inventory_service.get_product_by_id(product_id)
            if not product:
                return {'error': ERROR_MESSAGES['product_not_found']}

            # Verificar stock disponible
            if cantidad > product['Cantidad_en_stock']:
                return {'error': 'No hay suficiente stock disponible'}

            # Calcular total
            precio_unitario = product['Precio']
            total = precio_unitario * cantidad

            # Preparar datos de venta
            venta_data = {
                'Fecha': datetime.now().strftime('%Y-%m-%d'),
                'ID_producto': product_id,
                'Cantidad': cantidad,
                'Precio_unitario': precio_unitario,
                'Total': total,
                # Usuario por defecto si no se especifica
                'ID_usuario': sale_data.get('ID_usuario', 1)
            }

            # Iniciar transacción
            self.db_service.begin_transaction()

            try:
                # Registrar venta
                venta_id = self.db_service.insert('Ventas', venta_data)

                if not venta_id:
                    self.db_service.rollback()
                    return {'error': 'Error al registrar la venta'}

                # Actualizar stock
                new_stock = product['Cantidad_en_stock'] - cantidad
                self.inventory_service.update_product_stock(
                    product_id, new_stock)

                # Confirmar transacción
                self.db_service.commit()

                return {
                    'success': True,
                    'message': SUCCESS_MESSAGES['sale_completed'],
                    'sale_id': venta_id,
                    'total': total
                }
            except Exception as e:
                self.db_service.rollback()
                raise e

        except Exception as e:
            return {'error': f'Error al registrar la venta: {str(e)}'}

    def get_sales_by_date_range(self, start_date, end_date):
        """
        Obtiene las ventas realizadas en un rango de fechas.

        Args:
            start_date (str): Fecha de inicio en formato YYYY-MM-DD.
            end_date (str): Fecha de fin en formato YYYY-MM-DD.

        Returns:
            list: Lista de ventas.
        """
        try:
            query = """
                SELECT v.*, p.Nombre as Nombre_producto
                FROM Ventas v
                JOIN Producto p ON v.ID_producto = p.ID
                WHERE v.Fecha BETWEEN ? AND ?
                ORDER BY v.Fecha DESC
            """

            return self.db_service.fetch_all(query, (start_date, end_date))
        except Exception as e:
            print(f"Error al obtener ventas: {e}")
            return []

    def get_total_sales_by_date_range(self, start_date, end_date):
        """
        Obtiene el total de ventas realizadas en un rango de fechas.

        Args:
            start_date (str): Fecha de inicio en formato YYYY-MM-DD.
            end_date (str): Fecha de fin en formato YYYY-MM-DD.

        Returns:
            float: Total de ventas.
        """
        try:
            query = """
                SELECT SUM(Total) as total_ventas
                FROM Ventas
                WHERE Fecha BETWEEN ? AND ?
            """

            result = self.db_service.fetch_one(query, (start_date, end_date))

            if result and result['total_ventas']:
                return float(result['total_ventas'])

            return 0.0
        except Exception as e:
            print(f"Error al obtener total de ventas: {e}")
            return 0.0

    def get_most_sold_products(self, limit=5):
        """
        Obtiene los productos más vendidos.

        Args:
            limit (int, optional): Límite de productos a obtener. Defaults to 5.

        Returns:
            list: Lista de productos más vendidos con cantidad total vendida.
        """
        try:
            query = """
                SELECT p.ID, p.Nombre, SUM(v.Cantidad) as total_vendido
                FROM Ventas v
                JOIN Producto p ON v.ID_producto = p.ID
                GROUP BY p.ID, p.Nombre
                ORDER BY total_vendido DESC
                LIMIT ?
            """

            return self.db_service.fetch_all(query, (limit,))
        except Exception as e:
            print(f"Error al obtener productos más vendidos: {e}")
            return []

    def get_sales_by_product(self, product_id):
        """
        Obtiene las ventas de un producto específico.

        Args:
            product_id (int): ID del producto.

        Returns:
            list: Lista de ventas del producto.
        """
        try:
            query = """
                SELECT *
                FROM Ventas
                WHERE ID_producto = ?
                ORDER BY Fecha DESC
            """

            return self.db_service.fetch_all(query, (product_id,))
        except Exception as e:
            print(f"Error al obtener ventas por producto: {e}")
            return []

    def get_monthly_sales_summary(self, year=None):
        """
        Obtiene un resumen de ventas mensuales.

        Args:
            year (int, optional): Año para el resumen. Si es None, se usa el año actual.

        Returns:
            list: Lista con resumen de ventas por mes.
        """
        try:
            if year is None:
                year = datetime.now().year

            query = """
                SELECT 
                    strftime('%m', Fecha) as mes,
                    COUNT(*) as total_ventas,
                    SUM(Total) as monto_total
                FROM Ventas
                WHERE strftime('%Y', Fecha) = ?
                GROUP BY mes
                ORDER BY mes
            """

            return self.db_service.fetch_all(query, (str(year),))
        except Exception as e:
            print(f"Error al obtener resumen mensual: {e}")
            return []

    def get_daily_sales(self, start_date, end_date):
        """
        Obtiene las ventas diarias en un rango de fechas.

        Args:
            start_date (str): Fecha de inicio en formato YYYY-MM-DD.
            end_date (str): Fecha de fin en formato YYYY-MM-DD.

        Returns:
            list: Lista con ventas por día.
        """
        try:
            query = """
                SELECT 
                    Fecha,
                    COUNT(*) as total_ventas,
                    SUM(Total) as monto_total
                FROM Ventas
                WHERE Fecha BETWEEN ? AND ?
                GROUP BY Fecha
                ORDER BY Fecha
            """

            return self.db_service.fetch_all(query, (start_date, end_date))
        except Exception as e:
            print(f"Error al obtener ventas diarias: {e}")
            return []

    def delete_sale(self, sale_id):
        """
        Elimina una venta y restaura el stock.

        Args:
            sale_id (int): ID de la venta a eliminar.

        Returns:
            dict: Resultado de la operación.
        """
        try:
            # Obtener datos de la venta
            query = "SELECT * FROM Ventas WHERE ID = ?"
            venta = self.db_service.fetch_one(query, (sale_id,))

            if not venta:
                return {'error': 'Venta no encontrada'}

            # Iniciar transacción
            self.db_service.begin_transaction()

            try:
                # Restaurar stock
                product_id = venta['ID_producto']
                cantidad = venta['Cantidad']

                product = self.inventory_service.get_product_by_id(product_id)
                if product:
                    new_stock = product['Cantidad_en_stock'] + cantidad
                    self.inventory_service.update_product_stock(
                        product_id, new_stock)

                # Eliminar venta
                result = self.db_service.delete('Ventas', 'ID = ?', (sale_id,))

                if not result:
                    self.db_service.rollback()
                    return {'error': 'Error al eliminar la venta'}

                # Confirmar transacción
                self.db_service.commit()

                return {
                    'success': True,
                    'message': 'Venta eliminada correctamente'
                }
            except Exception as e:
                self.db_service.rollback()
                raise e

        except Exception as e:
            return {'error': f'Error al eliminar la venta: {str(e)}'}
