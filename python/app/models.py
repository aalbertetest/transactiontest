from typing import Dict, Optional
from pydantic import BaseModel, Field


class PaymentIntentCreateRequest(BaseModel):
    amount: int = Field(..., gt=0)
    currency: str = Field(..., min_length=3, max_length=3)
    customer_id: Optional[str] = None
    payment_method_token: str
    capture_method: str = "automatic"
    metadata: Dict[str, str] = Field(default_factory=dict)
    return_url: Optional[str] = None


class PaymentIntentResponse(BaseModel):
    id: str
    status: str
    amount: int
    currency: str
    client_secret: str
    charge_id: Optional[str] = None


class ConfirmResponse(BaseModel):
    id: str
    status: str
    charge_id: Optional[str] = None


class RefundRequest(BaseModel):
    amount: Optional[int] = None
    reason: Optional[str] = None


class RefundResponse(BaseModel):
    id: str
    status: str
    amount: int
    charge_id: str


class WebhookEndpointCreateRequest(BaseModel):
    url: str
    enabled: bool = True


class WebhookEndpointResponse(BaseModel):
    id: str
    url: str
    enabled: bool


class EventResponse(BaseModel):
    id: str
    type: str
    created_at: str
    data: Dict[str, object]

