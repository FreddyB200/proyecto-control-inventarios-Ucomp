from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox, QDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap

from src.services.auth_service import AuthService
from src.config.settings import APP
from src.views.main_window import MainWindow
from src.views.register_window import RegisterWindow

class LoginWindow(QMainWindow):
    """Login window for user authentication."""
    
    def __init__(self):
        """Initialize the login window."""
        super().__init__()
        
        # Initialize services
        self.auth_service = AuthService()
        
        # Set window properties
        self.setWindowTitle(f"{APP['name']} - Login")
        self.setFixedSize(400, 500)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Add logo
        logo_label = QLabel()
        logo_pixmap = QPixmap("assets/logo.png")
        if not logo_pixmap.isNull():
            logo_label.setPixmap(logo_pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(logo_label)
        
        # Add welcome message
        welcome_label = QLabel("Bienvenido")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet(f"color: {APP['theme']['primary_color']}; font-size: 24px; font-weight: bold;")
        layout.addWidget(welcome_label)
        
        # Add username field
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Usuario")
        self.username_edit.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #2196F3;
            }
        """)
        layout.addWidget(self.username_edit)
        
        # Add password field
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("Contraseña")
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.setStyleSheet(self.username_edit.styleSheet())
        layout.addWidget(self.password_edit)
        
        # Add login button
        login_button = QPushButton("Iniciar Sesión")
        login_button.setStyleSheet(f"""
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
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)
        
        # Add register link
        register_layout = QHBoxLayout()
        register_label = QLabel("¿No tienes una cuenta?")
        register_button = QPushButton("Registrarse")
        register_button.setStyleSheet("""
            QPushButton {
                border: none;
                color: #2196F3;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #FFC107;
            }
        """)
        register_button.clicked.connect(self.show_register)
        register_layout.addWidget(register_label)
        register_layout.addWidget(register_button)
        layout.addLayout(register_layout)
        
        # Add stretch to push everything to the top
        layout.addStretch()
        
    def login(self):
        """Handle login button click."""
        try:
            username = self.username_edit.text().strip()
            password = self.password_edit.text().strip()
            
            if not username or not password:
                QMessageBox.warning(self, "Error", "Por favor ingrese usuario y contraseña")
                return
                
            result = self.auth_service.verify_credentials(username, password)
            
            if 'success' in result:
                self.main_window = MainWindow()
                self.main_window.show()
                self.close()
            else:
                QMessageBox.warning(self, "Error", result.get('error', 'Error al iniciar sesión'))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al iniciar sesión: {str(e)}")
            
    def show_register(self):
        """Show registration dialog."""
        try:
            register_window = RegisterWindow(self)
            if register_window.exec() == QDialog.DialogCode.Accepted:
                # Limpiar campos después de un registro exitoso
                self.username_edit.clear()
                self.password_edit.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al mostrar ventana de registro: {str(e)}") 