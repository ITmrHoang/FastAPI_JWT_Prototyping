from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
from fastapi_utils.guid_type import setup_guids_postgresql
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session
from fastapi import Depends

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

class BaseModelORM():
    @classmethod
    def create(cls, name: str, email: str, db: Session = Depends(get_db)):
        user = cls(name=name, email=email)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user