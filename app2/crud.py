from sqlmodel import Session, select
from models import User
from schemas import UserCreate

def get_user_by_username(session: Session, username: str):
    return session.exec(select(User).where(User.username == username)).first()

def create_user(session: Session, user_create: UserCreate):
    user = User(username=user_create.username, password=user_create.password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
