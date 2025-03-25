import sqlite3
from datetime import datetime

def migrate_database():
    """Migrate the database to the new structure."""
    try:
        conn = sqlite3.connect("src/inventario.db")
        cursor = conn.cursor()
        
        # Create MovimientosStock table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS MovimientosStock (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producto_id INTEGER NOT NULL,
                cantidad INTEGER NOT NULL,
                tipo TEXT NOT NULL,
                fecha TEXT NOT NULL,
                FOREIGN KEY (producto_id) REFERENCES Productos(id)
            )
        """)
        
        # Create Ventas table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                total REAL NOT NULL,
                usuario_id INTEGER NOT NULL,
                FOREIGN KEY (usuario_id) REFERENCES Usuarios(id)
            )
        """)
        
        # Create DetalleVentas table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS DetalleVentas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                venta_id INTEGER NOT NULL,
                producto_id INTEGER NOT NULL,
                cantidad INTEGER NOT NULL,
                precio_unitario REAL NOT NULL,
                subtotal REAL NOT NULL,
                FOREIGN KEY (venta_id) REFERENCES Ventas(id),
                FOREIGN KEY (producto_id) REFERENCES Productos(id)
            )
        """)
        
        # Create Proveedores table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Proveedores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                nit TEXT UNIQUE NOT NULL,
                direccion TEXT,
                telefono TEXT,
                email TEXT
            )
        """)
        
        # Create Usuarios table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                rol TEXT NOT NULL
            )
        """)
        
        # Create Productos table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                categoria TEXT NOT NULL,
                stock INTEGER NOT NULL DEFAULT 0,
                precio REAL NOT NULL,
                proveedor_id INTEGER,
                fecha_vencimiento TEXT,
                FOREIGN KEY (proveedor_id) REFERENCES Proveedores(id)
            )
        """)
        
        # Insert default admin user if not exists
        cursor.execute("SELECT * FROM Usuarios WHERE username = 'admin'")
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO Usuarios (username, password, rol)
                VALUES (?, ?, ?)
            """, ('admin', 'admin123', 'admin'))
        
        # Create indexes for better performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_productos_categoria ON Productos(categoria)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_movimientos_producto ON MovimientosStock(producto_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_ventas_fecha ON Ventas(fecha)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_detalle_venta ON DetalleVentas(venta_id)")
        
        conn.commit()
        print("Migración de base de datos completada exitosamente")
        
    except sqlite3.Error as e:
        print(f"Error durante la migración: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database() 