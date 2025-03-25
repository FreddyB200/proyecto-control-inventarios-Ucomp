from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QLabel, QLineEdit,
                             QComboBox, QSpinBox, QDoubleSpinBox, QMessageBox)
from PyQt6.QtCore import Qt
from services.inventory_service import InventoryService

class InventoryView(QWidget):
    """Inventory management view with CRUD operations."""
    
    def __init__(self):
        super().__init__()
        self.inventory_service = InventoryService()
        self.setup_ui()
        self.load_inventory()
        
    def setup_ui(self):
        """Setup the inventory view UI."""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("Gestión de Inventario")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)
        
        # Search bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar producto...")
        self.search_input.textChanged.connect(self.filter_inventory)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Nombre", "Categoría", "Stock", "Precio", "Acciones"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)
        
        # Add product form
        form_layout = QHBoxLayout()
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nombre del producto")
        form_layout.addWidget(self.name_input)
        
        self.category_combo = QComboBox()
        self.category_combo.addItems(["Electrónicos", "Ropa", "Hogar", "Otros"])
        form_layout.addWidget(self.category_combo)
        
        self.stock_input = QSpinBox()
        self.stock_input.setRange(0, 9999)
        form_layout.addWidget(self.stock_input)
        
        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0, 999999.99)
        self.price_input.setPrefix("$")
        self.price_input.setDecimals(2)
        form_layout.addWidget(self.price_input)
        
        add_button = QPushButton("Agregar Producto")
        add_button.clicked.connect(self.add_product)
        form_layout.addWidget(add_button)
        
        layout.addLayout(form_layout)
        
    def load_inventory(self):
        """Load inventory data into the table."""
        try:
            products = self.inventory_service.get_all_products()
            self.table.setRowCount(len(products))
            
            for row, product in enumerate(products):
                # Add product data
                self.table.setItem(row, 0, QTableWidgetItem(str(product['id'])))
                self.table.setItem(row, 1, QTableWidgetItem(product['nombre']))
                self.table.setItem(row, 2, QTableWidgetItem(product['categoria']))
                self.table.setItem(row, 3, QTableWidgetItem(str(product['stock'])))
                self.table.setItem(row, 4, QTableWidgetItem(f"${product['precio']:.2f}"))
                
                # Add action buttons
                actions_widget = QWidget()
                actions_layout = QHBoxLayout(actions_widget)
                actions_layout.setContentsMargins(0, 0, 0, 0)
                
                edit_btn = QPushButton("✏️")
                edit_btn.clicked.connect(lambda checked, p=product: self.edit_product(p))
                actions_layout.addWidget(edit_btn)
                
                delete_btn = QPushButton("🗑️")
                delete_btn.clicked.connect(lambda checked, p=product: self.delete_product(p))
                actions_layout.addWidget(delete_btn)
                
                self.table.setCellWidget(row, 5, actions_widget)
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar el inventario: {str(e)}")
            
    def add_product(self):
        """Add a new product to the inventory."""
        try:
            product_data = {
                'nombre': self.name_input.text(),
                'categoria': self.category_combo.currentText(),
                'stock': self.stock_input.value(),
                'precio': self.price_input.value()
            }
            
            if not product_data['nombre']:
                QMessageBox.warning(self, "Error", "El nombre del producto es requerido")
                return
                
            self.inventory_service.add_product(product_data)
            self.load_inventory()
            self.clear_form()
            QMessageBox.information(self, "Éxito", "Producto agregado correctamente")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al agregar el producto: {str(e)}")
            
    def edit_product(self, product):
        """Edit an existing product."""
        try:
            # TODO: Implement edit dialog
            pass
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al editar el producto: {str(e)}")
            
    def delete_product(self, product):
        """Delete a product from the inventory."""
        try:
            reply = QMessageBox.question(
                self, "Confirmar", 
                f"¿Está seguro de eliminar el producto {product['nombre']}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.inventory_service.delete_product(product['id'])
                self.load_inventory()
                QMessageBox.information(self, "Éxito", "Producto eliminado correctamente")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al eliminar el producto: {str(e)}")
            
    def filter_inventory(self):
        """Filter inventory based on search text."""
        search_text = self.search_input.text().lower()
        
        for row in range(self.table.rowCount()):
            show_row = False
            for col in range(5):  # Exclude actions column
                item = self.table.item(row, col)
                if item and search_text in item.text().lower():
                    show_row = True
                    break
            self.table.setRowHidden(row, not show_row)
            
    def clear_form(self):
        """Clear the add product form."""
        self.name_input.clear()
        self.category_combo.setCurrentIndex(0)
        self.stock_input.setValue(0)
        self.price_input.setValue(0) 