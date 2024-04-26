from fastapi import status
import http

class ResponseException(Exception):
    _filename = None
    def __init__(
        self,
        detail: str | None = None,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        headers: dict[str, str] | None = None,
    ) -> None:
        if detail is None:
            detail = http.HTTPStatus(status_code).phrase
        self.type =  http.HTTPStatus(status_code).phrase
        self.status_code = status_code
        self.detail = detail
        self.headers = headers

    def __str__(self) -> str:
        class_name = self.__class__.__name__
        return f"{str(self._filename)} {class_name}-{self.status_code}/{self.type } : {self.detail}"

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(status_code={self.status_code!r}, detail={self.detail!r})"
    