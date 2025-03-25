from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QLabel, QLineEdit,
                             QComboBox, QSpinBox, QDoubleSpinBox, QMessageBox,
                             QDialog, QFormLayout, QDateEdit)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QIcon
from src.services.inventory_service import InventoryService
from src.config.settings import APP, STOCK
from datetime import datetime

class AddProductDialog(QDialog):
    """Dialog for adding/editing products."""
    
    def __init__(self, parent=None, product=None):
        """Initialize the dialog."""
        super().__init__(parent)
        self.product = product
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the dialog UI."""
        self.setWindowTitle("Agregar Producto" if not self.product else "Editar Producto")
        self.setFixedWidth(400)
        
        layout = QFormLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Name field
        self.name_edit = QLineEdit()
        if self.product:
            self.name_edit.setText(self.product[1])
        layout.addRow("Nombre:", self.name_edit)
        
        # Category field
        self.category_combo = QComboBox()
        self.category_combo.addItems(["Alimentos", "Bebidas", "Limpieza", "Otros"])
        if self.product:
            self.category_combo.setCurrentText(self.product[2])
        layout.addRow("Categoría:", self.category_combo)
        
        # Stock field
        self.stock_spin = QSpinBox()
        self.stock_spin.setRange(0, STOCK["max_stock"])
        if self.product:
            self.stock_spin.setValue(self.product[3])
        layout.addRow("Stock:", self.stock_spin)
        
        # Price field
        self.price_spin = QDoubleSpinBox()
        self.price_spin.setRange(0, 1000000)
        self.price_spin.setDecimals(2)
        self.price_spin.setPrefix("$ ")
        if self.product:
            self.price_spin.setValue(self.product[4])
        layout.addRow("Precio:", self.price_spin)
        
        # Expiration date field
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        if self.product and self.product[6]:
            self.date_edit.setDate(QDate.fromString(self.product[6], "yyyy-MM-dd"))
        layout.addRow("Fecha de vencimiento:", self.date_edit)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_button = QPushButton("Guardar")
        save_button.clicked.connect(self.accept)
        save_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {APP['theme']['success_color']};
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: {APP['theme']['primary_color']};
            }}
        """)
        button_layout.addWidget(save_button)
        
        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.reject)
        cancel_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {APP['theme']['error_color']};
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: {APP['theme']['warning_color']};
            }}
        """)
        button_layout.addWidget(cancel_button)
        
        layout.addRow("", button_layout)

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
                self.table.setItem(row, 0, QTableWidgetItem(str(product['ID'])))
                self.table.setItem(row, 1, QTableWidgetItem(product['Nombre']))
                self.table.setItem(row, 2, QTableWidgetItem(product['Categoria']))
                self.table.setItem(row, 3, QTableWidgetItem(str(product['Cantidad_en_stock'])))
                self.table.setItem(row, 4, QTableWidgetItem(f"${product['Precio']:.2f}"))
                
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
            print(f"Error detallado: {str(e)}")  # Para debugging
            
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
            dialog = AddProductDialog(self, product)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                updated_data = {
                    'Nombre': dialog.name_edit.text(),
                    'Categoria': dialog.category_combo.currentText(),
                    'Cantidad_en_stock': dialog.stock_spin.value(),
                    'Precio': dialog.price_spin.value()
                }
                
                self.inventory_service.update_product(product['ID'], updated_data)
                self.load_inventory()
                QMessageBox.information(self, "Éxito", "Producto actualizado exitosamente")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al editar el producto: {str(e)}")
            print(f"Error detallado: {str(e)}")  # Para debugging
            
    def delete_product(self, product):
        """Delete a product from the inventory."""
        try:
            reply = QMessageBox.question(
                self, "Confirmar", 
                f"¿Está seguro de eliminar el producto {product['Nombre']}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.inventory_service.delete_product(product['ID'])
                self.load_inventory()
                QMessageBox.information(self, "Éxito", "Producto eliminado correctamente")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al eliminar el producto: {str(e)}")
            print(f"Error detallado: {str(e)}")  # Para debugging
            
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