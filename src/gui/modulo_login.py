import tkinter as tk 
from tkinter import messagebox
from conexion import obtener_cursor
import sqlite3

class LoginWindow(tk.Tk): 
    """Esta clase permite crear una ventana de inicio de sesión, incluyendo los widgets 
    asociados y los métodos necesarios para su funcionamiento."""
    
    def __init__(self, conexion_usuarios, conexion_inventario, main_window):
        """Inicializa la ventana de inicio de sesión con la conexión a la base de datos de usuarios,
        inventario y la ventana principal."""
        super().__init__()
        
        self.conexion_usuarios = conexion_usuarios
        self.conexion_inventario = conexion_inventario
        self.main_window = main_window
        self.contador = 0  # Inicializa un contador en 0 para controlar los intentos fallidos
        
        # Propiedades de la ventana de login
        self.title("INICIO DE SESIÓN")  # Establece el título de la ventana
        self.geometry("350x275")  # Establece las dimensiones de la ventana
        self.config(bg="#bcd4cc")  # Establece el color de fondo
        self.resizable(False, False)  # Impide el cambio de tamaño de la ventana
        
        self.crear_widgets()  # Crea los widgets de la ventana
    
    def crear_widgets(self):
        """Crea y posiciona los widgets en la ventana de inicio de sesión."""
        # Fuentes
        fuente = ('Monaco', '12', 'bold')
        fuente2 = ('Monaco', '10', 'bold')
        fuenteTitulo = ('Fixedsys', '16', 'bold')
        # Colores
        colorFrame = "#DBF0F1"  # Color de fondo de los contenedores (frames)
        colorLetra = "#041A17"  # Color de la letra
        colorBoton = "#8CD4C8"  # Color de los botones
        highlight = "#99CCFF"  # Color del highlight
        
        # Contenedor principal
        frame_login = tk.Frame(self, bg=colorFrame, width=330, height=250, borderwidth=3, relief="groove", highlightbackground=highlight)
        frame_login.place(x=10, y=10)  # Ubicación del frame 
        frame_login.pack_propagate(False)  # Impide que el contenedor se ajuste automáticamente a su contenido
        
        # Etiqueta del título
        label_titulo = tk.Label(frame_login, text="INICIAR SESIÓN", font=fuenteTitulo, bg=colorFrame, fg=colorLetra)
        label_titulo.place(x=10, y=10)
        
        # Labels de usuario y contraseña
        label_usuario = tk.Label(frame_login, text="Usuario:", font=fuente, bg=colorFrame)
        label_usuario.place(x=10, y=50)
        
        label_password = tk.Label(frame_login, text="Contraseña:", font=fuente, bg=colorFrame)
        label_password.place(x=10, y=90)
        
        # Widgets de entrada de usuario y contraseña
        self.entry_usuario = tk.Entry(frame_login, relief="groove", bd=4)
        self.entry_usuario.place(x=150, y=50, width=150)
        
        self.entry_password = tk.Entry(frame_login, show="•", relief="groove", bd=4)
        self.entry_password.place(x=150, y=90, width=150)
        
        # Botones LOGIN, REGISTER y PASSWORD RECOVERY
        boton_login = tk.Button(frame_login, text="Ok", command=self.verificar_credenciales, font=fuente, bg=colorBoton, fg=colorLetra, relief="groove", bd=4, cursor="hand2")
        boton_login.place(x=25, y=150, width=100)
        
        boton_register = tk.Button(frame_login, text="Registrar", command=self.abrir_autenticacion_register, font=fuente, bg=colorBoton, fg=colorLetra, relief="groove", bd=4, cursor="hand2")
        boton_register.place(x=145, y=150, width=155)
        
        boton_passwordRecovery = tk.Button(frame_login, text="Recuperar contraseña", command=self.abrir_autenticacion_password, font=fuente2, bg=colorFrame, fg=colorLetra, relief="flat", highlightthickness=0, cursor="hand2")
        boton_passwordRecovery.place(x=140, y=210, width=160)
             
    def verificar_credenciales(self):
        """Verifica las credenciales ingresadas y permite el acceso a la aplicación si son correctas."""
        usuario = self.entry_usuario.get()
        password = self.entry_password.get()
        
        if usuario != "" and password != "":
            cursor = obtener_cursor(self.conexion_usuarios)
            cursor.execute("SELECT Nombre FROM Usuarios WHERE Usuario=? AND password=?", (usuario, password))
            resultado = cursor.fetchone()
            
            if resultado:
                self.nombre_usuario = resultado[0]
                self.destroy()
                self.abrir_main_window()
            else:
                self.contador += 1
                if self.contador > 5:
                    messagebox.showerror("Error", "Demasiados intentos fallidos. El acceso está bloqueado.")
                    self.destroy()
                else:
                    messagebox.showerror("Error", "Usuario o contraseña incorrectos. Intentos restantes: {}".format(5 - self.contador))
        else:
            messagebox.showerror("Error", "Ingrese todos los datos.") 
    
    def abrir_main_window(self):
        """Abre la ventana principal de la aplicación."""
        main_window_app = self.main_window(self.conexion_inventario, self.conexion_usuarios, self.nombre_usuario) # Crea una instancia de la clase pasada como argumento
        main_window_app.mainloop() # Ejecuta el mainloop de la ventana principal
    
    def abrir_autenticacion_register(self):
        """Abre la ventana de autenticación para el registro de usuario."""
        AuthWindow(self.conexion_usuarios, self, "user_register")
        
    def abrir_autenticacion_password(self):
        """Abre la ventana de autenticación para la recuperación de contraseña."""
        AuthWindow(self.conexion_usuarios, self, "password_recovery")
        
        
