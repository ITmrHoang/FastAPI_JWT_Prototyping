from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from models import User
from core import get_db, SessionLocal
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from schemas import ResponseAPISchema, UserResponse
from utils.responses import ResponseAPI
from utils import verify_password
from utils.authentication import create_access_token, create_refresh_token

from utils import errorResponse, susscessResponse



from schemas import Token

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

@router.post("/token", name="getToken", response_model=Token)
@router.post("/login",  response_model=Token, responses={404: {"model": ResponseAPISchema}})
async def login(form_data: OAuth2PasswordRequestForm = Depends()):

    user = User.getUserByUsername(form_data.username)


    if user is None:
        return errorResponse(
            message="Don't have a user with that username"
        )
  
    hashed_pass = user.hashed_password
    salt= user.salt

    if not verify_password(form_data.password + salt, hashed_pass):
         return errorResponse(
            message="Incorrect  username or password"
        )
    
    print(UserResponse(**user.__dict__))
    return {
        "access_token": 1,
        "refresh_token": 2
    }
    # if user is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Incorrect email or password"
    #     )

    # hashed_pass = user['password']
    # if not verify_password(form_data.password, hashed_pass):
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Incorrect email or password"
    #     )
    
    # return {
    #     "access_token": create_access_token(user['email']),
    #     "refresh_token": create_refresh_token(user['email']),
    # }