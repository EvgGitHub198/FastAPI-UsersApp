from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends
from models import User
from db import SessionLocal

user_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@user_router.get("/users")
async def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@user_router.post("/users")
async def create_user(user: User, db: Session = Depends(get_db)):
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User created successfully"}

@user_router.get("/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    return user

@user_router.put("/users/{user_id}")
async def update_user(user_id: int, user: User, db: Session = Depends(get_db)):
    user_data = db.query(User).filter(User.id == user_id).first()
    if user_data:
        user_data.name = user.name
        user_data.email = user.email
        db.commit()
        return {"message": "User updated successfully"}
    return {"message": "User not found"}

@user_router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    if user:
        db.delete(user)
        db.commit()
        return {"message": "User deleted successfully"}
    return {"message": "User not found"}