class AuthWindow(tk.Toplevel):
    """Clase para la ventana de autenticación requerida."""
    
    def __init__(self, conexion_usuarios, parent, mode):
        """Inicializa la ventana de autenticación con la conexión a la base de datos de usuarios,
        la ventana principal y el modo (registro o recuperación de contraseña)."""
        super().__init__(parent)
        
        self.conexion_usuarios = conexion_usuarios
        self.parent = parent
        self.mode = mode
        self.contador = 0  # Inicializa un contador en 0 para controlar los intentos fallidos
        
        # Propiedades de la ventana de autenticación
        self.title("AUTENTICACIÓN REQUERIDA")
        self.geometry("350x225")
        self.config(bg="#bcd4cc")
        self.resizable(False, False)
        
        self.crear_widgets()  # Crea los widgets de la ventana
        
    def crear_widgets(self):
        """Crea y posiciona los widgets en la ventana de autenticación."""
        # Fuentes
        fuente = ('Monaco', '12', 'bold')
        fuente2 = ('Monaco', '10', 'bold')
        fuenteTitulo = ('Fixedsys', '16', 'bold')
        # Colores
        colorFrame = "#DBF0F1"
        colorLetra = "#041A17"
        colorBoton = "#8CD4C8"
        highlight = "#99CCFF"
        
        # Contenedor principal
        frame_auth = tk.Frame(self, bg=colorFrame, width=330, height=200, borderwidth=3, relief="groove", highlightbackground=highlight)
        frame_auth.place(x=10, y=10)
        frame_auth.pack_propagate(False)
        
        # Labels
        label_titulo = tk.Label(frame_auth, text="AUTENTICACIÓN", font=fuenteTitulo, bg=colorFrame)
        label_titulo.place(x=10, y=10)
        
        label_admin = tk.Label(frame_auth, text="Admin:", font=fuente, bg=colorFrame)
        label_admin.place(x=10, y=50)
        
        label_password = tk.Label(frame_auth, text="Contraseña:", font=fuente, bg=colorFrame)
        label_password.place(x=10, y=90)
        
        # Entradas
        self.entry_admin = tk.Entry(frame_auth, relief="groove", bd=4)
        self.entry_admin.place(x=160, y=50, width=150)
        
        self.entry_password = tk.Entry(frame_auth, show="•", relief="groove", bd=4)
        self.entry_password.place(x=160, y=90, width=150)
        
        # Botón de autenticación
        boton_autenticar = tk.Button(frame_auth, text="AUTENTICAR", command=self.verificar_credenciales, font=fuente, bg=colorBoton, fg=colorLetra, relief="groove", bd=4, cursor="hand2")
        boton_autenticar.place(x=85, y=140, width=160)
    
    def verificar_credenciales(self):
        """Verifica las credenciales de administrador y abre la ventana correspondiente."""
        admin = self.entry_admin.get()
        password = self.entry_password.get()
        admin_password = "321"
        admin_user = "admin"
        
        if admin != "" and password != "":
            if admin == admin_user and password == admin_password:
                self.destroy()  # Cierra la ventana si las credenciales son correctas
                if self.mode == "user_register":
                    RegisterWindow(self.conexion_usuarios)
                elif self.mode == "password_recovery":
                    PassRecovWindow(self.conexion_usuarios)
            else:
                self.contador += 1
                if self.contador > 5:
                    messagebox.showerror("Error", "Demasiados intentos fallidos. El acceso está bloqueado.")
                    self.destroy()
                else:
                    messagebox.showerror("Error", "Usuario o contraseña incorrectos. Intentos restantes: {}".format(5 - self.contador))
        else:
            messagebox.showerror("Error", "Ingrese todos los datos.")
            
