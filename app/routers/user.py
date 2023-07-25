from fastapi import FastAPI, Depends, Response, status, HTTPException, APIRouter
from typing import List
from sqlalchemy.orm import Session

from .. import models
from ..database import engine, get_db
from ..schemas.schemas import UserCreate, UserOut
from ..utils import hash_password

router = APIRouter()

# HOME
@router.get("/sqlalchemy")
def home(db: Session = Depends(get_db)):
    return {"detail": "Welcome"}

# CREATE USER
@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Hash the password
    hashed_password = hash_password(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# GET ONE USER
@router.get("/users/{id}", response_model=UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id: {id} was not found')

    return user