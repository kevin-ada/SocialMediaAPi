import psycopg2 as psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI
import time
from routers import auth, users, posts,vote
from database import engine, Base

# Base.metadata.create_all(bind=engine)





app = FastAPI()





app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.routers)
app.include_router(vote.routers)