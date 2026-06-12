from sqlalchemy import Column, String, Boolean, TIMESTAMP, Enum, func, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
from sqlalchemy.orm import relationship
import uuid

class Wallets(Base):
    __tablename__ = "wallets"
    
    id = Column(UUID(as_uuid=True), unique=True, primary_key=True, nullable=False, index=True, default=uuid.uuid4)
    wallet_name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(String(255), nullable=True)
    wallet_type = Column(Enum('system', 'project', name='wallet_type'), nullable=False, default='project')
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

class Bills(Base):
    __tablename__ = "bills"
    
    id = Column(UUID(as_uuid=True), unique=True, primary_key=True, nullable=False, index=True, default=uuid.uuid4)
    bill_name = Column(String(255), nullable=False)
    amount = Column(Numeric, nullable=False)
    task_id = Column(UUID(as_uuid=True), ForeignKey('tasks.id'), index=True, nullable=False)
    submittedBy = Column(UUID(as_uuid=True), ForeignKey('users.id'), index=True, nullable=False)
    status = Column(Enum('pending', 'approved', 'rejected', 'cancelled'))
    approved_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), index=True, nullable=True)
    #for all wallet_tx, where wallet_tx.bill_id = id
    transaction_ids = relationship("WalletTransactions")
    description = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    resolved_at = Column(TIMESTAMP(timezone=True), nullable=True)
    
class WalletTransactions(Base):
    __tablename__ = "wallet_transactions"
    
    id = Column(UUID(as_uuid=True), unique=True, primary_key=True, nullable=False, index=True, default=uuid.uuid4)
    tx_name = Column(String(255), nullable=False)
    amount = Column(Numeric, nullable=False)
    tx_type = Column(Enum('deposit', 'allocation', 'bill_payment', 'refund', 'cancellation', 'pending', name='tx_type'), nullable=False, default='pending')
    from_wallet_id = Column(UUID(as_uuid=True), ForeignKey("wallets.id"), unique=True, index=True, nullable=True)
    to_wallet_id = Column(UUID(as_uuid=True), ForeignKey("wallets.id"), unique=True, index=True, nullable=True)
    bill_id = Column(UUID(as_uuid=True), ForeignKey("bills.id"), index=True, nullable=True)
    is_cancelled = Column(Boolean, nullable=False, default=False)
    refund_id = Column(UUID(as_uuid=True), ForeignKey('wallet_transactions.id'), nullable=True)
    description = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    cancelled_at = Column(TIMESTAMP(timezone=True), nullable=True)
    