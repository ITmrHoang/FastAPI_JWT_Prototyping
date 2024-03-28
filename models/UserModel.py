from typing import List, Set
from sqlalchemy import event, Boolean, Integer, Column, String, DateTime, Text, Float, ForeignKey, Date, Time
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.sql.functions import now
from sqlalchemy.orm import relationship, Mapped
from uuid import uuid4
import secrets
from core import hash as hashPassword,  SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends


from core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = Column(DateTime, server_default=now())

    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    _hashed_password = Column(String, nullable=False)
    salt = Column(String(16), nullable=False)
    is_active = Column(Boolean, nullable=False, default=False)
    is_supper_admin = Column(Boolean, nullable=False, default=False)
    last_login = Column(DateTime, server_default=now())

    created_at = Column(DateTime, server_default=now())

    roles: Mapped[List["Role"]] =  relationship("Role",secondary="user_has_roles", back_populates="users") 
    # roles: Mapped[List["Role"]] =  relationship("Role", back_populates="user") 
    permissions: Mapped[Set["Permission"]] =  relationship("Permission", secondary="user_has_permissions" ,  back_populates="users") 

    @property
    def hashed_password(self):
        return self._hashed_password

    @hashed_password.setter
    def hashed_password(self, plaintext_password):
        # Mã hóa mật khẩu và gán cho _hashed_password
        print(hashPassword('aaaa'), hashPassword('aaaa'))
        password = hashPassword(plaintext_password+self.salt)
        self._hashed_password = password


    def __str__(self):
        attributes = vars(self)  # Lấy tất cả các thuộc tính của đối tượng
        attributes_str = ", ".join([f"{key}={value}" for key, value in attributes.items()])  # Tạo chuỗi từ các thuộc tính và giá trị
        return f"User({attributes_str})"
    def __repr__(self) -> str:
        return f"<User {self.email}>"

    def __hash__(self) -> int:
        return hash(self.email)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, User):
            return self.email == other.email
        return False

    @classmethod
    def getUserByUsername(cls, username: int, db: Session = SessionLocal()):
        user = db.query(cls).filter(cls.username == username).first()
        return user
    
@event.listens_for(User, 'init')
def generate_salt_init( target, mapper, connection):
    if not hasattr(target, 'salt') or target.salt is None:
    # Tạo một salt ngẫu nhiên với 4 byte (tương đương 8 ký tự hex)
        target.salt = secrets.token_hex(4)

# # Sử dụng event.listen
# def before_hashed_password_change_listener(target, value, oldvalue, initiator):
#     print(f"Field {target}  : {target.__str__} is about to change from {oldvalue} to {value} ---- \n  {initiator} : {initiator.__str__}" )
#     initiator.hashed_password = hashPassword(value)

    

# event.listen(User.hashed_password, 'set', before_hashed_password_change_listener)



#TODO có thể tạo relation polymorphic
    

# Định nghĩa model cho User, Role, và Permission
# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     title = Column(String)
#     content = Column(String)
#     roles = relationship("Role", back_populates="roleable")
#     permissions = relationship("Permission", back_populates="permissionable")

# class Role(Base):
#     __tablename__ = 'roles'
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     description= Column(String)
#     model_type = Column(String)  # Loại của chủ sở hữu (post hoặc comment)
#     model_id = Column(Integer)   # ID của chủ sở hữu
#     roleable = relationship("User", back_populates="roles", foreign_keys=[model_id], primaryjoin="Role.model_type=='user'") 
# tạo thêm các able tương ứng cho các model relation ví dụ customer, ....
#     permissions = relationship("Permission", back_populates="roles")

# class Permission(Base):
#     __tablename__ = 'permissions'
#     id = Column(Integer, primary_key=True)
#     url = Column(String)
#     description= Column(String)
#     model_type = Column(String)  # Loại của chủ sở hữu (post hoặc comment)
#     model_id = Column(Integer)   # ID của chủ sở hữu
#     permissonable = relationship("User", back_populates="permissions", foreign_keys=[model_id], primaryjoin="Permission.model_type=='user'")  
    

#----------------------------------------------------------------
# Bảng ghi chứa mối quan hệ n-n giữa User và Role hoặc tạo một file modle quản hệ
# user_role_association = Table('user_role_association', Base.metadata,
#     Column('user_id', Integer, ForeignKey('users.id')),
#     Column('role_id', Integer, ForeignKey('roles.id'))
# )
    
# attr roles trong User : relation thêm prams secondary=role_permission_association hoặc secondary="user_roles", với user_role tên bảng


# Sử dụng @event.listens_for
# @event.listens_for(YourModelClass.your_field, 'set')
# def before_field_change_listener(target, value, oldvalue, initiator):
#     print(f"Field {target} is about to change from {oldvalue} to {value}")

# # Sử dụng event.listen
# def before_field_change_listener(target, value, oldvalue, initiator):
#     print(f"Field {target} is about to change from {oldvalue} to {value}")

# event.listen(YourModelClass.your_field, 'set', before_field_change_listener)