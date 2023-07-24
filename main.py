import psycopg2 as psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI
from routers import auth, users, posts,vote
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins=['*']



app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.routers)
app.include_router(vote.routers)


@app.get('/')
def root():
    return {"Message":"Success"}