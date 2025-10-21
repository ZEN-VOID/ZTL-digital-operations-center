"""
Figma REST API主应用
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from .core.config import get_settings
from .core.database import init_database, close_database
from .api.v1.endpoints import figma_router, figma_api_router
from .api.v1.endpoints.batch_replace import router as batch_replace_router
from .api.v1.endpoints.batch import router as batch_router
from .api.v1.endpoints.production_workflow import router as production_router
from .api.v1.endpoints.figma_complete import router as figma_complete_router
from .api.v1.endpoints.url_parser import router as url_parser_router


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时初始化
    logger.info("Starting Figma REST API application...")
    
    try:
        # 初始化数据库
        await init_database()
        logger.info("Database initialized")
        
        yield
        
    finally:
        # 关闭时清理
        logger.info("Shutting down Figma REST API application...")
        await close_database()
        logger.info("Database connection closed")


def create_app() -> FastAPI:
    """创建FastAPI应用实例"""
    settings = get_settings()
    
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="ZTL餐饮数智化平面设计工作台 - Figma REST API集成服务",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan
    )
    
    # 配置CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 生产环境中应该限制具体域名
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 注册路由
    app.include_router(figma_router, prefix="/api/v1")  # 内部任务管理API
    app.include_router(figma_api_router, prefix="/api")  # 官方Figma API兼容端点
    app.include_router(batch_replace_router, prefix="/api/v1")  # 批量替换功能
    app.include_router(batch_router, prefix="/api/v1")  # 增强版批量处理
    app.include_router(production_router, prefix="/api/v1")  # 量产工作流功能
    app.include_router(figma_complete_router, prefix="/api/v1")  # 完整Figma API功能
    app.include_router(url_parser_router, prefix="/api/v1")  # URL解析功能
    
    # 全局异常处理
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Global exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )
    
    # 健康检查端点
    @app.get("/health", tags=["health"])
    async def health_check():
        """应用健康检查"""
        return {
            "status": "healthy",
            "service": "figma-rest-api",
            "version": settings.app_version
        }
    
    # 根路径
    @app.get("/", tags=["root"])
    async def root():
        """根路径信息"""
        return {
            "message": "Figma REST API Service",
            "version": settings.app_version,
            "docs": "/docs",
            "health": "/health"
        }
    
    return app


# 创建应用实例
app = create_app()


def custom_openapi():
    """自定义OpenAPI文档"""
    if app.openapi_schema:
        return app.openapi_schema
    
    settings = get_settings()
    
    openapi_schema = get_openapi(
        title=settings.app_name,
        version=settings.app_version,
        description="""
        ## ZTL餐饮数智化平面设计工作台 - Figma REST API

        这是一个专为餐饮行业设计的Figma API集成服务，提供批量替换图片、量产设计工作流、任务编排等高级功能。

        ### 🚀 核心功能

        #### 1. 批量替换图片
        - **智能替换**: 批量替换Figma文件中的图片，支持URL和本地文件
        - **自动导出**: 替换完成后自动导出为指定格式
        - **插件桥接**: 与Figma插件协同工作，实现真正的写入操作

        #### 2. 量产设计工作流
        - **6张一批**: 经典的6张一批量产流水线
        - **智能编排**: 自动分批处理，支持暂停、恢复、取消
        - **进度跟踪**: 实时监控每个批次的处理进度
        - **断点续跑**: 失败自动重试，支持从中断点继续

        #### 3. 任务编排系统
        - **并发控制**: 智能控制并发任务数，避免API限流
        - **节流机制**: 可配置的批次间延迟，保护上游服务
        - **队列管理**: 多队列支持，优先级调度
        - **系统监控**: 实时监控系统负载和队列状态

        #### 4. 官方API兼容
        - **100%兼容**: 完全符合Figma官方API规范
        - **双层架构**: 兼容层 + 增强层，满足不同需求
        - **无缝迁移**: 现有Figma API客户端零成本迁移

        ### 📋 使用流程

        #### 批量替换图片
        1. 创建替换任务 (`POST /api/v1/batch-replace/`)
        2. 监控任务状态 (`GET /api/v1/batch-replace/{task_id}`)
        3. 处理失败重试 (`POST /api/v1/batch-replace/{task_id}/retry`)

        #### 量产设计工作流
        1. 创建工作流 (`POST /api/v1/production/workflow`)
        2. 监控工作流进度 (`GET /api/v1/production/workflow/{workflow_id}`)
        3. 管理工作流状态 (`POST /api/v1/production/workflow/{workflow_id}/pause`)

        #### 官方API兼容
        1. 获取文件信息 (`GET /api/v1/files/{file_key}`)
        2. 导出图片 (`GET /api/v1/images/{file_key}`)
        3. 获取节点数据 (`GET /api/v1/files/{file_key}/nodes`)

        ### 🔧 认证配置

        需要在环境变量中配置有效的Figma API Token:
        ```bash
        FIGMA_API_TOKEN=your_figma_token_here
        ```

        ### 🎯 典型场景

        - **餐饮菜单设计**: 批量替换菜品图片，一键生成多套菜单
        - **营销物料制作**: 6张一批的促销海报量产流水线
        - **品牌素材管理**: 批量更新品牌元素，保持视觉一致性
        - **季节性更新**: 定期批量更新季节性设计元素
        """,
        routes=app.routes,
    )
    
    # 添加服务器信息
    openapi_schema["servers"] = [
        {"url": "http://localhost:8000", "description": "开发环境"},
        {"url": "https://api.ztl-design.com", "description": "生产环境"}
    ]
    
    # 添加标签描述
    openapi_schema["tags"] = [
        {
            "name": "figma",
            "description": "Figma API基础操作，包括批量导出、任务管理等"
        },
        {
            "name": "figma-api",
            "description": "官方Figma API兼容端点，100%符合官方规范"
        },
        {
            "name": "batch-replace",
            "description": "批量替换图片功能，支持智能替换和自动导出"
        },
        {
            "name": "production-workflow",
            "description": "量产设计工作流，支持6张一批的流水线处理"
        },
        {
            "name": "figma-complete",
            "description": "完整的Figma官方API集成，100%覆盖所有官方端点"
        },
        {
            "name": "url-parser",
            "description": "Figma URL解析工具，自动提取file_key和node_id等参数"
        },
        {
            "name": "health",
            "description": "健康检查和服务状态监控"
        },
        {
            "name": "root",
            "description": "根路径和基本信息"
        }
    ]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == "__main__":
    import uvicorn
    
    settings = get_settings()
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
