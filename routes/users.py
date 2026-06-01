
from fastapi import APIRouter, Depends, HTTPException,status, Form
from fastapi.responses import RedirectResponse

from modules.schema import UserCreate, UserUpdate
from modules.model import one_user, all_users
from database import get_users_collection
from auth.auth import hash_pass, verify_hash_pass, create_access_token
from config import settings

from bson import ObjectId
from datetime import datetime, UTC, timedelta

router = APIRouter()


@router.get("/all-users")
def get_all_users(collection = Depends(get_users_collection)):
    users = all_users(collection.find())

    return {"users": users}


@router.get("/one-user/{user_id}")
def get_one_user(user_id: str, collection = Depends(get_users_collection)):
    user = collection.find_one({"_id": ObjectId(user_id)})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User doesn't exists"
        )
    
    return one_user(user)


@router.post("/add-user")
def add_user(user: UserCreate, collection = Depends(get_users_collection)):
    exists_username = collection.find_one({"username": user.username})
    
    if exists_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    exists_email = collection.find_one({"email": user.email})
    
    if exists_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    
    new_user = {
        "username": user.username,
        "email": user.email,
        "hash_password": hash_pass(user.hash_password),
        "create_at": datetime.now(UTC)
    }

    added_user = collection.insert_one(new_user)
    return {"message": "User created successfully.", "id": str(added_user.inserted_id)}


@router.patch("/update-user/{user_id}")
def update_user(user_id: str, user: UserUpdate, collection = Depends(get_users_collection)):
    get_user = one_user(collection.find_one({"_id": ObjectId(user_id)}))

    if not get_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User doesn't exists"
        )
    
    updated_data = {}

    if user.username is not None:
        updated_data["username"] = user.username

    if user.email is not None:
        updated_data["email"] = user.email

    if user.hash_password is not None:
        updated_data["hash_password"] = hash_pass(user.hash_password)

    collection.find_one_and_update(
        {"_id": ObjectId(user_id)},
        {"$set": updated_data}   
    )
    return {"message": "User updated successfully."}


@router.delete("/delete-user/{user_id}")
def delete_user(user_id: str, collection = Depends(get_users_collection)):
    user = collection.find_one_and_delete({"_id": ObjectId(user_id)})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User doesn't exists"
        )
    
    return {"message": "User deleted successfully."}


@router.post("/register", name="register")
def register(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    collection = Depends(get_users_collection)
):
    exists_username = collection.find_one({"username": username})

    if exists_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    exists_email = collection.find_one({"email": email})

    if exists_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    
    new_user = {
        "username": username,
        "email": email,
        "hash_password": hash_pass(password),
        "create_at": datetime.now(UTC)
    }

    collection.insert_one(new_user)
    return RedirectResponse("/login", status_code=303)


@router.post("/login", name="login")
def login(
    email: str = Form(...),
    password: str = Form(...),
    collection = Depends(get_users_collection)
):
    user = collection.find_one({"email": email})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email"
        )
    
    if not verify_hash_pass(password, user["hash_password"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid password"
        )
    
    token = create_access_token(
        data={"sub": str(user["_id"])},
        expire_delta=timedelta(minutes=settings.access_token_expire_minutes)
    )

    res = RedirectResponse("/", status_code=303)

    res.set_cookie(
        key="access_token",
        value=token,
        httponly=True
    )

    return res


@router.get("/logout", name="logout")
def logout():
    res = RedirectResponse("/login", status_code=303)

    res.delete_cookie(key="access_token")

    return res