from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import or_, select
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from app.core.database import get_db
from app.models.user import User, UserSession, hash_token
from app.schemas.auth import UserLogin, UserRegister, UserResponse
from fastapi import status
from sqlalchemy.exc import IntegrityError
import secrets
from datetime import datetime, timedelta, timezone
from fastapi import Response
import secrets
from datetime import datetime, timedelta, timezone
from fastapi import Response


from app.core.security import verify_password, hash_password


templates = Jinja2Templates(directory="app/templates")

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.get("/register")
def get_register(request: Request):
    return templates.TemplateResponse(
        request=request, #jinja2 templates require the request object to be passed in order to render the template correctly.
        name = "register.html" )


@router.post("/register",response_model=UserResponse, status_code=status.HTTP_201_CREATED) #response_model=UserResponse, is used to specify the response model for the endpoint. It ensures that the response returned by the endpoint will be validated against the UserResponse schema.
def register(
    data: UserRegister,
    db: Session = Depends(get_db),
):
    stmt = select(User).where(
        (User.username == data.username)
        | (User.email == data.email)
    )

    existing_user = db.execute(stmt).scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Username or email already exists",
        )

    password_hash = hash_password(data.password)

    user = User(
        username=data.username,
        email=data.email,
        password_hash=password_hash,
    )

    db.add(user)
    try:
        db.commit()
    except IntegrityError:          # two simultaneous requests slipped past the check
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, "Username or email already registered")
    db.refresh(user)  # is used to refresh the user object with the latest data from the database. It is useful when you want to get the auto-generated fields like id after committing the transaction.

    return user


SESSION_DAYS = 14
COOKIE_NAME = "session"


@router.get("/login")
def get_login(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
    )


@router.post("/login")
def login(
    response: Response,
    data: UserLogin,
    db: Session = Depends(get_db),
):
    
    user = db.scalar(
        select(User).where(
            or_(User.username == data.username)
        )
    )
    DUMMY_HASH = hash_password("dummy-password")  # module level

    user = db.scalar(select(User).where(User.username == data.username))
    stored = user.password_hash if user else DUMMY_HASH
    ok = verify_password(data.password, stored)
    if not user or not ok:
        raise HTTPException(401, "Incorrect username or password")

    token = secrets.token_urlsafe(32)            # 256 bits of randomness
    db.add(UserSession(
        token_hash=hash_token(token),
        user_id=user.id,
        expires_at=datetime.now(timezone.utc) + timedelta(days=SESSION_DAYS),
    ))
    db.commit()

    response.set_cookie(
        COOKIE_NAME, token,
        max_age=SESSION_DAYS * 86400,
        httponly=True,
        secure=False,        # set False only for local http development
        samesite="lax",
    )
    return {"ok": True}


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        raise HTTPException(401, "Not authenticated")

    sess = db.scalar(select(UserSession).where(
        UserSession.token_hash == hash_token(token),
        UserSession.expires_at > datetime.now(timezone.utc),
    ))
    if not sess:
        raise HTTPException(401, "Session expired or invalid")
    return sess.user

@router.get("/account")
def me(user: User = Depends(get_current_user)):
    return user