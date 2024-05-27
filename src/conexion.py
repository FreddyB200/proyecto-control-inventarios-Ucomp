import sqlite3

def conectar_base_datos(nombre_base_datos):
    """Función para establecer una conexión con la base de datos sqlite3.

    Args:
        nombre_base_datos (str): Nombre de la base de datos.

    Returns:
        sqlite3.Connection: Objeto de la conexión con la base de datos.
    """
    try:
        conexion = sqlite3.connect(nombre_base_datos)
        return conexion
    except sqlite3.Error as e:
        print(f"Ha ocurrido un error al intentar conectar con la base de datos: {e}")
        return None

def obtener_cursor(conexion):
    """Función para obtener un cursor de la conexión de la base de datos.
        este cursor nos permite interactuar con la base de datos.
    Args:
        conexion (sqlite3.Connection): Objeto de la conexión con la base de datos.

    Returns:
        sqlite3.Cursor: Objeto cursor para ejecutar consultas en la base de datos.
    """
    return conexion.cursor()

def ejecutar_consulta(conexion, consulta):
    """Función para ejecutar una consulta SQL en la base de datos.
       por ejemplo, consulta = "SELECT * FROM Usuarios" 
    Args:
        conexion (sqlite3.Connection): Objeto de la conexión con la base de datos.
        consulta (str): La consulta SQL a ejecutar.

    Returns:
        None
    """
    with obtener_cursor(conexion) as cursor:
        try:
            cursor.execute(consulta)  # Ejecuta la consulta proporcionada (str)
            conexion.commit()  # Guarda los cambios
        except sqlite3.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
