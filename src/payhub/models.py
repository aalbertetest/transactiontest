"""SQLAlchemy ORM models."""

from __future__ import annotations

import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def _uuid() -> str:
    return str(uuid.uuid4())


class Base(DeclarativeBase):
    pass


class UserRole(str, enum.Enum):
    customer = "customer"
    admin = "admin"


class AccountType(str, enum.Enum):
    """Coarse chart of accounts."""

    user_wallet = "user_wallet"  # liability: balance owed to user
    fee_revenue = "fee_revenue"  # revenue


class LedgerSide(str, enum.Enum):
    debit = "debit"
    credit = "credit"


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.customer)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    accounts: Mapped[list[Account]] = relationship(back_populates="user")
    api_keys: Mapped[list[ApiKey]] = relationship(back_populates="user")


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    user_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("users.id"), nullable=True)
    type: Mapped[AccountType] = mapped_column(Enum(AccountType))
    currency: Mapped[str] = mapped_column(String(3), default="USD")
    name: Mapped[str] = mapped_column(String(128))

    user: Mapped[User | None] = relationship(back_populates="accounts")
    ledger_entries: Mapped[list[LedgerEntry]] = relationship(back_populates="account")


class PaymentTransaction(Base):
    """Business-level payment (one journal)."""

    __tablename__ = "payment_transactions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    idempotency_key: Mapped[str | None] = mapped_column(String(128), index=True, nullable=True)
    payer_user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))
    payee_user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))
    amount_cents: Mapped[int] = mapped_column(BigInteger)
    fee_cents: Mapped[int] = mapped_column(BigInteger, default=0)
    status: Mapped[str] = mapped_column(String(32), default="posted")  # posted | failed
    fraud_flags: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    ledger_entries: Mapped[list[LedgerEntry]] = relationship(back_populates="payment")


class LedgerEntry(Base):
    __tablename__ = "ledger_entries"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    payment_id: Mapped[str] = mapped_column(String(36), ForeignKey("payment_transactions.id"))
    account_id: Mapped[str] = mapped_column(String(36), ForeignKey("accounts.id"))
    side: Mapped[LedgerSide] = mapped_column(Enum(LedgerSide))
    amount_cents: Mapped[int] = mapped_column(BigInteger)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    payment: Mapped[PaymentTransaction] = relationship(back_populates="ledger_entries")
    account: Mapped[Account] = relationship(back_populates="ledger_entries")


class IdempotencyRecord(Base):
    __tablename__ = "idempotency_records"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    scope: Mapped[str] = mapped_column(String(64), index=True)  # e.g. user_id
    key_hash: Mapped[str] = mapped_column(String(64), index=True)
    request_hash: Mapped[str] = mapped_column(String(64))
    response_status: Mapped[int] = mapped_column(Integer)
    response_body: Mapped[str] = mapped_column(Text)
    payment_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (UniqueConstraint("scope", "key_hash", name="uq_idempotency_scope_key"),)


class ApiKey(Base):
    __tablename__ = "api_keys"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String(128))
    key_prefix: Mapped[str] = mapped_column(String(16), index=True)
    key_hash: Mapped[str] = mapped_column(String(128))
    scopes: Mapped[str] = mapped_column(String(256), default="payments:write,ledger:read")
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped[User] = relationship(back_populates="api_keys")
