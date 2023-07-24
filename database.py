from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#
#
# while True:
#     try:
#         connection = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='Bright#1270',
#                                       cursor_factory=RealDictCursor)
#         cursor = connection.cursor()
#         print("Connection Was Successful")
#         break
#     except Exception as err:
#         print("Connection To DB failed")
#         print(f"The Error thrown was: {err}")
#         time.sleep(5)
#

