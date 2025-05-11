from logging.config import fileConfig

from sqlalchemy import create_engine
from sqlalchemy import pool
from sqlalchemy_utils import database_exists, create_database

from alembic import context

from app.tables import Base
from app.database import url_object


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name, disable_existing_loggers=False)

config.set_main_option('sqlalchemy.url', str(url_object))


target_metadata = Base.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=url_object,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = create_engine(url_object, poolclass=pool.NullPool)

    if not database_exists(url_object):
        create_database(url_object)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
