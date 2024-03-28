from pydantic import BaseModel, Field, UUID4 as UUID
from typing import Union, Optional,Annotated, List
from datetime import datetime

class Role(BaseModel):
    id: Union[UUID]
    name: str = Field(..., description="name is string value permission")
    description: Annotated[Union[str],"name is string value permission"]
    permissions: List["Permission"] = []
    
    class Config:
        orm_mode = True