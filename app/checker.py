import time, httpx, logging
from datetime import datetime
from app.database import SessionLocal
from app.models import Site, CheckLog
from app.alerts import dispatch_alert

log = logging.getLogger("checker")

async def check_site(site: Site) -> CheckLog:
    start = time.perf_counter()
    status, error, is_up = None, None, False
    try:
        async with httpx.AsyncClient(timeout=10, follow_redirects=True) as c:
            r = await c.get(site.url)
            status = r.status_code
            is_up = 200 <= status < 400
    except Exception as e:
        error = str(e)[:300]
    elapsed = (time.perf_counter() - start) * 1000
    return CheckLog(
        site_id=site.id, status_code=status, response_time_ms=elapsed,
        is_up=is_up, error=error, checked_at=datetime.utcnow(),
    )

async def run_checks():
    db = SessionLocal()
    try:
        sites = db.query(Site).filter(Site.is_active == True).all()
        for site in sites:
            entry = await check_site(site)
            db.add(entry); db.commit()
            # alert on transition to DOWN
            prev = (db.query(CheckLog)
                      .filter(CheckLog.site_id == site.id, CheckLog.id != entry.id)
                      .order_by(CheckLog.id.desc()).first())
            if not entry.is_up and (prev is None or prev.is_up):
                await dispatch_alert(site, entry, status="DOWN")
            elif entry.is_up and prev and not prev.is_up:
                await dispatch_alert(site, entry, status="RECOVERED")
    finally:
        db.close()
