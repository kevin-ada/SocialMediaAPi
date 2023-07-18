from fastapi import Depends
from jose import jwt,JWTError
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

import database
import models
import schemas
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status
from config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"expire": expire.strftime("%Y-%m-%d %H:%M:%S")})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY,ALGORITHM)

    return encoded_jwt

def verify_token_access(token:str, credentials_exception):

     try:
         payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)

         id:str = payload.get("user_id")

         if id is None:
             raise credentials_exception
         token_data = schemas.DataToken(id=id)
     except JWTError as e:
         print(e)
         raise credentials_exception

     return token_data


def get_current_user(token:str = Depends(oauth2_scheme), db:Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not Validate Credentials", headers={"WWW-Authenticate":"Bearer"})

    token = verify_token_access(token,credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user