from fastapi.responses import JSONResponse
from fastapi import status
import typing
from pydantic import BaseModel



class ResponseAPISchema(BaseModel):
    status: typing.Any = None
    error: typing.Optional[typing.Any] = None
    content: typing.Any 
    