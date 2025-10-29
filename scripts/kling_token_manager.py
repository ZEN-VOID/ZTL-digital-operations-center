#!/usr/bin/env python3
"""
Kling AI JWT Token Manager
管理Kling AI API的JWT Token生成和刷新

官方文档: https://platform.klingai.com/docs
认证方式: HMAC-SHA256签名生成JWT Token
"""

import os
import time
import hmac
import hashlib
import json
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime, timedelta


class KlingTokenManager:
    """
    Kling AI JWT Token管理器

    功能:
    - 从环境变量加载AccessKey和SecretKey
    - 生成JWT Token (使用HMAC-SHA256)
    - 自动刷新过期Token
    - 提供标准请求头
    """

    def __init__(self,
                 env_path: Optional[Path] = None,
                 access_key: Optional[str] = None,
                 secret_key: Optional[str] = None,
                 token_expire_seconds: int = 1800):
        """
        初始化Token管理器

        Args:
            env_path: .env文件路径（可选）
            access_key: Kling AI Access Key (默认从环境变量读取)
            secret_key: Kling AI Secret Key (默认从环境变量读取)
            token_expire_seconds: Token有效期（秒），默认1800秒（30分钟）
        """
        # 加载.env文件
        self._load_env(env_path)

        # API凭证
        self.access_key = access_key or os.getenv('KLING_ACCESS_KEY')
        self.secret_key = secret_key or os.getenv('KLING_SECRET_KEY')
        self.token_expire_seconds = token_expire_seconds

        # 验证凭证
        if not self.access_key or not self.secret_key:
            raise ValueError(
                "❌ 缺少Kling AI API凭证\n"
                "请设置环境变量: KLING_ACCESS_KEY, KLING_SECRET_KEY\n"
                "或在初始化时传入access_key和secret_key参数"
            )

        # Token缓存
        self._cached_token: Optional[str] = None
        self._token_expire_time: Optional[datetime] = None

        print(f"✅ Kling Token Manager已初始化")
        print(f"   Access Key: {self.access_key[:20]}...")
        print(f"   Token有效期: {token_expire_seconds}秒")

    def _load_env(self, env_path: Optional[Path] = None):
        """从.env文件加载环境变量"""
        # 如果指定了env_path，使用指定的路径
        if env_path:
            env_file = Path(env_path)
        else:
            # 查找.env文件
            current_dir = Path(__file__).resolve().parent
            project_root = current_dir.parent
            env_file = project_root / '.env'

        if env_file.exists():
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()

    def generate_jwt_token(self) -> str:
        """
        生成JWT Token

        使用HMAC-SHA256算法签名

        JWT结构:
        {
          "alg": "HS256",
          "typ": "JWT"
        }.
        {
          "iss": "access_key",
          "exp": expire_timestamp,
          "nbf": current_timestamp
        }.
        signature

        Returns:
            JWT Token字符串
        """
        import base64

        # 1. Header
        header = {
            "alg": "HS256",
            "typ": "JWT"
        }
        header_b64 = base64.urlsafe_b64encode(
            json.dumps(header, separators=(',', ':')).encode()
        ).decode().rstrip('=')

        # 2. Payload
        current_time = int(time.time())
        expire_time = current_time + self.token_expire_seconds

        payload = {
            "iss": self.access_key,
            "exp": expire_time,
            "nbf": current_time
        }
        payload_b64 = base64.urlsafe_b64encode(
            json.dumps(payload, separators=(',', ':')).encode()
        ).decode().rstrip('=')

        # 3. Signature
        message = f"{header_b64}.{payload_b64}".encode()
        signature = hmac.new(
            self.secret_key.encode(),
            message,
            hashlib.sha256
        ).digest()
        signature_b64 = base64.urlsafe_b64encode(signature).decode().rstrip('=')

        # 4. 组合JWT
        jwt_token = f"{header_b64}.{payload_b64}.{signature_b64}"

        # 更新缓存
        self._cached_token = jwt_token
        self._token_expire_time = datetime.fromtimestamp(expire_time)

        return jwt_token

    def get_token(self, force_refresh: bool = False) -> str:
        """
        获取JWT Token

        自动判断是否需要刷新:
        - 如果Token不存在，生成新Token
        - 如果Token即将过期（剩余时间<5分钟），刷新Token
        - 如果force_refresh=True，强制刷新

        Args:
            force_refresh: 是否强制刷新Token

        Returns:
            有效的JWT Token
        """
        # 检查是否需要刷新
        need_refresh = (
            force_refresh or
            self._cached_token is None or
            self._token_expire_time is None or
            (self._token_expire_time - datetime.now()).total_seconds() < 300
        )

        if need_refresh:
            print("🔄 正在生成新的JWT Token...")
            token = self.generate_jwt_token()
            print(f"✅ JWT Token已生成")
            print(f"   过期时间: {self._token_expire_time.strftime('%Y-%m-%d %H:%M:%S')}")
            return token

        return self._cached_token

    def get_headers(self) -> Dict[str, str]:
        """
        获取标准请求头

        包含:
        - Authorization: Bearer {jwt_token}
        - Content-Type: application/json

        Returns:
            请求头字典
        """
        token = self.get_token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    def is_token_valid(self) -> bool:
        """
        检查当前Token是否有效

        Returns:
            True if Token存在且未过期
        """
        if self._cached_token is None or self._token_expire_time is None:
            return False

        return datetime.now() < self._token_expire_time

    def get_token_info(self) -> Dict[str, any]:
        """
        获取Token信息

        Returns:
            包含Token状态的字典
        """
        if not self._cached_token:
            return {
                "status": "未生成",
                "valid": False
            }

        remaining_seconds = (
            self._token_expire_time - datetime.now()
        ).total_seconds() if self._token_expire_time else 0

        return {
            "status": "有效" if self.is_token_valid() else "已过期",
            "valid": self.is_token_valid(),
            "expire_time": self._token_expire_time.strftime('%Y-%m-%d %H:%M:%S') if self._token_expire_time else None,
            "remaining_seconds": max(0, int(remaining_seconds)),
            "remaining_minutes": max(0, int(remaining_seconds / 60)),
            "token_preview": self._cached_token[:50] + "..." if self._cached_token else None
        }


def main():
    """测试Token管理器"""
    print("\n" + "="*60)
    print("🔑 Kling AI JWT Token Manager 测试")
    print("="*60)

    try:
        # 初始化管理器
        manager = KlingTokenManager()

        # 生成Token
        print("\n1️⃣ 生成JWT Token...")
        token = manager.get_token()
        print(f"   Token: {token[:50]}...")

        # 获取请求头
        print("\n2️⃣ 获取标准请求头...")
        headers = manager.get_headers()
        print(f"   Authorization: {headers['Authorization'][:70]}...")
        print(f"   Content-Type: {headers['Content-Type']}")

        # Token信息
        print("\n3️⃣ Token信息...")
        info = manager.get_token_info()
        for key, value in info.items():
            print(f"   {key}: {value}")

        print("\n✅ Token管理器测试完成!")

    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()

    print("="*60 + "\n")


if __name__ == "__main__":
    main()
