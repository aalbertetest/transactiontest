from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from payhub.api_keys import generate_api_key
from payhub.db import get_db
from payhub.deps import require_user
from payhub.models import ApiKey, User
from payhub.schemas import ApiKeyCreate, ApiKeyOut

router = APIRouter(prefix="/v1/api-keys", tags=["api-keys"])


@router.post("", response_model=ApiKeyOut, status_code=status.HTTP_201_CREATED)
def create_key(
    body: ApiKeyCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_user),
) -> ApiKeyOut:
    secret, prefix, digest = generate_api_key()
    row = ApiKey(
        user_id=user.id,
        name=body.name,
        key_prefix=prefix,
        key_hash=digest,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return ApiKeyOut(
        id=row.id,
        name=row.name,
        key_prefix=row.key_prefix,
        scopes=row.scopes,
        created_at=row.created_at,
        secret=secret,
    )
