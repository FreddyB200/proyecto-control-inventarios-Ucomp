"""
Módulo de configuración de la aplicación.
Contiene constantes y configuraciones utilizadas en toda la aplicación.
"""

import os
from pathlib import Path

# Rutas base
BASE_DIR = Path(__file__).resolve().parent.parent.parent
SRC_DIR = os.path.join(BASE_DIR, 'src')

# Configuración de base de datos
DATABASE = {
    'usuarios': {
        'path': os.path.join(SRC_DIR, 'usuarios.db'),
        'name': 'usuarios.db'
    },
    'inventario': {
        'path': os.path.join(SRC_DIR, 'inventario.db'),
        'name': 'inventario.db'
    }
}

# Configuración de la interfaz de usuario
UI = {
    'title': 'Control de Inventario',
    'icon': os.path.join(BASE_DIR, 'inventario_icono.ico'),
    'theme': {
        'primary_color': '#bcd4cc',
        'secondary_color': '#DBF0F1',
        'accent_color': '#8CD4C8',
        'text_color': '#041A17',
        'highlight_color': '#99CCFF'
    },
    'fonts': {
        'title': ('Fixedsys', 18, 'bold'),
        'subtitle': ('Fixedsys', 16, 'bold'),
        'label': ('Monaco', 12, 'bold'),
        'small': ('Monaco', 10, 'bold')
    },
    'dimensions': {
        'login': '350x275',
        'main': '620x400',
        'inventario': '1350x320'
    }
}

# Configuración de seguridad
SECURITY = {
    'max_login_attempts': 5,
    'admin_credentials': {
        'username': 'admin',
        'password': '321'  # En producción, esto debería estar encriptado o en variables de entorno
    }
}

# Configuración de alertas
ALERTS = {
    'stock_min': 10,  # Cantidad mínima de stock antes de alertar
    'expiry_days': 7,  # Días antes de vencimiento para alertar
    'discount_percent': 20  # Porcentaje de descuento para productos próximos a vencer
}
