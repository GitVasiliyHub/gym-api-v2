from datetime import datetime
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseRepository
from ..database.postgres.base import SessionProvider
from ..config import db
from ..manager import manager_link as ml
from ..schemas import schema_link as sl



_session_provider = SessionProvider(
    async_mode=True,
    engine_settings={'pool_pre_ping': True},
    db_settings=db
)

class LinkRepository(BaseRepository):
    @classmethod
    @_session_provider
    async def get_links_by_id(
            cls,
            link_ids: List[int],
            session: AsyncSession = None
    ):
        manager = ml.LinkManager
        model = ml.LinkManager.model

        query = select(model).where(model.link_id.in_(link_ids))
        query = query.order_by(model.title)

        return await manager.get_all(statement=query, session=session)

    @classmethod
    @_session_provider
    async def create(
            cls,
            link: sl.CreateLink,
            session: AsyncSession = None
    ) -> sl.Link:
        new_link = await ml.LinkManager.create(
            session=session,
            link=link.link,
            title=link.title,
            master_id=link.master_id,
            create_dttm=datetime.utcnow()
        )
        new_link = sl.Link.model_validate(new_link)

        return new_link