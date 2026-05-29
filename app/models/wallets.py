from sqlalchemy import Column, String, Boolean, TIMESTAMP, Enum, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid

class Wallets(Base):
    __tablename__ = "wallets"
    
    id = Column(String, unique=True, primary_key=True, nullable=False, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    description = Column(String(255), nullable=True)
    wallet_type = Column(Enum('system', 'project', name='wallet_type'), nullable=False, default='project')
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)