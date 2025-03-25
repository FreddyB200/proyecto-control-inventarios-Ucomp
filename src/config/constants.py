"""
Constantes utilizadas en toda la aplicación.
Este módulo contiene constantes que no cambian durante la ejecución de la aplicación.
"""

# Constantes para mensajes de error
ERROR_MESSAGES = {
    'db_connection': 'Ha ocurrido un error al intentar conectar con la base de datos: {}',
    'query_execution': 'Error al ejecutar la consulta: {}',
    'login_failed': 'Usuario o contraseña incorrectos. Intentos restantes: {}',
    'login_blocked': 'Demasiados intentos fallidos. El acceso está bloqueado.',
    'empty_fields': 'Ingrese todos los datos.',
    'invalid_date': 'Formato de fecha inválido. Use AAAA-MM-DD.',
    'invalid_number': 'Ingrese un valor numérico válido.',
    'product_not_found': 'Producto no encontrado.',
    'provider_not_found': 'Proveedor no encontrado.',
    'product_add_error': 'Error al agregar producto: {}',
    'product_update_error': 'Error al actualizar producto: {}',
    'product_delete_error': 'Error al eliminar producto: {}',
    'no_selection': 'Por favor, seleccione un elemento para continuar.'
}

# Constantes para mensajes de éxito
SUCCESS_MESSAGES = {
    'product_added': 'Producto agregado correctamente',
    'product_updated': 'Producto actualizado correctamente',
    'product_deleted': 'Producto eliminado correctamente',
    'user_added': 'Usuario registrado correctamente',
    'password_updated': 'Contraseña actualizada correctamente',
    'sale_completed': 'Venta registrada correctamente'
}

# Constantes para consultas SQL
SQL_QUERIES = {
    'get_user': 'SELECT Nombre FROM Usuarios WHERE Usuario=? AND password=?',
    'get_products': 'SELECT ID, Nombre, Precio, Fecha_vencimiento, cantidad_en_stock FROM Producto',
    'search_products': 'SELECT ID, Nombre, Precio, Fecha_vencimiento, cantidad_en_stock FROM Producto WHERE Nombre LIKE ?',
    'get_providers': 'SELECT razon_social, NIT FROM Proveedor',
    'add_product': 'INSERT INTO Producto (Nombre, Precio, Fecha_vencimiento, Cantidad_en_stock, NIT_proveedor) VALUES (?, ?, ?, ?, ?)',
    'update_product': 'UPDATE Producto SET Nombre=?, Precio=?, Fecha_vencimiento=?, Cantidad_en_stock=?, NIT_proveedor=? WHERE ID=?',
    'delete_product': 'DELETE FROM Producto WHERE ID=?',
    'low_stock_products': 'SELECT Nombre FROM Producto WHERE Cantidad_en_stock < ?',
    'expiring_products': 'SELECT Nombre, Precio FROM Producto WHERE Fecha_vencimiento BETWEEN ? AND ?',
    'update_product_price': 'UPDATE Producto SET Precio = ? WHERE Nombre = ?'
}

# Constantes para tablas de la base de datos
DB_TABLES = {
    'usuarios': 'Usuarios',
    'productos': 'Producto',
    'proveedores': 'Proveedor',
    'ventas': 'Ventas'
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
