"""
数据库配置和连接管理
"""

import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from .config import get_settings
from .models.figma import Base


logger = logging.getLogger(__name__)


class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self):
        self.engine = None
        self.session_factory = None
        self._initialized = False

    async def initialize(self):
        """初始化数据库连接"""
        if self._initialized:
            return
            
        settings = get_settings()
        
        # 创建异步引擎
        self.engine = create_async_engine(
            settings.database_url,
            echo=settings.echo_sql,
            poolclass=StaticPool if "sqlite" in settings.database_url else None,
            connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {}
        )
        
        # 创建会话工厂
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        
        # 创建表
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        self._initialized = True
        logger.info("Database initialized successfully")

    async def close(self):
        """关闭数据库连接"""
        if self.engine:
            await self.engine.dispose()
            self._initialized = False
            logger.info("Database connection closed")

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """获取数据库会话"""
        if not self._initialized:
            await self.initialize()
            
        async with self.session_factory() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()


# 全局数据库管理器实例
db_manager = DatabaseManager()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """获取数据库会话的依赖函数"""
    async for session in db_manager.get_session():
        yield session


async def init_database():
    """初始化数据库"""
    await db_manager.initialize()


async def close_database():
    """关闭数据库连接"""
    await db_manager.close()
