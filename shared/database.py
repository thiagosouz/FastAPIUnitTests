from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@localhost/db_fast_api_to_deploy"

# Configuração do engine para conexão com o banco de dados
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

# Configuração da sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos declarativos
Base = declarative_base()
