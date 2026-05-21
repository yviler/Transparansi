from sqlalchemy import Column, Integer, String, Date, Boolean, TIMESTAMP, Enum, func
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid

class Wallets(Base):
    __tablename__ = "wallets"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    description = Column(String(255), nullable=True)
    type = Column(Enum('system, project'), nullable=False, default='project')
    #set FK to projects.id
    project_id = Column(Integer, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    #FK to users.id/employee.id
    created_by = Column(UUID(as_uuid=True), nullable=False)