class RegisterWindow(tk.Toplevel):
    """Clase para la ventana de registro de usuarios."""
    
    def __init__(self, conexion_usuarios):
        """Inicializa la ventana de registro con la conexión a la base de datos de usuarios."""
        super().__init__()
        self.conexion = conexion_usuarios
        
        self.title("VENTANA DE REGISTRO")
        self.geometry("360x310")
        self.resizable(False, False)
        self.config(bg="#bcd4cc")

        self.crear_widgets()  # Crea los widgets de la ventana
        
    def crear_widgets(self):
        """Crea y posiciona los widgets en la ventana de registro."""
        # Fuentes
        fuente = ('Monaco', '12', 'bold')
        fuente2 = ('Monaco', '10', 'bold')
        fuenteTitulo = ('Fixedsys', '16', 'bold')
        
        # Colores
        colorFrame = "#DBF0F1"
        colorLetra = "#041A17"
        colorBoton = "#8CD4C8"
        highlight = "#99CCFF"
        
        # Contenedor principal
        frame_register = tk.Frame(self, bg=colorFrame, width=340, height=290, borderwidth=3, relief="groove", highlightbackground=highlight)
        frame_register.place(x=10, y=10)
        frame_register.pack_propagate(False)
        
        # Labels
        label_titulo = tk.Label(frame_register, text="REGISTRO DE USUARIO", font=fuenteTitulo, bg=colorFrame)
        label_titulo.place(x=10, y=10)
        
        label_nombre = tk.Label(frame_register, text="Nombre:", font=fuente, bg=colorFrame)
        label_nombre.place(x=20, y=60)
        
        label_apellido = tk.Label(frame_register, text="Apellido:", font=fuente, bg=colorFrame)
        label_apellido.place(x=20, y=100)
        
        label_usuario = tk.Label(frame_register, text="Usuario:", font=fuente, bg=colorFrame)
        label_usuario.place(x=20, y=140)
        
        label_password = tk.Label(frame_register, text="Contraseña:", font=fuente, bg=colorFrame)
        label_password.place(x=20, y=180)
        
        # Entradas
        self.entry_nombre = tk.Entry(frame_register, relief="groove", bd=4)
        self.entry_nombre.place(x=160, y=60, width=150)
        
        self.entry_apellido = tk.Entry(frame_register, relief="groove", bd=4)
        self.entry_apellido.place(x=160, y=100, width=150)

        self.entry_usuario = tk.Entry(frame_register, relief="groove", bd=4)
        self.entry_usuario.place(x=160, y=140, width=150)
                
        self.entry_password = tk.Entry(frame_register, relief="groove", bd=4)
        self.entry_password.place(x=160, y=180, width=150)

        # Botón de registro
        boton_registrar = tk.Button(frame_register, text="Registrar", command=self.registrar_usuario, font=fuente, bg=colorBoton, fg=colorLetra, relief="groove", bd=4, cursor="hand2")
        boton_registrar.place(x=90, y=230, width=160)

    def registrar_usuario(self):
        """Registra un nuevo usuario en la base de datos."""
        nombre = self.entry_nombre.get()
        apellido = self.entry_apellido.get()
        usuario = self.entry_usuario.get()
        password = self.entry_password.get()
        
        if not (nombre and apellido and usuario and password):
            messagebox.showerror("ERROR", "Todos los campos son obligatorios.")
            return
        
        try:
            cursor = obtener_cursor(self.conexion)
            cursor.execute("INSERT INTO Usuarios (Nombre, Apellido, Usuario, password) VALUES (?, ?, ?, ?)",
                           (nombre, apellido, usuario, password))
            self.conexion.commit()
            messagebox.showinfo("Éxito", "Usuario registrado exitosamente.")
            self.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El nombre de usuario ya existe.")
                
