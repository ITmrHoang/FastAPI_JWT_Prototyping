from typing import List, Set
from sqlalchemy import event, Boolean, Integer, Column, String, DateTime, Text, Float, ForeignKey, Date, Time
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.sql.functions import now
from sqlalchemy.orm import relationship, Mapped
from uuid import uuid4
import secrets

from core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = Column(DateTime, server_default=now())

    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    salt = Column(String(16), nullable=False)
    is_active = Column(Boolean, nullable=False, default=False)
    is_supper_admin = Column(Boolean, nullable=False, default=False)
    last_login = Column(DateTime, server_default=now())

    created_at = Column(DateTime, server_default=now())

    roles: Mapped[List["Role"]] =  relationship("Role",secondary="user_has_roles", back_populates="users") 
    # roles: Mapped[List["Role"]] =  relationship("Role", back_populates="user") 
    permissions: Mapped[Set["Permission"]] =  relationship("Permission", secondary="user_has_permissions" ,  back_populates="users") 

@event.listens_for(User, 'init')
def generate_salt_init(mapper, connection, target):
    if not hasattr(target, 'salt') or target.salt is None:
    # Tạo một salt ngẫu nhiên với 4 byte (tương đương 8 ký tự hex)
        target.salt = secrets.token_hex(4)




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
