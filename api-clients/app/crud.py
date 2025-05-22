from sqlalchemy.orm import Session
from . import models, schemas

def create_client(db: Session, client: schemas.ClientCreate):
    db_client = models.Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def get_clients(db: Session, skip: int = 0, limit: int = 10, search: str = None):
    query = db.query(models.Client)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            models.Client.nom.ilike(search_term) |
            models.Client.email.ilike(search_term)
        )
    return query.offset(skip).limit(limit).all()

def get_client(db: Session, client_id: int):
    return db.query(models.Client).filter(models.Client.id == client_id).first()

def update_client(db: Session, client_id: int, new_data: schemas.ClientCreate):
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if client:
        client.nom = new_data.nom
        client.email = new_data.email
        db.commit()
        db.refresh(client)
    return client

def delete_client(db: Session, client_id: int):
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if client:
        db.delete(client)
        db.commit()
    return client
