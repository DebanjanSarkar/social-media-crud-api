from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session
from .. import database, models, schemas, oauth2


router = APIRouter(
    prefix = "/vote",
    tags = ["Votes"]
)

"""
    Path operations for Handling votes related operations
"""
@router.post("/", status_code = status.HTTP_201_CREATED )
async def vote( vote: schemas.Vote, db: Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user) ):
    # If post with passed id does not exist, user gets a 404 error
    post_voted = db.query( models.Post ).filter( models.Post.id == vote.post_id ).first()
    if not post_voted:
        raise HTTPException( status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id={vote.post_id} does not exist!" )
    
    vote_query = db.query( models.Vote ).filter( 
            models.Vote.user_id == current_user.id,
            models.Vote.post_id == vote.post_id)
    existing_vote = vote_query.first()
    if vote.dir == True:
        # Post is being liked/voted by user -- number of votes increases        
        if not existing_vote:
            # If the user post combination does not exist, then vote will be added for the post
            vote_to_be_added = models.Vote( post_id=vote.post_id, user_id=current_user.id )
            db.add( vote_to_be_added )
            db.commit()
            db.refresh( vote_to_be_added )
            return {"vote": vote_to_be_added, "detail": "Successfully voted for the post!"}
        else:
            # Vote exists, and still voting with dir 1 is attempted
            raise HTTPException( status_code = status.HTTP_409_CONFLICT,
                detail = f"User with user id = {current_user.id} has already voted post with id = {vote.post_id}." )
    else:
        # Vote is being removed from the post by user -- number of votes decreases
        if existing_vote:
            # Vote exists, thus needs to be deleted.
            vote_query.delete( synchronize_session = False )
            db.commit()
            return {"detail": "Successfully removed the vote for the post!"}
        else:
            # Vote does not exists, then too attempted to be deleted.
            raise HTTPException( status_code = status.HTTP_404_NOT_FOUND,
                detail = "Vote does not exists!" )
