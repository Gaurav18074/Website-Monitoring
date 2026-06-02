import asyncio, logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.checker import run_checks
from app.config import settings
from app.database import Base, engine

logging.basicConfig(level=logging.INFO)

async def main():
    Base.metadata.create_all(bind=engine)
    sched = AsyncIOScheduler()
    sched.add_job(run_checks, "interval", seconds=settings.check_interval_seconds, max_instances=1)
    sched.start()
    logging.info("Scheduler started, interval=%ss", settings.check_interval_seconds)
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