class PassRecovWindow(tk.Toplevel):
    """Clase para la ventana de recuperación de contraseña."""
    
    def __init__(self, conexion_usuarios):
        """Inicializa la ventana de recuperación de contraseña con la conexión a la base de datos de usuarios."""
        super().__init__()
        self.conexion = conexion_usuarios
   
        self.title("Actualizar contraseña")
        self.geometry("415x225")
        self.config(bg="#bcd4cc")
        self.resizable(False, False)
        
        self.crear_widgets()  # Crea los widgets de la ventana
        
    def crear_widgets(self):
        """Crea y posiciona los widgets en la ventana de recuperación de contraseña."""
        # Fuentes
        fuente = ('Monaco', '12', 'bold')
        fuente2 = ('Monaco', '10', 'bold')
        fuenteTitulo = ('Fixedsys', '16', 'bold')
        # Colores
        colorFrame = "#DBF0F1"
        colorLetra = "#041A17"
        colorBoton = "#8CD4C8"
        highlight = "#99CCFF"
        
        # Contenedor principal
        frame_principal = tk.Frame(self, bg=colorFrame, width=390, height=200, borderwidth=3, relief="groove", highlightbackground=highlight)
        frame_principal.place(x=10, y=10)
        frame_principal.pack_propagate(False)
        
        # Labels
        label_titulo = tk.Label(frame_principal, text="Ingrese los datos", font=fuenteTitulo, bg=colorFrame)
        label_titulo.place(x=10, y=10)
        
        label_usuario = tk.Label(frame_principal, text="Ingrese su usuario:", font=fuente, bg=colorFrame)
        label_usuario.place(x=10, y=50)
        
        label_newPassword = tk.Label(frame_principal, text="Nueva contraseña:", font=fuente, bg=colorFrame)
        label_newPassword.place(x=10, y=90)
        
        # Entradas
        self.entry_usuario = tk.Entry(frame_principal, relief="groove", bd=4)
        self.entry_usuario.place(x=220, y=50, width=150)
        
        self.entry_new_password = tk.Entry(frame_principal, relief="groove", bd=4)
        self.entry_new_password.place(x=220, y=90, width=150)
        
        # Botón de actualización
        boton_actualizar = tk.Button(frame_principal, text="ACTUALIZAR", command=self.update_password, font=fuente, bg=colorBoton, fg=colorLetra, relief="groove", bd=4, cursor="hand2")
        boton_actualizar.place(x=115, y=140, width=160)
        
    def update_password(self):
        """Actualiza la contraseña del usuario especificado."""
        usuario = self.entry_usuario.get()
        nueva_contra = self.entry_new_password.get()

        if not usuario or not nueva_contra:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return

        try:
            cursor = obtener_cursor(self.conexion)
            cursor.execute("SELECT COUNT(*) FROM Usuarios WHERE Usuario = ?", (usuario,))
            usuario_existente = cursor.fetchone()[0]

            if usuario_existente == 0:
                messagebox.showerror("Error", "El usuario especificado no existe.")
                return
            
            # Actualizar la contraseña en la base de datos
            cursor.execute("UPDATE Usuarios SET password = ? WHERE Usuario = ?", (nueva_contra, usuario))
            self.conexion.commit()
            messagebox.showinfo("Éxito", "Contraseña actualizada correctamente.")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar la contraseña: {str(e)}")
