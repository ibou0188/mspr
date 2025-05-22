from fastapi import FastAPI
from app import routes
from app.database import engine, Base

# Crée les tables en BDD
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Clients - Paye ton Kawa")

# Inclure les routes clients
app.include_router(routes.router, prefix="/clients", tags=["Clients"])
