from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get('/')
async def healthy():
    return JSONResponse({'status':'healthy'})