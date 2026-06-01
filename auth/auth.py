import jwt
from datetime import datetime, timedelta, UTC
from typing import Optional

from fastapi import Request, HTTPException, status
from pwdlib import PasswordHash

from config import settings

hashed_pass = PasswordHash.recommended()


def hash_pass(password: str) -> str:
    return hashed_pass.hash(password)


def verify_hash_pass(plain_pass: str, hash_password: str) -> bool:
    return hashed_pass.verify(plain_pass, hash_password)


def create_access_token(data: dict, expire_delta: Optional[timedelta] = None) -> str:
    encode_data = data.copy()

    if expire_delta:
        expire = datetime.now(UTC) + expire_delta

    else:
        expire = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)

    encode_data.update({"exp": expire})
    access_token = jwt.encode(
        encode_data,
        key=settings.secret_key.get_secret_value(),
        algorithm=settings.algorithm
    )

    return access_token


def verify_access_token(token: str) -> str | None:
    try:
        data = jwt.decode(
            token,
            key=settings.secret_key.get_secret_value(),
            algorithms=[settings.algorithm],
            options={"require": ["sub", "exp"]}
        )

    except jwt.InvalidTokenError:
        return None

    get_id = data.get("sub")
    
    if not get_id:
        return None
    
    return str(get_id)
    

def get_current_user(request: Request) -> str | None:
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authenticated!"
        )
    
    user_id = verify_access_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    return user_id
