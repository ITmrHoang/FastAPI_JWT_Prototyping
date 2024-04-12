from pydantic import BaseModel, Field, UUID4 as UUID
from typing import Union, Optional,Annotated, List
from datetime import datetime
from schemas.PermissionSchema import Permission

class Role(BaseModel):
    id: Union[UUID]
    name: str = Field(..., description="name is string value permission")
    description: Annotated[Union[str],"name is string value permission"]
    permissions: List[Permission] = []
    # permissions: List['Permission'] = [] #XXX python tự tìm module permission trong cùng folder nếu không được import nhưng swagers khi render không tự tìm được nên lỗi
    
    class Config:
        orm_mode = True