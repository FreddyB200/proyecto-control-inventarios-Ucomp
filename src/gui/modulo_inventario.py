import tkinter as tk  
from tkinter import messagebox  # Importa messagebox para mostrar cuadros de mensaje
from tkinter import ttk  # Importa ttk para usar el Treeview y otros widgets mejorados
from tkinter.ttk import Combobox  # Importa Combobox para usar en los formularios
from datetime import datetime  # Importa datetime para manejar fechas
from conexion import obtener_cursor 

class InventarioWindow(tk.Toplevel):
    """Clase para crear la ventana de inventario, hereda de Toplevel para crear una ventana secundaria."""
    
    def __init__(self, conexion):
        """Inicializa la ventana de inventario con la conexión a la base de datos."""
        super().__init__()
        self.conexion = conexion
        self.title("PRODUCTOS")
        self.geometry("1350x320")
        self.resizable(0, 0)
        self.configure(bg="#64a49c")
        self.crear_widgets()  # Crea los widgets de la ventana
        self.configurar_treeview()  # Configura el treeview
        self.cargar_productos_en_treeview()  # Carga los productos en el treeview
        
        # Enlazar evento de selección del Treeview
        self.treeview.bind("<<TreeviewSelect>>", self.mostrar_producto_seleccionado)

    def crear_widgets(self):
        """Crea y posiciona los widgets en la ventana."""
        # Fuentes
        fuente = ('Monaco', '12', 'bold')
        fuente2 = ('Monaco', '10', 'bold')
        fuenteTitulo = ('Fixedsys', '16', 'bold')
        # Colores
        colorFrame = "#DBF0F1"
        colorLetra = "#041A17"
        colorBoton = "#8CD4C8"
        highlight = "#99CCFF"
        colorWind = "#64a49c"

        # Contenedor para los datos del producto
        frame_datos_producto = tk.LabelFrame(self, text="Datos del producto", font=fuente2, bg=colorFrame, width=435, height=282, borderwidth=4, relief="groove", highlightbackground=highlight)
        frame_datos_producto.place(x=25, y=18)
        frame_datos_producto.pack_propagate(False)
        
        # Contenedor para los botones de búsqueda, filtrado, etc.
        frame_otras_opciones = tk.Frame(self, bg=colorFrame, width=200, height=282, borderwidth=4, relief="groove", highlightbackground=highlight)
        frame_otras_opciones.place(x=1130, y=18)
        frame_otras_opciones.pack_propagate(False)
        
        campos = ["Nombre del producto:", "Precio:", "Fecha de vencimiento:", "Cantidad:", "Nombre del proveedor:"]
        self.entries = []
        
        # Crea labels y entradas para los campos del producto
        for i, campo in enumerate(campos):
            label = tk.Label(frame_datos_producto, text=campo, font=fuente, bg=colorFrame)
            label.place(x=10, y=10 + i*40)
            
            if campo == "Nombre del proveedor:":
                entry = Combobox(frame_datos_producto, state="readonly")
                entry.place(x=240, y=10 + i*40, width=160, height=22)
                self.cargar_nombres_proveedores(entry)  # Carga nombres de proveedores en el combobox
            else:
                entry = tk.Entry(frame_datos_producto, relief="groove", bd=4)
                entry.place(x=240, y=10 + i*40, width=160, height=22)
                if campo == "Fecha de vencimiento:":
                    entry.insert(0, "AAAA-MM-DD")
            
            self.entries.append(entry)

        # Botón para agregar un producto
        boton_agregar = tk.Button(frame_datos_producto, text="AGREGAR", command=self.agregar_producto, font=fuente, bg=colorBoton, fg=colorLetra, relief="groove", bd=4, cursor="hand2")
        boton_agregar.place(x=10, y=210, width=120, height=36)
       
        # Botón para actualizar un producto
        boton_actualizar = tk.Button(frame_datos_producto, text="Modificar", command=self.actualizar_producto, font=fuente, bg=colorBoton, fg=colorLetra, relief="groove", bd=4, cursor="hand2")
        boton_actualizar.place(x=150, y=210, width=120, height=36)
       
        # Botón para eliminar un producto
        boton_eliminar = tk.Button(frame_datos_producto, text="ELIMINAR", command=self.eliminar_producto, font=fuente, bg=colorBoton, fg=colorLetra, relief="groove", bd=4, cursor="hand2")
        boton_eliminar.place(x=290, y=210, width=120, height=36)
        
        # Botón para recargar el inventario
        boton_recargar = tk.Button(frame_otras_opciones, text="Recargar inventario", command=self.cargar_productos_en_treeview, font=fuente2, bg=colorBoton, fg=colorLetra, relief="groove", bd=4, cursor="hand2")
        boton_recargar.place(x=15, y=15, width=160, height=30)
        
        # Label para búsqueda de productos
        label_buscar = tk.Label(frame_otras_opciones, text="Buscar productos", font=fuente, bg=colorFrame)
        label_buscar.place(x=15,y=60)
        
        # Entry para búsqueda de productos
        self.entry_buscar = tk.Entry(frame_otras_opciones, font=fuente2, relief="groove", bd=4)
        self.entry_buscar.place(x=15, y=90, width=160, height=30)
        self.entry_buscar.bind('<KeyRelease>', self.buscar_producto)  # Enlaza la búsqueda con la entrada

        # Treeview para mostrar los productos
        self.treeview = ttk.Treeview(self, columns=("ID", "Nombre", "Precio", "Fecha de Vencimiento", "Cantidad"), show='headings')
        self.treeview.place(x=490, y=18, width=620, height=282)

    def configurar_treeview(self):
        """Configura las columnas del Treeview."""
        self.treeview.heading("ID", text="ID")
        self.treeview.heading("Nombre", text="Nombre")
        self.treeview.heading("Precio", text="Precio")
        self.treeview.heading("Fecha de Vencimiento", text="Fecha de Vencimiento")
        self.treeview.heading("Cantidad", text="Cantidad")

        self.treeview.column("ID", width=70)
        self.treeview.column("Nombre", width=180)
        self.treeview.column("Precio", width=110)
        self.treeview.column("Fecha de Vencimiento", width=130)
        self.treeview.column("Cantidad", width=130)

    def cargar_productos_en_treeview(self):
        """Carga los productos en el Treeview desde la base de datos."""
        cursor = obtener_cursor(self.conexion)
        cursor.execute('''SELECT ID, Nombre, Precio, Fecha_vencimiento, cantidad_en_stock FROM Producto''')

        self.treeview.delete(*self.treeview.get_children())  # Borra los datos actuales en el Treeview

        datos_productos = cursor.fetchall()  # Obtiene todos los productos

        for producto in datos_productos:
            self.treeview.insert("", "end", values=producto)  # Inserta cada producto en el Treeview
            
    def buscar_producto(self, event):
        """Busca productos en la base de datos y los muestra en el Treeview."""
        busqueda = self.entry_buscar.get()
        cursor = obtener_cursor(self.conexion)
        cursor.execute('''SELECT ID, Nombre, Precio, Fecha_vencimiento, cantidad_en_stock FROM Producto WHERE Nombre LIKE ?''', ('%' + busqueda + '%',))

        self.treeview.delete(*self.treeview.get_children())  # Borra los datos actuales en el Treeview

        datos_productos = cursor.fetchall()  # Obtiene los productos que coinciden con la búsqueda

        for producto in datos_productos:
            self.treeview.insert("", "end", values=producto)  # Inserta cada producto en el Treeview

    def cargar_nombres_proveedores(self, combobox):
        """Carga los nombres de proveedores en el combobox."""
        cursor = obtener_cursor(self.conexion)
        cursor.execute("SELECT razon_social, NIT FROM Proveedor")
        proveedores = cursor.fetchall()
        nombres_proveedores = [row[0] for row in proveedores]
        self.proveedores_nit = {nombre: nit for nombre, nit in proveedores}
        combobox['values'] = nombres_proveedores

    def agregar_producto(self):
        """Agrega un nuevo producto a la base de datos."""
        nombre = self.entries[0].get()
        precio = self.entries[1].get()
        fecha_vencimiento = self.entries[2].get()
        cantidad = self.entries[3].get()
        nombre_proveedor = self.entries[4].get()

        try:
            precio = float(precio)
            cantidad = int(cantidad)
            fecha_vencimiento = datetime.strptime(fecha_vencimiento, '%Y-%m-%d').date()
            nit_proveedor = self.proveedores_nit.get(nombre_proveedor)
            
            if nit_proveedor is None:
                raise ValueError("No se ha seleccionado un proveedor válido")

            cursor = obtener_cursor(self.conexion)
            cursor.execute('''INSERT INTO Producto (Nombre, Precio, Fecha_vencimiento, Cantidad_en_stock, NIT_proveedor)
                              VALUES (?, ?, ?, ?, ?)''',
                           (nombre, precio, fecha_vencimiento, cantidad, nit_proveedor))
            self.conexion.commit()
            
            messagebox.showinfo("Éxito", "Producto agregado correctamente")
            self.cargar_productos_en_treeview()  # Recarga los productos en el Treeview
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar producto: {e}")

        for entry in self.entries:
            entry.delete(0, tk.END)  # Limpia las entradas

    def actualizar_producto(self):
        """Abre una ventana para actualizar el producto seleccionado."""
        seleccion = self.treeview.focus()
        if seleccion:
            datos_producto = self.treeview.item(seleccion, "values")
            self.update_window = UpdateProductWindow(self.conexion, datos_producto)
        else:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un producto para actualizar")

    def eliminar_producto(self):
        """Elimina el producto seleccionado de la base de datos."""
        seleccion = self.treeview.focus()
        if seleccion:
            producto_id = self.treeview.item(seleccion, "values")[0]
            confirmacion = messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este producto?")
            if confirmacion:
                try:
                    cursor = self.conexion.cursor()
                    cursor.execute("DELETE FROM Producto WHERE ID = ?", (producto_id,))
                    self.conexion.commit()
                    messagebox.showinfo("Éxito", "Producto eliminado correctamente")
                    self.cargar_productos_en_treeview()  # Recarga los productos en el Treeview
                except Exception as e:
                    messagebox.showerror("Error", f"Error al eliminar producto: {e}")
        else:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un producto para eliminar")
    
    def mostrar_producto_seleccionado(self, event):
        """Muestra los datos del producto seleccionado en los campos de entrada."""
        seleccion = self.treeview.focus()
        if seleccion:
            datos_producto = self.treeview.item(seleccion, "values")
            for entry, value in zip(self.entries, datos_producto[1:]):
                entry.delete(0, tk.END)
                entry.insert(0, value)


