from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QStackedWidget, QFrame)
from PyQt6.QtCore import Qt
from .base_window import BaseWindow
from .inventory_view import InventoryView
from .sales_view import SalesView
from .reports_view import ReportsView
from .graphs_view import GraphsView

class MainWindow(BaseWindow):
    """Main window implementation with dashboard layout."""
    
    def __init__(self, user_name: str):
        super().__init__()
        self.user_name = user_name
        self.setup_main_ui()
        
    def setup_main_ui(self):
        """Setup the main window UI with dashboard layout."""
        self.setWindowTitle("Sistema de Control de Inventarios")
        self.setMinimumSize(1200, 800)
        
        # Create main layout
        main_layout = QHBoxLayout()
        
        # Create sidebar
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)
        
        # Create content area
        content = self.create_content_area()
        main_layout.addWidget(content)
        
        self.layout.addLayout(main_layout)
        
    def create_sidebar(self) -> QFrame:
        """Create the sidebar with navigation buttons."""
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setStyleSheet("""
            #sidebar {
                background-color: #2c3e50;
                min-width: 200px;
                max-width: 200px;
            }
            QPushButton {
                text-align: left;
                padding: 15px;
                border: none;
                color: white;
                font-size: 14px;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
            QPushButton:checked {
                background-color: #3498db;
            }
            QLabel {
                color: white;
                font-size: 16px;
                padding: 20px;
                border-bottom: 1px solid #34495e;
            }
        """)
        
        layout = QVBoxLayout(sidebar)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # User info
        user_label = QLabel(f"Bienvenido, {self.user_name}")
        layout.addWidget(user_label)
        
        # Navigation buttons
        self.inventory_btn = QPushButton("📦 Inventario")
        self.inventory_btn.setCheckable(True)
        self.inventory_btn.setChecked(True)
        self.inventory_btn.clicked.connect(lambda: self.change_page(0))
        layout.addWidget(self.inventory_btn)
        
        self.sales_btn = QPushButton("💰 Ventas")
        self.sales_btn.setCheckable(True)
        self.sales_btn.clicked.connect(lambda: self.change_page(1))
        layout.addWidget(self.sales_btn)
        
        self.reports_btn = QPushButton("📊 Informes")
        self.reports_btn.setCheckable(True)
        self.reports_btn.clicked.connect(lambda: self.change_page(2))
        layout.addWidget(self.reports_btn)
        
        self.graphs_btn = QPushButton("📈 Gráficos")
        self.graphs_btn.setCheckable(True)
        self.graphs_btn.clicked.connect(lambda: self.change_page(3))
        layout.addWidget(self.graphs_btn)
        
        # Add stretch to push buttons to top
        layout.addStretch()
        
        return sidebar
        
    def create_content_area(self) -> QStackedWidget:
        """Create the content area with different views."""
        content = QStackedWidget()
        content.setStyleSheet("""
            QStackedWidget {
                background-color: #f5f6fa;
            }
        """)
        
        # Add different views
        self.inventory_view = InventoryView()
        content.addWidget(self.inventory_view)
        
        self.sales_view = SalesView()
        content.addWidget(self.sales_view)
        
        self.reports_view = ReportsView()
        content.addWidget(self.reports_view)
        
        self.graphs_view = GraphsView()
        content.addWidget(self.graphs_view)
        
        return content
        
    def change_page(self, index: int):
        """Change the current page in the content area."""
        # Update button states
        self.inventory_btn.setChecked(index == 0)
        self.sales_btn.setChecked(index == 1)
        self.reports_btn.setChecked(index == 2)
        self.graphs_btn.setChecked(index == 3)
        
        # Change page
        self.content.setCurrentIndex(index) 