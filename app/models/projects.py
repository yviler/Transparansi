from sqlalchemy import Column, Numeric, String, TIMESTAMP, Enum, func, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
from sqlalchemy.orm import relationship
import uuid

class Projects(Base):
    __tablename__ = "projects"
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    project_name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    expected_budget = Column(Numeric, nullable=False)
    status = Column(Enum('pending', 'ongoing', 'delayed', 'finished', 'cancelled', name='project_status'), nullable=False, default='pending')
    supervisor_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    wallet_id = Column(UUID, ForeignKey("wallets.id"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    finished_at = Column(TIMESTAMP(timezone=True), nullable=True)   
    
class Tasks(Base):
    __tablename__ = "tasks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    task_name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    projectID = Column(UUID, ForeignKey("projects.id"), nullable=False, index=True)
    parentTaskID = Column(UUID, ForeignKey("tasks.id"), nullable=True, index=True)
    assignees = relationship("Users", secondary="task_assignees", 
                            primaryjoin="Tasks.id == TaskAssignees.task_id",
                            secondaryjoin="TaskAssignees.user_id == Users.id")
    status = Column(Enum('pending', 'ongoing', 'completed', 'cancelled', name='task_status'), nullable=False, default='pending')
    created_by = Column(UUID, ForeignKey("users.id"),nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    finished_at = Column(TIMESTAMP(timezone=True), nullable=True)
        
class TaskAssignees(Base):
    __tablename__ = "task_assignees"
    
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, index=True, default=uuid.uuid4)
    task_id = Column(UUID, ForeignKey("tasks.id"), nullable=False, index=True)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False, index=True)
    assigned_by = Column(UUID, ForeignKey("users.id"), nullable=False)
    assigned_at = Column(TIMESTAMP(timezone=True), nullable=False, default=func.now())
    is_revoked = Column(Boolean, nullable=False, default=False)
    revoked_at = Column(TIMESTAMP(timezone=True), nullable=True)