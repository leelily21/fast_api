from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Session
from database import engine, get_session
from models import User
from schemas import UserCreate, UserLogin
from crud import get_user_by_username, create_user

app = FastAPI()

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.post("/register")
def register(user_create: UserCreate, session: Session = Depends(get_session)):
    existing_user = get_user_by_username(session, user_create.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    user = create_user(session, user_create)
    return {"id": user.id, "username": user.username}

@app.post("/login")
def login(user_login: UserLogin, session: Session = Depends(get_session)):
    user = get_user_by_username(session, user_login.username)
    if not user or user.password != user_login.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful", "username": user.username}
