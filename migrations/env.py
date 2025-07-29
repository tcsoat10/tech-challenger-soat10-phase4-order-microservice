from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv
import os
load_dotenv()
from config.database import DATABASE
from src.adapters.driven.repositories.models.base_model import BaseModel

SQLALCHEMY_URL_KEY = "sqlalchemy.url"

# Carrega a configuração do Alembic
config = context.config
fileConfig(config.config_file_name)

# Geração da URL do banco de dados

# config.set_main_option(SQLALCHEMY_URL_KEY, database_url)

# Metadados das tabelas (BaseModel como base para todas as entidades)
target_metadata = BaseModel.metadata

def set_database_url(config):
    database_url = config.get_main_option(SQLALCHEMY_URL_KEY)

    if database_url and 'driver://' in database_url:
        database_url = (
            f"{DATABASE['drivername']}://{DATABASE['user']}:{DATABASE['password']}@"
            f"{DATABASE['host']}:{DATABASE['port']}/{DATABASE['name']}"
        )

    config.set_main_option(SQLALCHEMY_URL_KEY, database_url)


# Modo offline: Gera SQL sem conexão ao banco
def run_migrations_offline():
    url = config.get_main_option(SQLALCHEMY_URL_KEY)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True,
    )
    with context.begin_transaction():
        context.run_migrations()

# Modo online: Executa as migrações com conexão ativa ao banco
def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


set_database_url(config)

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
