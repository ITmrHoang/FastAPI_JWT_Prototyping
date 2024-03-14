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

. dynamic import model and class trong folder models

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
