from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from core.db import get_db
from models.event import Event
from schemas.event import EventCreate, EventUpdate, EventOut

router = APIRouter(prefix="/events", tags=["events"])

# Listar events com paginação e busca
@router.get("/", response_model=dict)
def list_events(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100), q: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Event)
    if q:
        like = f"%{q}%"
        query = query.filter(Event.title.ilike(like) | Event.description.ilike(like))
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    total = query.count()
    return {"data": items, "meta": {"page": page, "page_size": page_size, "total": total}}

# Criar novo event
@router.post("/", response_model=EventOut, status_code=201)
def create_event(payload: EventCreate, db: Session = Depends(get_db)):
    obj = Event(**payload.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

# Obter um event específico
@router.get("/{event_id}", response_model=EventOut)
def get_event(event_id: int, db: Session = Depends(get_db)):
    obj = db.query(Event).get(event_id)
    if not obj:
        raise HTTPException(404, "Not found")
    return obj

# Atualizar event
@router.patch("/{event_id}", response_model=EventOut)
def update_event(event_id: int, payload: EventUpdate, db: Session = Depends(get_db)):
    obj = db.query(Event).get(event_id)
    if not obj:
        raise HTTPException(404, "Not found")
    for k, v in payload.dict(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

# Deletar event
@router.delete("/{event_id}", status_code=204)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    obj = db.query(Event).get(event_id)
    if not obj:
        raise HTTPException(404, "Not found")
    db.delete(obj)
    db.commit()
