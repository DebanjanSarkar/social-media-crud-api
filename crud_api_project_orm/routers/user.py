from fastapi import APIRouter, Depends, status, HTTPException
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix = "/users",
    tags = ["Users"]
)

"""
    Path Operations handling users
"""
# New User registration
@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.UserResponse)
async def create_user(user: schemas.UserCreate ,db: Session = Depends(get_db)):
    # converting the password into hash, and storing it into the original variable
    user.password = utils.hash( user.password )

    new_user = models.User( **user.dict() )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Fetching a User's details
@router.get("/{id}", response_model = schemas.UserResponse )
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query( models.User ).filter( models.User.id == id ).first()
    if user == None:
        raise HTTPException( status_code = status.HTTP_404_NOT_FOUND, detail = f"User with id = {id} does not exist!" )
    else:
        return user

