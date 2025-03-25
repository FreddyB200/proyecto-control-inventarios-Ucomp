"""
Modelo para representar una venta en el sistema.
"""

from datetime import datetime

class Venta:
    """
    Clase que representa una venta en el sistema.
    Encapsula los datos y la lógica de negocio relacionada con las ventas.
    """
    
    def __init__(self, id=None, fecha=None, id_producto=None, cantidad=0, 
                 precio_unitario=0.0, total=0.0):
        """
        Inicializa una nueva venta.
        
        Args:
            id (int, optional): ID de la venta. Defaults to None.
            fecha (str, optional): Fecha de la venta en formato YYYY-MM-DD. Defaults to None.
            id_producto (int, optional): ID del producto vendido. Defaults to None.
            cantidad (int, optional): Cantidad vendida. Defaults to 0.
            precio_unitario (float, optional): Precio unitario del producto. Defaults to 0.0.
            total (float, optional): Total de la venta. Defaults to 0.0.
        """
        self.id = id
        self.fecha = fecha if fecha else datetime.now().strftime('%Y-%m-%d')
        self.id_producto = id_producto
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.total = total if total else self.calcular_total()
    
    @classmethod
    def from_dict(cls, data):
        """
        Crea una instancia de Venta a partir de un diccionario.
        
        Args:
            data (dict): Diccionario con los datos de la venta.
            
        Returns:
            Venta: Instancia de Venta.
        """
        return cls(
            id=data.get('ID'),
            fecha=data.get('Fecha'),
            id_producto=data.get('ID_producto'),
            cantidad=data.get('Cantidad', 0),
            precio_unitario=data.get('Precio_unitario', 0.0),
            total=data.get('Total', 0.0)
        )
    
    def to_dict(self):
        """
        Convierte la instancia de Venta a un diccionario.
        
        Returns:
            dict: Diccionario con los datos de la venta.
        """
        data = {
            'Fecha': self.fecha,
            'ID_producto': self.id_producto,
            'Cantidad': self.cantidad,
            'Precio_unitario': self.precio_unitario,
            'Total': self.total
        }
        
        if self.id is not None:
            data['ID'] = self.id
        
        return data
    
    def calcular_total(self):
        """
        Calcula el total de la venta.
        
        Returns:
            float: Total de la venta.
        """
        self.total = round(self.cantidad * self.precio_unitario, 2)
        return self.total
    
    def validar(self):
        """
        Valida que la venta tenga datos válidos.
        
        Returns:
            bool: True si la venta es válida, False en caso contrario.
        """
        if not self.id_producto:
            return False
        
        if self.cantidad <= 0:
            return False
        
        if self.precio_unitario <= 0:
            return False
        
        return True
    
    def __str__(self):
        """
        Representación en string de la venta.
        
        Returns:
            str: Representación en string.
        """
        return f"Venta #{self.id} - Producto: {self.id_producto} - Cantidad: {self.cantidad} - Total: ${self.total}"
