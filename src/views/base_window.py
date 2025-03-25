from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor

class BaseWindow(QMainWindow):
    """Base window class that provides common functionality for all windows."""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_styles()
        
    def setup_ui(self):
        """Setup the basic UI structure."""
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
    def setup_styles(self):
        """Setup the application styles."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLabel {
                color: #333333;
                font-size: 12px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 1px solid #4CAF50;
            }
        """)
        
    def show_error(self, message):
        """Show an error message to the user."""
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.critical(self, "Error", message)
        
    def show_success(self, message):
        """Show a success message to the user."""
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.information(self, "Éxito", message) 