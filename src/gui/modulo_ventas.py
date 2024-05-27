import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
from conexion import obtener_cursor

class VentasWindow(tk.Toplevel):
    def __init__(self, conexion):
        """Inicializa la ventana de ventas, estableciendo la conexión a la base de datos."""
        super().__init__()
        self.conexion = conexion
        self.title("Registrar Venta")
        self.geometry("1130x280")
        
        colorWind = "#bcd4cc"
        self.configure(bg=colorWind)
        self.resizable(False, False)
        
        self.crear_widgets()
        
    def crear_widgets(self):
        """Crea y posiciona los widgets en la ventana de ventas."""
        fuente = ('Monaco', '12', 'bold')
        fuente2 = ('Monaco', '10', 'bold')
        fuenteTitulo = ('Fixedsys', '16', 'bold')
        
        # Colores
        colorFrame = "#DBF0F1"
        colorLetra = "#041A17"
        colorBoton = "#8CD4C8"
        highlight = "#99CCFF"
        
        # Contenedor para el formulario de venta
        frame_venta = tk.LabelFrame(self, text="Formulario de venta", font=fuente2, bg=colorFrame, width=400, height=240, borderwidth=5, relief="groove", highlightbackground=highlight)
        frame_venta.place(x=25, y=18)
        frame_venta.pack_propagate(False)
        
        # Etiqueta y combobox para seleccionar producto
        label_producto = tk.Label(frame_venta, text="Producto:", font=fuente, bg=colorFrame)
        label_producto.place(x=10, y=10)
        
        self.combobox_producto = ttk.Combobox(frame_venta, state="readonly")
        self.combobox_producto.place(x=200, y=10, width=160)
        self.cargar_productos()
        self.combobox_producto.bind("<<ComboboxSelected>>", self.actualizar_precio_unitario)

        # Etiqueta y entrada para el precio unitario
        label_precio_unitario = tk.Label(frame_venta, text="Precio Unitario:", font=fuente, bg=colorFrame)
        label_precio_unitario.place(x=10, y=60)
        self.entry_precio_unitario = tk.Entry(frame_venta, relief="groove", bd=4)
        self.entry_precio_unitario.place(x=200, y=60, width=160)

        # Etiqueta y entrada para la cantidad
        label_cantidad = tk.Label(frame_venta, text="Cantidad:", font=fuente, bg=colorFrame)
        label_cantidad.place(x=10, y=110)
        self.entry_cantidad = tk.Entry(frame_venta, relief="groove", bd=4)
        self.entry_cantidad.place(x=200, y=110, width=160)
        
        # Botón para registrar la venta
        boton_vender = tk.Button(frame_venta, text="Vender", command=self.registrar_venta, font=fuente, bg=colorBoton, fg=colorLetra, relief="groove", bd=4, cursor="hand2")
        boton_vender.place(x=30, y=160, width=100)
        
        # Botón para cargar el historial de ventas
        boton_historial = tk.Button(frame_venta, text="Cargar historial", command=self.cargar_datos_treeview, font=fuente, bg=colorBoton, fg=colorLetra, relief="groove", bd=4, cursor="hand2")
        boton_historial.place(x=180, y=160, width=180)
        
        # TreeView para mostrar el historial de ventas
        self.treeview_historial_ventas = ttk.Treeview(self)
        self.treeview_historial_ventas["columns"] = ("ID", "Producto", "Cantidad", "Precio Total", "Fecha y Hora")
        self.treeview_historial_ventas.heading("#0", text="")
        self.treeview_historial_ventas.heading("ID", text="ID de la Venta")
        self.treeview_historial_ventas.heading("Producto", text="Producto")
        self.treeview_historial_ventas.heading("Cantidad", text="Cantidad")
        self.treeview_historial_ventas.heading("Precio Total", text="Precio Total")
        self.treeview_historial_ventas.heading("Fecha y Hora", text="Fecha y Hora")
        self.treeview_historial_ventas.place(x=460, y=18, width=630, height=240)
        self.treeview_historial_ventas.column("#0", width=0)
        self.treeview_historial_ventas.column("ID", width=110)
        self.treeview_historial_ventas.column("Producto", width=130)
        self.treeview_historial_ventas.column("Cantidad", width=100)
        self.treeview_historial_ventas.column("Precio Total", width=130)
        self.treeview_historial_ventas.column("Fecha y hora", width=130)
        
    def cargar_datos_treeview(self):
        """Carga el historial de ventas desde la base de datos y lo muestra en el TreeView."""
        cursor = obtener_cursor(self.conexion)
        cursor.execute("SELECT Venta.ID_venta, Producto.Nombre, Venta.Cantidad_producto_vendida, Venta.Precio_total, Venta.Fecha_hora_venta FROM Venta INNER JOIN Producto ON Venta.ID_producto = Producto.ID")
        
        # Limpiar el TreeView antes de cargar nuevos datos
        self.treeview_historial_ventas.delete(*self.treeview_historial_ventas.get_children())
        
        ventas = cursor.fetchall()

        # Mostrar las ventas en el TreeView
        for venta in ventas:
            self.treeview_historial_ventas.insert("", tk.END, values=venta)
        
    def cargar_productos(self):
        """Carga los productos desde la base de datos y los agrega al combobox."""
        cursor = obtener_cursor(self.conexion)
        cursor.execute("SELECT Nombre, Precio FROM Producto")
        productos = cursor.fetchall()
        lista_productos = [producto[0] for producto in productos]
        self.precios_productos = {producto[0]: producto[1] for producto in productos}
        self.combobox_producto['values'] = lista_productos
         
    def actualizar_precio_unitario(self, event):
        """Actualiza el precio unitario en la entrada correspondiente al seleccionar un producto."""
        producto_seleccionado = self.combobox_producto.get()
        precio_unitario = self.precios_productos.get(producto_seleccionado)
        if precio_unitario is not None:
            self.entry_precio_unitario.delete(0, tk.END)
            self.entry_precio_unitario.insert(0, precio_unitario)

    def registrar_venta(self):
        """Registra una venta en la base de datos y actualiza el historial de ventas."""
        nombre_producto = self.combobox_producto.get()
        cantidad = int(self.entry_cantidad.get())
        precio_unitario = float(self.entry_precio_unitario.get())
        precio_total = float(cantidad * precio_unitario)
        fecha_hora_venta = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor = obtener_cursor(self.conexion)
        cursor.execute("SELECT ID, Cantidad_en_stock FROM Producto WHERE Nombre = ?", (nombre_producto,))
        producto = cursor.fetchone()

        if producto:
            producto_id, cantidad_en_stock = producto
            if cantidad_en_stock >= cantidad:  # Verificar si hay suficiente stock
                nueva_cantidad = cantidad_en_stock - cantidad
                cursor.execute("UPDATE Producto SET Cantidad_en_stock = ? WHERE ID = ?", (nueva_cantidad, producto_id))
                cursor.execute("INSERT INTO Venta (ID_producto, Cantidad_producto_vendida, Precio_total, Fecha_hora_venta) VALUES (?, ?, ?, ?)", (producto_id, cantidad, precio_total, fecha_hora_venta))
                self.conexion.commit()

                messagebox.showinfo("Venta registrada", f"Se ha registrado la venta de {cantidad} unidades de {nombre_producto} por un total de ${precio_total} el {fecha_hora_venta}.")
                self.cargar_datos_treeview()
            else:
                messagebox.showerror("Error", f"No hay suficiente stock para la venta de {cantidad} unidades de {nombre_producto}.")
        else:
            messagebox.showerror("Error", "Producto no encontrado.")
