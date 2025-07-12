from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import os

# Obter configurações do banco de dados diretamente das variáveis de ambiente
DATABASE = {
    "drivername": "mysql+pymysql",
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "port": os.getenv("MYSQL_PORT", "3306"),
    "user": os.getenv("MYSQL_USER", "user"),
    "password": os.getenv("MYSQL_PASSWORD", "password"),
    "name": os.getenv("MYSQL_DATABASE", "db_name"),
}

# Construir a URL do banco de dados
DATABASE_URL = (
    f"{DATABASE['drivername']}://{DATABASE['user']}:{DATABASE['password']}@"
    f"{DATABASE['host']}:{DATABASE['port']}/{DATABASE['name']}"
)

DELETE_MODE = os.getenv("DELETE_MODE", "soft")

# Criar o motor do SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True, pool_recycle=3600)

# Configurar a sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base para os modelos
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
