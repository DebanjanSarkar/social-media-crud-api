from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from .database import engine
from .routers import post, user, auth, vote

# Create the database table using sqlalchemy, if it does not exists
# models.Base.metadata.create_all(bind = engine)


app = FastAPI()

# CORS configuration
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Demo Path operation on the root path, for testing purposes.
@app.get("/")
async def home():
    return {"detail": "This API is developed by Debanjan Sarkar, using FastAPI framework."}

# Path operations related to user functionality, i.e., user registrations
app.include_router( user.router )

# Path operations related to User Authentication and Login
app.include_router( auth.router )

# Path operations related to CRUD operations on posts
app.include_router( post.router )

# Path operations related to vote operations on posts
app.include_router( vote.router )
