from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
from fastapi_utils.guid_type import setup_guids_postgresql
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session
from fastapi import Depends
from typing import Any, Dict, TypeVar, Generic
from uuid import UUID
from fastapi.security import OAuth2PasswordBearer
import inspect

# POSTGRES_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOSTNAME}:{settings.DATABASE_PORT}/{settings.POSTGRES_DB}"
POSTGRES_URL = URL.create(
    "postgresql+psycopg2",
    username=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD,  # plain (unescaped) text
    host=settings.POSTGRES_HOSTNAME, # dùng khi run bằng docker
    # host=settings.POSTGRES_HOST,  # dùng khi run trực tiếp
    database=settings.POSTGRES_DB,
    # port=settings.DATABASE_PORT # dùng khi chạy môi trường ngoài nếu chạy docker thì đang trong netwwrok ảo dùng port mặc định db là dk
)

engine = create_engine(
    POSTGRES_URL, echo=True
)
with engine.connect() as connection:
    connection.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto"')
# dùng trục tiếp session engine

# session = Session(engine)
#  stmt = select(User).where(User.name.in_(["spongebob", "sandy"]))
#  for user in session.scalars(stmt):
#   print(user)
###---------------------------------##
# from sqlalchemy.orm import Session
# with Session(engine) as session:
#     spongebob = User(
#         name="spongebob",
#         fullname="Spongebob Squarepants",
#         addresses=[Address(email_address="spongebob@sqlalchemy.org")],
#     )
#     sandy = User(
#         name="sandy",
#         fullname="Sandy Cheeks",
#         addresses=[
#             Address(email_address="sandy@sqlalchemy.org"),
#             Address(email_address="sandy@squirrelpower.org"),
#         ],
#     )
#     patrick = User(name="patrick", fullname="Patrick Star")
#     session.add_all([spongebob, sandy, patrick])
#     session.commit()


setup_guids_postgresql(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/login",
)


# có thể tạo BaseORM module để các model kế thừa như sau
class BaseORM:
 
    @classmethod
    def search(cls, page=1, page_size=10, db: Session = next(get_db())):
        try:
            if page < 1:
                page = 1
            offset = (page - 1) * page_size
            instance = db.query(cls).order_by(cls.id).limit(page_size).offset(offset)
            result = [ item.getJson() for item in instance]  
            """  getJSon() hàm sẽ gọi tới các cột relastion nên sẽ \
            get data relastion nếu không có chỉ get các field của model đó không có relationship"""
            return result
        except:
           db.close()
    def getJson(self):
        item = self.to_dict()
        return item
    @classmethod
    def get(cls, id: int | str, db: Session = SessionLocal()):
        #NOTE không cần kiểm tra cột id là uuid và chuyển thành kiểu tương ứng vì SQLAlchemy tự động chuyển đổi kiểu dữ liệu nếu cột đó là UUID
        # from sqlalchemy.dialects.postgresql import UUID
        # import uuid
        # if isinstance(cls.id.type , UUID):
        # id = uuid.UUID(id)

        instance = db.query(cls).filter(cls.id == id).first()
        return instance
    @classmethod 
    def create (cls, db: Session = next(get_db()), **kwargs: Dict[str, Any]):# cách 1 , Session= SessionLocal() # cách 2 
        try:
            obj = cls(**kwargs)
            db.add(obj)
            db.commit()
            db.refresh(obj)
            return obj
        except:
            db.close()
    @classmethod
    def get(cls, id: int, db: Session = next(get_db())):
       return db.query(cls).filter(cls.id == id).first()      
    def update(self, db: Session = next(get_db()), **kwargs: Dict[str, Any]):
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

    def to_dict(self, includes= None, excludes= []):
            attrs = [
                     attr for attr in dir(self) \
                     if not attr.startswith("_") and not callable(getattr(self, attr)) \
                        and (attr != 'metadata') and (attr != 'registry') and attr not in excludes ] \
                    if includes is None else includes 
            return { column: getattr(self, column) for column in attrs}



def orm_to_dict(orm_instance):
    result = {}
    for column in orm_instance.__table__.columns:
        result[column.name] = getattr(orm_instance, column.name)
    return result

ModelType = TypeVar("ModelType", bound=Base)
class BaseRepository(Generic[ModelType]):
    model = None
    def __init__(self, db: Session = next(get_db())):
        self.db = db
    

    def get(self, id: int | UUID):
        try:
            return self.db.query(self.model).filter(self.model.id == id).first()
        except:
            self.db.close()
            raise Exception("Get {id} failed.")

    # def create(cls, name: str, email: str, db: Session = SessionLocal() ''' next(get_db() # cách 2 '''): # cách 1
    def create(self, **kwargs : Dict[str, Any]) -> ModelType:
        try:
            obj = self.model(**kwargs)
            self.db.add(obj)
            self.db.commit()
            self.db.refresh(obj)
            return obj
        except:
            self.db.close()
            raise Exception("Create failed.")

    def _update(self, obj: ModelType, **kwargs: Dict[str, Any]) -> ModelType:
        try:
            if obj is None:
                raise ValueError("Do not find instance of ${ModelType.__name__}")
            for key, value in kwargs.items():
                setattr(obj, key, value)
            self.db.commit()
            self.db.refresh(obj)
            return obj
        except:
            self.db.close()
            raise Exception("Error occurred during update.")

    def update(self, id= int| UUID| str, **kwargs: Dict[str, Any]) -> ModelType:
        obj = self.get(id)
        return self._update(obj, **kwargs)
    def _delete(self, obj: ModelType) -> None:
        try:
            if obj is None:
                raise ValueError("Do not find instance of ${ModelType.__name__}")
            self.db.delete(obj)
            self.db.commit()
            return True
        except:
            self.db.close()
            return False
    def delete(self, id= int| UUID| str) -> ModelType:
        obj = self.get(id)
        return self._delete(obj)

    def to_dict(self, obj):
            return {column.name: getattr(obj, column.name) for column in self.model.__table__.columns}

class QueryBuilder:
    def __init__(self, table, db: Session = next(get_db())):
        self.table = table
        self.query = db.query(self.table)
        
    def filter_by(self, **kwargs):
        if self.query is None:
            raise Exception("No select statement has been called yet.")
        self.query = self.query.filter_by(**kwargs)
        return self

    def order_by(self, *args):
        if self.query is None:
            raise Exception("No select statement has been called yet.")
        self.query = self.query.order_by(*args)
        return self

    def limit(self, limit):
        if self.query is None:
            raise Exception("No select statement has been called yet.")
        self.query = self.query.limit(limit)
        return self

    def offset(self, offset):
        if self.query is None:
            raise Exception("No select statement has been called yet.")
        self.query = self.query.offset(offset)
        return self

    def execute(self):
        if self.query is None:
            raise Exception("No select statement has been called yet.")
        return self.query.all()
    
# # In ra câu SQL đã tạo
# print(query.statement)    
