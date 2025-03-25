"""
Script para inicializar la base de datos con las tablas necesarias.
"""

import sqlite3
import os
from src.utils.security import hash_password

def init_database():
    """Inicializa la base de datos con las tablas necesarias."""
    # Asegurarse de que el directorio src existe
    if not os.path.exists('src'):
        os.makedirs('src')
    
    # Eliminar la base de datos si existe
    if os.path.exists('src/inventario.db'):
        os.remove('src/inventario.db')
    
    # Conectar a la base de datos
    conn = sqlite3.connect('src/inventario.db')
    cursor = conn.cursor()
    
    # Crear tabla de usuarios
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Usuarios (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Usuario TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        Nombre TEXT NOT NULL,
        Apellido TEXT NOT NULL,
        Rol TEXT DEFAULT 'user',
        Fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Crear usuario administrador por defecto
    admin_password = hash_password('admin123')
    cursor.execute('''
    INSERT INTO Usuarios (Usuario, password, Nombre, Apellido, Rol)
    VALUES (?, ?, ?, ?, ?)
    ''', ('admin', admin_password, 'Administrador', 'Sistema', 'admin'))
    
    # Crear tabla de productos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Producto (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Nombre TEXT NOT NULL,
        Categoria TEXT NOT NULL,
        Cantidad_en_stock INTEGER NOT NULL DEFAULT 0,
        Precio REAL NOT NULL,
        Fecha_vencimiento DATE,
        Fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Crear tabla de ventas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Ventas (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Fecha DATE NOT NULL,
        ID_producto INTEGER NOT NULL,
        Cantidad INTEGER NOT NULL,
        Precio_unitario REAL NOT NULL,
        Total REAL NOT NULL,
        ID_usuario INTEGER NOT NULL,
        FOREIGN KEY (ID_producto) REFERENCES Producto (ID),
        FOREIGN KEY (ID_usuario) REFERENCES Usuarios (ID)
    )
    ''')
    
    # Crear tabla de movimientos de stock
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Movimientos_stock (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        ID_producto INTEGER NOT NULL,
        Cantidad INTEGER NOT NULL,
        Tipo TEXT NOT NULL,
        ID_usuario INTEGER NOT NULL,
        FOREIGN KEY (ID_producto) REFERENCES Producto (ID),
        FOREIGN KEY (ID_usuario) REFERENCES Usuarios (ID)
    )
    ''')
    
    # Guardar cambios y cerrar conexión
    conn.commit()
    conn.close()
    
    print("Base de datos inicializada correctamente")

if __name__ == "__main__":
    init_database() 