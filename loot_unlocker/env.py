import os
import psycopg
import redis

def get_postgres_conn():
    host = os.environ.get("POSTGRES_HOST", "localhost")
    return psycopg.connect(
        f"dbname=loot_unlocker user=postgres host={host}"
    )

def get_redis(db=0, decode_responses=False):
    host = os.environ.get("REDIS_HOST", "localhost")
    return redis.Redis(host, db=db, decode_responses=decode_responses)