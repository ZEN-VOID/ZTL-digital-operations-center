"""
Figma URL解析API端点
提供URL解析和参数提取功能
"""

import logging
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Query, Body
from pydantic import BaseModel, Field

from ....core.utils.figma_url_parser import (
    FigmaUrlParser, 
    FigmaUrlInfo,
    parse_figma_url,
    extract_file_key,
    extract_node_ids,
    build_api_params
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/url-parser", tags=["url-parser"])


class UrlParseRequest(BaseModel):
    """URL解析请求"""
    url: str = Field(..., description="Figma URL")


class UrlParseResponse(BaseModel):
    """URL解析响应"""
    success: bool = Field(..., description="是否解析成功")
    data: FigmaUrlInfo = Field(..., description="解析结果")
    api_params: Dict[str, Any] = Field(..., description="API调用参数")


class BatchUrlParseRequest(BaseModel):
    """批量URL解析请求"""
    urls: list[str] = Field(..., description="Figma URL列表", min_items=1, max_items=20)


class BatchUrlParseResponse(BaseModel):
    """批量URL解析响应"""
    success: bool = Field(..., description="是否全部解析成功")
    results: list[Dict[str, Any]] = Field(..., description="解析结果列表")
    failed_urls: list[str] = Field(..., description="解析失败的URL")


@router.post(
    "/parse",
    response_model=UrlParseResponse,
    summary="解析Figma URL",
    description="从Figma URL中提取file_key、node_id等参数"
)
async def parse_url(request: UrlParseRequest) -> UrlParseResponse:
    """解析单个Figma URL"""
    try:
        # 解析URL
        url_info = parse_figma_url(request.url)
        
        # 构建API参数
        api_params = build_api_params(request.url)
        
        logger.info(f"URL解析成功: {request.url} -> {url_info.file_key}")
        
        return UrlParseResponse(
            success=True,
            data=url_info,
            api_params=api_params
        )
        
    except ValueError as e:
        logger.error(f"URL解析失败: {request.url} - {e}")
        raise HTTPException(status_code=400, detail=f"URL解析失败: {e}")
    except Exception as e:
        logger.error(f"URL解析异常: {request.url} - {e}")
        raise HTTPException(status_code=500, detail=f"解析过程中发生错误: {e}")


@router.post(
    "/parse-batch",
    response_model=BatchUrlParseResponse,
    summary="批量解析Figma URL",
    description="批量解析多个Figma URL"
)
async def parse_batch_urls(request: BatchUrlParseRequest) -> BatchUrlParseResponse:
    """批量解析Figma URL"""
    results = []
    failed_urls = []
    
    for url in request.urls:
        try:
            # 解析URL
            url_info = parse_figma_url(url)
            api_params = build_api_params(url)
            
            results.append({
                "url": url,
                "success": True,
                "data": url_info.dict(),
                "api_params": api_params
            })
            
            logger.info(f"URL解析成功: {url} -> {url_info.file_key}")
            
        except Exception as e:
            failed_urls.append(url)
            results.append({
                "url": url,
                "success": False,
                "error": str(e)
            })
            
            logger.error(f"URL解析失败: {url} - {e}")
    
    success = len(failed_urls) == 0
    
    return BatchUrlParseResponse(
        success=success,
        results=results,
        failed_urls=failed_urls
    )


@router.get(
    "/extract-file-key",
    summary="提取File Key",
    description="从Figma URL中快速提取file_key"
)
async def extract_file_key_endpoint(
    url: str = Query(..., description="Figma URL")
) -> Dict[str, str]:
    """快速提取file_key"""
    try:
        file_key = extract_file_key(url)
        
        logger.info(f"File Key提取成功: {url} -> {file_key}")
        
        return {
            "url": url,
            "file_key": file_key
        }
        
    except ValueError as e:
        logger.error(f"File Key提取失败: {url} - {e}")
        raise HTTPException(status_code=400, detail=f"File Key提取失败: {e}")


@router.get(
    "/extract-node-ids",
    summary="提取Node IDs",
    description="从Figma URL中提取node_ids"
)
async def extract_node_ids_endpoint(
    url: str = Query(..., description="Figma URL")
) -> Dict[str, Any]:
    """提取node_ids"""
    try:
        node_ids = extract_node_ids(url)
        
        logger.info(f"Node IDs提取成功: {url} -> {node_ids}")
        
        return {
            "url": url,
            "node_ids": node_ids,
            "node_id": node_ids[0] if node_ids else None,
            "count": len(node_ids)
        }
        
    except ValueError as e:
        logger.error(f"Node IDs提取失败: {url} - {e}")
        raise HTTPException(status_code=400, detail=f"Node IDs提取失败: {e}")


@router.get(
    "/validate",
    summary="验证Figma URL",
    description="检查URL是否为有效的Figma URL"
)
async def validate_url(
    url: str = Query(..., description="待验证的URL")
) -> Dict[str, Any]:
    """验证Figma URL"""
    is_valid = FigmaUrlParser.is_valid_figma_url(url)
    
    result = {
        "url": url,
        "is_valid": is_valid
    }
    
    if is_valid:
        try:
            url_info = parse_figma_url(url)
            result.update({
                "file_key": url_info.file_key,
                "url_type": url_info.url_type,
                "has_node_id": bool(url_info.node_id)
            })
        except Exception as e:
            result["validation_error"] = str(e)
    
    logger.info(f"URL验证: {url} -> {is_valid}")
    
    return result


@router.post(
    "/build-api-params",
    summary="构建API参数",
    description="从Figma URL构建API调用参数"
)
async def build_api_params_endpoint(
    request: UrlParseRequest
) -> Dict[str, Any]:
    """构建API参数"""
    try:
        api_params = build_api_params(request.url)
        
        logger.info(f"API参数构建成功: {request.url}")
        
        return {
            "url": request.url,
            "api_params": api_params
        }
        
    except ValueError as e:
        logger.error(f"API参数构建失败: {request.url} - {e}")
        raise HTTPException(status_code=400, detail=f"API参数构建失败: {e}")


@router.get(
    "/examples",
    summary="URL示例",
    description="获取各种Figma URL格式的示例"
)
async def get_url_examples() -> Dict[str, Any]:
    """获取URL示例"""
    examples = {
        "file_url": {
            "description": "基本文件URL",
            "url": "https://www.figma.com/file/ABC123DEF456/Restaurant-Menu-Design",
            "extracted": {
                "file_key": "ABC123DEF456",
                "file_name": "Restaurant-Menu-Design"
            }
        },
        "file_with_node": {
            "description": "包含节点ID的文件URL",
            "url": "https://www.figma.com/file/ABC123DEF456/Restaurant-Menu-Design?node-id=1%3A23",
            "extracted": {
                "file_key": "ABC123DEF456",
                "file_name": "Restaurant-Menu-Design",
                "node_id": "1:23"
            }
        },
        "prototype_url": {
            "description": "原型URL",
            "url": "https://www.figma.com/proto/ABC123DEF456/Restaurant-Menu-Design?node-id=1%3A23",
            "extracted": {
                "file_key": "ABC123DEF456",
                "url_type": "prototype",
                "node_id": "1:23"
            }
        },
        "design_url": {
            "description": "设计URL",
            "url": "https://www.figma.com/design/ABC123DEF456/Restaurant-Menu-Design?node-id=1%3A23",
            "extracted": {
                "file_key": "ABC123DEF456",
                "url_type": "design",
                "node_id": "1:23"
            }
        },
        "multiple_nodes": {
            "description": "多个节点ID",
            "url": "https://www.figma.com/file/ABC123DEF456/Restaurant-Menu-Design?node-ids=1%3A23,1%3A24,1%3A25",
            "extracted": {
                "file_key": "ABC123DEF456",
                "node_ids": ["1:23", "1:24", "1:25"]
            }
        }
    }
    
    return {
        "description": "Figma URL格式示例",
        "examples": examples,
        "usage_tips": [
            "file_key是必需的，用于标识Figma文件",
            "node_id用于定位文件中的具体元素",
            "URL中的%3A会被自动解码为:",
            "支持file、proto、design等多种URL类型",
            "可以同时提取多个node_ids"
        ]
    }
