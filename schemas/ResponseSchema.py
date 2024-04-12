from fastapi.responses import JSONResponse
from fastapi import status
import typing
from pydantic import BaseModel
from typing import Generic, TypeVar, List


class ResponseAPISchema(BaseModel):
    status: typing.Any = None
    error: typing.Optional[typing.Any] = None
    content: typing.Any 
    

#TODO validate response cấp cao hơn 
# # Định nghĩa kiểu dữ liệu cho User
# class User:
#     def __init__(self, ...):  # Định nghĩa các trường dữ liệu của User
#         pass

# # Định nghĩa kiểu dữ liệu cho responseData
T = TypeVar('T')

class ResponseData(Generic[T]):
    def __init__(self, status: int, data: T):
        self.status = status
        self.data = data

# Sử dụng kiểu dữ liệu của User cho trường data của ResponseData
# Response = ResponseData[User]