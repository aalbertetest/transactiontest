from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from payhub.auth import authenticate_user, create_access_token, get_user_by_email, hash_password
from payhub.db import get_db
from payhub.deps import require_user
from payhub.models import User, UserRole
from payhub.rate_limit import limiter
from payhub.schemas import LoginBody, Token, UserCreate, UserOut

router = APIRouter(prefix="/v1/users", tags=["users"])


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(body: UserCreate, db: Session = Depends(get_db)) -> User:
    if get_user_by_email(db, body.email):
        raise HTTPException(status_code=409, detail="email_taken")
    u = User(
        email=str(body.email),
        hashed_password=hash_password(body.password),
        role=UserRole.customer,
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    return u


@router.post("/token", response_model=Token)
@limiter.limit("20/minute")
def login(request: Request, body: LoginBody, db: Session = Depends(get_db)) -> Token:
    user = authenticate_user(db, str(body.email), body.password)
    if not user:
        raise HTTPException(status_code=401, detail="invalid_credentials")
    token = create_access_token(user.id, user.role)
    return Token(access_token=token)


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(require_user)) -> User:
    return user
