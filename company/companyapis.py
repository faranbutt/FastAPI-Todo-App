from fastapi import APIRouter

router =  APIRouter()

@router.get('/')
async def companies_data():
    return {"company name":"Example Comapny, LLC"}

@router.get("/employees")
async def no_of_employees():
    return 416