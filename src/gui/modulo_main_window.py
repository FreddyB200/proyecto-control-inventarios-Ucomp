import tkinter as tk
from datetime import datetime, timedelta
from conexion import obtener_cursor
from .modulo_inventario import InventarioWindow
from .modulo_ventas import VentasWindow
from .modulo_informes import InformeWindow
from .modulo_graficos import GraficosWindow

class MainWindow(tk.Toplevel):
    def __init__(self, conexion_inventario, conexion_usuarios, nombre_usuario):
        super().__init__()
        self.conexion = conexion_inventario
        self.title("Control de inventario") # Título de la ventana
        self.geometry("620x400") #Dimensiones de la ventana
        self.resizable(False, False)   # Impidiendo que se agrande la ventana hacia abajo
        self.conexion_usuarios = conexion_usuarios
        self.nombre_usuario = nombre_usuario
        
        try:    
            self.iconbitmap("inventario_icono.ico")
        except Exception as e:
            print("Icono no encontrado, continuando sin icono.")
        self.config(bg="#bcd4cc")
        
        self.crear_widgets()
        
    def crear_widgets(self):
        #fuentes
        fuente = ('consola', '12', 'bold')
        fuente3 = ('consola', '16', 'bold')
        fuente2 = ('Monaco', '10', 'bold')
        fuenteTitulo = ('Fixedsys', '18', 'bold')
        #colores
        colorWind = "#bcd4cc"
        colorFrame = "#DBF0F1"
        colorLetra = "#041A17"
        colorBoton = "#8CD4C8"
        highlight = "#99CCFF"
        
        """contenedores"""
        #Contenedor superior
        frame_titulos = tk.Frame(self, bg=colorWind, width=800, height=80)
        frame_titulos.place(x=0,  y=0) 
        frame_titulos.pack_propagate(False) #esto hace que el marco superior mantega sus dimensiones fijas sin ajustarse a su contenido 
        #contenedor del menu
        frame_menu = tk.LabelFrame(self, text="Menu", font=fuente2, bg=colorFrame, width=300, height=300, borderwidth=4, relief="groove", highlightbackground=highlight)
        frame_menu.place(x=20, y=80)
        frame_menu.pack_propagate(False)
        #Contenedor de las otras opciones
        frame_alertas = tk.LabelFrame(self, text="Alertas", font=fuente2, bg=colorFrame, width=240, height=300, borderwidth=4, relief="groove", highlightbackground=highlight)
        frame_alertas.place(x=360, y=80)
        frame_alertas.pack_propagate(False)  
        
        """labels"""
        #Label del titulo
        label_titulo_menu = tk.Label(frame_titulos, text=f"Hola de nuevo, {self.nombre_usuario}!", bg=colorWind, fg=colorLetra, font=fuenteTitulo)
        label_titulo_menu.place(x=120, y=10)
        #label del subtitulo
        label_subtitulo_menu = tk.Label(frame_titulos, text="Es hora de organizar tu inventario.", bg=colorWind, fg=colorLetra, font=fuente3)
        label_subtitulo_menu.place(x=120, y=40)

        # Obtener productos con poco stock
        productos_poco_stock = self.obtener_productos_poco_stock()

        # Etiqueta para productos con poco stock
        if productos_poco_stock:
            label_poco_stock = tk.Label(frame_alertas, text="Productos con poco stock:", font=fuente, bg=colorFrame, fg=colorLetra)
            label_poco_stock.pack()

            for producto in productos_poco_stock:
                label_producto_poco_stock = tk.Label(frame_alertas, text=producto, font=fuente, bg=colorFrame, fg=colorLetra)
                label_producto_poco_stock.pack()

        # Obtener productos próximos a vencer
        productos_proximos_vencer = self.obtener_productos_proximos_vencer()
        

        # Etiqueta para productos próximos a vencer
        if productos_proximos_vencer:
            label_proximos_vencer = tk.Label(frame_alertas, text="Productos próximos a vencer:", font=fuente, bg=colorFrame, fg=colorLetra)
            label_proximos_vencer.pack()
        
            for producto, precio in productos_proximos_vencer.items():
                precio_con_descuento = precio * 0.8  # Aplicar descuento del 20%
                label_producto_proximo_vencer = tk.Label(frame_alertas, text=f"{producto}: ${precio_con_descuento:.2f}", font=fuente, bg=colorFrame, fg=colorLetra)
                label_producto_proximo_vencer.pack()

        # Si no hay alertas
        if not productos_poco_stock and not productos_proximos_vencer:
            label_no_alertas = tk.Label(frame_alertas, text="No hay alertas por el momento", font=fuente, bg=colorFrame, fg=colorLetra)
            label_no_alertas.pack()
            
        #Buttons
        opciones_menu = ["Inventario", "Vender", "Gráficos", "Reportes"]
        comandos_menu = [self.abrir_inventario, self.abrir_ventas, self.mostrar_graficos, self.mostrar_informes]
        botones_menu = []

        for opcion, comando in zip(opciones_menu, comandos_menu):
            boton = tk.Button(frame_menu, text=opcion, fg=colorLetra, bg=colorBoton, relief="groove", bd=5, command=comando, font=fuente, width=20, height=2, cursor="hand2")
            boton.pack(anchor="w", pady=5, padx=25)
            botones_menu.append(boton)
            
    def obtener_productos_poco_stock(self):
        cursor = obtener_cursor(self.conexion)
        cursor.execute("SELECT Nombre FROM Producto WHERE Cantidad_en_stock < 10")
        productos_poco_stock = cursor.fetchall()
        return [producto[0] for producto in productos_poco_stock]

    
    def obtener_productos_proximos_vencer(self):
        hoy = datetime.now().date()
        una_semana_despues = hoy + timedelta(days=7)

        cursor = obtener_cursor(self.conexion)
        cursor.execute("SELECT Nombre, Precio FROM Producto WHERE Fecha_vencimiento BETWEEN ? AND ?", (hoy, una_semana_despues))
        productos_proximos_vencer = cursor.fetchall()
        
        for producto in productos_proximos_vencer:
            precio_original = producto[1]
            producto_nombre = producto[0]
            precio_descuento = precio_original * 0.8
            cursor.execute("UPDATE Producto SET Precio = ? WHERE Nombre = ?", (precio_descuento, producto_nombre))
            self.conexion.commit() 
        return {producto[0]: producto[1] for producto in productos_proximos_vencer}
    
    
    """abrir ventanas"""
    
    def abrir_inventario(self):
        InventarioWindow(self.conexion)
    
    def abrir_ventas(self):
        VentasWindow(self.conexion)
        
    def mostrar_graficos(self):
        GraficosWindow(self.conexion)
 
    def mostrar_informes(self):
        InformeWindow(self.conexion)
    