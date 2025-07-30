import redis
import os
import logging

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

try:
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, socket_timeout=2)
    redis_client.ping()
    REDIS_AVAILABLE = True
    print("Connected to Redis!")
except Exception:
    redis_client = None
    REDIS_AVAILABLE = False
    print("Redis not available, using in-memory store")
    _session_store = {}

def save_session_chunk(session_id: str, chunk_id: int):
    if REDIS_AVAILABLE:
        redis_client.set(session_id, chunk_id)
    else:
        _session_store[session_id] = chunk_id

def get_session_chunk(session_id: str):
    if REDIS_AVAILABLE:
        v = redis_client.get(session_id)
        if v is None:
            return 0
        return int(v)
    else:
        return _session_store.get(session_id, 0)
