from asgiref.sync import sync_to_async
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from django.conf import settings

from accounts import schemas, models, utils


router = APIRouter()


@router.post("/create-employee", response_model=schemas.Employee)
async def create_employee(employee: schemas.EmployeeCreate):
    #TODO: Add check for email validations
    employee_db = models.Employee(
        name = employee.name,
        email = employee.email,
    )

    employee_db.set_password(employee.password)
    employee_db.save()

    return employee_db


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """
    Route to login an employee and return Token
    """
    user = utils.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = utils.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/forgot-password")
async def forgot_password(email: str) -> bool:
    """
    Route to forget the password
    """
    # TODO: Check if the user with this email exists in db
    # TODO: Send an email with the password reset link using celery
    # TODO: Return Succes True or False
    pass


@router.get("/me/", response_model=schemas.Profile)
async def read_profile(
    current_user: Annotated[schemas.Employee, Depends(utils.get_current_user)]
):
    """
    Route to get the profile of the user
    """
    profile = models.Profile.objects.get(user=current_user)
    return profile


#TODO: Add route to update user profile details.
#TODO: Add route to update profile picture.

@router.post('/logout')
async def logout(current_user: schemas.Employee = Depends(utils.get_current_user)):
    """
    Route to logout employee
    """
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authenticated')
    response = JSONResponse(content={"messsage": "Logged Out sucessfully."})
    response.delete_cookie('access_token')
    return response
