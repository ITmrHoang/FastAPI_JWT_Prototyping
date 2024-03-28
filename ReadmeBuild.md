# Install Python

============================================

# Install package python

## install virtualenv create env

    python -m pip install --user virtualenv
    python -m virtualenv <name_env>

    or

    pip install virtualenv
    virtualenv --python C:\Path\To\Python\python.exe venv

## package

    pip install SQLAlchemy fastapi-utils psycopg2

# export auto package use to requirements.txt python

`pip freeze > requirements.txt`

## Docker postgsql (psycopg2)

docker : docker-compose.yml

```

```

## access to env

`.\vsiem_env\Scripts\activate `

## alembic migration

### note

. cần import các class model vào file env.py
. import Base từ model
. gán target_metadata = Base.metadata

### setup

```
  pip install alembic
  alembic init alembic
```

### auto create migration

`alembic revision --autogenerate -m "New migration "`

### apply migration

`alembic upgrade head`

### một số lệnh thường dùng

.Autogenerate:
`alembic revision --autogenerate -m <message>`
.Tạo 1 migration:
`alembic revision -m <message> `
.Hiển thị version hiện tại database
`alembic current`
.Migration history:
`alembic history --verbose`
.Revert tất cả migrations:
`alembic downgrade base`
.Revert migrations one by one:
`alembic downgrade -1`
.Áp dụng all migrations:
`alembic upgrade head`
.Áp dụng migrations one by one:
`alembic upgrade +1`
.Hiển thị all raw SQL:như craete , delete alter ...
`alembic upgrade head --sql`
.Reset the database:
`alembic downgrade base && alembic upgrade head`

#

### documents

