import os
from functools import cache
import redis
from sqlmodel import create_engine

@cache
def get_sql_engine(tid: int):
    assert tid > 0
    host = os.environ.get("POSTGRES_HOST", "localhost")
    engine = create_engine(f"postgresql+psycopg://postgres@{host}/loot_unlocker")
    return engine

def get_redis(db=0, decode_responses=False):
    host = os.environ.get("REDIS_HOST", "localhost")
    return redis.Redis(host, db=db, decode_responses=decode_responses)