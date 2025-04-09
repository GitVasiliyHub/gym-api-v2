from sqlalchemy.ext.asyncio import AsyncSession

from ..config import db
from ..database.postgres.base import SessionProvider

_session_provider = SessionProvider(
    async_mode=True,
    engine_settings={'pool_pre_ping': True},
    db_settings=db
)


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session