"""
Constantes utilizadas en toda la aplicación.
Este módulo contiene constantes que no cambian durante la ejecución de la aplicación.
"""

# Error messages
ERROR_MESSAGES = {
    "db_error": "Error en la base de datos",
    "invalid_credentials": "Usuario o contraseña inválidos",
    "user_exists": "El usuario ya existe",
    "password_mismatch": "Las contraseñas no coinciden",
    "insufficient_stock": "Stock insuficiente",
    "invalid_quantity": "Cantidad inválida",
    "invalid_price": "Precio inválido",
    "product_exists": "El producto ya existe",
    "product_not_found": "Producto no encontrado",
    "supplier_exists": "El proveedor ya existe",
    "supplier_not_found": "Proveedor no encontrado",
    "sale_not_found": "Venta no encontrada",
    "invalid_date": "Fecha inválida"
}

# Success messages
SUCCESS_MESSAGES = {
    "login_success": "Inicio de sesión exitoso",
    "register_success": "Usuario registrado exitosamente",
    "password_changed": "Contraseña cambiada exitosamente",
    "product_added": "Producto agregado exitosamente",
    "product_updated": "Producto actualizado exitosamente",
    "product_deleted": "Producto eliminado exitosamente",
    "stock_updated": "Stock actualizado exitosamente",
    "sale_registered": "Venta registrada exitosamente",
    "supplier_added": "Proveedor agregado exitosamente",
    "supplier_updated": "Proveedor actualizado exitosamente",
    "supplier_deleted": "Proveedor eliminado exitosamente"
}

# SQL Queries
SQL_QUERIES = {
    "get_user": "SELECT * FROM Usuarios WHERE Usuario = ?",
    "create_user": "INSERT INTO Usuarios (Usuario, password, Rol) VALUES (?, ?, ?)",
    "update_password": "UPDATE Usuarios SET password = ? WHERE Usuario = ?",
    "get_product": "SELECT * FROM Productos WHERE ID = ?",
    "get_products": "SELECT * FROM Productos",
    "get_products_by_category": "SELECT * FROM Productos WHERE Categoria = ?",
    "create_product": """
        INSERT INTO Productos (Nombre, Categoria, Cantidad_en_stock, Precio, Fecha_vencimiento)
        VALUES (?, ?, ?, ?, ?)
    """,
    "update_product": """
        UPDATE Productos 
        SET Nombre = ?, Categoria = ?, Cantidad_en_stock = ?, Precio = ?, Fecha_vencimiento = ?
        WHERE ID = ?
    """,
    "delete_product": "DELETE FROM Productos WHERE ID = ?",
    "update_stock": "UPDATE Productos SET Cantidad_en_stock = ? WHERE ID = ?",
    "register_stock_movement": """
        INSERT INTO MovimientosStock (ID_producto, Cantidad, Tipo, Fecha)
        VALUES (?, ?, ?, ?)
    """,
    "get_stock_movements": "SELECT * FROM MovimientosStock WHERE ID_producto = ?",
    "create_sale": "INSERT INTO Ventas (Fecha, ID_producto, Cantidad, Precio_unitario, Total, ID_usuario) VALUES (?, ?, ?, ?, ?, ?)",
    "create_sale_detail": """
        INSERT INTO DetalleVentas (venta_id, producto_id, cantidad, precio_unitario, subtotal)
        VALUES (?, ?, ?, ?, ?)
    """,
    "get_sale": "SELECT * FROM Ventas WHERE ID = ?",
    "get_sale_details": "SELECT * FROM Ventas WHERE ID = ?",
    "get_sales_by_date": "SELECT * FROM Ventas WHERE Fecha BETWEEN ? AND ?",
    "get_supplier": "SELECT * FROM Proveedores WHERE id = ?",
    "get_suppliers": "SELECT * FROM Proveedores",
    "create_supplier": """
        INSERT INTO Proveedores (nombre, nit, direccion, telefono, email)
        VALUES (?, ?, ?, ?, ?)
    """,
    "update_supplier": """
        UPDATE Proveedores 
        SET nombre = ?, nit = ?, direccion = ?, telefono = ?, email = ?
        WHERE id = ?
    """,
    "delete_supplier": "DELETE FROM Proveedores WHERE id = ?"
}

# Database table names
DB_TABLES = {
    "users": "Usuarios",
    "products": "Productos",
    "stock_movements": "MovimientosStock",
    "sales": "Ventas",
    "sale_details": "DetalleVentas",
    "suppliers": "Proveedores"
}

# Constantes para campos de formularios
FORM_FIELDS = {
    'product': ['Nombre del producto', 'Precio', 'Fecha de vencimiento', 'Cantidad', 'Nombre del proveedor'],
    'user': ['Nombre', 'Usuario', 'Contraseña', 'Confirmar contraseña'],
    'sale': ['Producto', 'Cantidad', 'Precio unitario', 'Total']
}

# Constantes para tipos de operaciones
OPERATION_TYPES = {
    'add': 'Agregar',
    'update': 'Actualizar',
    'delete': 'Eliminar',
    'search': 'Buscar',
    'view': 'Ver'
}
