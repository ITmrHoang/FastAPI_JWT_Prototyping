from core.database import BaseService
from models import Role
class RoleService(BaseService[Role]):
    def set_model(self):
        self.model = Role
