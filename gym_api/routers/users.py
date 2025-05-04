import json
from typing import Optional

from typing import List
from fastapi import APIRouter, Path

from ..schemas.user import MastersGymer
from ..repositories.gym import GymRepository


router = APIRouter(prefix='/user')

@router.get(
    '/{master_id}/gymers',
    summary='Get master gymers',
    response_model=List[MastersGymer]
)
async def get_list_of_masters_gymer(
    master_id: int = Path(
        ...,
        description='master id'
    )
):
    return await GymRepository.select_master_gymers_data(master_id)
    