from typing import List, Set
from sqlalchemy import Boolean, Integer, Column, String, DateTime, Text, Float, ForeignKey, Date, Time
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.sql.functions import now
from sqlalchemy.orm import relationship, Mapped
from uuid import uuid4
# from User import User # có thể import hoặc không đây chỉ hiện cảnh báo python sẽ tự tìm kiếm trong module hiện tại

from core.database import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True, default="", unique=True)
    created_at = Column(DateTime, server_default=now())

    users: Mapped[List["User"]] =  relationship("User",secondary="user_has_roles", back_populates="roles") 
    permissions: Mapped[List["Permission"]] =  relationship("Permission", secondary="role_has_permissions", back_populates="roles") 



