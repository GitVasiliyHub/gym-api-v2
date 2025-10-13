from datetime import datetime

from fastapi import HTTPException
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from .base import BaseRepository
from ..database.postgres.base import SessionProvider
from ..config import db
from ..schemas import user as user_schema
from ..manager import manager_user as mu



_session_provider = SessionProvider(
    async_mode=True,
    engine_settings={'pool_pre_ping': True},
    db_settings=db
)

class UserRepository(BaseRepository):
    @classmethod
    @_session_provider
    async def add_masters_gymer(
        cls,
        master_id: int,
        gymer_id: int,
        session: AsyncSession=None
    ):
        await mu.MasterGymManager.create(
            session=session,
            master_id=master_id,
            gymer_id=gymer_id,
            create_dttm=datetime.now()
        )
    
    @classmethod
    @_session_provider
    async def add_user(
        cls,
        user_data: user_schema.UserIn,
        session: AsyncSession=None
    ):
        try:
            user = mu.UserManager.model(**user_data.model_dump())
            session.add(user)
            await session.flush()
            u = user_schema.UserBase.model_validate(user)

            master = mu.MasterManager.model(user_id=u.user_id,
                                        create_dttm=datetime.now())
            gymer = mu.GymerManager.model(user_id=u.user_id,
                                     create_dttm=datetime.now())

            session.add(master)
            session.add(gymer)

            await session.flush()

            m = user_schema.Master.model_validate(master)
            g = user_schema.Gymer.model_validate(gymer)

            await cls.add_masters_gymer(
                master_id=m.master_id,
                gymer_id=g.gymer_id,
                session=session
            )
        except IntegrityError as e:
            await session.rollback()
            print(e)
            detail_line = 'duplicate key value'
            error_detail = str(e.orig)
            if 'UniqueViolationError' in error_detail:
                if "DETAIL:" in error_detail:
                    detail_line = \
                    [line for line in error_detail.split('\n') if
                     'DETAIL:' in line]
                    detail_line = ';'.join(detail_line)

            raise HTTPException(status_code=409, detail=detail_line)
        except Exception:
            await session.rollback()
            raise HTTPException(status_code=500, detail="Internal server error")
        
        return await cls.select_user_data(
            telegram_id=u.telegram_id,
            session=session
        )

    @classmethod
    @_session_provider
    async def select_user_data(
        cls,
        telegram_id: int,
        session: AsyncSession=None
    ) -> Optional[user_schema.User]:
        user_stmt = (
            select(mu.UserManager.model)
            .where(mu.UserManager.model.telegram_id == telegram_id)
        )
        user = await session.execute(user_stmt)
        user = user.scalars().first()

        if not user:
            return None

        master_stmt = (
            select(mu.MasterManager.model)
            .where(mu.MasterManager.model.user_id == user.user_id)
        )
        master = await session.execute(master_stmt)
        master = master.scalars().first()
        
        gymer_stmt = (
            select(mu.GymerManager.model)
            .where(mu.GymerManager.model.user_id == user.user_id)
        )
        gymer = await session.execute(gymer_stmt)
        gymer = gymer.scalars().first() 

        return user_schema.User(
                user_id=user.user_id,
                username=user.username,
                phone=user.phone,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                telegram_id=user.telegram_id,
                photo=user.photo,
                master=master,
                gymer=gymer
        )

    @classmethod
    @_session_provider
    async def select_master_gymers(
        cls,
        master_id: int,
        session: AsyncSession=None
    ) -> List[user_schema.MastersGymer]:

        mg = mu.MasterGymManager.model
        g = mu.GymerManager.model
        u = mu.UserManager.model
   
        sub = select(mg.gymer_id).where(
            mg.master_id == master_id,
            mg.close_dttm.is_(None)
            )
        
        statement = select(
            u.username,
            u.first_name,
            u.last_name,
            u.photo,
            g.gymer_id
        ).join(
            g, g.user_id == u.user_id
        ).where(g.gymer_id.in_(sub))
        
        rows = await session.execute(statement)
       
        result = []
        for row in rows:
            result.append(user_schema.MastersGymer.model_validate(row))
       
        return result
