from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import ClientOut, ClientCreate
from crud import create_client, get_clients
from database import SessionLocal
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
from schemas import UserCreate, Token
from models import User
from fastapi.security import OAuth2PasswordRequestForm
import auth  # fichier auth.py

from app.event_bus import publish_event
from fastapi.encoders import jsonable_encoder
from crud import create_client as db_create_client, update_client as db_update_client, get_clients, delete_client as db_delete_client


router = APIRouter()

# Dépendance pour ouvrir/fermer la session BDD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ClientOut, dependencies=[Depends(auth.get_current_user)])
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    new_client = db_create_client(db, client)
    publish_event("clients.created", jsonable_encoder(new_client))
    return new_client

@router.get("/", response_model=list[ClientOut])
def read_clients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_clients(db, skip=skip, limit=limit)

@router.get("/", response_model=list[ClientOut])
def read_clients(
    skip: int = 0,
    limit: int = 10,
    search: str = None,
    db: Session = Depends(get_db)
):
    return get_clients(db, skip=skip, limit=limit, search=search)


@router.put("/{client_id}", response_model=ClientOut)
def update_client(client_id: int, client_data: ClientCreate, db: Session = Depends(get_db)):
    updated_client = db_update_client(db, client_id, client_data)
    if not updated_client:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    publish_event("clients.updated", jsonable_encoder(updated_client))
    return updated_client


@router.delete("/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = db_delete_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    publish_event("clients.deleted", {"id": client_id})
    return {"message": "Client supprimé avec succès"}


templates = Jinja2Templates(directory="app/templates")

@router.get("/view", response_class=HTMLResponse)
def view_clients(request: Request, db: Session = Depends(get_db), page: int = 1, search: str = ""):
    limit = 5
    skip = (page - 1) * limit
    clients = get_clients(db, skip=skip, limit=limit, search=search)
    has_next = len(clients) == limit  # le probablement une suite

    return templates.TemplateResponse("clients.html", {
        "request": request,
        "clients": clients,
        "page": page,
        "search": search,
        "has_next": has_next
    })
    
@router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Nom d'utilisateur déjà pris")
    hashed_password = auth.get_password_hash(user.password)
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    token = auth.create_access_token({"sub": new_user.username})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Identifiants incorrects")
    token = auth.create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
