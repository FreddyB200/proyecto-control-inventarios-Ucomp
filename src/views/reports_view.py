from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QComboBox, 
                             QPushButton, QLabel, QTableWidget, QTableWidgetItem,
                             QDateEdit, QMessageBox)
from PyQt6.QtCore import Qt, QDate
from services.inventory_service import InventoryService
from services.ventas_service import VentasService
from services.reports_service import ReportsService

class ReportsView(QWidget):
    """View for generating and displaying various reports."""
    
    def __init__(self):
        super().__init__()
        self.inventory_service = InventoryService()
        self.ventas_service = VentasService()
        self.reports_service = ReportsService()
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the reports view UI."""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("Informes")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)
        
        # Controls
        controls_layout = QHBoxLayout()
        
        # Report type selector
        self.report_type = QComboBox()
        self.report_type.addItems([
            "Inventario Bajo",
            "Ventas por Período",
            "Productos más Vendidos",
            "Movimientos de Stock",
            "Valor Total del Inventario"
        ])
        self.report_type.currentTextChanged.connect(self.update_report)
        controls_layout.addWidget(self.report_type)
        
        # Date range
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addMonths(-1))
        controls_layout.addWidget(QLabel("Desde:"))
        controls_layout.addWidget(self.start_date)
        
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        controls_layout.addWidget(QLabel("Hasta:"))
        controls_layout.addWidget(self.end_date)
        
        # Generate button
        generate_btn = QPushButton("Generar Informe")
        generate_btn.clicked.connect(self.generate_report)
        controls_layout.addWidget(generate_btn)
        
        # Export button
        export_btn = QPushButton("Exportar a Excel")
        export_btn.clicked.connect(self.export_report)
        controls_layout.addWidget(export_btn)
        
        layout.addLayout(controls_layout)
        
        # Report table
        self.table = QTableWidget()
        layout.addWidget(self.table)
        
        # Initial report
        self.update_report()
        
    def update_report(self):
        """Update the current report based on selection."""
        report_type = self.report_type.currentText()
        
        try:
            if report_type == "Inventario Bajo":
                self.show_low_stock_report()
            elif report_type == "Ventas por Período":
                self.show_sales_report()
            elif report_type == "Productos más Vendidos":
                self.show_top_products_report()
            elif report_type == "Movimientos de Stock":
                self.show_stock_movements_report()
            elif report_type == "Valor Total del Inventario":
                self.show_inventory_value_report()
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al generar el informe: {str(e)}")
            
    def show_low_stock_report(self):
        """Display low stock report."""
        products = self.inventory_service.get_low_stock_products()
        
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "ID", "Nombre", "Categoría", "Stock Actual"
        ])
        
        self.table.setRowCount(len(products))
        for row, product in enumerate(products):
            self.table.setItem(row, 0, QTableWidgetItem(str(product['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(product['nombre']))
            self.table.setItem(row, 2, QTableWidgetItem(product['categoria']))
            self.table.setItem(row, 3, QTableWidgetItem(str(product['stock'])))
            
    def show_sales_report(self):
        """Display sales report for the selected period."""
        start_date = self.start_date.date().toString("yyyy-MM-dd")
        end_date = self.end_date.date().toString("yyyy-MM-dd")
        sales = self.ventas_service.get_sales_by_period(start_date, end_date)
        
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "Fecha", "Total", "Cantidad de Productos", "Usuario"
        ])
        
        self.table.setRowCount(len(sales))
        for row, sale in enumerate(sales):
            self.table.setItem(row, 0, QTableWidgetItem(sale['fecha']))
            self.table.setItem(row, 1, QTableWidgetItem(f"${sale['total']:.2f}"))
            self.table.setItem(row, 2, QTableWidgetItem(str(sale['cantidad_productos'])))
            self.table.setItem(row, 3, QTableWidgetItem(sale['usuario']))
            
    def show_top_products_report(self):
        """Display top selling products report."""
        products = self.ventas_service.get_top_products(limit=20)
        
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "Nombre", "Categoría", "Cantidad Vendida", "Total"
        ])
        
        self.table.setRowCount(len(products))
        for row, product in enumerate(products):
            self.table.setItem(row, 0, QTableWidgetItem(product['nombre']))
            self.table.setItem(row, 1, QTableWidgetItem(product['categoria']))
            self.table.setItem(row, 2, QTableWidgetItem(str(product['cantidad'])))
            self.table.setItem(row, 3, QTableWidgetItem(f"${product['total']:.2f}"))
            
    def show_stock_movements_report(self):
        """Display stock movements report."""
        start_date = self.start_date.date().toString("yyyy-MM-dd")
        end_date = self.end_date.date().toString("yyyy-MM-dd")
        movements = self.inventory_service.get_stock_movements_by_period(start_date, end_date)
        
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Fecha", "Producto", "Cantidad", "Tipo", "Usuario"
        ])
        
        self.table.setRowCount(len(movements))
        for row, movement in enumerate(movements):
            self.table.setItem(row, 0, QTableWidgetItem(movement['fecha']))
            self.table.setItem(row, 1, QTableWidgetItem(movement['producto_nombre']))
            self.table.setItem(row, 2, QTableWidgetItem(str(movement['cantidad'])))
            self.table.setItem(row, 3, QTableWidgetItem(movement['tipo']))
            self.table.setItem(row, 4, QTableWidgetItem(movement['usuario']))
            
    def show_inventory_value_report(self):
        """Display inventory value report."""
        inventory_value = self.inventory_service.get_inventory_value()
        
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels([
            "Categoría", "Cantidad de Productos", "Valor Total"
        ])
        
        self.table.setRowCount(len(inventory_value))
        for row, category in enumerate(inventory_value):
            self.table.setItem(row, 0, QTableWidgetItem(category['categoria']))
            self.table.setItem(row, 1, QTableWidgetItem(str(category['cantidad'])))
            self.table.setItem(row, 2, QTableWidgetItem(f"${category['valor_total']:.2f}"))
            
    def generate_report(self):
        """Generate the current report."""
        self.update_report()
        QMessageBox.information(self, "Éxito", "Informe generado correctamente")
        
    def export_report(self):
        """Export the current report to Excel."""
        try:
            report_type = self.report_type.currentText()
            start_date = self.start_date.date().toString("yyyy-MM-dd")
            end_date = self.end_date.date().toString("yyyy-MM-dd")
            
            self.reports_service.export_to_excel(
                report_type,
                start_date,
                end_date,
                self.table
            )
            
            QMessageBox.information(self, "Éxito", "Informe exportado correctamente")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al exportar el informe: {str(e)}") 