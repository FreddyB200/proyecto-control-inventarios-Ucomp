import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
from conexion import obtener_cursor

class GraficosWindow:
    def __init__(self, conexion):
        self.conexion = conexion  # Conexión a la base de datos
        self.ventana = tk.Tk()  # Crear una nueva ventana de Tkinter
        self.ventana.title("Dashboard graficos estadisticos")  # Establecer el título de la ventana
        self.ventana.geometry("800x600")  # Establecer el tamaño de la ventana
        self.ventana.resizable(False, False)  # No permitir el redimensionamiento de la ventana

        self.crear_dashboard()  # Llamar al método para crear el dashboard

    def crear_dashboard(self):
        """Crear el dashboard con dos frames: uno para las ventas y otro para los ingresos."""
        # Frame para el gráfico de ventas
        frame_ventas = tk.Frame(self.ventana)
        frame_ventas.place(x=20, y=20, width=760, height=260)  # Posicionar el frame en la ventana
        self.grafico_ventas(frame_ventas)  # Llamar al método para crear el gráfico de ventas

        # Frame para el gráfico de ganancias
        frame_ingresos = tk.Frame(self.ventana)
        frame_ingresos.place(x=20, y=300, width=760, height=260)  # Posicionar el frame en la ventana
        self.grafico_ingresos(frame_ingresos)  # Llamar al método para crear el gráfico de los ingresos

    def grafico_ventas(self, frame):
        """Crear un gráfico de barras que muestra las ventas diarias de productos."""
        cursor = obtener_cursor(self.conexion)  # Obtener un cursor para ejecutar consultas SQL
        fecha_inicio = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)  # Fecha de inicio del día actual
        fecha_fin = fecha_inicio + timedelta(days=1)  # Fecha de fin (día siguiente)

        # Consultar la base de datos para obtener la cantidad vendida de cada producto en el día actual
        cursor.execute(
            "SELECT Producto.Nombre, SUM(Venta.Cantidad_producto_vendida) "
            "FROM Venta JOIN Producto ON Venta.ID_producto = Producto.ID "
            "WHERE Venta.Fecha_hora_venta BETWEEN ? AND ? "
            "GROUP BY Producto.Nombre", (fecha_inicio, fecha_fin)
        )

        datos = cursor.fetchall()  # Obtener los resultados de la consulta

        productos = []  # Lista para los nombres de los productos
        cantidad = []  # Lista para la cantidad vendida de cada producto

        for dato in datos:
            productos.append(dato[0])  # Agregar el nombre del producto a la lista
            cantidad.append(dato[1])  # Agregar la cantidad vendida a la lista

        # Crear una figura de Matplotlib para el gráfico de barras
        fig = Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)  # Añadir un subplot a la figura
        ax.bar(productos, cantidad, color='skyblue')  # Crear el gráfico de barras
        ax.set_xlabel('Producto')  # Establecer la etiqueta del eje x
        ax.set_ylabel('Cantidad Vendida')  # Establecer la etiqueta del eje y
        ax.set_title('Productos más vendidos en el día')  # Establecer el título del gráfico

        # Crear un canvas de Tkinter para mostrar la figura de Matplotlib
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()  # Dibujar el gráfico
        canvas.get_tk_widget().pack()  # Empaquetar el canvas en el frame

    def grafico_ingresos(self, frame):
        """Crear un gráfico de barras que muestra los ingresos totales por producto."""
        cursor = obtener_cursor(self.conexion)  # Obtener un cursor para ejecutar consultas SQL

        # Consultar la base de datos para obtener las ganancias totales por producto
        cursor.execute(
            "SELECT Producto.Nombre, SUM(Venta.Cantidad_producto_vendida * Producto.Precio) "
            "FROM Venta JOIN Producto ON Venta.ID_producto = Producto.ID "
            "GROUP BY Producto.Nombre "
            "ORDER BY SUM(Venta.Cantidad_producto_vendida * Producto.Precio) DESC "
            "LIMIT 5"
        )

        datos = cursor.fetchall()  # Obtener los resultados de la consulta

        productos = []  # Lista para los nombres de los productos
        ingresos = []  # Lista para las ganancias de cada producto

        for dato in datos:
            productos.append(dato[0])  # Agregar el nombre del producto a la lista
            ingresos.append(dato[1])  # Agregar las ganancias del producto a la lista

        # Crear una figura de Matplotlib para el gráfico de barras
        fig = Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)  # Añadir un subplot a la figura
        ax.bar(productos, ingresos, color='salmon')  # Crear el gráfico de barras
        ax.set_xlabel('Producto')  # Establecer la etiqueta del eje x
        ax.set_ylabel('Ingresos')  # Establecer la etiqueta del eje y
        ax.set_title('Productos con más ingresos totales')  # Establecer el título del gráfico

        # Crear un canvas de Tkinter para mostrar la figura de Matplotlib
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()  # Dibujar el gráfico
        canvas.get_tk_widget().pack()  # Empaquetar el canvas en el frame
