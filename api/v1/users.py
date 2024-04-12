from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from schemas import Token, UserResponse

router = APIRouter(
    prefix="/users",
    # tags=["users"],
    # dependencies=[Depends(oauth2_scheme)],
    responses={404: {"description": "page not found"}},
)

@router.get("/")
async def read_users():
    return {"message": "Read users"}

@router.post("/", summary="Create a new user", response_model=UserResponse)
async def create_user(): 
    return {"message": "Create user"}