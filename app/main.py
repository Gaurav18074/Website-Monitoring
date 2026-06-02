from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db
from app.models import Site
from app.routes import sites, logs

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Website Monitor")
app.include_router(sites.router)
app.include_router(logs.router)
templates = Jinja2Templates(directory="app/templates")

@app.get("/health")
def health(): return {"ok": True}

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("dashboard.html",
        {"request": request, "sites": db.query(Site).all()})
