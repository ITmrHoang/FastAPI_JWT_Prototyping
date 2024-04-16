from typing import Union

from fastapi import FastAPI, Query, Path, Request, Body, Response, Form
from core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from core import constant, get_subdirectories, BASE_DIR
from api import auth as auth_router
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, ResponseValidationError

# load env in file .env
import os 
from dotenv import load_dotenv
# #Đặt đường dẫn cho tập tin .env
#dotenv_path = '/path/to/your/.env'
## Load biến môi trường từ tập tin .env tại đường dẫn tùy chỉnh
#load_dotenv(dotenv_path)
load_dotenv()
app = FastAPI(root_path="/api",title="VSIEM", summary="create by HiMoDev", openapi_url='/openapi.json')

# Middleware to handle validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content={"detail": "Validation error",
                                                   "data": exc._errors})

@app.exception_handler(ResponseValidationError)
async def response_validation_exception_handler(request: Request, exc: ResponseValidationError):
    return JSONResponse(status_code=400, content={"detail": "Response validation error",
                                                  "data": exc._errors})

# app.include_router(auth_router)
# auto import route in api 
app.include_router(auth_router.router)

ROUTER_DIR = os.path.join(BASE_DIR, 'api')

excluded_folder = ["__pycache__", "dependencies", "middleware"]

LIST_PATH_ROUTE = get_subdirectories(ROUTER_DIR, excluded_folder)

# duyệt list subfolder trong api
for folder in LIST_PATH_ROUTE:
    path_version = os.path.join(ROUTER_DIR,folder)
    print(path_version)
# # Duyệt qua các file trong thư mục
    for file_name in os.listdir(path_version):
        # Kiểm tra nếu là file Python
        if file_name.endswith(".py"):
            try:
#               # Import module và thêm router vào ứng dụng chính
                module_name = f"api.{folder}.{file_name[:-3]}"  # Loại bỏ phần mở rộng .py
                module = __import__(module_name, fromlist=["router"])
                if hasattr(module, "router"):
                    # Module chứa router, bạn có thể truy cập nó bình thường có thể đặt prefix tại đây hoặc bỏ cài trong router nếu để cả 2 sẽ concat prefix
                    app.include_router(module.router, prefix=f"/{folder}/{file_name[:-3]}")
                else:
                    # Module không chứa router, xử lý tùy ý
                    print(f"Không tìm thấy router trong module: {module_name}")
            except Exception as e: 
                print(f"error import router file in {file_name}: \n {e}")
           

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {
        "infor": "FastAPI_JWT_Prototyping",
        "createby": "HiModev",
        "github": "https://github.com/ITmrHoang/FastAPI_JWT_Prototyping.git",
        "contact": "itmrhoang@gmail.com",
        "phone": "0582625538",
        "donate": ""
        }

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

# @app.get("/items/{item_id}")
# async def read_items(
#     item_id: int = Path(title="The ID of the item to get"),
#     q: Union[str, None] =  Body(default=None, alias="item-query"),
# ):
#     results = {"item_id": item_id}
#     if q:
#         results.update({"q": str(q)})
#     return results