from typing import List, Set
from sqlalchemy import Boolean, Integer, Column, String, DateTime, Text, Float, ForeignKey, Date, Time
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.sql.functions import now
from sqlalchemy.orm import relationship, Mapped
from uuid import uuid4

from core.database import Base

class UserHasRoles(Base):
    __tablename__ = 'user_has_roles'
    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    role_id = Column(UUID(as_uuid=True), ForeignKey('roles.id'))



