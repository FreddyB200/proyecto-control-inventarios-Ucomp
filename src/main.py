import sys
from PyQt6.QtWidgets import QApplication
from src.views.login_window import LoginWindow
from src.config.settings import APP
from src.utils.database_init import init_database

def main():
    """Main application entry point."""
    try:
        # Initialize database
        init_database()
        
        # Create application
        app = QApplication(sys.argv)
        
        # Set application name and version
        app.setApplicationName(APP["name"])
        app.setApplicationVersion(APP["version"])
        
        # Create and show login window
        login_window = LoginWindow()
        login_window.show()
        
        # Start application event loop
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"Error al iniciar la aplicación: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
