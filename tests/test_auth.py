from dotenv import load_dotenv
load_dotenv('.env.test',override=True)


from typing import override
from httpx import Client
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from app.core.database import Base, get_db
from app.core.config import settings

engine=create_engine(settings.DATABASE_URL)
TestingSessionLocal=sessionmaker(bind=engine)

def override_get_db():
    db=TestingSessionLocal()
    try:
        yield db
    
    finally:
        db.close()

app.dependency_overrides[get_db]=override_get_db
client=TestClient(app)


def test_register_success():
    response=client.post("/api/auth/register", json={
        "email":"test1@gmail.com",
        "password":"password123"
    })
    assert response.status_code==201
    data=response.json()
    assert "email" in data
    assert data['email']=="test1@gmail.com"


def test_register_duplicate_email():
    payload={
        "email":"duplicate@gmail.com",
        "password":"password123"
    }
    client.post("/api/auth/register",json=payload)
    response=client.post("/api/auth/register",json=payload)
    assert response.status_code==400

def test_login_status():
    payload={
        "email":"login@gmail.com",
        "password":"password123"
    }
    client.post("/api/auth/register",json=payload)
    response=client.post("/api/auth/login",json=payload)
    
    assert response.status_code==200
    data=response.json()
    assert "access_token" in data
    assert data['token_type']=="bearer"

def test_login_wrong_password():
    payload={
        "email":"wrongpass@gmail.com",
        "password":"password123",
    }
    client.post("/api/auth/register",json=payload)

    response=client.post('/api/auth/login',json={
        "email":"wrongpass@gmail.com",
        "password":"wrongpassword"
    })
    assert response.status_code==401

def test_protected_route_without_token():
    response=client.get("/api/auth/me")

    assert response.status_code==401

@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
