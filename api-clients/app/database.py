from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base  
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:rkb.0102@postgres:5432/paye_ton_kawa")


DATABASE_URL = os.getenv("DATABASE_URL")

# ✅ Initialisation SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

