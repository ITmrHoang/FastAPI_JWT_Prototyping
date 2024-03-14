from typing import List, Set
from sqlalchemy import Boolean, Integer, Column, String, DateTime, Text, Float, ForeignKey, Date, Time
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.sql.functions import now
from sqlalchemy.orm import relationship, Mapped
from uuid import uuid4
# from User import User # có thể import hoặc không đây chỉ hiện cảnh báo python sẽ tự tìm kiếm trong module hiện tại

from core.database import Base

class UserHasPermissions(Base):
    __tablename__ = 'user_has_permissions'
    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    permission_id = Column(UUID(as_uuid=True), ForeignKey('permissions.id'))



