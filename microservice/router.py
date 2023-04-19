from fastapi import APIRouter

from services import StatisticsService

router = APIRouter(
    tags=["items"],
    responses={404: {"status": "Page not found"}}
)


@router.get('/statistics')
async def get_statistics():
    return StatisticsService.get_statistics()