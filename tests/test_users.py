from fastapi import status

from datetime import datetime, UTC
from bson import ObjectId


# get all users
def test_get_all_users(test_client):
    users = test_client.get(
        "/api/users/all-users"
    )

    assert users.status_code == status.HTTP_200_OK
    assert "users" in users.json()


# get one user
def test_get_one_user(test_client):
    add_user = test_client.post(
        "/api/users/add-user",
        json={
            "username": "omar1",
            "email": "omar1@gmail.com",
            "hash_password": "omar12345",
            "create_at": datetime.now(UTC).isoformat()
        }
    )

    assert add_user.status_code == status.HTTP_200_OK
    assert "id" in add_user.json()

    user_id = add_user.json()["id"]

    get_user = test_client.get(
        f"/api/users/one-user/{user_id}"
    )

    assert get_user.status_code == status.HTTP_200_OK
    assert get_user.json()["username"] == "omar1"


# get one user error
def test_get_one_user_invalid(test_client):
    fake_id = str(ObjectId())

    get_user = test_client.get(
        f"/api/users/one-user/{fake_id}"
    )

    assert get_user.status_code == status.HTTP_404_NOT_FOUND


# add user
def test_add_user(test_client):
    add_user = test_client.post(
        "/api/users/add-user",
        json={
            "username": "omar1",
            "email": "omar1@gmail.com",
            "hash_password": "omar12345",
            "create_at": datetime.now(UTC).isoformat()
        }
    )

    assert add_user.status_code == status.HTTP_200_OK
    assert add_user.json()["message"] == "User created successfully."
    assert "id" in add_user.json()


# add user error
def test_add_user_invalid(test_client):
    add_user = test_client.post(
        "/api/users/add-user",
        json={
            "username": "omar1",
            "email": "omar1@gmail.com",
            "hash_password": "omar12345",
            "create_at": datetime.now(UTC).isoformat()
        }
    )

    assert add_user.status_code == status.HTTP_200_OK

    exists_email = test_client.post(
        "/api/users/add-user",
        json={
            "username": "omar2",
            "email": "omar1@gmail.com",
            "hash_password": "omar123456",
            "create_at": datetime.now(UTC).isoformat()
        }
    )

    assert exists_email.status_code == status.HTTP_400_BAD_REQUEST


# update user
def test_update_user(test_client):
    add_user = test_client.post(
        "/api/users/add-user",
        json={
            "username": "omar1",
            "email": "omar1@gmail.com",
            "hash_password": "omar12345",
            "create_at": datetime.now(UTC).isoformat()
        }
    )

    assert add_user.status_code == status.HTTP_200_OK
    assert "id" in add_user.json()

    user_id = add_user.json()["id"]

    updated_date = {
        "username": "omar3"
    }

    update_username = test_client.patch(
        f"/api/users/update-user/{user_id}",
        json=updated_date
    )

    assert update_username.status_code == status.HTTP_200_OK
    assert update_username.json()["message"] == "User updated successfully."


# delete user
def test_delete_user(test_client):
    add_user = test_client.post(
        "/api/users/add-user",
        json={
            "username": "omar1",
            "email": "omar1@gmail.com",
            "hash_password": "omar12345",
            "create_at": datetime.now(UTC).isoformat()
        }
    )

    assert add_user.status_code == status.HTTP_200_OK
    assert "id" in add_user.json()

    user_id = add_user.json()["id"]

    delete_user = test_client.delete(
        f"/api/users/delete-user/{user_id}"
    )

    assert delete_user.status_code == status.HTTP_200_OK
    assert delete_user.json()["message"] == "User deleted successfully."


# delete user error
def test_delete_user_invalid(test_client):
    fake_id = str(ObjectId())

    delete_user = test_client.delete(
        f"/api/users/delete-user/{fake_id}"
    )

    assert delete_user.status_code == status.HTTP_404_NOT_FOUND


# register
def test_register(test_client):
    register = test_client.post(
        "/api/users/register",
        data={
            "username": "omar2",
            "email": "omar1@gmail.com",
            "password": "omar123456"
        },
        follow_redirects=False
    )

    assert register.status_code == 303
    assert register.headers["location"] == "/login"


# register error
def test_register_invalid(test_client):
    register = test_client.post(
        "/api/users/register",
        data={
            "username": "omar2",
            "email": "omar1@gmail.com",
            "password": "omar123456"
        },
        follow_redirects=False
    )

    assert register.status_code == 303
    
    invalid_register = test_client.post(
        "/api/users/register",
        data={
            "username": "omar4",
            "email": "omar1@gmail.com",
            "password": "omar1234"
        },
        follow_redirects=False
    )

    assert invalid_register.status_code == status.HTTP_400_BAD_REQUEST


# login
def test_login(test_client):
    register = test_client.post(
        "/api/users/register",
        data={
            "username": "omar2",
            "email": "omar1@gmail.com",
            "password": "omar123456"
        },
        follow_redirects=False
    )

    assert register.status_code == 303

    login = test_client.post(
        "/api/users/login",
        data={
            "email": "omar1@gmail.com",
            "password": "omar123456"
        },
        follow_redirects=False
    )

    assert login.status_code == 303
    assert login.headers["location"] == "/"


# login error
def test_login_invalid_email(test_client):
    register = test_client.post(
        "/api/users/register",
        data={
            "username": "omar2",
            "email": "omar1@gmail.com",
            "password": "omar123456"
        },
        follow_redirects=False
    )

    assert register.status_code == 303

    login = test_client.post(
        "/api/users/login",
        data={
            "email": "omar2@gmail.com",
            "password": "omar123456"
        },
        follow_redirects=False
    )

    assert login.status_code == status.HTTP_400_BAD_REQUEST


def test_login_invalid_password(test_client):
    register = test_client.post(
        "/api/users/register",
        data={
            "username": "omar2",
            "email": "omar1@gmail.com",
            "password": "omar123456"
        },
        follow_redirects=False
    )

    assert register.status_code == 303

    login = test_client.post(
        "/api/users/login",
        data={
            "email": "omar2@gmail.com",
            "password": "omar1234"
        },
        follow_redirects=False
    )

    assert login.status_code == status.HTTP_400_BAD_REQUEST


# logout
def test_logout(logged_in_client):
    logout = logged_in_client.get(
        "/api/users/logout",
        follow_redirects=False
    )

    assert logout.status_code == 303
    assert logout.headers["location"] == "/login"

