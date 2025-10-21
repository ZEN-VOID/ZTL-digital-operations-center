# AIGC共享核心库

本目录包含所有AIGC Skills共享的核心执行引擎代码。

## 核心组件

- `banana_api_core.py`: NanoBananaAPI核心类
- `plan_executor.py`: JSON计划执行器
- `config.py`: 配置管理(API密钥、模型等)

## 使用方式

各Skill通过相对路径导入:

```python
import sys
from pathlib import Path
shared = Path(__file__).parent.parent.parent / "_shared"
sys.path.insert(0, str(shared))

from banana_api_core import NanoBananaAPI
```

## 版本管理

- 版本: 2.0
- 最后更新: 2025-10-20
- 兼容Skills: text-to-image, image-to-image, image-recognition, advanced-processing
