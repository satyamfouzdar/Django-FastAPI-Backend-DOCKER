import requests
import json

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


# TODO: Route to View all financial institutions from flinks api
@router.get('/institutions', response_model=List[schemas.Institution])
async def get_all_institutions():
    """
    Method to get all institutions from flinks api.
    """
    mode = "sandbox"
    customerId = "3780d239-9630-4897-8d7c-142cae653000"

    url = f"https://{mode}-api.private.fin.ag/v3/{customerId}/BankingServices/Institutions?skip=0&take=249&countries=CA"

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)
    data = json.loads(response.text)

    institutions = []

    for institution in data['Data']:
        institution_dict = {}
        institution_dict['name'] = institution['Localizations'][0]['Name']
        institutions.append(institution_dict)

    return institutions
# TODO: Route to post login credentials for specific financial institution and get the request_id for user
# TODO: Route to Get all accounts for that user using the request id