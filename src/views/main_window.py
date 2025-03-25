from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QStackedWidget, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from src.config.settings import APP
from src.views.inventory_view import InventoryView
from src.views.graphs_view import GraphsView
from src.views.reports_view import ReportsView

class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        
        # Set window properties
        self.setWindowTitle(APP["name"])
        self.resize(APP["window_size"]["width"], APP["window_size"]["height"])
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create sidebar
        sidebar = QWidget()
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet(f"""
            QWidget {{
                background-color: {APP['theme']['primary_color']};
            }}
            QPushButton {{
                color: white;
                border: none;
                padding: 15px;
                text-align: left;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {APP['theme']['secondary_color']};
            }}
        """)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setSpacing(0)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add logo/title to sidebar
        title_label = QLabel(APP["name"])
        title_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold; padding: 20px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(title_label)
        
        # Create navigation buttons
        self.inventory_btn = QPushButton("Inventario")
        self.inventory_btn.clicked.connect(lambda: self.show_view(0))
        sidebar_layout.addWidget(self.inventory_btn)
        
        self.graphs_btn = QPushButton("Gráficos")
        self.graphs_btn.clicked.connect(lambda: self.show_view(1))
        sidebar_layout.addWidget(self.graphs_btn)
        
        self.reports_btn = QPushButton("Reportes")
        self.reports_btn.clicked.connect(lambda: self.show_view(2))
        sidebar_layout.addWidget(self.reports_btn)
        
        # Add stretch to push logout button to bottom
        sidebar_layout.addStretch()
        
        # Add logout button
        self.logout_btn = QPushButton("Cerrar Sesión")
        self.logout_btn.clicked.connect(self.logout)
        sidebar_layout.addWidget(self.logout_btn)
        
        # Add sidebar to main layout
        layout.addWidget(sidebar)
        
        # Create stacked widget for views
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet(f"background-color: {APP['theme']['background_color']};")
        
        # Add views to stacked widget
        self.inventory_view = InventoryView()
        self.stacked_widget.addWidget(self.inventory_view)
        
        self.graphs_view = GraphsView()
        self.stacked_widget.addWidget(self.graphs_view)
        
        self.reports_view = ReportsView()
        self.stacked_widget.addWidget(self.reports_view)
        
        # Add stacked widget to main layout
        layout.addWidget(self.stacked_widget)
        
    def show_view(self, index: int):
        """Show the selected view."""
        self.stacked_widget.setCurrentIndex(index)
        
    def logout(self):
        """Handle logout button click."""
        reply = QMessageBox.question(
            self,
            "Cerrar Sesión",
            "¿Está seguro que desea cerrar sesión?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            from src.views.login_window import LoginWindow
            self.login_window = LoginWindow()
            self.login_window.show()
            self.close() 