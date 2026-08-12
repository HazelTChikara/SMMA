from collections.abc import Generator
from datetime import datetime, timezone

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.auth import hash_session_token
from app.db import SessionLocal
from app.models import Session as AuthSession, User


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    token = request.cookies.get("smma_session")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    auth_session = db.query(AuthSession).filter(AuthSession.token_hash == hash_session_token(token)).first()
    if not auth_session or auth_session.expires_at <= datetime.now(timezone.utc) or not auth_session.user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired")
    return auth_session.user
