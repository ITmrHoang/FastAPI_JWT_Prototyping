from core.database import BaseService
from models import Permission
class PermissionService(BaseService[Permission]):
    def set_model(self):
        self.model = Permission
