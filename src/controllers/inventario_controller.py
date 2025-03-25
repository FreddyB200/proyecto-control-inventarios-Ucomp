"""
Controlador para gestionar el inventario de productos.
"""

from src.models.producto import Producto
from src.config.constants import ERROR_MESSAGES
from src.config.settings import ALERTS

class InventarioController:
    """
    Controlador para gestionar el inventario de productos.
    Coordina las operaciones entre la vista de inventario y los servicios/modelos.
    """
    
    def __init__(self, inventory_service):
        """
        Inicializa el controlador de inventario.
        
        Args:
            inventory_service (InventoryService): Servicio de inventario.
        """
        self.inventory_service = inventory_service
    
    def get_all_products(self):
        """
        Obtiene todos los productos del inventario.
        
        Returns:
            list: Lista de objetos Producto.
        """
        products_data = self.inventory_service.get_all_products()
        return [Producto.from_dict(product) for product in products_data]
    
    def search_products(self, search_term):
        """
        Busca productos por nombre.
        
        Args:
            search_term (str): Término de búsqueda.
            
        Returns:
            list: Lista de objetos Producto que coinciden con la búsqueda.
        """
        products_data = self.inventory_service.search_products(search_term)
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
    
    def add_product(self, product_data):
        """
        Agrega un nuevo producto al inventario.
        
        Args:
            product_data (dict): Datos del producto a agregar.
            
        Returns:
            dict: Resultado de la operación.
        """
        # Validar datos de entrada
        try:
            producto = Producto.from_dict(product_data)
            if not producto.nombre:
                return {'error': ERROR_MESSAGES['empty_fields']}
            
            # Agregar producto
            result = self.inventory_service.add_product(product_data)
            
            if 'success' in result and result['success']:
                producto.id = result['id']
                return {'success': True, 'message': result['message'], 'product': producto}
            
            return result
        except Exception as e:
            return {'error': ERROR_MESSAGES['product_add_error'].format(str(e))}
    
    def update_product(self, product_id, product_data):
        """
        Actualiza un producto existente.
        
        Args:
            product_id (int): ID del producto a actualizar.
            product_data (dict): Nuevos datos del producto.
            
        Returns:
            dict: Resultado de la operación.
        """
        # Validar datos de entrada
        try:
            producto = Producto.from_dict(product_data)
            if not producto.nombre:
                return {'error': ERROR_MESSAGES['empty_fields']}
            
            # Actualizar producto
            result = self.inventory_service.update_product(product_id, product_data)
            
            if 'success' in result and result['success']:
                producto.id = product_id
                return {'success': True, 'message': result['message'], 'product': producto}
            
            return result
        except Exception as e:
            return {'error': ERROR_MESSAGES['product_update_error'].format(str(e))}
    
    def delete_product(self, product_id):
        """
        Elimina un producto del inventario.
        
        Args:
            product_id (int): ID del producto a eliminar.
            
        Returns:
            dict: Resultado de la operación.
        """
        return self.inventory_service.delete_product(product_id)
    
    def get_low_stock_products(self):
        """
        Obtiene productos con stock bajo.
        
        Returns:
            list: Lista de objetos Producto con stock bajo.
        """
        products_data = self.inventory_service.get_low_stock_products()
        return [Producto.from_dict(product) for product in products_data]
    
    def get_expiring_products(self):
        """
        Obtiene productos próximos a vencer.
        
        Returns:
            list: Lista de objetos Producto próximos a vencer.
        """
        products_data = self.inventory_service.get_expiring_products()
        return [Producto.from_dict(product) for product in products_data]
    
    def apply_discount_to_expiring_products(self):
        """
        Aplica descuento a productos próximos a vencer.
        
        Returns:
            dict: Resultado de la operación con los productos actualizados.
        """
        result = self.inventory_service.apply_discount_to_expiring_products()
        
        if 'success' in result and result['success']:
            # Convertir productos actualizados a objetos Producto
            updated_products = []
            for product_data in result['updated_products']:
                producto = Producto(
                    nombre=product_data['nombre'],
                    precio=product_data['precio_descuento']
                )
                updated_products.append(producto)
            
            result['updated_products'] = updated_products
        
        return result
    
    def get_providers(self):
        """
        Obtiene todos los proveedores.
        
        Returns:
            list: Lista de proveedores.
        """
        return self.inventory_service.get_providers()
    
    def format_product_for_display(self, product):
        """
        Formatea un producto para su visualización en la interfaz.
        
        Args:
            product (Producto): Producto a formatear.
            
        Returns:
            tuple: Tupla con los datos formateados del producto.
        """
        return (
            product.id,
            product.nombre,
            f"${product.precio:.2f}",
            product.fecha_vencimiento,
            product.cantidad_en_stock
        )
    
    def get_product_alerts(self):
        """
        Obtiene alertas sobre productos (stock bajo y próximos a vencer).
        
        Returns:
            dict: Diccionario con las alertas.
        """
        low_stock = self.get_low_stock_products()
        expiring = self.get_expiring_products()
        
        return {
            'low_stock': low_stock,
            'expiring': expiring,
            'has_alerts': len(low_stock) > 0 or len(expiring) > 0
        }
