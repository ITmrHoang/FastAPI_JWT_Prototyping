from fastapi.responses import JSONResponse
from fastapi import status
import typing
from pydantic import BaseModel



class BaseResponse(BaseModel):
    status: typing.Any = None
    error: typing.Optional[typing.Any] = None
    content: typing.Any 
    

class ResponseAPI(JSONResponse):
    def __init__(
    self,
    content: typing.Any = None, 
    status_code: int = status.HTTP_200_OK,
    error: dict= None,
    message: str = None,
    headers: typing.Mapping[str, str] | None = None,
    media_type: str | None = None,
    background: typing.Any | None = None,
    ) -> None:
        if error:
            content = {"status": 0, "error": error, "data": None, "message": message}
        else:
            content = {"status": 1, "error": None,  "data": content,  "message": message}
        if  status_code >= 400 and status_code <= 600 and error is None:
             content.update({"status": 0, "error": content.get("data", None)})
        super().__init__(content, status_code, headers, media_type, background)