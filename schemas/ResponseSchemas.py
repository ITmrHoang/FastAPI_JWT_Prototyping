from fastapi.responses import JSONResponse
from fastapi import status as _status_code
from pydantic import BaseModel, root_validator
from typing import Generic, TypeVar, List, Optional, Type,Any


class ResponseAPISchema(BaseModel):
    status: Any = None
    error: Optional[Any] = None
    data: Optional[Any] = None
    

#TODO validate response cấp cao hơn 
# # Định nghĩa kiểu dữ liệu cho User
# class User:
#     def __init__(self, ...):  # Định nghĩa các trường dữ liệu của User
#         pass

# # Định nghĩa kiểu dữ liệu cho responseData
T = TypeVar('T', str, list, dict, BaseModel)


class ResponseData(BaseModel, Generic[T]):
    data: Optional[T]
    status: Optional[int] = 200
    error: Optional[Any] = None
    def int(self, data:T = None, status=200, error=None):
        self.data = data
        self.status = status
        self.error = error
        return self
class ResponsePagination(ResponseData):
    page: int = 1
    page_size: int = 10
    total_count: int = 0


# Sử dụng kiểu dữ liệu của User cho trường data của ResponseData
# Response = ResponseData[User]