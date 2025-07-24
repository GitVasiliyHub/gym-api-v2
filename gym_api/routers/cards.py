from typing import Optional

from typing import List
from fastapi import APIRouter, Path, Query, HTTPException, Body

from ..repositories.repo_card import CardRepository




router = APIRouter(prefix='/card')


@router.get(
    "/{master_id}/card",
    summary='Getting a list of exercise by master_id',
    response_model=
)
async def get_list_of_exercise(
    master_id: int,
    search: Optional[str] = Query(
        None,
        description="Поиск по названию упражнения"
    )
):