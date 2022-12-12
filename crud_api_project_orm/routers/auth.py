from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, models, schemas, utils, oauth2

router = APIRouter( tags = ['Authentication'] )

@router.post("/login", response_model = schemas.Token )
async def login(user_cred: OAuth2PasswordRequestForm = Depends() ,db: Session = Depends(database.get_db)):
    # user_cred has following attributes
    # username : ....
    # password : ....
    user = db.query(models.User).filter( models.User.email == user_cred.username ).first()
    if user == None:
        raise HTTPException( status_code = status.HTTP_403_FORBIDDEN, detail = "Invalid credentials!" )
    elif not utils.verify( user_cred.password, user.password ):
        # This is the case where email exists in database, but provided PASSWORD IS INCORRECT!
        raise HTTPException( status_code = status.HTTP_403_FORBIDDEN, detail = "Invalid Credentials!" )
    else:
        access_token = oauth2.create_access_token( data = {"user_id": user.id} )
        return {"access_token": access_token, "token_type": "bearer"}