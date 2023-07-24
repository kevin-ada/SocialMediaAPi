from pydantic import BaseSettings

class Settings(BaseSettings):
    secret_key:str
    algorithm:str
    access_token_expire_minutes:int
    database_name:str
    database_username:str
    database_password:str
    database_hostname:str

    class Config:
        env_file = ".env"

settings = Settings(
    secret_key="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7",
    algorithm="HS256",
    access_token_expire_minutes=30,  # Some appropriate value
    database_name="fastapi",
    database_username="postgres",
    database_password="Bright#1270",
    database_hostname="localhost"
    ,)

