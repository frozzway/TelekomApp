from typing import Generator, Any

from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session

from app.settings import settings


url_params = {
    'username': settings.db_username,
    'password': settings.db_password,
    'host': settings.db_host,
    'port': settings.db_port,
}

url_object = URL.create(
    settings.db_dialect,
    database=settings.db_database,
    **url_params
)

engine = create_engine(url_object)
session_maker = sessionmaker(bind=engine)
session_scope = scoped_session(session_maker)


def get_session() -> Generator[scoped_session[Session], Any, None]:
    try:
        yield session_scope
    finally:
        session_scope.remove()
