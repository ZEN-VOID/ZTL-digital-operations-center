"""
通义万相2.5图生视频API包

模块导出:
- WanAPIClient: API客户端（来自wan-base.py）
- E8ExecutionEngine: 执行引擎（来自wan-execute.py）
"""

import importlib.util
import sys
from pathlib import Path

# 获取当前目录
current_dir = Path(__file__).parent

# 动态导入wan-base.py
wan_base_path = current_dir / "wan-base.py"
spec_base = importlib.util.spec_from_file_location("wan_base", wan_base_path)
wan_base = importlib.util.module_from_spec(spec_base)
sys.modules["wan_base"] = wan_base
spec_base.loader.exec_module(wan_base)

# 动态导入wan-execute.py
wan_execute_path = current_dir / "wan-execute.py"
spec_execute = importlib.util.spec_from_file_location("wan_execute", wan_execute_path)
wan_execute = importlib.util.module_from_spec(spec_execute)
sys.modules["wan_execute"] = wan_execute
spec_execute.loader.exec_module(wan_execute)

# 导出主要类
WanAPIClient = wan_base.WanAPIClient
E8ExecutionEngine = wan_execute.E8ExecutionEngine

__all__ = ['WanAPIClient', 'E8ExecutionEngine']
