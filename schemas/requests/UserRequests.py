from pydantic import BaseModel,UUID4 as UUID
from typing import Union, List, Optional
from schemas import Role,Permission
from fastapi import UploadFile

class CreateUserRequest(BaseModel):
    username: str
    email: Union[str]
    password: Union[str]
    password_confirmation: Union[str]
    is_supper_admin: Optional[bool] = False
    is_active: Optional[bool] = False

class AssignPermissionRequest(BaseModel):
    user: str
    permissions: List[str]

    
class AssignRoleRequest(BaseModel):
    user: str
    roles: List[str]
