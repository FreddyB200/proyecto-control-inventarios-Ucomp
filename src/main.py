import tkinter as tk  # Importa el módulo tkinter para crear interfaces gráficas
from conexion import conectar_base_datos  # Importa la función para conectar con la base de datos
from gui.modulo_login import LoginWindow  # Importa la clase LoginWindow desde el módulo correspondiente
from gui.modulo_main_window import MainWindow  # Importa la clase MainWindow desde el módulo correspondiente

def main():
    """Función principal para iniciar la aplicación."""

    # Conecta a la base de datos de usuarios
    conexion_usuarios = conectar_base_datos("src/usuarios.db")
    
    # Conecta a la base de datos de inventario
    conexion_inventario = conectar_base_datos("src/inventario.db")
    
    # Crea una instancia de la ventana de login, pasando las conexiones de las bases de datos
    # y la clase MainWindow como argumentos
    login_app = LoginWindow(conexion_usuarios, conexion_inventario, MainWindow)
    
    # Inicia el bucle principal de la aplicación de tkinter
    login_app.mainloop()

# Si el script se está ejecutando directamente (no importado como módulo), llama a la función main
if __name__ == "__main__":
    main()
