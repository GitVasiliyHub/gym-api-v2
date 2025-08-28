from typing import List
from fastapi import APIRouter, Query, Body

from ..repositories.repo_link import LinkRepository
from ..schemas import schema_link as sl


router = APIRouter(prefix='/link')

@router.get(
    "",
    summary='Getting a list of links by id',
    response_model=List[sl.Link]
)
async def get_links_by_id(
        link_ids: List[int] = Query(
            ...,
            default='List link_ids'
        )
):
    return await LinkRepository.get_links_by_id(link_ids=link_ids)

@router.post(
    "",
    summary='Create Link',
    response_model=sl.Link
)
async def create_link(
        link: sl.CreateLink = Body(
            ...,
            default='Link description'
        )
):
    return await LinkRepository.create(link=link)
