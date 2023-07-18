from typing import List
from fastapi import HTTPException, Depends, APIRouter,status
from sqlalchemy.orm import Session
import models
import schemas
from database import get_db
from utils import hash_pass


router = APIRouter(
        prefix='/users',
        tags=['Users']
)


@router.post('/', response_model=List[schemas.UserOutput])
def get_users(user:schemas.CreateUser,db:Session = Depends(get_db)):

    # Hash The Password
    hashed_pass = hash_pass(user.password)

    user.password = hashed_pass

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return [new_user]

@router.get('/{id}', response_model=schemas.UserOutput)
def getoneUser(id:int,user:schemas.CreateUser,db:Session = Depends(get_db)):

    one_post = models.User(**user.dict())

    if one_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id: {id} does not exist")

    db.commit()

    return one_post