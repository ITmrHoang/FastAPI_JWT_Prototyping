from pydantic import BaseModel,UUID4 as UUID
from typing import Union, List
from schemas import Role,Permission

class CreateUserRequest(BaseModel):
    username: str
    email: Union[str]
    password: Union[str]
    password_confirmation: Union[str]
    roles: List[Role] = []
    permissions: List[Permission] = []

    