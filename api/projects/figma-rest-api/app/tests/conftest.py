"""
pytest配置文件

提供测试fixtures和配置
"""

import pytest
import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from ..core.config import Settings
from ..core.database import Base


@pytest.fixture(scope="session")
def event_loop():
    """创建事件循环"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def test_settings() -> Settings:
    """测试环境配置"""
    return Settings(
        # 使用内存数据库进行测试
        database_url="sqlite+aiosqlite:///:memory:",
        echo_sql=False,
        figma_api_token="test_token_12345",
        figma_api_base_url="https://api.figma.com/v1/",
        figma_timeout=30,
        app_debug=True,
        app_log_level="DEBUG",
        export_dir="./test_exports",
    )


@pytest.fixture
async def test_db(test_settings: Settings) -> AsyncGenerator[AsyncSession, None]:
    """创建测试数据库会话"""
    # 创建内存数据库引擎
    engine = create_async_engine(
        test_settings.database_url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=test_settings.echo_sql,
    )

    # 创建所有表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 创建会话
    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session

    # 清理
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
def sample_figma_file_data() -> dict:
    """示例Figma文件数据"""
    return {
        "name": "Test File",
        "lastModified": "2025-09-30T12:00:00Z",
        "thumbnailUrl": "https://example.com/thumb.png",
        "version": "1.0",
        "document": {
            "id": "0:0",
            "name": "Document",
            "type": "DOCUMENT",
            "children": [
                {
                    "id": "1:0",
                    "name": "Page 1",
                    "type": "PAGE",
                    "children": [
                        {
                            "id": "dish-001",
                            "name": "dish-001",
                            "type": "FRAME",
                            "children": [
                                {
                                    "id": "2:1",
                                    "name": "Image",
                                    "type": "RECTANGLE",
                                }
                            ],
                        },
                        {
                            "id": "dish-002",
                            "name": "dish-002",
                            "type": "FRAME",
                            "children": [],
                        },
                        {
                            "id": "drink-001",
                            "name": "drink-001",
                            "type": "FRAME",
                            "children": [],
                        },
                    ],
                }
            ],
        },
    }


@pytest.fixture
def sample_replacement_rules() -> list:
    """示例替换规则"""
    return [
        {
            "target_node_path": "dish-001",
            "image_url": "https://example.com/images/dish-001.jpg",
        },
        {
            "target_node_path": "dish-002",
            "image_url": "https://example.com/images/dish-002.jpg",
        },
    ]


@pytest.fixture
def sample_export_config() -> dict:
    """示例导出配置"""
    return {
        "format": "png",
        "scale": 1.0,
        "save_to_cloud": False,
        "cloud_dir": None,
    }


# Pytest标记配置
def pytest_configure(config):
    """配置pytest标记"""
    config.addinivalue_line("markers", "asyncio: mark test as async")
    config.addinivalue_line("markers", "unit: mark test as unit test")
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "slow: mark test as slow running")