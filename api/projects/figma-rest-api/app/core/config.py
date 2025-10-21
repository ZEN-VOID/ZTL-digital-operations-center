"""
Figma REST API项目配置
"""

import os
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class DatabaseConfig(BaseSettings):
    """数据库配置"""
    database_url: str = Field(
        default="sqlite+aiosqlite:///./figma_api.db",
        description="数据库连接URL"
    )
    echo_sql: bool = Field(default=False, description="是否打印SQL语句")
    
    model_config = {"env_prefix": "DB_"}


class FigmaConfig(BaseSettings):
    """Figma API配置"""
    api_token: str = Field(..., description="Figma API访问令牌")
    api_base_url: str = Field(
        default="https://api.figma.com/v1/",
        description="Figma API基础URL"
    )
    timeout: int = Field(default=30, description="请求超时时间(秒)")
    max_retries: int = Field(default=3, description="最大重试次数")
    rate_limit_per_minute: int = Field(default=60, description="每分钟请求限制")
    concurrent_requests: int = Field(default=5, description="并发请求数")
    
    model_config = {"env_prefix": "FIGMA_"}


class AppConfig(BaseSettings):
    """应用配置"""
    app_name: str = Field(default="Figma REST API", description="应用名称")
    app_version: str = Field(default="1.0.0", description="应用版本")
    debug: bool = Field(default=False, description="调试模式")
    log_level: str = Field(default="INFO", description="日志级别")
    
    # 文件存储配置
    upload_dir: str = Field(default="./uploads", description="上传目录")
    export_dir: str = Field(default="./exports", description="导出目录")
    max_file_size: int = Field(default=100 * 1024 * 1024, description="最大文件大小(字节)")
    
    # 任务配置
    default_batch_size: int = Field(default=6, description="默认批次大小")
    max_batch_size: int = Field(default=20, description="最大批次大小")
    task_cleanup_days: int = Field(default=7, description="任务清理天数")
    
    model_config = {"env_prefix": "APP_"}


class Settings(BaseSettings):
    """应用设置"""

    # 直接定义配置字段而不是嵌套配置类
    # 数据库配置
    database_url: str = Field(
        default="sqlite+aiosqlite:///./figma_api.db",
        description="数据库连接URL"
    )
    echo_sql: bool = Field(default=False, description="是否打印SQL语句")

    # Figma API配置
    figma_api_token: str = Field(..., description="Figma API Token")
    figma_api_base_url: str = Field(
        default="https://api.figma.com/v1/",
        description="Figma API基础URL"
    )
    figma_timeout: int = Field(default=30, description="请求超时时间(秒)")
    figma_max_retries: int = Field(default=3, description="最大重试次数")
    figma_rate_limit_per_minute: int = Field(default=60, description="每分钟请求限制")
    figma_concurrent_requests: int = Field(default=5, description="并发请求数")

    # 应用配置
    app_name: str = Field(default="Figma REST API", description="应用名称")
    app_version: str = Field(default="1.0.0", description="应用版本")
    debug: bool = Field(default=False, description="调试模式")
    log_level: str = Field(default="INFO", description="日志级别")

    # 文件存储配置
    upload_dir: str = Field(default="./uploads", description="上传目录")
    export_dir: str = Field(default="./exports", description="导出目录")
    max_file_size: int = Field(default=100*1024*1024, description="最大文件大小(字节)")

    # 任务配置
    default_batch_size: int = Field(default=6, description="默认批次大小")
    max_batch_size: int = Field(default=20, description="最大批次大小")
    task_cleanup_days: int = Field(default=7, description="任务清理天数")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore"
    }

    def __init__(self, **kwargs):
        """初始化设置"""
        super().__init__(**kwargs)
        # 确保目录存在
        os.makedirs(self.upload_dir, exist_ok=True)
        os.makedirs(self.export_dir, exist_ok=True)


# 全局设置实例
settings = Settings()


def get_settings() -> Settings:
    """获取应用设置"""
    return settings
