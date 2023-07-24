from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from database import get_db, Base
import pytest
from main import app
import httpx


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Bright#1270@localhost:5432/test_fastapi"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)






@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
        app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)



def test_root():
    res = client.get('/')
    assert res.json() == {"Message":"Success"}
    assert res.status_code == 200

def test_create_user(client):
    res = client.post('/users', json={"email":"jim@gmail.com", "password":"joe@123"})
    assert res.status_code  == 201
    user = res.json()
    assert user.get("email") == "jim@gmail.com"

