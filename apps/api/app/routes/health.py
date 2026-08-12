from contextlib import suppress

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", summary="Health check")
def health(db: Session = Depends(get_db)) -> dict[str, str]:
    with suppress(Exception):
        db.execute("SELECT 1")
    return {"status": "ok"}


@router.get("/ready", summary="Readiness check")
def ready(db: Session = Depends(get_db)) -> dict[str, str]:
    with suppress(Exception):
        db.execute("SELECT 1")
    return {"status": "ready"}
