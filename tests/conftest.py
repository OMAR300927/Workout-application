import pytest

from fastapi.testclient import TestClient
from fastapi import status
from pymongo import MongoClient

from main import app
from database import get_users_collection, get_workout_collection, get_db
from config import settings


uri = settings.database_url


@pytest.fixture()
def test_db():
    client = MongoClient(uri)

    db = client.test_workout_app

    yield db

    client.drop_database("test_workout_app")


@pytest.fixture()
def test_client(test_db):

    def override_db():
        return test_db

    def override_get_users_collection():
        return test_db["test_users"]
    
    def override_get_workout_collection():
        return test_db["test_workouts"]
    
    app.dependency_overrides[get_db] = override_db
    app.dependency_overrides[get_users_collection] = override_get_users_collection
    app.dependency_overrides[get_workout_collection] = override_get_workout_collection

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture()
def logged_in_client(test_client):
    register = test_client.post(
        "/api/users/register",
        data={
            "username": "test",
            "email": "test@gmail.com",
            "password": "test1234"
        }
    )

    assert register.status_code == status.HTTP_200_OK

    login = test_client.post(
        "/api/users/login",
        data={
            "email": "test@gmail.com",
            "password": "test1234"
        }
    )

    assert login.status_code == status.HTTP_200_OK

    return test_client