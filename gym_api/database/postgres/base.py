from typing import Optional, Callable

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

from ...config import Database
from ...utils.utils import find_session


async def async_commiter(session: AsyncSession):
    try:
        await session.commit()
    except Exception:
        await session.rollback()
        raise


def get_db_url(db: Database):
    return URL.create(
        drivername=db.drivername,
        username=db.login,
        password=db.password.get_secret_value() if db.password else None,
        host=db.host,
        port=db.port,
        database=db.database
    ) # noqa


def get_engine(
        db_settings: Database,
        async_mode: bool = False,
        pool_pre_ping: bool = False,
        echo: bool = False
):
    if async_mode:
        return create_async_engine(
            get_db_url(db_settings),
            pool_pre_ping=pool_pre_ping,
            future=True,
            echo=echo
        )
    return create_engine(
        get_db_url(db_settings),
        pool_pre_ping=pool_pre_ping,
        echo=echo
    )


class Session:
    """
    The class is used to get the session

    Attributes
    ----------
    autocommit : bool
        sqlalchemy session autocommit flag
    autoflush : bool
        sqlalchemy session autoflush flag
    async_mode : bool
        defines asynchronous or synchronous engines and session
    """

    def __init__(
            self,
            *,
            db_settings: Database,
            autocommit: bool = False,
            autoflush: bool = False,
            async_mode: bool = False,
            engine_settings: Optional[dict] = None
    ):
        if not engine_settings:
            engine_settings = {}

        self.__engine = get_engine(
            async_mode=async_mode,
            db_settings=db_settings,
            **engine_settings
        )

        self.autocommit = autocommit
        self.autoflush = autoflush
        self.async_mode = async_mode

    @property
    def session(self):
        if self.async_mode:
            return sessionmaker(
                autocommit=self.autocommit,
                autoflush=self.autoflush,
                bind=self.__engine,
                class_=AsyncSession
            )

        return sessionmaker(
            autocommit=self.autocommit,
            autoflush=self.autoflush,
            bind=self.__engine
        )


class SessionProvider(Session):
    """
    Session provider wrapper hold session in wrapped function
    """

    def __call__(self, func: Callable):
        find_session(func)

        _session = self.session

        async def async_wrapper(*args, **kwargs):
            in_ses = kwargs.get('session')
            if in_ses and isinstance(in_ses, AsyncSession):
                return await func(*args, **kwargs)
            async with _session() as ses:
                return await func(*args, **kwargs, session=ses)

        def wrapper(*args, **kwargs):
            in_ses = kwargs.get('session')
            if in_ses and isinstance(in_ses, Session):
                return func(*args, **kwargs)
            with _session() as ses:
                return func(*args, **kwargs, session=ses)

        if self.async_mode:
            return async_wrapper

        return wrapper