from sqlalchemy.orm import Session
from app.models import Client
from app.schemas import ClientCreate

def create_client(db: Session, client: ClientCreate):
    db_client = Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def get_clients(db: Session, skip: int = 0, limit: int = 10, search: str = None):
    query = db.query(Client)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            Client.nom.ilike(search_term) |
            Client.email.ilike(search_term)
        )
    return query.offset(skip).limit(limit).all()

def get_client(db: Session, client_id: int):
    return db.query(Client).filter(Client.id == client_id).first()

def update_client(db: Session, client_id: int, new_data: ClientCreate):
    client = db.query(Client).filter(Client.id == client_id).first()
    if client:
        client.nom = new_data.nom
        client.email = new_data.email
        db.commit()
        db.refresh(client)
    return client

def delete_client(db: Session, client_id: int):
    client = db.query(Client).filter(Client.id == client_id).first()
    if client:
        db.delete(client)
        db.commit()
    return client