[base and postgesql](https://codevoweb.com/build-a-crud-app-with-fastapi-and-sqlalchemy/)

# [stuct forder ](https://www.youtube.com/watch?v=G8MsHbCzyZ4)

- main.py : Điểm truy cập cho ứng dụng FastAPI.
- api/ : Chứa mã dành riêng cho API. có thể có Phiên bản API :

  - v1
  - v2

- endpoints/ : Triển khai điểm cuối riêng lẻ.
- core/ : Chức năng ứng dụng cốt lõi.
- config.py : Cài đặt cấu hình.
  - security.py : Các chức năng liên quan đến bảo mật.
  - databse.py : Thiết lập kết nối cơ sở dữ liệu.
- dependencies/ : Mã liên quan đến phụ thuộc.
  - authentication.py : Phụ thuộc xác thực.
- models/ : mô hình SQLAlchemy.
- schemas/ : Mô hình Pydantic định nghĩa dữ liệu ORM
- test/ : Các trường hợp thử nghiệm cho ứng dụng.
- utils/ : Các hàm tiện ích.
- main.py : Điểm vào chính để chạy ứng dụng FastAPI.
- .env : Cấu hình biến môi trường.
- Dockerfile : Cấu hình Docker để container hóa.
- requirements.txt : Danh sách các phụ thuộc Python.
- docker-compose.yml : Cấu hình Docker Compose để chạy ứng dụng trong vùng chứa.

# [setup pgadmin](https://stackoverflow.com/questions/25540711/docker-postgres-pgadmin-local-connection)

Thực hiện docker psđể lấy id vùng chứa và sau đódocker inspect <dockerContainerId_postgers> | grep IPAddress
or dùng network

# NOTE

1. khi connect các container trong docker bằng network docker các container sẽ liên kết với nhau bằng network trong mạng ảo docker không phải host nên dùng port trong docker không phải port bind ra ngoài

# other

. clear cache python **pycache**
`find . -type d -name  "__pycache__" -exec rm -r {} +`

## dynamic import model and class trong folder models

```
import os
import sys
from importlib import import_module
BASE_DIR= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.abspath(os.path.join(BASE_DIR, 'models'))
# Thêm đường dẫn của thư mục models vào sys.path
sys.path.append(MODEL_PATH)
sys.path.append(BASE_DIR)

# Lấy danh sách tất cả các file trong thư mục models
model_files = [f[:-3] for f in os.listdir(MODEL_PATH) if f.endswith('.py') and f != '__init__.py']

# Import tất cả các class model từ các file trong thư mục models
for model_file in model_files:
    module = import_module(f'models.{model_file}')
    classes = [cls for cls in module.__dict__.values() if isinstance(cls, type)]
    print({cls.__name__: cls for cls in classes if cls.__module__ == module.__name__})
    globals().update({cls.__name__: cls for cls in classes if cls.__module__ == module.__name__})
```

```
import os
import sys
from importlib import import_module
BASE_DIR= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOLDER_PATH = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
CURRENT_FOLDE_NAME = os.path.basename(os.path.dirname(FOLDER_PATH))
# Thêm đường dẫn của thư mục  vào sys.path
sys.path.append(BASE_DIR)
sys.path.append(FOLDER_PATH)

# # load class trong  module thư mục hiện tại
# Lấy danh sách tất cả các file trong thư mục hiện tại
#module_files = [f[:-3] for f in os.listdir(FOLDER_PATH) if f.endswith('.py') and f != '__init__.py']

# # # Import tất cả các class model từ các file trong thư mục hiện tại
# for module_file in module_files:
#     module = import_module(f'{CURRENT_FOLDER_NAME}.{module_file}')
#     classes = [cls for cls in module.__dict__.values() if isinstance(cls, type)]
#     print(classes)
#     for cls in classes:
#         print(module_file, 'clss', cls.__module__, module.__name__, sep=' 00  ---- ----00')
#     globals().update({cls.__name__: cls for cls in classes if cls.__module__ == module.__name__})

## load class toàn bộ class trong folder hiện tại và sub folder của nó
def get_path_module(directory):
    path_list = []
    for root, dirs, files in os.walk(directory):
        base_name = os.path.basename(root)
        if base_name == "__pycache__": continue 
        file_name_list = [ f for f in files if f.endswith('.py') and f != '__init__.py']
        for f in file_name_list:
            path = os.path.join(root,f)
            path_list.append(path)
        # for file in files:
            # file_path = os.path.join(root, file)
            # files_list.append(file_path)
    # remove base path
    result = []
    for path in path_list:
        # # Sử dụng str.replace()
        # relative_path = path.replace(root_folder, '')

        # # Hoặc sử dụng str.split()
        # relative_path = path.split(root_folder)[1]
        relative_path = os.path.relpath(path, BASE_DIR)
        ## os.sep là hằng số ký tự phân cách tương ứng với hệ điều hành
        str_module = relative_path[:-3].replace(os.sep, ".")
        result.append(str_module)
    return result

path_module = get_path_module(FOLDER_PATH)

for module_path in path_module:
    module = import_module(f'{module_path}')
    classes = [cls for cls in module.__dict__.values() if isinstance(cls, type)]
    globals().update({cls.__name__: cls for cls in classes if cls.__module__ == module.__name__})


```

## dyamic import file route

```
# Đường dẫn tới thư mục chứa các file routers
routers_dir = "routers"

# Duyệt qua các file trong thư mục
for file_name in os.listdir(routers_dir):
    # Kiểm tra nếu là file Python
    if file_name.endswith(".py"):
        # Import module và thêm router vào ứng dụng chính
        module_name = f"routers.{file_name[:-3]}"  # Loại bỏ phần mở rộng .py
        module = __import__(module_name, fromlist=["router"])
        app.include_router(module.router)

```

## get subforder

```
  subdirectories = [folder for folder in os.listdir(path) if os.path.isdir(os.path.join(path, folder))]
```

```

def get_subdirectories(path, excluded_names=None):
  # Lấy tất cả các tệp và thư mục trong thư mục hiện tại
  contents = os.listdir(path)
  subdirectories = []
  for item in contents:
      item_path = os.path.join(path, item)
      if os.path.isdir(item_path) and item not in excluded_names and not item.startswith('.'):
          subdirectories.append(item)
  return subdirectories

# Lấy tất cả các thư mục trong thư mục hiện tại, loại bỏ các thư mục trong danh sách được chỉ định và các thư mục bắt đầu bằng dấu '.'
current_directory = os.getcwd()
excluded_names = ["__pycache__", ".git"]
subdirectories = get_subdirectories(current_directory, excluded_names)

print("Các thư mục trong thư mục hiện tại:")
for directory in subdirectories:
  print(directory)

```

## custome orm model

base

```
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# SQLAlchemy configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FastAPI app
app = FastAPI()

# Dependency to get database session
def get_db():
   db = SessionLocal()
   try:
       yield db
   finally:
       db.close()

# SQLAlchemy ORM model
class User(Base):
   __tablename__ = "users"

   id = Column(Integer, primary_key=True, index=True)
   name = Column(String, index=True)
   email = Column(String, unique=True, index=True)

   @classmethod
   def create(cls, db: Session, name: str, email: str):
       user = cls(name=name, email=email)
       db.add(user)
       db.commit()
       db.refresh(user)
       return user

   @classmethod
   def get(cls, db: Session, user_id: int):
       return db.query(cls).filter(cls.id == user_id).first()

   def update(self, db: Session, name: str, email: str):
       self.name = name
       self.email = email
       db.add(self)
       db.commit()
       db.refresh(self)
       return self

   def delete(self, db: Session):
       db.delete(self)
       db.commit()
       return self

# Create table
Base.metadata.create_all(bind=engine)

# Example usage
if __name__ == "__main__":
   # Example of CRUD operations
   # Create a user
   with SessionLocal() as session:
       created_user = User.create(db=session, name="John Doe", email="john@example.com")
       print("Created user:", created_user.id, created_user.name, created_user.email)

       # Retrieve a user by ID
       retrieved_user = User.get(db=session, user_id=created_user.id)
       print("Retrieved user by ID:", retrieved_user.id, retrieved_user.name, retrieved_user.email)

       # Update a user
       updated_user = retrieved_user.update(db=session, name="Jane Doe", email="jane@example.com")
       print("Updated user:", updated_user.id, updated_user.name, updated_user.email)

       # Delete a user
       deleted_user = updated_user.delete(db=session)
       print("Deleted user:", deleted_user.id, deleted_user.name, deleted_user.email)

```

update

```
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Any, Dict

# SQLAlchemy configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FastAPI app
app = FastAPI()

# Dependency to get database session
def get_db():
   db = SessionLocal()
   try:
       yield db
   finally:
       db.close()

# SQLAlchemy ORM model
class User(Base):
   __tablename__ = "users"

   id = Column(Integer, primary_key=True, index=True)
   name = Column(String, index=True)
   email = Column(String, unique=True, index=True)

   @classmethod
   def create(cls, db: Session, **kwargs: Dict[str, Any]):
       user = cls(**kwargs)
       db.add(user)
       db.commit()
       db.refresh(user)
       return user

   @classmethod
   def get(cls, db: Session, user_id: int):
       return db.query(cls).filter(cls.id == user_id).first()

   def update(self, db: Session, **kwargs: Dict[str, Any]):
       for attr, value in kwargs.items():
           setattr(self, attr, value)
       db.add(self)
       db.commit()
       db.refresh(self)
       return self

   def delete(self, db: Session):
       db.delete(self)
       db.commit()
       return self

# Create table
Base.metadata.create_all(bind=engine)

# Example usage
if __name__ == "__main__":
   # Example of CRUD operations
   # Create a user
   with SessionLocal() as session:
       try:
           created_user = User.create(db=session, name="John Doe", email="john@example.com")
           print("Created user:", created_user.id, created_user.name, created_user.email)

           # Retrieve a user by ID
           retrieved_user = User.get(db=session, user_id=created_user.id)
           print("Retrieved user by ID:", retrieved_user.id, retrieved_user.name, retrieved_user.email)

           # Update a user
           updated_user = retrieved_user.update(db=session, name="Jane Doe", email="jane@example.com")
           print("Updated user:", updated_user.id, updated_user.name, updated_user.email)

           # Delete a user
           deleted_user = updated_user.delete(db=session)
           print("Deleted user:", deleted_user.id, deleted_user.name, deleted_user.email)
       except Exception as e:
           print(f"An error occurred: {e}")
````
