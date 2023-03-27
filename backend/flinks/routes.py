from typing import List
from fastapi import APIRouter

from flinks import schemas, models

router = APIRouter()

@router.get('/countries', response_model=List[schemas.Country])
async def get_active_countries():
    """
    Method to get the active countries
    """
    all_countries = models.Country.objects.filter(is_active=True).values("name")
    return list(all_countries)

