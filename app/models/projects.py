from sqlalchemy import Column, Integer, String, Date, Boolean, TIMESTAMP, Enum, func, Float
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid

class Projects(Base):
    __tablename__ = "projects"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    expected_budget = Column(Float, nullable=False)
    status = Column(Enum('pending, ongoing, delayed, finished, cancelled'), nullable=False, default='pending')
    # set as FK to users.id/ users.employee_id
    supervisor_id = Column(UUID(as_uuid=True), nullable=False)
    # set as FK to wallet
    wallet_id = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    finished_at = Column(TIMESTAMP(timezone=True), nullable=True)