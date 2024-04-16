from fastapi import APIRouter, Depends, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from schemas import UserResponse, ResponseAPISchema
from schemas.ResponseSchemas import ResponseData, ResponsePagination
from core.database import oauth2_scheme
from models.UserModel import User
# from api.dependencies import check_header_has_authorization

router = APIRouter(
    # prefix="/users",
    tags=["users"],
    # dependencies=[Security(oauth2_scheme)],
    responses={404: {"description": "page not found"}},
)

@router.get("/")
async def read_users(page: int | None = 1, page_size: int | None = 10):
    data = User.search()
    return data
    # return ResponsePagination(data=data)
# @router.post("/", summary="Create a new user", response_model=UserResponse)
# async def create_user(): 
#     return {"message": "Create user"}