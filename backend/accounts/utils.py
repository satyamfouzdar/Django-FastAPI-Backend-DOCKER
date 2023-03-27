from asgiref.sync import sync_to_async
from datetime import timedelta, datetime
from typing import Annotated

from jose import JWTError, jwt
from passlib.hash import django_pbkdf2_sha256

from django.conf import settings

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from accounts.models import Employee
from accounts.schemas import TokenData


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/accounts/token")


def verify_password(password, hash_password):
    """
    Method to verify if the user password is correct.
    """
    if django_pbkdf2_sha256.verify(password, hash_password):
        return True
    else:
        return False


def get_user(email:str):
    """
    Method to get a user by email
    """

    user = Employee.objects.filter(email=email)

    if user.exists():
        return user.first()
    return False



def authenticate_user(email:str, password:str, employee:bool=True):
    if employee:
        usr_query = Employee.objects.filter(email=email)

        if usr_query.exists():
            usr = usr_query.first()
        else:
            return False

        if not verify_password(password, usr.password):
            return False

        return usr


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Method to create access token based on the data and the expires_delta
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Method to get current user
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

