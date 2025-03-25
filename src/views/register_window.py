from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QMessageBox, QFormLayout
)
from PyQt6.QtCore import Qt
from src.services.auth_service import AuthService
from src.config.settings import APP

class RegisterWindow(QDialog):
    """Ventana para registro de nuevos usuarios."""
    
    def __init__(self, parent=None):
        """Inicializa la ventana de registro."""
        super().__init__(parent)
        self.auth_service = AuthService()
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz de usuario."""
        self.setWindowTitle(f"{APP['name']} - Registro")
        self.setFixedWidth(400)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Título
        title = QLabel("Registro de Usuario")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"color: {APP['theme']['primary_color']}; font-size: 24px; font-weight: bold;")
        layout.addWidget(title)
        
        # Formulario
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        # Campos de entrada
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Nombre de usuario")
        form_layout.addRow("Usuario:", self.username_edit)
        
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("Contraseña")
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("Contraseña:", self.password_edit)
        
        self.confirm_password_edit = QLineEdit()
        self.confirm_password_edit.setPlaceholderText("Confirmar contraseña")
        self.confirm_password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("Confirmar:", self.confirm_password_edit)
        
        self.nombre_edit = QLineEdit()
        self.nombre_edit.setPlaceholderText("Nombre")
        form_layout.addRow("Nombre:", self.nombre_edit)
        
        self.apellido_edit = QLineEdit()
        self.apellido_edit.setPlaceholderText("Apellido")
        form_layout.addRow("Apellido:", self.apellido_edit)
        
        layout.addLayout(form_layout)
        
        # Botones
        button_layout = QHBoxLayout()
        
        register_button = QPushButton("Registrarse")
        register_button.clicked.connect(self.register)
        register_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {APP['theme']['primary_color']};
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {APP['theme']['secondary_color']};
            }}
        """)
        button_layout.addWidget(register_button)
        
        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.reject)
        cancel_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {APP['theme']['error_color']};
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {APP['theme']['warning_color']};
            }}
        """)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        
    def register(self):
        """Maneja el registro de un nuevo usuario."""
        username = self.username_edit.text()
        password = self.password_edit.text()
        confirm_password = self.confirm_password_edit.text()
        nombre = self.nombre_edit.text()
        apellido = self.apellido_edit.text()
        
        # Validaciones
        if not all([username, password, confirm_password, nombre, apellido]):
            QMessageBox.warning(self, "Error", "Por favor complete todos los campos")
            return
            
        if password != confirm_password:
            QMessageBox.warning(self, "Error", "Las contraseñas no coinciden")
            return
            
        if len(password) < 6:
            QMessageBox.warning(self, "Error", "La contraseña debe tener al menos 6 caracteres")
            return
            
        try:
            success = self.auth_service.register_user(username, password, nombre, apellido)
            if success:
                QMessageBox.information(self, "Éxito", "Usuario registrado correctamente")
                self.accept()
            else:
                QMessageBox.warning(self, "Error", "No se pudo registrar el usuario")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al registrar usuario: {str(e)}") 