from sqlalchemy import Column, String, Date, Boolean, TIMESTAMP, Enum, func
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid

class Users(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String(255), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    clearance_level = Column(Enum('observer', 'staff', 'supervisor', 'admin', name='clearance_level'), nullable=False, default='observer')
    employee_id = Column(String(100), unique=True, index=True, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    date_joined = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    date_left = Column(TIMESTAMP(timezone=True))
    session_token = Column(String, nullable=True, unique=True)
    session_token_expires_at = Column(TIMESTAMP(timezone=True), nullable=True)