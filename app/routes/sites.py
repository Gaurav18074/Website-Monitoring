from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Site
from pydantic import BaseModel, HttpUrl

router = APIRouter(prefix="/api/sites", tags=["sites"])

class SiteIn(BaseModel):
    name: str
    url: HttpUrl

@router.get("")
def list_sites(db: Session = Depends(get_db)):
    return db.query(Site).all()

@router.post("", status_code=201)
def add_site(payload: SiteIn, db: Session = Depends(get_db)):
    site = Site(name=payload.name, url=str(payload.url))
    db.add(site); db.commit(); db.refresh(site)
    return site

@router.delete("/{site_id}", status_code=204)
def delete_site(site_id: int, db: Session = Depends(get_db)):
    site = db.get(Site, site_id)
    if not site: raise HTTPException(404)
    db.delete(site); db.commit()
