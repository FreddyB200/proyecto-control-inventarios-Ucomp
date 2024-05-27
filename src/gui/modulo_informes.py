import tkinter as tk
from conexion import obtener_cursor

class InformeWindow(tk.Tk): 
    def __init__(self, conexion):
        super().__init__() 
        self.conexion = conexion  # Conexión a la base de datos
        self.title("Reportes")  # Título de la ventana
        self.geometry("600x550")  # Dimensiones de la ventana
        self.resizable(False, False)  # No permitir redimensionar la ventana
        self.crear_widgets()  # Llamada al método para crear widgets

    def crear_widgets(self):
        """Método para crear y configurar los widgets en la ventana."""
        fuente = ('consola', '12', 'bold')
        fuenteTitulo = ('Fixedsys', '18', 'bold')
        # Colores
        colorWind = "#bcd4cc"
        colorFrame = "#DBF0F1"
        colorLetra = "#041A17"
        highlight = "#99CCFF"
        
        # Frame principal
        frame_principal = tk.LabelFrame(self, text="Información sobre tu inventario", font=fuente, bg=colorFrame, width=560, height=500, borderwidth=4, relief="groove", highlightbackground=highlight)
        frame_principal.place(x=20, y=20)
        frame_principal.pack_propagate(False)  # Evitar que el frame se redimensione con el contenido
        
        # Título
        label_titulo = tk.Label(frame_principal, text="CIFRAS RELEVANTES", font=fuenteTitulo)
        label_titulo.pack(pady=10)

        # Etiqueta y valor de ingresos totales
        label_ganancias = tk.Label(frame_principal, text="Ingresos Totales:", font=fuenteTitulo, bg=colorWind, fg=colorLetra)
        label_ganancias.pack(pady=10)
        ganancias_totales = self.calcular_ganancias_totales()  # Calcular ingresos totales
        label_ganancias_valor = tk.Label(frame_principal, text="${:.2f}".format(ganancias_totales), font=fuente, bg=colorWind, fg=colorLetra)
        label_ganancias_valor.pack()

        # Etiqueta y valor de la cantidad de productos
        label_cantidad_productos = tk.Label(frame_principal, text="Cantidad de Productos:", font=fuenteTitulo, bg=colorWind, fg=colorLetra)
        label_cantidad_productos.pack(pady=10)
        cantidad_productos = self.contar_productos()  # Contar productos
        label_cantidad_productos_valor = tk.Label(frame_principal, text=str(cantidad_productos), font=fuente, bg=colorWind, fg=colorLetra)
        label_cantidad_productos_valor.pack()

        # Etiqueta y valor del promedio de ventas
        label_promedio_ventas = tk.Label(frame_principal, text="Promedio de Ventas:", font=fuenteTitulo, bg=colorWind, fg=colorLetra)
        label_promedio_ventas.pack(pady=10)
        promedio_ventas = self.calcular_promedio_ventas()  # Calcular promedio de ventas
        label_promedio_ventas_valor = tk.Label(frame_principal, text="${:.2f}".format(promedio_ventas), font=fuente, bg=colorWind, fg=colorLetra)
        label_promedio_ventas_valor.pack()

        # Etiqueta y valor de la cantidad total de ventas
        label_cantidad_ventas = tk.Label(frame_principal, text="Cantidad Total de Ventas:", font=fuenteTitulo, bg=colorWind, fg=colorLetra)
        label_cantidad_ventas.pack(pady=10)
        cantidad_ventas = self.contar_ventas()  # Contar ventas
        label_cantidad_ventas_valor = tk.Label(frame_principal, text=str(cantidad_ventas), font=fuente, bg=colorWind, fg=colorLetra)
        label_cantidad_ventas_valor.pack()

        # Etiqueta y valor del producto más vendido
        label_producto_mas_vendido = tk.Label(frame_principal, text="Producto Más Vendido:", font=fuenteTitulo, bg=colorWind, fg=colorLetra)
        label_producto_mas_vendido.pack(pady=10)
        producto_mas_vendido = self.obtener_producto_mas_vendido()  # Obtener producto más vendido
        label_producto_mas_vendido_valor = tk.Label(frame_principal, text=producto_mas_vendido, font=fuente, bg=colorWind, fg=colorLetra)
        label_producto_mas_vendido_valor.pack()

    def calcular_ganancias_totales(self):
        """Método para calcular las ganancias totales."""
        cursor = obtener_cursor(self.conexion)
        cursor.execute("SELECT SUM(Venta.Cantidad_producto_vendida * Producto.Precio) FROM Venta JOIN Producto ON Venta.ID_producto = Producto.ID")
        ganancias = cursor.fetchone()[0]  # Obtener el resultado de la consulta
        return ganancias if ganancias is not None else 0  # Devolver 0 si no hay ganancias

    def contar_productos(self):
        """Método para contar la cantidad de productos en el inventario."""
        cursor = obtener_cursor(self.conexion)
        cursor.execute("SELECT COUNT(*) FROM Producto")
        cantidad = cursor.fetchone()[0]  # Obtener el resultado de la consulta
        return cantidad if cantidad is not None else 0  # Devolver 0 si no hay productos

    def calcular_promedio_ventas(self):
        """Método para calcular el promedio de ventas."""
        cursor = obtener_cursor(self.conexion)
        cursor.execute("SELECT AVG(Venta.Cantidad_producto_vendida * Producto.Precio) FROM Venta JOIN Producto ON Venta.ID_producto = Producto.ID")
        promedio = cursor.fetchone()[0]  # Obtener el resultado de la consulta
        return promedio if promedio is not None else 0  # Devolver 0 si no hay ventas

    def contar_ventas(self):
        """Método para contar la cantidad total de ventas."""
        cursor = obtener_cursor(self.conexion)
        cursor.execute("SELECT COUNT(*) FROM Venta")
        cantidad = cursor.fetchone()[0]  # Obtener el resultado de la consulta
        return cantidad if cantidad is not None else 0  # Devolver 0 si no hay ventas

    def obtener_producto_mas_vendido(self):
        """Método para obtener el producto más vendido."""
        cursor = obtener_cursor(self.conexion)
        cursor.execute("SELECT Producto.Nombre FROM Producto JOIN (SELECT ID_producto, SUM(Cantidad_producto_vendida) as total_vendido FROM Venta GROUP BY ID_producto ORDER BY total_vendido DESC LIMIT 1) as ventas ON Producto.ID = ventas.ID_producto")
        producto = cursor.fetchone()  # Obtener el resultado de la consulta
        return producto[0] if producto is not None else "No hay ventas registradas"  # Devolver un mensaje si no hay ventas
