from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

from app.core.config import get_config

config = get_config()
DATABASE_URL = f"{config.DB_TYPE}+{config.DB_DRIVER}://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}?charset=utf8"
ASYNC_ENGINE = create_async_engine(DATABASE_URL,
                                   echo=config.DEBUG,
                                   future=True,
                                   pool_size=10, max_overflow=0, pool_recycle=300,  # 5분마다 연결 재활용
                                   # encoding="utf-8"
                                   )

# 세션 로컬 클래스 생성
AsyncSessionLocal = async_sessionmaker(
    ASYNC_ENGINE,
    class_=AsyncSession,  # add
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
    # poolclass=NullPool,  # SQLite에서는 NullPool 권장
)
"""
 autocommit=False 부분은 주의하자. 
 autocommit=False로 설정하면 데이터를 변경했을때 commit 이라는 사인을 주어야만 실제 저장이 된다. 

 만약 autocommit=True로 설정할 경우에는 commit이라는 사인이 없어도 즉시 데이터베이스에 변경사항이 적용된다. 

 그리고 autocommit=False인 경우에는 데이터를 잘못 저장했을 경우 rollback 사인으로 되돌리는 것이 가능하지만 
 autocommit=True인 경우에는 commit이 필요없는 것처럼 rollback도 동작하지 않는다는 점에 주의해야 한다.
"""

Base = declarative_base()  # Base 클래스 (모든 모델이 상속)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    session: AsyncSession = AsyncSessionLocal()
    print(f"[get_session] new session: {id(session)}")
    try:
        yield session
    except Exception as e:
        print(f"Session rollback triggered due to exception: {e}")
        await session.rollback()
        raise
    finally:
        print(f"[get_session] close session: {id(session)}")
        await session.close()