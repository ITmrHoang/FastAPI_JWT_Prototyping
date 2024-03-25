from pydantic import BaseModel
from typing import  Optional


class Token(BaseModel):
    token_type: str = "Bearer"
    access_token: str
    refresh_token: Optional[str]
    
