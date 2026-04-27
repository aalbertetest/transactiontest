"""Pydantic request/response models."""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from payhub.models import LedgerSide, UserRole


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserOut(BaseModel):
    id: str
    email: str
    role: UserRole
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginBody(BaseModel):
    email: EmailStr
    password: str


class PaymentCreate(BaseModel):
    payee_user_id: str
    amount_cents: int = Field(gt=0, le=10_000_000_000)
    idempotency_key: str | None = Field(default=None, max_length=128)


class LedgerLineOut(BaseModel):
    account_id: str
    side: LedgerSide
    amount_cents: int


class PaymentOut(BaseModel):
    id: str
    payer_user_id: str
    payee_user_id: str
    amount_cents: int
    fee_cents: int
    status: str
    fraud_flags: str | None
    created_at: datetime
    ledger: list[LedgerLineOut]

    model_config = {"from_attributes": True}


class ApiKeyCreate(BaseModel):
    name: str = Field(max_length=128)


class ApiKeyOut(BaseModel):
    id: str
    name: str
    key_prefix: str
    scopes: str
    created_at: datetime
    secret: str | None = None  # only on create

    model_config = {"from_attributes": True}


class HealthOut(BaseModel):
    status: str
    environment: str
