from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QFrame)
from PyQt6.QtCore import Qt
from .base_window import BaseWindow
from services.auth_service import AuthService

class LoginWindow(BaseWindow):
    """Login window implementation using PyQt6."""
    
    def __init__(self, auth_service: AuthService):
        super().__init__()
        self.auth_service = auth_service
        self.setup_login_ui()
        
    def setup_login_ui(self):
        """Setup the login window UI."""
        self.setWindowTitle("Inicio de Sesión")
        self.setFixedSize(400, 300)
        
        # Main container
        container = QFrame()
        container.setObjectName("loginContainer")
        container.setStyleSheet("""
            #loginContainer {
                background-color: white;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        
        # Layout
        layout = QVBoxLayout(container)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Iniciar Sesión")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        layout.addWidget(title)
        
        # Username
        username_layout = QHBoxLayout()
        username_label = QLabel("Usuario:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Ingrese su usuario")
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        layout.addLayout(username_layout)
        
        # Password
        password_layout = QHBoxLayout()
        password_label = QLabel("Contraseña:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Ingrese su contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        layout.addLayout(password_layout)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        self.login_button = QPushButton("Iniciar Sesión")
        self.login_button.clicked.connect(self.handle_login)
        buttons_layout.addWidget(self.login_button)
        
        self.register_button = QPushButton("Registrarse")
        self.register_button.clicked.connect(self.handle_register)
        buttons_layout.addWidget(self.register_button)
        
        layout.addLayout(buttons_layout)
        
        # Recovery link
        self.recovery_link = QPushButton("¿Olvidó su contraseña?")
        self.recovery_link.setStyleSheet("color: #4CAF50; text-decoration: underline;")
        self.recovery_link.clicked.connect(self.handle_password_recovery)
        layout.addWidget(self.recovery_link)
        
        self.layout.addWidget(container)
        
    def handle_login(self):
        """Handle login button click."""
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            self.show_error("Por favor, complete todos los campos")
            return
            
        try:
            if self.auth_service.login(username, password):
                self.show_success("Inicio de sesión exitoso")
                # TODO: Navigate to main window
            else:
                self.show_error("Usuario o contraseña incorrectos")
        except Exception as e:
            self.show_error(f"Error al iniciar sesión: {str(e)}")
            
    def handle_register(self):
        """Handle register button click."""
        # TODO: Open register window
        pass
        
    def handle_password_recovery(self):
        """Handle password recovery link click."""
        # TODO: Open password recovery window
        pass 