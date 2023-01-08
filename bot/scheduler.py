"""Bot Scheduler."""

from datetime import datetime
from typing import Callable

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.triggers.date import DateTrigger

from pymongo import MongoClient

from config import get_config


config = get_config()

JOBSTORE = {
    'default': MongoDBJobStore(client=MongoClient(config.mongo_db)),
}

scheduler = AsyncIOScheduler(jobstores=JOBSTORE, timezone=config.timezone)


def add_job(
    func: Callable,
    run_date: datetime,
    args=None,
    kwargs=None,
    id=None,
    name=None
):
    """Add a job to the scheduler."""

    scheduler.add_job(
        func, trigger=DateTrigger(run_date=run_date, timezone=config.timezone),
        args=args, kwargs=kwargs, id=id, name=name, replace_existing=True
    )
