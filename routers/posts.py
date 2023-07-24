from typing import List, Optional
from fastapi import HTTPException, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from starlette import status
import models
import oauth2
import schemas
from fastapi import APIRouter
from database import get_db

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

# @router.get('/', response_model=List[schemas.GetallPosts])
@router.get('/', response_model=List[schemas.OrmPostout])
def test_posts(db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user),limit:int=5,offset:int = 2 ,search:Optional[str]=""):
    # post = db.query(models.Post).filter(func.lower(models.Post.title).contains(search)).limit(limit).offset(skip).all()

    results =  db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Post.id == models.Votes.post_id,
                                                                                           isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search).limit(limit).offset(offset)).all()


    return  results

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=List[schemas.GetallPosts])
def test_posts_sent(post_post:schemas.CreatePost, db:Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    """This function creates post when the user is logged in"""
    new_post = models.Post(**post_post.dict(),owner_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return [new_post]


@router.get('/{id}', response_model=schemas.OrmPostout, status_code=status.HTTP_200_OK)
def get_test_one_post(id:int ,db:Session = Depends(get_db)):

    # idv_post = db.query(models.Post).filter(models.Post.id == id).first()

    indivual_post =db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Post.id == models.Votes.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not indivual_post:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"The id: {id} you requested for does not exist")
    return indivual_post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_test_post(id:int, db:Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):

    deleted_post_query = db.query(models.Post).filter(models.Post.id == id)


    deleted_post = deleted_post_query.first()

    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"The id: {id} you requested for does not exist")

    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Access Denied")

    deleted_post_query.delete(synchronize_session=False)
    db.commit()



@router.put('/{id}', response_model=schemas.GetallPosts)
def update_test_post(update_post:schemas.CreatePost, id:int, db:Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):

    updated_query =  db.query(models.Post).filter(models.Post.id == id)

    updated_post = updated_query.first()


    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id:{id} does not exist")

    if updated_post.owner_id != current_user.id:
        print(updated_post.owner_id)
        print(current_user.id)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access Denied")


    updated_query.update(update_post.dict(), synchronize_session=False)
    db.commit()


    return  updated_query.first()