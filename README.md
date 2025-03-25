# Sistema de Control de Inventarios

Sistema de control de inventarios desarrollado con PyQt6 y SQLite.

## Características

- Interfaz gráfica moderna y responsiva con PyQt6
- Gestión completa de inventario
- Control de ventas
- Gestión de proveedores
- Generación de gráficos y reportes
- Exportación de datos a Excel y PDF
- Sistema de autenticación seguro
- Base de datos SQLite

## Requisitos

- Python 3.8 o superior
- PyQt6
- Matplotlib
- Pandas
- OpenPyXL
- ReportLab
- SQLAlchemy
- bcrypt

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/proyecto-control-inventarios-Ucomp.git
cd proyecto-control-inventarios-Ucomp
```

2. Crear un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Uso

1. Ejecutar la aplicación:
```bash
python src/main.py
```

2. Iniciar sesión con las credenciales por defecto:
- Usuario: admin
- Contraseña: admin123

## Estructura del Proyecto

```
src/
├── config/
│   └── __init__.py
├── controllers/
│   ├── __init__.py
│   └── main_controller.py
├── models/
│   ├── __init__.py
│   ├── product.py
│   ├── category.py
│   ├── user.py
│   └── database.py
├── services/
│   ├── __init__.py
│   ├── auth_service.py
│   ├── inventory_service.py
│   ├── sales_service.py
│   └── reports_service.py
├── utils/
│   ├── __init__.py
│   ├── security.py
│   └── database_migration.py
├── views/
│   ├── __init__.py
│   ├── base_window.py
│   ├── login_window.py
│   ├── main_window.py
│   ├── inventory_view.py
│   ├── graphs_view.py
│   └── reports_view.py
└── main.py
```

## Funcionalidades Principales

### Gestión de Inventario
- Agregar, editar y eliminar productos
- Control de stock
- Categorización de productos
- Historial de movimientos

### Ventas
- Registro de ventas
- Detalle de ventas
- Historial de transacciones

### Reportes y Gráficos
- Reporte de inventario bajo
- Ventas por período
- Productos más vendidos
- Movimientos de stock
- Valor total del inventario
- Exportación a Excel y PDF

### Seguridad
- Autenticación de usuarios
- Encriptación de contraseñas
- Control de acceso

## Contribuir

1. Fork el repositorio
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.


