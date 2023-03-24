from asgiref.sync import sync_to_async
from fastapi import APIRouter

from accounts import schemas, models


router = APIRouter()


@router.post("/create-employee", response_model=schemas.Employee)
async def create_employee(employee: schemas.EmployeeCreate):
    #TODO: Add check for email validations
    employee_db = await sync_to_async(models.Employee.objects.create_user)(
        name = employee.name,
        email = employee.email,
        password = employee.password
    )

    return employee_db

