from contextlib import asynccontextmanager

import redis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_config, DevelopmentConfig
from app.core.database import ASYNC_ENGINE
from app.core.redis import redis_client
from app.core.settings import ORIGINS
from app.views import root, swagger

config = get_config()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing database......")
    # FastAPI 인스턴스 기동시 필요한 작업 수행.
    try:
        await redis_client.ping() # Redis 연결 테스트
        print("Redis connection established......")
    except redis.exceptions.ConnectionError:
        print("Failed to connect to Redis......")
    print("Starting up...")
    yield
    # FastAPI 인스턴스 종료시 필요한 작업 수행
    await redis_client.aclose()
    print("Redis connection closed......")
    print("Shutting down...")
    await ASYNC_ENGINE.dispose()


def including_router(app):
    app.include_router(swagger.router, prefix="/swagger")
    app.include_router(root.router, prefix="", tags=["Root"]) # root 페이지는 / 슬래시를 없애라.


def including_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def initialize_app():
    app = FastAPI(title=config.APP_NAME,
                  version=config.APP_VERSION,
                  description=config.APP_DESCRIPTION,
                  lifespan=lifespan,
                  # docs_url=None, redoc_url=None 을 주면 기본 /docs, /redoc 페이지가 비활성화됩니다.
                  docs_url=None , redoc_url=None) # docs_url을 지정하는 커스텀 마이징할 때 (CSRF_TOKEN적용시)
                  # docs_url = None, redoc_url = "/swagger/redoc")
    '''# 주소만 커스터마이징할 때 redoc_url = "/swagger/redoc" 이렇게 하면된다. 
        주소 뿐만 아니라 html 문서자체를 커스텀 마이징하는 경우는 views/swagger.py 의 함수를 사용하면 된다.
    '''

    including_router(app)
    including_middleware(app)

    if config == DevelopmentConfig():
        print("DEV create_app dev: ", config.APP_NAME)
        print("DEV config.DEBUG: ", config.DEBUG)
    else:
        print("PROD create_app prod: ", config.APP_NAME)
        print("PROD config.DEBUG: ", config.DEBUG)
    return app