"""
Controlador para gestionar los proveedores.
"""

from src.models.proveedor import Proveedor
from src.config.constants import ERROR_MESSAGES, SUCCESS_MESSAGES, DB_TABLES

class ProveedoresController:
    """
    Controlador para gestionar los proveedores.
    Coordina las operaciones entre la vista de proveedores y los servicios/modelos.
    """
    
    def __init__(self, db_service):
        """
        Inicializa el controlador de proveedores.
        
        Args:
            db_service (DatabaseService): Servicio de base de datos.
        """
        self.db_service = db_service
    
    def get_all_providers(self):
        """
        Obtiene todos los proveedores.
        
        Returns:
            list: Lista de objetos Proveedor.
        """
        try:
            query = "SELECT * FROM Proveedores ORDER BY razon_social"
            providers_data = self.db_service.fetch_all(query)
            return [Proveedor.from_dict(provider) for provider in providers_data]
        except Exception as e:
            print(f"Error al obtener proveedores: {e}")
            return []
    
    def get_provider_by_nit(self, nit):
        """
        Obtiene un proveedor por su NIT.
        
        Args:
            nit (str): NIT del proveedor.
            
        Returns:
            Proveedor: Objeto Proveedor o None si no existe.
        """
        try:
            query = "SELECT * FROM Proveedores WHERE NIT = ?"
            provider_data = self.db_service.fetch_one(query, (nit,))
            return Proveedor.from_dict(provider_data) if provider_data else None
        except Exception as e:
            print(f"Error al obtener proveedor: {e}")
            return None
    
    def add_provider(self, provider_data):
        """
        Agrega un nuevo proveedor.
        
        Args:
            provider_data (dict): Datos del proveedor a agregar.
            
        Returns:
            dict: Resultado de la operación.
        """
        try:
            # Validar datos de entrada
            proveedor = Proveedor.from_dict(provider_data)
            if not proveedor.nit or not proveedor.razon_social:
                return {'error': ERROR_MESSAGES['empty_fields']}
            
            # Verificar si ya existe un proveedor con el mismo NIT
            existing = self.get_provider_by_nit(proveedor.nit)
            if existing:
                return {'error': 'Ya existe un proveedor con este NIT'}
            
            # Agregar proveedor
            result = self.db_service.insert(DB_TABLES['proveedores'], proveedor.to_dict())
            
            if result:
                return {
                    'success': True,
                    'message': SUCCESS_MESSAGES['provider_added'],
                    'provider': proveedor
                }
            else:
                return {'error': ERROR_MESSAGES['provider_add_error']}
        except Exception as e:
            return {'error': f'Error al agregar proveedor: {str(e)}'}
    
    def update_provider(self, nit, provider_data):
        """
        Actualiza un proveedor existente.
        
        Args:
            nit (str): NIT del proveedor a actualizar.
            provider_data (dict): Nuevos datos del proveedor.
            
        Returns:
            dict: Resultado de la operación.
        """
        try:
            # Validar datos de entrada
            proveedor = Proveedor.from_dict(provider_data)
            if not proveedor.razon_social:
                return {'error': ERROR_MESSAGES['empty_fields']}
            
            # Verificar si existe el proveedor
            existing = self.get_provider_by_nit(nit)
            if not existing:
                return {'error': 'Proveedor no encontrado'}
            
            # Actualizar proveedor
            result = self.db_service.update(
                DB_TABLES['proveedores'],
                proveedor.to_dict(),
                {'NIT': nit}
            )
            
            if result:
                return {
                    'success': True,
                    'message': SUCCESS_MESSAGES['provider_updated'],
                    'provider': proveedor
                }
            else:
                return {'error': ERROR_MESSAGES['provider_update_error']}
        except Exception as e:
            return {'error': f'Error al actualizar proveedor: {str(e)}'}
    
    def delete_provider(self, nit):
        """
        Elimina un proveedor.
        
        Args:
            nit (str): NIT del proveedor a eliminar.
            
        Returns:
            dict: Resultado de la operación.
        """
        try:
            # Verificar si existe el proveedor
            existing = self.get_provider_by_nit(nit)
            if not existing:
                return {'error': 'Proveedor no encontrado'}
            
            # Verificar si hay productos asociados al proveedor
            query = "SELECT COUNT(*) as count FROM Producto WHERE NIT_proveedor = ?"
            result = self.db_service.fetch_one(query, (nit,))
            
            if result and result['count'] > 0:
                return {'error': 'No se puede eliminar el proveedor porque tiene productos asociados'}
            
            # Eliminar proveedor
            result = self.db_service.delete_where(
                DB_TABLES['proveedores'],
                {'NIT': nit}
            )
            
            if result:
                return {
                    'success': True,
                    'message': SUCCESS_MESSAGES['provider_deleted']
                }
            else:
                return {'error': ERROR_MESSAGES['provider_delete_error']}
        except Exception as e:
            return {'error': f'Error al eliminar proveedor: {str(e)}'}
    
    def search_providers(self, search_term):
        """
        Busca proveedores por razón social o NIT.
        
        Args:
            search_term (str): Término de búsqueda.
            
        Returns:
            list: Lista de objetos Proveedor que coinciden con la búsqueda.
        """
        try:
            query = """
                SELECT * FROM Proveedores 
                WHERE razon_social LIKE ? OR NIT LIKE ?
                ORDER BY razon_social
            """
            search_pattern = f"%{search_term}%"
            providers_data = self.db_service.fetch_all(query, (search_pattern, search_pattern))
            return [Proveedor.from_dict(provider) for provider in providers_data]
        except Exception as e:
            print(f"Error al buscar proveedores: {e}")
            return []
    
    def format_provider_for_display(self, proveedor):
        """
        Formatea un proveedor para su visualización en la interfaz.
        
        Args:
            proveedor (Proveedor): Proveedor a formatear.
            
        Returns:
            tuple: Tupla con los datos formateados del proveedor.
        """
        return (
            proveedor.nit,
            proveedor.razon_social,
            proveedor.direccion or "",
            proveedor.telefono or "",
            proveedor.email or ""
        )
