"""
API v1版本
"""

from fastapi import APIRouter
from .endpoints import figma_router
from .endpoints.batch_replace import router as batch_replace_router
from .endpoints.batch import router as batch_router
from .endpoints.production_workflow import router as production_router

# 创建v1路由器
router = APIRouter(prefix="/v1")

# 注册子路由
router.include_router(figma_router)
router.include_router(batch_replace_router)
router.include_router(batch_router)  # 增强版批量处理端点
router.include_router(production_router)

__all__ = ["router"]
