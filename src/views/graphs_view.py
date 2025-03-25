from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QComboBox, 
                             QPushButton, QLabel)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from src.services.inventory_service import InventoryService
from src.config.settings import APP
from src.services.ventas_service import VentasService

class GraphsView(QWidget):
    """View for displaying various graphs and charts."""
    
    def __init__(self):
        super().__init__()
        self.inventory_service = InventoryService()
        self.ventas_service = VentasService()
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the graphs view UI."""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("Gráficos y Estadísticas")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)
        
        # Controls
        controls_layout = QHBoxLayout()
        
        # Graph type selector
        self.graph_type = QComboBox()
        self.graph_type.addItems([
            "Stock por Categoría",
            "Ventas por Día",
            "Productos más Vendidos",
            "Valor del Inventario"
        ])
        self.graph_type.currentTextChanged.connect(self.update_graph)
        controls_layout.addWidget(self.graph_type)
        
        # Refresh button
        refresh_btn = QPushButton("Actualizar")
        refresh_btn.clicked.connect(self.update_graph)
        controls_layout.addWidget(refresh_btn)
        
        layout.addLayout(controls_layout)
        
        # Graph area
        self.figure, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        # Initial graph
        self.update_graph()
        
    def update_graph(self):
        """Update the current graph based on selection."""
        graph_type = self.graph_type.currentText()
        
        # Clear previous graph
        self.ax.clear()
        
        try:
            if graph_type == "Stock por Categoría":
                self.plot_stock_by_category()
            elif graph_type == "Ventas por Día":
                self.plot_sales_by_day()
            elif graph_type == "Productos más Vendidos":
                self.plot_top_products()
            elif graph_type == "Valor del Inventario":
                self.plot_inventory_value()
                
            self.canvas.draw()
            
        except Exception as e:
            self.ax.text(0.5, 0.5, f"Error al generar gráfico: {str(e)}",
                        ha='center', va='center')
            self.canvas.draw()
            
    def plot_stock_by_category(self):
        """Plot stock levels by category."""
        products = self.inventory_service.get_all_products()
        
        # Group products by category
        categories = {}
        for product in products:
            category = product['categoria']
            if category not in categories:
                categories[category] = 0
            categories[category] += product['stock']
            
        # Create bar chart
        self.ax.bar(categories.keys(), categories.values())
        self.ax.set_title("Stock por Categoría")
        self.ax.set_xlabel("Categoría")
        self.ax.set_ylabel("Stock Total")
        plt.xticks(rotation=45)
        
    def plot_sales_by_day(self):
        """Plot sales data by day."""
        sales = self.ventas_service.get_sales_by_day()
        
        # Extract dates and totals
        dates = [sale['fecha'] for sale in sales]
        totals = [sale['total'] for sale in sales]
        
        # Create line chart
        self.ax.plot(dates, totals, marker='o')
        self.ax.set_title("Ventas por Día")
        self.ax.set_xlabel("Fecha")
        self.ax.set_ylabel("Total de Ventas")
        plt.xticks(rotation=45)
        
    def plot_top_products(self):
        """Plot top selling products."""
        top_products = self.ventas_service.get_top_products(limit=10)
        
        # Extract product names and quantities
        products = [p['nombre'] for p in top_products]
        quantities = [p['cantidad'] for p in top_products]
        
        # Create horizontal bar chart
        self.ax.barh(products, quantities)
        self.ax.set_title("Productos más Vendidos")
        self.ax.set_xlabel("Cantidad Vendida")
        self.ax.set_ylabel("Producto")
        
    def plot_inventory_value(self):
        """Plot inventory value by category."""
        products = self.inventory_service.get_all_products()
        
        # Group products by category and calculate total value
        categories = {}
        for product in products:
            category = product['categoria']
            if category not in categories:
                categories[category] = 0
            categories[category] += product['stock'] * product['precio']
            
        # Create pie chart
        self.ax.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%')
        self.ax.set_title("Valor del Inventario por Categoría") 