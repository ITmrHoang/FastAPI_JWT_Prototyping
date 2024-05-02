from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
from fastapi_utils.guid_type import setup_guids_postgresql
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session
from fastapi import Depends, Request
from typing import Any, Dict, TypeVar, Generic, List,Tuple
from uuid import UUID
from fastapi.security import OAuth2PasswordBearer
from .schema_api import ResponseException
from sqlalchemy import tuple_
from fastapi.encoders import jsonable_encoder

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

BaseCore = declarative_base()
class Base(BaseCore):
    __abstract__ = True
    def to_dict(self, includes= None, excludes= []):
        attrs = [
                    attr for attr in dir(self) \
                    if not attr.startswith("_") and not callable(getattr(self, attr)) \
                    and (attr != 'metadata') and (attr != 'registry') and attr not in excludes ] \
                if includes is None else includes 
        return { column: getattr(self, column) for column in attrs}
    def getJson(self):
        item = self.to_dict()
        return item

_global_db = None
_global_request_db = None
def get_global_db():
    global _global_db
    try:
        if _global_db is None:
            _global_db = SessionLocal()
        return _global_db
    except Exception as e:
        # Xử lý ngoại lệ một cách chính xác
        print(f"An error occurred while creating the session: {e}")
        if _global_db:
            _global_db.close()
            _global_db  = None
        raise ResponseException("Session  database errors")
        # Trong một khối finally, bạn cần đảm bảo rằng session sẽ được đóng nếu có bất kỳ ngoại lệ nào xảy ra
      

def get_global_request_db():
    global _global_request_db
    try:
        if _global_request_db is None:
            _global_request_db = SessionLocal()
        return _global_request_db
    except Exception as e:
        # Xử lý ngoại lệ một cách chính xác
        print(f"An error occurred while creating the session: {e}")
        if _global_request_db:
            _global_request_db.close()
            _global_request_db= None
        raise ResponseException("Session  database errors")
        # Trong một khối finally, bạn cần đảm bảo rằng session sẽ được đóng nếu có bất kỳ ngoại lệ nào xảy ra


# Middleware để quản lý global session
async def manage_global_session(request: Request, call_next):
    global _global_request_db
    try:
        # Khởi tạo session mới cho mỗi yêu cầu
        _global_request_db = get_global_request_db()

        # Thêm session vào state của request để có thể truy cập trong các route handler
        request.state.db = _global_request_db

        # Tiếp tục xử lý yêu cầu
        response = await call_next(request)
        _global_request_db.commit()

        return response
    except Exception as e:
        # Xử lý ngoại lệ nếu có
        print(f"\nlog middware session db erros: {e}")
        raise ResponseException("Middleware session  database errors: " + str(e))
    finally:
        # Sau khi xử lý yêu cầu, đóng session và xóa biến global del or gán Nonee
        if _global_request_db:
            _global_request_db.close()
            _global_request_db = None       
    
