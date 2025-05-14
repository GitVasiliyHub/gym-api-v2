import json
from typing import Optional

from typing import List
from fastapi import APIRouter, Path, HTTPException, Body, Query


from ..schemas.user import MastersGymer, User, UserIn
from ..repositories.gym import GymRepository


router = APIRouter(prefix='/user')

@router.get(
    '/{master_id}/gymers',
    summary='Getting a list of master gymers',
    response_model=List[MastersGymer]
)
async def get_list_of_masters_gymer(
    master_id: int = Path(
        ...,
        description='master id'
    )
):
    return await GymRepository.select_master_gymers_data(master_id)


@router.get(
    '/{telegram_id}',
    summary='Getting user data by telegram_id',
    response_model=User
)
async def get_list_of_masters_gymer(
    telegram_id: int = Path(
        ...,
        description='user id'
    )
):
    user = await GymRepository.select_user_data(telegram_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user


@router.post(
    '',
    summary='Adding user',
    response_model=User
)
async def add_user(
    user_data: UserIn = Body(
        ...,
        description='Данные пользователя'
    )
):
    user_exist = await GymRepository.select_user_data(user_data.telegram_id)
    if user_exist:
        raise HTTPException(status_code=409, detail="User already exists")
    
    return await GymRepository.add_user(user_data)
    
    
@router.post(
    '/{master_id}/gymer_id',
    summary='Adding gymer for master',
    response_model=List[MastersGymer]
)
async def add_gymer_for_master(
    master_id: int = Path(
        ...,
        description='master id'
    ),
    gymer_id: int = Query(
        ...,
        description='user id'
    ),
):
    users = await GymRepository.select_master_gymers_data(master_id)
    if users:
        for u in users:
            if gymer_id == u.gymer_id:
                raise HTTPException(
                    status_code=409,
                    detail="User already exists"
                )
    
    await GymRepository.add_user_for_master(
        master_id=master_id,
        gymer_id=gymer_id
    )
    await GymRepository.select_master_gymers_data(master_id)
