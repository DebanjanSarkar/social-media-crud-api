from fastapi import APIRouter, Depends, Response, status, HTTPException
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func


router = APIRouter(
    prefix = "/posts",
    tags = ["Posts"]
)

"""
    Path operations for Handling Post related CRUD operations
"""
# Getting all the posts
# @router.get("/", response_model = List[schemas.PostResponse])
@router.get("/", response_model = List[schemas.PostVotesResponse])
async def get_posts(db: Session = Depends(get_db) , current_user = Depends(oauth2.get_current_user) ,
limit: int = 10, skip: int = 0, search: Optional[str] = "" ):
    # all_posts = db.query(models.Post).filter( models.Post.title.contains(search) ).limit(limit).offset(skip).all()
    # return all_posts
    all_posts_with_votes = db.query( models.Post, func.count( models.Vote.post_id ).label("votes") ).join( models.Vote, models.Vote.post_id == models.Post.id, isouter=True ).group_by(models.Post.id).filter( models.Post.title.contains(search) ).limit(limit).offset(skip).all()
    return all_posts_with_votes


# Getting single specified post
@router.get("/{id}", response_model = schemas.PostVotesResponse)
async def get_post(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # req_post = db.query(models.Post).filter( models.Post.id == id ).first()
    req_post = db.query( models.Post, func.count( models.Vote.post_id ).label("votes") ).join( models.Vote, models.Vote.post_id == models.Post.id, isouter=True ).group_by(models.Post.id).filter( models.Post.id == id ).first()
    if req_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Post with id={id} does not exist!")
    else:
        return req_post

# Creating a post
@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.PostResponse)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user) ):
    # new_post = models.Post( title=post.title, content=post.content, published=post.published )
    new_post = models.Post( **post.dict() )
    # Adding owner_id column value to the new_post object
    new_post.owner_id = current_user.id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# Updating a post
@router.put("/{id}", response_model = schemas.PostResponse)
async def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    fetched_post = post_query.first()
    if fetched_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id = {id} does not exist!")
    elif fetched_post.owner_id != current_user.id:
        # Case when user being logged in is trying to delete post created by other user.
        raise HTTPException( status_code = status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform requested action!" )
    else:
        post_query.update( post.dict(), synchronize_session = False )
        db.commit()
        return post_query.first()


# Deleting a post
@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    fetched_post = post_query.first()
    if fetched_post == None:
        raise HTTPException( status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id={id} does not exist!" )
    elif fetched_post.owner_id != current_user.id:
        # Case when user being logged in is trying to delete post created by other user.
        raise HTTPException( status_code = status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform requested action!" )
    else:
        post_query.delete( synchronize_session = False )
        db.commit()
        return Response( status_code = status.HTTP_204_NO_CONTENT )