class UpdateProductWindow(tk.Toplevel):
    """Clase para la ventana de actualización de producto."""
    def __init__(self, conexion, producto):
        """Inicializa la ventana de actualización con la conexión a la base de datos y los datos del producto."""
        super().__init__()
        
        self.conexion = conexion
        self.producto = producto
        self.title("ACTUALIZAR PRODUCTO")
        self.geometry("420x320")
        self.resizable(0, 0)
        self.configure(bg="#bcd4cc")
        
        self.crear_widgets()  # Crea los widgets de la ventana    
        
    def crear_widgets(self):
        """Crea y posiciona los widgets en la ventana."""
        # Fuentes
        fuente = ('Monaco', '12', 'bold')
        fuente2 = ('Monaco', '10', 'bold')
        fuenteTitulo = ('Fixedsys', '16', 'bold')
        # Colores
        colorFrame = "#DBF0F1"
        colorLetra = "#041A17"
        colorBoton = "#8CD4C8"
        highlight = "#99CCFF"
        colorWind = "#bcd4cc"
        
        frame_actualizar_producto = tk.Frame(self, bg=colorFrame, width=380, height=280, borderwidth=5, relief="groove", highlightbackground=highlight)
        frame_actualizar_producto.place(x=20, y=20)
        frame_actualizar_producto.pack_propagate(False)
        
        campos = ["ID del producto:", "Nuevo nombre:", "Nuevo precio:", "Nueva fecha:", "Nueva cantidad:"]
        self.entries = []
        
        # Crea labels y entradas para los campos de actualización del producto
        for i, campo in enumerate(campos):
            label = tk.Label(frame_actualizar_producto, text=campo, font=fuente, bg=colorFrame)
            label.place(x=10, y=10 + i*40)
            
            entry = tk.Entry(frame_actualizar_producto, relief="groove", bd=4)
            entry.place(x=230, y=10 + i*40, width=120, height=25)
            self.entries.append(entry)
            
        # Botón para actualizar el producto
        self.boton_actualizar = tk.Button(frame_actualizar_producto, text="ACTUALIZAR", command=self.actualizar_producto, font=fuente, bg=colorBoton, fg=colorLetra, relief="groove", bd=5, cursor="hand2")
        self.boton_actualizar.place(x=115, y=220, width=140, height=36)
        
        self.llenar_campos_producto()  # Llena los campos de entrada con los datos del producto
        
    def llenar_campos_producto(self):
        """Llena los campos de entrada con los datos del producto."""
        for i, entry in enumerate(self.entries):
            entry.delete(0, tk.END)
            entry.insert(0, self.producto[i])
        
    def actualizar_producto(self):
        """Actualiza el producto en la base de datos con los nuevos valores."""
        id = self.entries[0].get()
        nuevo_nombre = self.entries[1].get()
        nuevo_precio = self.entries[2].get()
        nueva_fecha_vencimiento = self.entries[3].get()
        nueva_cantidad = self.entries[4].get()
        
        try:
            id = int(id)
            nuevo_precio = float(nuevo_precio)
            nueva_fecha_vencimiento = datetime.strptime(nueva_fecha_vencimiento, '%Y-%m-%d').date()
            nueva_cantidad = int(nueva_cantidad)
            
            cursor = self.conexion.cursor()
            cursor.execute('''UPDATE Producto
                              SET Nombre = ?,
                                  Precio = ?,
                                  Fecha_vencimiento = ?,
                                  Cantidad_en_stock = ?  
                              WHERE ID = ?''',
                           (nuevo_nombre, nuevo_precio, nueva_fecha_vencimiento, nueva_cantidad, id))  
            self.conexion.commit()
            
            messagebox.showinfo("Éxito", "Producto actualizado correctamente")
            self.destroy()  # Cierra la ventana de actualización
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar producto: {e}")  # Muestra un mensaje de error
