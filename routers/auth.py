from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
import schemas
import utils
from database import get_db
from oauth2 import create_access_token
from fastapi.security import  OAuth2PasswordRequestForm

routers = APIRouter(
    tags= ['Authentication']
)

@routers.post('/login', response_model=schemas.Token)
def login(userdetails:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    user  = db.query(models.User).filter(models.User.email == userdetails.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"The User Does not exist")

    if not utils.verify_password(userdetails.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The Passwords do not match")

    access_token = create_access_token(data={"user_id":user.id})

    return {"access_token":access_token, "token_type":"bearer"}