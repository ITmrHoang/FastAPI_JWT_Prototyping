from typing import List
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.sql.functions import now
from sqlalchemy.orm import relationship, Mapped
from uuid import uuid4
# from User import User # có thể import hoặc không đây chỉ hiện cảnh báo python sẽ tự tìm kiếm trong module hiện tại

from core.database import Base

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True, default="", unique=True)
    created_at = Column(DateTime, server_default=now())

    users: Mapped[List["User"]] =  relationship("User",secondary="user_has_permissions", back_populates="permissions") 
    roles: Mapped[List["Role"]] =  relationship("Role",secondary="role_has_permissions", back_populates="permissions") 



