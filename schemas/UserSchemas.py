from pydantic import BaseModel, UUID4 as UUID, validator
from typing import Union, Optional, List, Annotated
from datetime import datetime
from schemas import Role,Permission

class User(BaseModel):
    id= Union[UUID]
    username: str
    email: Union[str]
    # email: Optional[str]  = Field(None)  #  Union[str, None] = None
    hashed_password= Union[str]
    is_active: bool = False
    is_supper_admin: bool = False
    _last_login: datetime
    _created_at: datetime
    roles: List[Role] = []
    permissions: List[Permission] = []

    @property
    def created_at(self) -> str:
        return self._created_at.strftime('%d/%m/%Y %H:%M')

    @created_at.setter
    def created_at(self, value: Union[str, datetime]):
        if isinstance(value, str):
            self._created_at = datetime.strptime(value, '%d/%m/%Y %H:%M')
        elif isinstance(value, datetime):
            self._created_at = value
        else:
            raise ValueError("Invalid value type for created_at")
    
    @property
    def last_login(self) -> str:
        return self._last_login.strftime('%d/%m/%Y %H:%M')

    @last_login.setter
    def last_login(self, value: Union[str, datetime]):
        if isinstance(value, str):
            self._last_login = datetime.strptime(value, '%d/%m/%Y %H:%M')
        elif isinstance(value, datetime):
            self._last_login = value
        else:
            raise ValueError("Invalid value type for created_at")

    class Config:
        orm_mode = True


class UserDataToken(BaseModel):
    username: str = None
    email: Union[str]= None
    # email: Optional[str]  = Field(None)  #  Union[str, None] = None
    is_active: bool = False
    is_supper_admin: bool = False
    has_roles: List[str] = []
    has_permissions: List[str] = []

    def __getitem__(self, key):
        return self.get(key)
    def get(self,  filed):
        return getattr(self, filed)

    class Config:
        orm_mode = True

