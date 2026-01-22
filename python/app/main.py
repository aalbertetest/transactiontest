from typing import Dict

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse

from .config import API_KEY
from .idempotency import request_hash
from .models import (
    ConfirmResponse,
    EventResponse,
    PaymentIntentCreateRequest,
    PaymentIntentResponse,
    RefundRequest,
    RefundResponse,
    WebhookEndpointCreateRequest,
    WebhookEndpointResponse,
)
from .payments import process_payment_intent
from .storage import STORE, InMemoryStore


app = FastAPI(title="Payment Processing API", version="1.0.0")


def init_default_merchant(store: InMemoryStore) -> None:
    if not store.merchants:
        store.add_merchant("Demo Merchant", API_KEY)


def get_merchant(authorization: str = Header(...)) -> Dict[str, object]:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="invalid authorization header")
    api_key = authorization.replace("Bearer ", "").strip()
    merchant = STORE.get_merchant_by_api_key(api_key)
    if not merchant:
        raise HTTPException(status_code=401, detail="invalid api key")
    return merchant


def idempotent_response(
    merchant_id: str,
    idempotency_key: str,
    payload: Dict[str, object],
    handler,
) -> JSONResponse:
    idempotency = STORE.get_idempotency(merchant_id, idempotency_key)
    payload_hash = request_hash(payload)
    if idempotency:
        if idempotency["request_hash"] != payload_hash:
            raise HTTPException(status_code=409, detail="idempotency key reuse with different payload")
        return JSONResponse(content=idempotency["response_body"], status_code=idempotency["status_code"])

    response_body, status_code = handler()
    STORE.set_idempotency(merchant_id, idempotency_key, payload_hash, response_body, status_code)
    return JSONResponse(content=response_body, status_code=status_code)


@app.on_event("startup")
def startup() -> None:
    init_default_merchant(STORE)


@app.post("/v1/payment_intents", response_model=PaymentIntentResponse)
async def create_payment_intent(
    request: Request,
    payload: PaymentIntentCreateRequest,
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
    merchant: Dict[str, object] = Depends(get_merchant),
) -> JSONResponse:
    request_payload = {"path": request.url.path, "body": payload.model_dump()}

    def handler():
        intent = STORE.create_payment_intent(merchant["id"], payload.model_dump())
        response = PaymentIntentResponse(
            id=intent["id"],
            status=intent["status"],
            amount=intent["amount"],
            currency=intent["currency"],
            client_secret=intent["client_secret"],
        ).model_dump()
        return response, 200

    return idempotent_response(merchant["id"], idempotency_key, request_payload, handler)


@app.post("/v1/payment_intents/{intent_id}/confirm", response_model=ConfirmResponse)
async def confirm_payment_intent(
    request: Request,
    intent_id: str,
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
    merchant: Dict[str, object] = Depends(get_merchant),
) -> JSONResponse:
    request_payload = {"path": request.url.path, "body": {"intent_id": intent_id}}

    def handler():
        intent = STORE.get_payment_intent(intent_id)
        if not intent or intent["merchant_id"] != merchant["id"]:
            raise HTTPException(status_code=404, detail="payment intent not found")
        if intent["status"] not in {"requires_confirmation", "processing"}:
            response = ConfirmResponse(
                id=intent_id,
                status=intent["status"],
                charge_id=intent.get("charge_id"),
            ).model_dump()
            return response, 200
        STORE.update_payment_intent(intent_id, {"status": "processing"})
        STORE.enqueue_task({"type": "process_payment", "intent_id": intent_id})
        response = ConfirmResponse(id=intent_id, status="processing", charge_id=None).model_dump()
        return response, 202

    return idempotent_response(merchant["id"], idempotency_key, request_payload, handler)


@app.get("/v1/payment_intents/{intent_id}", response_model=PaymentIntentResponse)
async def get_payment_intent(
    intent_id: str,
    merchant: Dict[str, object] = Depends(get_merchant),
) -> PaymentIntentResponse:
    intent = STORE.get_payment_intent(intent_id)
    if not intent or intent["merchant_id"] != merchant["id"]:
        raise HTTPException(status_code=404, detail="payment intent not found")
    return PaymentIntentResponse(
        id=intent["id"],
        status=intent["status"],
        amount=intent["amount"],
        currency=intent["currency"],
        client_secret=intent["client_secret"],
        charge_id=intent.get("charge_id"),
    )


@app.post("/v1/charges/{charge_id}/refunds", response_model=RefundResponse)
async def refund_charge(
    request: Request,
    charge_id: str,
    payload: RefundRequest,
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
    merchant: Dict[str, object] = Depends(get_merchant),
) -> JSONResponse:
    request_payload = {"path": request.url.path, "body": payload.model_dump()}

    def handler():
        charge = STORE.get_charge(charge_id)
        if not charge:
            raise HTTPException(status_code=404, detail="charge not found")
        refund_amount = payload.amount or charge["amount"]
        refund = STORE.create_refund(charge_id, refund_amount, "succeeded")
        STORE.create_event(
            merchant["id"],
            "charge.refunded",
            {"id": refund["id"], "charge_id": charge_id, "amount": refund_amount},
        )
        response = RefundResponse(
            id=refund["id"],
            status=refund["status"],
            amount=refund["amount"],
            charge_id=charge_id,
        ).model_dump()
        return response, 200

    return idempotent_response(merchant["id"], idempotency_key, request_payload, handler)


@app.post("/v1/webhook_endpoints", response_model=WebhookEndpointResponse)
async def create_webhook_endpoint(
    request: Request,
    payload: WebhookEndpointCreateRequest,
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
    merchant: Dict[str, object] = Depends(get_merchant),
) -> JSONResponse:
    request_payload = {"path": request.url.path, "body": payload.model_dump()}

    def handler():
        endpoint = STORE.add_webhook_endpoint(merchant["id"], payload.url, payload.enabled)
        response = WebhookEndpointResponse(
            id=endpoint["id"], url=endpoint["url"], enabled=endpoint["enabled"]
        ).model_dump()
        return response, 200

    return idempotent_response(merchant["id"], idempotency_key, request_payload, handler)


@app.get("/v1/events", response_model=list[EventResponse])
async def list_events(
    merchant: Dict[str, object] = Depends(get_merchant),
) -> list[EventResponse]:
    events = STORE.list_events(merchant["id"])
    return [
        EventResponse(
            id=event["id"],
            type=event["type"],
            created_at=event["created_at"],
            data=event["data"],
        )
        for event in events
    ]

