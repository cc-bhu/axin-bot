"""Internal API for the bot."""

from datetime import datetime

from pymongo import MongoClient

from config import get_config
from internal.models import Question


config = get_config()
client = MongoClient(config.mongo_db)


async def get_question(level=None, success=0) -> Question:
    """Get a random question from the database."""

    col = client[config.db_name][config.questions_collection]

    query = {
        "date": None,
        "success": { "$gte": success },
    }
    if level:
        query["level"] = level

    # get random question where date is not set
    question = col.aggregate([
        {"$match": query},
        {"$sample": {"size": 1}}
    ]).next()

    # add date to the question.
    col.find_one_and_update({"_id": question["_id"]}, {"$set": {"date": datetime.now()}})

    return Question(**question)
