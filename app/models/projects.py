from sqlalchemy import Column, Numeric, String, TIMESTAMP, Enum, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid

class Projects(Base):
    __tablename__ = "projects"
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    expected_budget = Column(Numeric, nullable=False)
    status = Column(Enum('pending', 'ongoing', 'delayed', 'finished', 'cancelled', name='project_status'), nullable=False, default='pending')
    supervisor_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    wallet_id = Column(UUID, ForeignKey("wallets.id"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    finished_at = Column(TIMESTAMP(timezone=True), nullable=True)   