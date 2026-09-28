from typing import Annotated
from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel, EmailStr, Field
app = FastAPI(title="Video Hosting API")
templates = Jinja2Templates(directory="app/templates")


class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)





@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse(
        request=request, # do not forget the the new version of starlette requires the request parameter to be passed to the template response
        name="register.html"
    )


@app.post("/register")
async def register(data: UserRegister):
    print(data)
    return {"message": "User registered successfully", "user": data.dict()}