from fastapi import FastAPI, Depends, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List

from .. import models
from ..database import engine, get_db
from ..schemas.schemas import PostBase, PostCreate, PostUpdate, PostResponse

router = APIRouter()

# GET POSTS
@router.get("/posts", response_model=List[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    post_query = db.query(models.Post)
    posts = post_query.all()
    return posts

# CREATE A POST
@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_posts(post: PostCreate, db: Session = Depends(get_db)):
    # new_post = models.Post(**post.dict())
    new_post = models.Post(title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# GET ONE PRODUCT
@router.get("/posts/{id}", response_model=PostResponse)
def get_product(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id: {id} was not found')

    return post

# DELETE ONE PRODUCT
@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_one_product(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    deleted_post = post_query.first()

    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id: {id} was not found')

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# UPDATE A PRODUCT
@router.put("/posts/{id}", response_model=PostResponse)
def update_one_product(id: int, post: PostUpdate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id: {id} was not found')

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()