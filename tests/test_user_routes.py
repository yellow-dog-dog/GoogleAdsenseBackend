import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from tortoise.contrib.test import finalizer, initializer
import asyncio

from app.main import app
from app.config import settings
from app.user.schemas import UserCreate, UserLogin

@pytest.fixture(scope="module")
def test_app():
    initializer(["app.user.models"])
    yield app
    finalizer()

@pytest.fixture(scope="module")
def event_loop(request):
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.mark.asyncio
async def test_register_user(test_app: FastAPI):
    async with AsyncClient(app=test_app, base_url="http://test") as ac:
        response = await ac.post("/api/register", json={
            "username": "testuser",
            "password": "password123",
            "email": "test@example.com"
        })
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

@pytest.mark.asyncio
async def test_login_user(test_app: FastAPI):
    async with AsyncClient(app=test_app, base_url="http://test") as ac:
        # Register user first
        await ac.post("/api/register", json={
            "username": "testuser",
            "password": "password123",
            "email": "test@example.com"
        })
        # Login user
        response = await ac.post("/api/login", json={
            "username": "testuser",
            "password": "password123"
        })
    assert response.status_code == 200
    assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_get_current_user(test_app: FastAPI):
    async with AsyncClient(app=test_app, base_url="http://test") as ac:
        # Register and login user
        await ac.post("/api/register", json={
            "username": "testuser",
            "password": "password123",
            "email": "test@example.com"
        })
        login_response = await ac.post("/api/login", json={
            "username": "testuser",
            "password": "password123"
        })
        token = login_response.json()["access_token"]

        # Get current user
        response = await ac.get("/api/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
