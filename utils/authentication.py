from core import hash, verifyHash,\
      JWT_SECRET_KEY, JWT_REFRESH_SECRET_KEY, ALGORITHM, \
      ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES, oauth2_scheme, ResponseException
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt

from typing import Union
from fastapi import Depends, Security
from schemas import UserDataToken

def verify_password(plain_password: str, hashed_password:str):
    return verifyHash(plain_password, hashed_password)


def get_password_hash(password):
    return hash(password)


# Hàm để giải mã token và trả về thông tin từ payload
def decode_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise ResponseException(status_code=401, detail=f"Invalid token {e}")

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_token_info(token:str  = Security(oauth2_scheme)):
    try:
        payload = decode_token(token)
        return UserDataToken(**payload)
    except JWTError as e:
        raise ResponseException(status_code=401, detail=f"Invalid token {e}")
