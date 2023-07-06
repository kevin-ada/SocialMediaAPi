import psycopg2 as psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, status, HTTPException, Depends
import schemas
from pydantic import BaseModel
import time

from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




while True:
    try:
        connection = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='Bright#1270',
                                      cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        print("Connection Was Successful")
        break
    except Exception as err:
        print("Connection To DB failed")
        print(f"The Error thrown was: {err}")
        time.sleep(5)








@app.get('/posts')
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}

@app.get('/sqlalchemy')
def test_posts(db: Session = Depends(get_db)):

    post = db.query(models.Post).all()


    return {"Data": post}

@app.post('/sqlalchemy')
def test_posts_sent(post_post:schemas.CreatePost, db:Session = Depends(get_db)):

    new_post = models.Post(**post_post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"Details":new_post}


@app.get('/sqlalchemy/{id}')
def get_test_one_post(id:int ,db:Session = Depends(get_db)):

    idv_post = db.query(models.Post).filter(models.Post.id == id).first()

    if idv_post is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"The id: {id} you requested for does not exist")
    return {"message": idv_post}

@app.delete('/sqlalchemy/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_test_post(id:int, db:Session = Depends(get_db)):

    deleted_post = db.query(models.Post).filter(models.Post.id == id)


    if deleted_post.first() is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"The id: {id} you requested for does not exist")
    deleted_post.delete(synchronize_session=False)
    db.commit()

    return {"Status", "Successfully Deleted"}


@app.put('/sqlalchemy/{id}')
def update_test_post(update_post:schemas.UpdatePost, id:int, db:Session = Depends(get_db)):

    updated_post =  db.query(models.Post).filter(models.Post.id == id)

    if updated_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id:{id} does not exist")
    updated_post.update(update_post.dict(), synchronize_session=False)
    db.commit()


    return {"Detail": updated_post.first()}





@app.post('/posts',status_code=status.HTTP_201_CREATED)
def post(post:schemas.CreatePost):
    cursor.execute("""INSERT INTO posts (title, contents) VALUES(%s, %s) RETURNING *""",(post.title, post.contents))

    new_post = cursor.fetchone()

    connection.commit()

    return {"Data":new_post}

@app.get('/posts/{id}')
def indv_post(id:int):
    
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)),)

    post = cursor.fetchone()

    if post is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"The id: {id} you requested for does not exist")
    return {"message": post}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    """Deleting a post by popping the index indicated"""
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """,(str(id),))

    deleted_post = cursor.fetchone()

    connection.commit()

    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id: {id} does not Exist")


    return {"message": deleted_post}


@app.put('/posts/{id}', status_code=status.HTTP_200_OK)
def update_post(new_post:schemas.UpdatePost, id:int):

    """Updating Posts"""

    cursor.execute("""UPDATE posts SET title=%s, contents=%s WHERE id = %s RETURNING *""", (new_post.title, new_post.contents, str(id),),)

    updated_post = cursor.fetchone()

    connection.commit()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id:{id} does not exist")
    return {"data": updated_post}