def get_request_db(request: Request):
    return request.state.db

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
    def search(cls, page=None, page_size=None,filters= None, db: Session = next(get_db())) -> List[Any]:
        try:
            query = db.query(cls).order_by(cls.id)
            data = query.all()
            if filters:
                for field, value in filters.items():
                    query = query.filter(getattr(cls, field) == value)
            if page is not None and page_size is not None:
                if page < 1: page = 1
                total_count = query.count()
                query = query.offset((page - 1) * page_size).limit(page_size)
                result = [ item.getJson() for item in query]  
                """  getJSon() hàm sẽ gọi tới các cột relastion nên sẽ \
                get data relastion nếu không có chỉ get các field của model đó không có relationship"""
                return result, total_count
            else:
                result = [ item.getJson() for item in query]  
                """  getJSon() hàm sẽ gọi tới các cột relastion nên sẽ \
                get data relastion nếu không có chỉ get các field của model đó không có relationship"""
                return result
        except Exception as e:
            db.close()
            raise ResponseException("Search error {}".format(str(e)))

    def getJson(self):
        item = self.to_dict()
        return item
    
    # @classmethod
    # def get(cls, id: int, db: Session = next(get_db())):
    #    return db.query(cls).filter(cls.id == id).first()     
    @classmethod
    def get(cls, id: int | str, db: Session = next(get_db())):
        #NOTE không cần kiểm tra cột id là uuid và chuyển thành kiểu tương ứng vì SQLAlchemy tự động chuyển đổi kiểu dữ liệu nếu cột đó là UUID
        # from sqlalchemy.dialects.postgresql import UUID
        # import uuid
        # if isinstance(cls.id.type , UUID):
        # id = uuid.UUID(id)
        try:
            instance = db.query(cls).filter(cls.id == id).first()
            return instance
        except Exception as er:
            db.close()
            raise ResponseException("get user error {}".format(str(er)))
    @classmethod
    def get_by_username(cls, username: int | str, db: Session = next(get_db())):
        #NOTE không cần kiểm tra cột id là uuid và chuyển thành kiểu tương ứng vì SQLAlchemy tự động chuyển đổi kiểu dữ liệu nếu cột đó là UUID
        # from sqlalchemy.dialects.postgresql import UUID
        # import uuid
        # if isinstance(cls.id.type , UUID):
        # id = uuid.UUID(id)
        try:
            instance = db.query(cls).filter(cls.username == username).first()
            return instance
        except Exception as er:
            db.close()
            raise ResponseException("get user by username error {}".format(str(er)))
    @classmethod 
    def create (cls, db: Session=SessionLocal(), **kwargs: Dict[str, Any]):#TODO cách 1 , Session= SessionLocal() # cách 2 next(get_db()) dùng 2 cách này tất cả các lần gọi hàm này thực thi statemnt đều chung 1 session
        # Lọc kwargs chỉ giữ lại các trường có trong annotations của lớp mô hình
        valid_kwargs = {k: v for k, v in kwargs.items() if k in  [
                     attr for attr in vars(cls) \
                     if not attr.startswith("_") and not callable(getattr(cls, attr))]
        }
        try:
            obj = cls(**valid_kwargs)
            db.add(obj)
            db.commit()
            db.refresh(obj)
            return obj
        except Exception as er:
            db.close()
            raise ResponseException("Create record error {}".format(str(er)))
 
    def update(self, db: Session = None, rq = None, **kwargs: Dict[str, Any]):
        if db is None:
            db = get_global_request_db()
        if rq is not None:
            json_data = jsonable_encoder(rq)
            for attr, value in json_data.items():
                setattr(self, attr, value)

        for attr, value in kwargs.items():
           setattr(self, attr, value)

        db.add(self)
        db.commit()
        db.refresh(self)
        return self
    def delete(self, db: Session= None):
       if db is None:
           db = get_global_request_db()
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
    model:ModelType = None
    def __init__(self):
        self.set_db()
        self.set_model()
    
    def set_model(self):
        pass

    def get_model(self) -> ModelType:
        return self.model

    def set_db(self, db = None):
        if db is None:
            self.db = get_global_request_db()
    

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

    def _update(self, obj: ModelType, rq=None, **kwargs: Dict[str, Any]) -> ModelType:
        try:
            if obj is None:
                raise ValueError("Do not find instance of ${ModelType.__name__}")

            if rq is not None:
                json_data = jsonable_encoder(rq)
                for attr, value in json_data.items():
                    setattr(self, attr, value)

            for attr, value in kwargs.items():
                setattr(self, attr, value)

            self.db.commit()
            self.db.refresh(obj)
            return obj
        except:
            self.db.close()
            raise Exception("Error occurred during update.")

    def update(self, id= int| UUID| str, rq = None, **kwargs: Dict[str, Any]) -> ModelType:
        obj = self.get(id)
        return self._update(obj,rq, **kwargs)
    
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
    db=None
    model = None
    query = None
    def __init__(self):
        self.set_db()
        self.set_model()
        self.set_query()
    
    def set_model(self):
        pass

    def set_db(self, db = None):
        if db is None:
            self.db = get_global_request_db()
        else:
            self.db = db
    def set_query(self):
        self.query = self.db.query(self.model)

    def get_db(self):
        return self.db

    def get_query(self):
        return self.query
    
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
    def whereIn(self, col: str|list|tuple, array: list) -> list[ModelType]:
        try:
            
            if isinstance(col, str):
                column = getattr(self.model, col)
                return self.query.filter(column.in_(array))
            elif isinstance(col, list) or isinstance(col, tuple):
                columns  = []
                for c in col:
                      self.db.expunge(col)
                      columns.append(getattr(self.model, c))
                return self.query.filter(tuple_(*columns ).in_(array))
            else:
                raise ResponseException("Invalid type for 'col'")
        except Exception as e:
            self.db.close()
            raise ResponseException("Error occurred during whereIn:" + str(e))
class BaseService(BaseRepository[Generic[ModelType]],QueryBuilder ):
    def __init__(self):
    # super().__init__()  # Gọi constructor của BaseRepository
    # super(QueryBuilder, self).__init__()  # Gọi constructor của QueryBuilder
       BaseRepository.__init__(self)
       QueryBuilder.__init__(self)
# # In ra câu SQL đã tạo
# print(query.statement)    
