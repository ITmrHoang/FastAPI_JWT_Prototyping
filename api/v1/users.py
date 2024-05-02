from fastapi import APIRouter, Depends, Security, Form, Body, UploadFile, Query, File
from fastapi.responses import JSONResponse

from schemas import UserResponse, CreateUserRequest, AssignPermissionRequest, AssignRoleRequest, UpdateUserRequest
from schemas.ResponseSchemas import ResponseData, ResponsePagination
from core.database import oauth2_scheme, get_global_request_db
from utils import get_token_info
from models.UserModel import User
from typing import Annotated, Optional, List
# from api.dependencies import check_header_has_authorization
from core import ResponseException
from services.permission_service import PermissionService
from services.role_service import RoleService
from core import ResponseException as RException

ResponseException._filename = __file__

router = APIRouter(
    # prefix="/users",
    tags=["users"],
    # dependencies=[Security(oauth2_scheme)],
    responses={404: {"description": "page not found"}},
)

@router.get("/", response_model=ResponseData)
async def read_users(page: Optional[int] = None, page_size: Optional[int] =None):
    if page is not None and page_size is not None:
        data, count = User.search(page=page, page_size=page_size)
        return ResponsePagination(data=data, total_count=count)
    else:
        data = User.search()
    return ResponseData(data=data)

@router.get("/{user}", summary="get infor user", response_model=ResponseData)
async def get_user(user): 
    iuser = User.get_by_username(user)
    if iuser is None:
        try: 
            iuser  = User.get(user) 
        except:
            raise ResponseException('Dont have a user matching')
    return ResponseData(data=iuser.getJson())

@router.post("/assign-permission", response_model=ResponseData)
async def user_assign_permission( form: AssignPermissionRequest):
    user = User.get_by_username(form.user, get_global_request_db())
    if user is None:
        raise ResponseException('Dont have a user matching')
    permisions = PermissionService().whereIn('name', form.permissions).all()
   
    if permisions is None or len(permisions) == 0:
        raise ResponseException('Dont have a permision')
    else:
        user.clear_permissions()
        user.assign_permission(permisions)
    return ResponseData(data=user.getJson())

@router.post("/assign-role", response_model=ResponseData)
async def user_assign_permission( form: AssignRoleRequest):
    user = User.get_by_username(form.user, get_global_request_db())
    if user is None:
        raise ResponseException('Dont have a user matching')
    role = RoleService().whereIn('name', form.role).all()
   
    if role is None or len(role) == 0:
        raise ResponseException('Dont have a permision')
    else:
        user.assign_role(role)
    return ResponseData(data=user.getJson())


@router.post("/", summary="Create a new user", response_model=ResponseData)
@router.post("/register", summary="register", response_model=ResponseData)
async def create_user(user: Annotated[CreateUserRequest, str]): 
    user_dict = user.dict()
    iuser  = User.create(**user_dict)

    return ResponseData(data=iuser.getJson())
@router.patch("/{user}", summary="update  user", response_model=ResponseData)
async def patch_user(user: str, form : Annotated[UpdateUserRequest, str], db = Depends(get_global_request_db)): 
    print('\n\napi', db)
    iuser = User.get_by_username(user, db)
    if iuser is None:
        try: 
            iuser  = User.get(user, db) 
        except:
            iuser = None
    if iuser is None:
        raise ResponseException('Dont have a user matching')

    iuser.update(name= 'aaa', rq=form)
    return ResponseData(data=iuser.getJson())


@router.delete("/{user}", summary="get infor user", response_model=ResponseData)
async def get_user(user, db = Depends(get_global_request_db)): 
    iuser = User.get_by_username(user, db)
    if iuser is None:
        try: 
            iuser  = User.get(user, db) 
        except:
            iuser = None
    if iuser is None:
        raise ResponseException('Dont have a user matching')
    iuser.delete(db)
    return ResponseData(data="delete user successfully")
