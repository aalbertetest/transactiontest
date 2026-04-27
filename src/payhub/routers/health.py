from fastapi import APIRouter

from payhub.config import get_settings
from payhub.schemas import HealthOut

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthOut)
def health() -> HealthOut:
    s = get_settings()
    return HealthOut(status="ok", environment=s.environment)
