from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from app.core.database import get_db
from app.models.user import User
from app.schemas.auth import UserRegister, UserResponse

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


@router.post("/register",response_model=UserResponse,) #response_model=UserResponse, is used to specify the response model for the endpoint. It ensures that the response returned by the endpoint will be validated against the UserResponse schema.
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

    password_hash = data.password

    user = User(
        username=data.username,
        email=data.email,
        password_hash=password_hash,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user