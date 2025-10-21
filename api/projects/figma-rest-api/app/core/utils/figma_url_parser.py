"""
Figma URL解析工具
自动从Figma URL中提取file_key、node_id等参数
"""

import re
import urllib.parse
from typing import Dict, List, Optional, Tuple
from pydantic import BaseModel


class FigmaUrlInfo(BaseModel):
    """Figma URL解析结果"""
    file_key: str
    file_name: Optional[str] = None
    node_id: Optional[str] = None
    node_ids: List[str] = []
    page_id: Optional[str] = None
    team_id: Optional[str] = None
    project_id: Optional[str] = None
    url_type: str  # file, prototype, dev, etc.
    original_url: str


class FigmaUrlParser:
    """Figma URL解析器"""
    
    # Figma URL模式
    URL_PATTERNS = {
        'file': r'https://www\.figma\.com/file/([a-zA-Z0-9]+)/([^/?]+)',
        'prototype': r'https://www\.figma\.com/proto/([a-zA-Z0-9]+)/([^/?]+)',
        'dev': r'https://www\.figma\.com/dev/([a-zA-Z0-9]+)/([^/?]+)',
        'design': r'https://www\.figma\.com/design/([a-zA-Z0-9]+)/([^/?]+)',
    }
    
    @classmethod
    def parse_url(cls, url: str) -> FigmaUrlInfo:
        """
        解析Figma URL，提取所有相关参数
        
        Args:
            url: Figma URL
            
        Returns:
            FigmaUrlInfo: 解析结果
            
        Raises:
            ValueError: URL格式不正确
        """
        if not url or not isinstance(url, str):
            raise ValueError("URL不能为空")
        
        # 清理URL
        url = url.strip()
        
        # 检测URL类型并提取基本信息
        file_key = None
        file_name = None
        url_type = None
        
        for pattern_type, pattern in cls.URL_PATTERNS.items():
            match = re.match(pattern, url)
            if match:
                file_key = match.group(1)
                file_name = urllib.parse.unquote(match.group(2))
                url_type = pattern_type
                break
        
        if not file_key:
            raise ValueError(f"无法识别的Figma URL格式: {url}")
        
        # 解析URL参数
        parsed_url = urllib.parse.urlparse(url)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        
        # 提取node-id参数
        node_id = None
        node_ids = []
        
        if 'node-id' in query_params:
            # 处理单个node-id
            node_id_raw = query_params['node-id'][0]
            node_id = urllib.parse.unquote(node_id_raw)
            node_ids = [node_id]
        elif 'node-ids' in query_params:
            # 处理多个node-ids
            node_ids_raw = query_params['node-ids'][0]
            node_ids = [urllib.parse.unquote(nid) for nid in node_ids_raw.split(',')]
            if node_ids:
                node_id = node_ids[0]  # 第一个作为主要node_id
        
        # 从fragment中提取node-id (某些URL格式)
        if parsed_url.fragment and not node_id:
            fragment_match = re.search(r'node-id=([^&]+)', parsed_url.fragment)
            if fragment_match:
                node_id = urllib.parse.unquote(fragment_match.group(1))
                node_ids = [node_id]
        
        # 提取其他参数
        page_id = query_params.get('page-id', [None])[0]
        if page_id:
            page_id = urllib.parse.unquote(page_id)
        
        team_id = query_params.get('team-id', [None])[0]
        project_id = query_params.get('project-id', [None])[0]
        
        return FigmaUrlInfo(
            file_key=file_key,
            file_name=file_name,
            node_id=node_id,
            node_ids=node_ids,
            page_id=page_id,
            team_id=team_id,
            project_id=project_id,
            url_type=url_type,
            original_url=url
        )
    
    @classmethod
    def extract_file_key(cls, url: str) -> str:
        """
        快速提取file_key
        
        Args:
            url: Figma URL
            
        Returns:
            str: file_key
        """
        info = cls.parse_url(url)
        return info.file_key
    
    @classmethod
    def extract_node_ids(cls, url: str) -> List[str]:
        """
        快速提取node_ids
        
        Args:
            url: Figma URL
            
        Returns:
            List[str]: node_ids列表
        """
        info = cls.parse_url(url)
        return info.node_ids
    
    @classmethod
    def is_valid_figma_url(cls, url: str) -> bool:
        """
        检查是否为有效的Figma URL
        
        Args:
            url: 待检查的URL
            
        Returns:
            bool: 是否有效
        """
        try:
            cls.parse_url(url)
            return True
        except ValueError:
            return False
    
    @classmethod
    def normalize_node_id(cls, node_id: str) -> str:
        """
        标准化node_id格式
        
        Args:
            node_id: 原始node_id
            
        Returns:
            str: 标准化后的node_id
        """
        if not node_id:
            return node_id
        
        # URL解码
        decoded = urllib.parse.unquote(node_id)
        
        # 处理常见的编码格式
        # %3A -> :
        decoded = decoded.replace('%3A', ':')
        
        return decoded
    
    @classmethod
    def build_api_params(cls, url: str) -> Dict[str, any]:
        """
        从URL构建API调用参数
        
        Args:
            url: Figma URL
            
        Returns:
            Dict: API参数字典
        """
        info = cls.parse_url(url)
        
        params = {
            'file_key': info.file_key
        }
        
        if info.node_id:
            params['node_id'] = info.node_id
        
        if info.node_ids:
            params['node_ids'] = info.node_ids
            params['ids'] = ','.join(info.node_ids)  # 用于官方API
        
        if info.page_id:
            params['page_id'] = info.page_id
        
        return params


# 便捷函数
def parse_figma_url(url: str) -> FigmaUrlInfo:
    """解析Figma URL的便捷函数"""
    return FigmaUrlParser.parse_url(url)


def extract_file_key(url: str) -> str:
    """提取file_key的便捷函数"""
    return FigmaUrlParser.extract_file_key(url)


def extract_node_ids(url: str) -> List[str]:
    """提取node_ids的便捷函数"""
    return FigmaUrlParser.extract_node_ids(url)


def build_api_params(url: str) -> Dict[str, any]:
    """构建API参数的便捷函数"""
    return FigmaUrlParser.build_api_params(url)


# 示例用法
if __name__ == "__main__":
    # 测试URL解析
    test_urls = [
        "https://www.figma.com/file/ABC123DEF456/Restaurant-Menu-Design",
        "https://www.figma.com/file/ABC123DEF456/Restaurant-Menu-Design?node-id=1%3A23",
        "https://www.figma.com/file/ABC123DEF456/Restaurant-Menu-Design?node-id=1%3A23&page-id=0%3A1",
        "https://www.figma.com/proto/ABC123DEF456/Restaurant-Menu-Design?node-id=1%3A23",
        "https://www.figma.com/design/ABC123DEF456/Restaurant-Menu-Design?node-id=1%3A23&node-ids=1%3A23,1%3A24,1%3A25"
    ]
    
    for url in test_urls:
        try:
            info = parse_figma_url(url)
            print(f"URL: {url}")
            print(f"  File Key: {info.file_key}")
            print(f"  File Name: {info.file_name}")
            print(f"  Node ID: {info.node_id}")
            print(f"  Node IDs: {info.node_ids}")
            print(f"  URL Type: {info.url_type}")
            print(f"  API Params: {build_api_params(url)}")
            print()
        except ValueError as e:
            print(f"解析失败: {url} - {e}")
            print()
