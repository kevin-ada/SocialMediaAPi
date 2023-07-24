from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

import oauth2, models, database
import schemas

routers = APIRouter(
    tags=["VOTES"],
    prefix="/vote"
)

@routers.post('/', status_code=status.HTTP_201_CREATED)
def vote(voted:schemas.Vote, db:Session = Depends(database.get_db), current_user:int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == voted.post_id).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post id {voted.post_id} does not exist")

    vote_query = db.query(models.Votes).filter(models.Votes.post_id == voted.post_id,
                                               models.Votes.user_id == current_user.id)
    vote_exists = vote_query.first()

    if voted.dir == 1:
        if vote_exists is None:
            new_vote = models.Votes(post_id=voted.post_id, user_id=current_user.id)
            db.add(new_vote)
            db.commit()
            return {"Detail":"Success"}
        raise HTTPException(status_code=status.HTTP_226_IM_USED, detail="The User has already Voted")
    else:
        if vote_exists is None:
            raise HTTPException(detail="Doesnt Exist", status_code=status.HTTP_404_NOT_FOUND)

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"Message":"Unliked"}





