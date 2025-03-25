# Estructura Propuesta para Refactorización

## Estructura de Directorios
```
proyecto-control-inventarios-Ucomp/
│
├── src/
│   ├── __init__.py
│   ├── main.py                  # Punto de entrada de la aplicación
│   │
│   ├── config/                  # Configuración de la aplicación
│   │   ├── __init__.py
│   │   ├── settings.py          # Configuraciones generales
│   │   └── constants.py         # Constantes de la aplicación
│   │
│   ├── models/                  # Modelos de datos
│   │   ├── __init__.py
│   │   ├── producto.py
│   │   ├── usuario.py
│   │   ├── venta.py
│   │   └── proveedor.py
│   │
│   ├── views/                   # Interfaces gráficas
│   │   ├── __init__.py
│   │   ├── base_view.py         # Clase base para vistas
│   │   ├── login_view.py
│   │   ├── main_view.py
│   │   ├── inventario_view.py
│   │   ├── ventas_view.py
│   │   ├── informes_view.py
│   │   └── graficos_view.py
│   │
│   ├── controllers/             # Controladores
│   │   ├── __init__.py
│   │   ├── auth_controller.py
│   │   ├── inventario_controller.py
│   │   ├── ventas_controller.py
│   │   └── informes_controller.py
│   │
│   ├── services/                # Servicios
│   │   ├── __init__.py
│   │   ├── database_service.py  # Servicio de base de datos mejorado
│   │   ├── auth_service.py      # Servicio de autenticación
│   │   └── report_service.py    # Servicio de generación de informes
│   │
│   ├── utils/                   # Utilidades
│   │   ├── __init__.py
│   │   ├── validators.py        # Validadores de datos
│   │   ├── formatters.py        # Formateadores de datos
│   │   └── exceptions.py        # Excepciones personalizadas
│   │
│   └── assets/                  # Recursos estáticos
│       ├── styles/              # Estilos para la interfaz
│       └── images/              # Imágenes e iconos
│
├── tests/                       # Pruebas unitarias
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_controllers.py
│   └── test_services.py
│
├── docs/                        # Documentación
│   └── manual_usuario.md
│
├── requirements.txt             # Dependencias del proyecto
└── README.md                    # Documentación general
```

## Principios de Diseño a Aplicar

1. **Separación de Responsabilidades**: Cada componente tiene una única responsabilidad.
2. **Principio de Abierto/Cerrado**: Componentes abiertos para extensión, cerrados para modificación.
3. **Inyección de Dependencias**: Las dependencias se inyectan, no se crean dentro de las clases.
4. **Programación Orientada a Interfaces**: Usar interfaces para desacoplar componentes.
5. **Manejo de Errores Consistente**: Excepciones personalizadas y manejo uniforme.
6. **Configuración Centralizada**: Valores configurables en archivos de configuración.
7. **Documentación Completa**: Docstrings en todas las clases y métodos.
