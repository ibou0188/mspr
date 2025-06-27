from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    firstName = Column(String)
    lastName = Column(String)
    name = Column(String)
    createdAt = Column(String)
    # Adresse
    postalCode = Column(String)
    city = Column(String)
    # Profil
    profileFirstName = Column(String)
    profileLastName = Column(String)
    # Société
    companyName = Column(String)
    email = Column(String, unique=True, index=True)  # on garde aussi ce champ

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
