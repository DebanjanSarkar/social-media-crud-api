from passlib.context import CryptContext

# Creating context object for hasing passwords
pwd_context = CryptContext(schemes = "bcrypt", deprecated = "auto")

def hash(password):
    """
    Takes 1 argument - the plain text password, and returns the hashed password.
    Algorithm library used - Bcrypt
    """
    return pwd_context.hash( password )

def verify(plain_password, hashed_password):
    """
    Takes 2 argument:-
    1st - Takes the plain text password
    2nd - Takes the hashed password, usually retrieved from database
    Returns - 
    """
    return pwd_context.verify(plain_password, hashed_password)