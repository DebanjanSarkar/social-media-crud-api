from jose import jwt, JWTError
from datetime import datetime, timedelta
from . import schemas, database, models
from .config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer( tokenUrl = "login" )

# Details for the JWT generation
SECRET_KEY = settings.secret_key
ALGORITHM = settings.password_hash_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    # Making a copy of the data that is passed as argument, and is to be encoded in the payload
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta( minutes = ACCESS_TOKEN_EXPIRE_MINUTES )
    to_encode.update( {"exp": expire} )

    # Generating the JWT token with all the information
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM )

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM] )
        user_id: str = payload.get("user_id")

        if user_id == None:
            raise credentials_exception
        token_data = schemas.TokenData( id = user_id )
    except JWTError:
        raise credentials_exception
    return token_data


def get_current_user( token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db) ):
    credentials_exception = HTTPException( 
        status_code = status.HTTP_401_UNAUTHORIZED, 
        detail = "Could not validate credentials.", 
        headers = {"WWW-Authenticate": "Bearer"}
        )
    
    # Verify the token and get the user id from the returned token_data, the fetch the user from database
    token_data = verify_access_token( token, credentials_exception )
    user = db.query( models.User ).filter( models.User.id == token_data.id ).first()
    return user
