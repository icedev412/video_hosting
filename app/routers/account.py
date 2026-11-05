from fastapi import APIRouter, HTTPException
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import or_, select
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from app.core.database import get_db
from app.models.user import User, UserSession, hash_token
from app.schemas.auth import UserChangePassword, UserDeleteAccount, UserLogin, UserRegister, UserResponse
from fastapi import status
from sqlalchemy.exc import IntegrityError
import secrets
from datetime import datetime, timedelta, timezone
from fastapi import Response
import secrets
from datetime import datetime, timedelta, timezone
from fastapi import Response


from app.core.security import verify_password, hash_password

from app.routers.auth import templates
from app.routers.auth import get_current_user








router = APIRouter(
    prefix="/account",
    tags=["Authentication"],
)



@router.get("/")
def account(request: Request, db: Session = Depends(get_db)):
    users = db.scalars(select(User)).all()

    return templates.TemplateResponse(
        request=request,
        name="accounts.html",
        context={"users": users},
    )



@router.get("/settings/")
def account(request: Request, user: User = Depends(get_current_user)):
    return templates.TemplateResponse(
        request=request,
        name="account_settings.html",
        context={"user": user},
    )


@router.get("/settings/admin")
def account(request: Request, user: User = Depends(get_current_user)):

    return templates.TemplateResponse(
        request=request,
        name="account_settings.html",
        context={"user": user},
    )


@router.post("/change-password")
def account(data: UserChangePassword, request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    ok = verify_password(data.old_password, user.password_hash)
    if ok:
        user.password_hash = hash_password(data.new_password)
        db.commit()
    if not user or not ok:
        raise HTTPException(401, "Incorrect username or password")
    return {"ok": True}


@router.post("/delete-account")
def account(data: UserDeleteAccount, request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    ok = verify_password(data.password, user.password_hash)
    if ok:
        db.delete(user)
        db.commit()
    if not user or not ok:
        raise HTTPException(401, "Incorrect username or password")
    return {"ok": True}