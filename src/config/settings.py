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
    "path": "src/inventario.db",
    "timeout": 30,
    "check_same_thread": False
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
    "password_min_length": 8,
    "max_login_attempts": 3,
    "lockout_duration": 300,  # 5 minutes in seconds
    "session_timeout": 3600,  # 1 hour in seconds
    "bcrypt_rounds": 12
}

# Configuración de alertas
ALERTS = {
    'stock_min': 10,  # Cantidad mínima de stock antes de alertar
    'expiry_days': 7,  # Días antes de vencimiento para alertar
    'discount_percent': 20  # Porcentaje de descuento para productos próximos a vencer
}

# Application settings
APP = {
    "name": "Sistema de Control de Inventarios",
    "version": "2.0.0",
    "company": "Universidad Compensar",
    "window_size": {
        "width": 1024,
        "height": 768
    },
    "theme": {
        "primary_color": "#2196F3",
        "secondary_color": "#FFC107",
        "error_color": "#F44336",
        "success_color": "#4CAF50",
        "warning_color": "#FF9800",
        "info_color": "#2196F3",
        "background_color": "#FFFFFF",
        "text_color": "#000000"
    }
}

# Report settings
REPORTS = {
    "output_dir": "reports",
    "date_format": "%Y-%m-%d",
    "datetime_format": "%Y-%m-%d %H:%M:%S",
    "currency_symbol": "$",
    "decimal_places": 2,
    "page_size": "A4",
    "font_family": "Helvetica",
    "font_size": 12
}

# Stock settings
STOCK = {
    "low_stock_threshold": 10,
    "reorder_point": 20,
    "max_stock": 1000,
    "default_category": "Sin categoría"
}

# Email settings (for future use)
EMAIL = {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "use_tls": True,
    "from_email": "",
    "from_name": "Sistema de Inventarios"
}
