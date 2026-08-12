from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from app.auth import hash_password, hash_session_token, new_session_token, verify_password
from app.config import settings
from app.dependencies import get_current_user, get_db
from app.models import Session as AuthSession, User

router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=120)
    password: str = Field(min_length=12, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str


def set_session(response: Response, db: Session, user: User) -> None:
    token = new_session_token()
    db.add(AuthSession(user_id=user.id, token_hash=hash_session_token(token), expires_at=datetime.now(timezone.utc) + timedelta(hours=settings.session_ttl_hours)))
    db.commit()
    response.set_cookie("smma_session", token, httponly=True, secure=settings.session_cookie_secure, samesite="lax", max_age=settings.session_ttl_hours * 3600, path="/")


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, response: Response, db: Session = Depends(get_db)) -> User:
    email = payload.email.lower()
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=409, detail="An account with this email already exists")
    user = User(email=email, full_name=payload.full_name.strip(), password_hash=hash_password(payload.password))
    db.add(user)
    db.flush()
    set_session(response, db, user)
    return user


@router.post("/login", response_model=UserResponse)
def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)) -> User:
    user = db.query(User).filter(User.email == payload.email.lower()).first()
    if not user or not verify_password(payload.password, user.password_hash) or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    set_session(response, db, user)
    return user


@router.get("/me", response_model=UserResponse)
def me(user: User = Depends(get_current_user)) -> User:
    return user


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(request: Request, response: Response, db: Session = Depends(get_db)) -> None:
    token = request.cookies.get("smma_session")
    if token:
        db.query(AuthSession).filter(AuthSession.token_hash == hash_session_token(token)).delete()
        db.commit()
    response.delete_cookie("smma_session", path="/")
