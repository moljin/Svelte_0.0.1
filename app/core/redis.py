import os

from dotenv import load_dotenv
from redis.asyncio import Redis, ConnectionPool

from app.core.config import get_config

# # Connection Pool 기반 access ##############################
""" # AI Chat # 비동기적으로 ConnectionPool 적용
비동기 Redis 클라이언트와 함께 쓰려면 동기용 ConnectionPool이 아니라 asyncio 전용 풀을 써야 합니다. 
즉, redis.ConnectionPool이 아니라 redis.asyncio.ConnectionPool을 사용해야 합니다.
from redis.asyncio import Redis, ConnectionPool
예시 1) asyncio용 ConnectionPool을 직접 생성해서 사용
"""

load_dotenv()
config = get_config()

host = os.environ.get("REDIS_HOST") if config.APP_ENV == "production" else "localhost"
port = os.environ.get("REDIS_PORT") if config.APP_ENV == "production" else 6379
password = os.environ.get("REDIS_PASSWORD") if config.APP_ENV == "production" else None

redis_pool = ConnectionPool(
    host=host,
    port=port,
    db=os.environ.get("REDIS_DB"),
    password=password,
    decode_responses=True,  # 문자열 응답을 자동으로 디코딩
    max_connections=10)

redis_client = Redis(connection_pool=redis_pool)
