import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# 1. Ajusta caminho e importa módulos da app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
load_dotenv()

# 2. Configuração Alembic
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 3. Sobrescreve sqlalchemy.url com o valor do .env
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    config.set_main_option("sqlalchemy.url", DATABASE_URL)

# 4. Importa os modelos e metadata
from src.database.core import Base
from src.entities.user import User
from src.entities.todo import Todo

target_metadata = Base.metadata

# 5. Funções padrão de execução de migrations
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
