from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Это позволит использовать настройки из alembic.ini
config = context.config

# Здесь вы можете передать конфигурацию из alembic.ini в Alembic
def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url)

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=None
        )

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
