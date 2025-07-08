from fastapi import FastAPI
from app.routes import router
from app.database import engine, Base

# Crée les tables en BDD
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Microservice:API Clients - Paye ton Kawa")

# Inclure les routes clients
app.include_router(router, prefix="/clients", tags=["Clients"])
