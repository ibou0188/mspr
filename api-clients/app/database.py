from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Modifier  PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:rkb.0102@localhost:5432/paye_ton_kawa"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
