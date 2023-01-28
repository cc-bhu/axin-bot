"""Dailyquest API."""

from datetime import datetime, timedelta
from string import Template
from typing import Optional

from pymongo import MongoClient

from bot.api import send_message
from bot.config import get_config
from bot.internal.models import Question
from bot.templates.message import DAILYQUEST_TEMPALTE, DAILYQUEST_HINT_TEMPALTE
from bot.scheduler import add_job


config = get_config()
client = MongoClient(config.mongo_db)


async def get_question(
    level: Optional[str] = None,
    success: int = 0,
    set_date: bool = True,
) -> Question:
    """Get a random question from the database."""

    col = client[config.db_name][config.questions_collection]

    query = {
        "date": None,
        "success": { "$gte": success },
    }
    if level:
        query["level"] = level

    # get random question where date is not set.
    question = col.aggregate([
        {"$match": query},
        {"$sample": {"size": 1}}
    ]).next()

    # set date of the question.
    if set_date:
        col.find_one_and_update(
            {"_id": question["_id"]}, {"$set": {"date": datetime.now()}}
        )

    return Question(**question)


async def send_dailyquest(_id: int):
    """Send Daily Quest Message."""

    # Get Question
    question = await get_question(level="easy", success=65)

    # Generate Message
    message = Template(DAILYQUEST_TEMPALTE).substitute(
        title=question.title,
        description=question.description,
        slug=question.slug,
    )

    # Send Message
    message = await send_message(_id, message, thread_name=question.title)
    thread_id = message["thread"]["id"]
    await send_message(thread_id, "Discussion Thread")

    # Send Question Hint
    if question.hint:
        delta = timedelta(hours=20)
        hint = Template(DAILYQUEST_HINT_TEMPALTE).substitute(
            hint=question.hint)

        add_job(
            send_message,
            datetime.now(tz=config.timezone) + delta,
            args=[thread_id, hint]
        )
