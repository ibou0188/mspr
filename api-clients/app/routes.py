from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import ClientOut, ClientCreate
from crud import create_client, get_clients
from database import SessionLocal
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request



router = APIRouter()

# Dépendance pour ouvrir/fermer la session BDD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ClientOut)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    return create_client(db, client)

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
    client = update_client(db, client_id, client_data)
    if not client:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    return client

@router.delete("/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = delete_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client non trouvé")
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
