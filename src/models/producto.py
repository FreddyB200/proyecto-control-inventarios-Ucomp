"""
Modelo para representar un producto en el inventario.
"""

from datetime import datetime

class Producto:
    """
    Clase que representa un producto en el inventario.
    Encapsula los datos y la lógica de negocio relacionada con los productos.
    """
    
    def __init__(self, id=None, nombre="", precio=0.0, fecha_vencimiento=None, 
                 cantidad_en_stock=0, nit_proveedor=None):
        """
        Inicializa un nuevo producto.
        
        Args:
            id (int, optional): ID del producto. Defaults to None.
            nombre (str, optional): Nombre del producto. Defaults to "".
            precio (float, optional): Precio del producto. Defaults to 0.0.
            fecha_vencimiento (str, optional): Fecha de vencimiento en formato YYYY-MM-DD. Defaults to None.
            cantidad_en_stock (int, optional): Cantidad en stock. Defaults to 0.
            nit_proveedor (str, optional): NIT del proveedor. Defaults to None.
        """
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.fecha_vencimiento = fecha_vencimiento
        self.cantidad_en_stock = cantidad_en_stock
        self.nit_proveedor = nit_proveedor
    
    @classmethod
    def from_dict(cls, data):
        """
        Crea una instancia de Producto a partir de un diccionario.
        
        Args:
            data (dict): Diccionario con los datos del producto.
            
        Returns:
            Producto: Instancia de Producto.
        """
        return cls(
            id=data.get('ID'),
            nombre=data.get('Nombre', ""),
            precio=data.get('Precio', 0.0),
            fecha_vencimiento=data.get('Fecha_vencimiento'),
            cantidad_en_stock=data.get('Cantidad_en_stock', 0),
            nit_proveedor=data.get('NIT_proveedor')
        )
    
    def to_dict(self):
        """
        Convierte la instancia de Producto a un diccionario.
        
        Returns:
            dict: Diccionario con los datos del producto.
        """
        data = {
            'Nombre': self.nombre,
            'Precio': self.precio,
            'Cantidad_en_stock': self.cantidad_en_stock
        }
        
        if self.id is not None:
            data['ID'] = self.id
        
        if self.fecha_vencimiento:
            data['Fecha_vencimiento'] = self.fecha_vencimiento
        
        if self.nit_proveedor:
            data['NIT_proveedor'] = self.nit_proveedor
        
        return data
    
    def is_low_stock(self, min_stock=10):
        """
        Verifica si el producto tiene stock bajo.
        
        Args:
            min_stock (int, optional): Cantidad mínima de stock. Defaults to 10.
            
        Returns:
            bool: True si el producto tiene stock bajo, False en caso contrario.
        """
        return self.cantidad_en_stock < min_stock
    
    def is_expiring_soon(self, days=7):
        """
        Verifica si el producto está próximo a vencer.
        
        Args:
            days (int, optional): Días para considerar próximo a vencer. Defaults to 7.
            
        Returns:
            bool: True si el producto está próximo a vencer, False en caso contrario.
        """
        if not self.fecha_vencimiento:
            return False
        
        if isinstance(self.fecha_vencimiento, str):
            try:
                fecha_vencimiento = datetime.strptime(self.fecha_vencimiento, '%Y-%m-%d').date()
            except ValueError:
                return False
        else:
            fecha_vencimiento = self.fecha_vencimiento
        
        today = datetime.now().date()
        days_until_expiry = (fecha_vencimiento - today).days
        
        return 0 <= days_until_expiry <= days
    
    def apply_discount(self, discount_percent=20):
        """
        Aplica un descuento al precio del producto.
        
        Args:
            discount_percent (int, optional): Porcentaje de descuento. Defaults to 20.
            
        Returns:
            float: Nuevo precio con descuento.
        """
        discount_factor = 1 - (discount_percent / 100)
        self.precio = round(self.precio * discount_factor, 2)
        return self.precio
    
    def increase_stock(self, quantity):
        """
        Aumenta la cantidad en stock del producto.
        
        Args:
            quantity (int): Cantidad a aumentar.
            
        Returns:
            int: Nueva cantidad en stock.
        """
        if quantity < 0:
            raise ValueError("La cantidad a aumentar no puede ser negativa")
        
        self.cantidad_en_stock += quantity
        return self.cantidad_en_stock
    
    def decrease_stock(self, quantity):
        """
        Disminuye la cantidad en stock del producto.
        
        Args:
            quantity (int): Cantidad a disminuir.
            
        Returns:
            int: Nueva cantidad en stock.
            
        Raises:
            ValueError: Si la cantidad a disminuir es mayor que la cantidad en stock.
        """
        if quantity < 0:
            raise ValueError("La cantidad a disminuir no puede ser negativa")
        
        if quantity > self.cantidad_en_stock:
            raise ValueError("No hay suficiente stock disponible")
        
        self.cantidad_en_stock -= quantity
        return self.cantidad_en_stock
    
    def __str__(self):
        """
        Representación en string del producto.
        
        Returns:
            str: Representación en string.
        """
        return f"{self.nombre} - ${self.precio} - Stock: {self.cantidad_en_stock}"
