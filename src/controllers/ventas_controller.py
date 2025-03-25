"""
Controlador para gestionar las ventas de productos.
"""

from src.models.venta import Venta
from src.models.producto import Producto
from src.config.constants import ERROR_MESSAGES, SUCCESS_MESSAGES

class VentasController:
    """
    Controlador para gestionar las ventas de productos.
    Coordina las operaciones entre la vista de ventas y los servicios/modelos.
    """
    
    def __init__(self, inventory_service, db_service):
        """
        Inicializa el controlador de ventas.
        
        Args:
            inventory_service (InventoryService): Servicio de inventario.
            db_service (DatabaseService): Servicio de base de datos.
        """
        self.inventory_service = inventory_service
        self.db_service = db_service
    
    def get_all_products(self):
        """
        Obtiene todos los productos disponibles para venta.
        
        Returns:
            list: Lista de objetos Producto.
        """
        products_data = self.inventory_service.get_all_products()
        return [Producto.from_dict(product) for product in products_data]
    
    def get_product_by_id(self, product_id):
        """
        Obtiene un producto por su ID.
        
        Args:
            product_id (int): ID del producto.
            
        Returns:
            Producto: Objeto Producto o None si no existe.
        """
        product_data = self.inventory_service.get_product_by_id(product_id)
        return Producto.from_dict(product_data) if product_data else None
    
    def register_sale(self, sale_data):
        """
        Registra una nueva venta.
        
        Args:
            sale_data (dict): Datos de la venta.
            
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
            
            producto = self.get_product_by_id(product_id)
            if not producto:
                return {'error': ERROR_MESSAGES['product_not_found']}
            
            # Verificar stock disponible
            if cantidad > producto.cantidad_en_stock:
                return {'error': 'No hay suficiente stock disponible'}
            
            # Calcular total
            precio_unitario = producto.precio
            total = precio_unitario * cantidad
            
            # Crear objeto Venta
            venta = Venta(
                id_producto=product_id,
                cantidad=cantidad,
                precio_unitario=precio_unitario,
                total=total
            )
            
            # Validar venta
            if not venta.validar():
                return {'error': 'Datos de venta inválidos'}
            
            # Iniciar transacción
            with self.db_service.transaction() as cursor:
                # Registrar venta
                venta_id = self.db_service.insert('Ventas', venta.to_dict())
                
                if not venta_id:
                    return {'error': 'Error al registrar la venta'}
                
                # Actualizar stock
                producto.decrease_stock(cantidad)
                self.inventory_service.update_product(
                    product_id,
                    {'Cantidad_en_stock': producto.cantidad_en_stock}
                )
            
            return {
                'success': True,
                'message': SUCCESS_MESSAGES['sale_completed'],
                'sale': venta,
                'product': producto
            }
        except Exception as e:
            return {'error': f'Error al registrar la venta: {str(e)}'}
    
    def get_sales_by_date_range(self, start_date, end_date):
        """
        Obtiene las ventas realizadas en un rango de fechas.
        
        Args:
            start_date (str): Fecha de inicio en formato YYYY-MM-DD.
            end_date (str): Fecha de fin en formato YYYY-MM-DD.
            
        Returns:
            list: Lista de objetos Venta.
        """
        try:
            query = """
                SELECT v.*, p.Nombre as Nombre_producto
                FROM Ventas v
                JOIN Producto p ON v.ID_producto = p.ID
                WHERE v.Fecha BETWEEN ? AND ?
            """
            
            sales_data = self.db_service.fetch_all(query, (start_date, end_date))
            
            ventas = []
            for sale in sales_data:
                venta = Venta.from_dict(sale)
                # Agregar nombre del producto como atributo adicional
                venta.nombre_producto = sale.get('Nombre_producto', '')
                ventas.append(venta)
            
            return ventas
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
            
            if result and 'total_ventas' in result:
                return float(result['total_ventas'] or 0)
            
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
            
            result = self.db_service.fetch_all(query, (limit,))
            
            return result
        except Exception as e:
            print(f"Error al obtener productos más vendidos: {e}")
            return []
    
    def format_sale_for_display(self, venta):
        """
        Formatea una venta para su visualización en la interfaz.
        
        Args:
            venta (Venta): Venta a formatear.
            
        Returns:
            tuple: Tupla con los datos formateados de la venta.
        """
        return (
            venta.id,
            venta.fecha,
            getattr(venta, 'nombre_producto', f"Producto #{venta.id_producto}"),
            venta.cantidad,
            f"${venta.precio_unitario:.2f}",
            f"${venta.total:.2f}"
        )
