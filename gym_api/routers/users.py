from typing import List
from fastapi import APIRouter, Path, HTTPException, Body, Query
from sqlalchemy.exc import IntegrityError

from ..schemas import user as user_schema
from ..repositories.repo_user import UserRepository


router = APIRouter(prefix='/user')

@router.get(
    '/{master_id}/gymers',
    summary='Getting a list of master gymers',
    response_model=List[user_schema.MastersGymer]
)
async def get_list_of_masters_gymer(
    master_id: int = Path(
        ...,
        description='master id'
    )
):
    return await UserRepository.select_master_gymers(master_id)


@router.get(
    '/{telegram_id}',
    summary='Getting user data by telegram_id',
    response_model=user_schema.User
)
async def get_user_data_by_telegram_id(
    telegram_id: int = Path(
        ...,
        description='telegram id'
    )
):
    user = await UserRepository.select_user_data(telegram_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user


@router.post(
    '',
    summary='Adding user',
    response_model=user_schema.User
)
async def add_user(
    user_data: user_schema.UserIn = Body(
        ...,
        description='Данные пользователя'
    )
):
    try:
        return await UserRepository.add_user(user_data)
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail="User already exists")
    
    
@router.post(
    '/{master_id}/gymer_id',
    summary='Adding gymer for master',
    response_model=List[user_schema.MastersGymer]
)
async def add_gymer_for_master(
    master_id: int = Path(
        ...,
        description='master id'
    ),
    gymer_id: int = Query(
        ...,
        description='gymer id'
    ),
):
    try:
        await UserRepository.add_masters_gymer(
            master_id=master_id,
            gymer_id=gymer_id
        )
    except IntegrityError as e:
        print(e)
        detail_line = 'Gymer already exists'
        error_detail = str(e.orig)
        if 'ForeignKeyViolationError' in error_detail:
            if "DETAIL:" in error_detail:
                detail_line = \
                    [line for line in error_detail.split('\n') if
                     'DETAIL:' in line]
                detail_line = ';'.join(detail_line)
        raise HTTPException(status_code=409, detail=detail_line)
    return await UserRepository.select_master_gymers(master_id)
