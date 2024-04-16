from pydantic import BaseModel, validator
from typing import Union, List, Annotated
from datetime import datetime

class UserResponse(BaseModel):
    username: str = None
    email: Union[str]= None
    # email: Optional[str]  = Field(None)  #  Union[str, None] = None
    is_active: bool = False
    is_supper_admin: bool = False
    has_roles:  Annotated[List[str], "List name Role"] = []
    has_permissions: Annotated[List[str], "List name Permission"] = []
    created_at: str= None
    last_login: str= None

    @validator('created_at', pre=True)  # pre=True để chạy trước khi giá trị được xác thực
    def datetime_to_str_created_at(cls, value):
        # Kiểm tra nếu giá trị đầu vào đã là datatime
        if isinstance(value, datetime):
            return datetime.strftime(value, '%d-%m-%Y %H:%M:%S')
        # Nếu không, giữ nguyên giá trị
        return value
    
    @validator('last_login', pre=True)  # pre=True để chạy trước khi giá trị được xác thực
    def datetime_to_str_last_login(cls, value):
        # Kiểm tra nếu giá trị đầu vào đã là datatime
        if isinstance(value, datetime):
            return datetime.strftime(value, '%d-%m-%Y %H:%M:%S')
        # Nếu không, giữ nguyên giá trị
        return value
    class Config:
        orm_mode = True

