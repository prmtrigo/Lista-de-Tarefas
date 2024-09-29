from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# BANCO DE DADOS
SQLALCHEMY_DATABASE_URL = "sqlite:///tarefas.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# OBTER NO BANCO DE DADOS
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()