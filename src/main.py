import sys
from PyQt6.QtWidgets import QApplication
from views.login_window import LoginWindow
from services.auth_service import AuthService
from services.inventory_service import InventoryService

def main():
    """Main application entry point."""
    # Create application instance
    app = QApplication(sys.argv)
    
    # Initialize services
    auth_service = AuthService("src/usuarios.db")
    inventory_service = InventoryService("src/inventario.db")
    
    # Create and show login window
    login_window = LoginWindow(auth_service)
    login_window.show()
    
    # Start application event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
