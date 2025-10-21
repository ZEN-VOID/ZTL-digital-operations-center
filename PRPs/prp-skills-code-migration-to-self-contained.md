# AIGC Skills代码迁移PRP
## 将执行引擎从外部目录迁移到Skills自包含结构

---

## 📋 项目概述

### 目标
将AIGC智能体的执行引擎代码从 `api/projects/nano-banana-api/` 迁移到 `.claude/skills/aigc/` 各子Skill目录中,实现符合Claude Code官方规范的自包含Skills架构。

### 背景
当前AIGC Skills使用符号链接引用外部API代码,虽然功能正常,但不符合官方推荐的"自包含能力包"理念。根据Anthropic官方文档:
> "Skills can bundle pre-written code that Claude executes directly as tools"

Skills应该包含完整的执行引擎,而不仅是知识文档。

### 价值
- ✅ **符合官方规范**: 实现真正的自包含Skills
- ✅ **提高可移植性**: Skills可独立复制到其他项目
- ✅ **增强可分发性**: 未来可作为Plugin Skills分发
- ✅ **清晰职责边界**: Skills完整拥有其能力实现

---

## 🔍 现状分析

### 当前架构

```
当前目录结构:
├── .claude/skills/aigc/
│   ├── text-to-image/
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       ├── banana-all-in-one.py → (符号链接)
│   │       └── execute_plan.py → (符号链接)
│   ├── image-to-image/
│   ├── image-recognition/
│   └── advanced-processing/
│
└── api/projects/nano-banana-api/
    ├── banana-all-in-one.py        # 1574行, 63KB
    ├── execute_plan.py             # 235行, 7.9KB
    └── models/
        └── execution_plan.py
```

### 依赖关系

#### 4个Skills共享相同代码
- `text-to-image` (E1)
- `image-to-image` (E2)
- `image-recognition` (E3)
- `advanced-processing` (E4-E9)

#### 外部依赖
```python
# 所有SKILL.md中的引用方式
sys.path.append('./api/projects/nano-banana-api')
from banana_all_in_one import NanoBananaAPI
```

#### 核心文件
1. **banana-all-in-one.py** (63KB)
   - NanoBananaAPI类
   - 支持E1-E9全系列方法
   - OpenRouter API集成
   - 图片保存和元数据管理

2. **execute_plan.py** (7.9KB)
   - JSON计划执行器
   - 参数提取和验证
   - 方法路由

---

## 🎯 迁移方案设计

### 方案A: 完全分散(每个Skill独立副本)

```
目标结构:
.claude/skills/aigc/
├── text-to-image/
│   ├── SKILL.md
│   └── scripts/
│       ├── banana-all-in-one.py    # 完整副本
│       └── execute_plan.py         # 完整副本
├── image-to-image/
│   ├── SKILL.md
│   └── scripts/
│       ├── banana-all-in-one.py    # 完整副本
│       └── execute_plan.py         # 完整副本
├── image-recognition/
│   └── scripts/
│       ├── banana-all-in-one.py    # 完整副本
│       └── execute_plan.py         # 完整副本
└── advanced-processing/
    └── scripts/
        ├── banana-all-in-one.py    # 完整副本
        └── execute_plan.py         # 完整副本
```

**优点**:
- ✅ 每个Skill完全自包含
- ✅ 无依赖关系
- ✅ 可独立分发

**缺点**:
- ❌ 代码重复(4份相同代码,共252KB)
- ❌ 维护成本高(修改需同步4份)
- ❌ 版本不一致风险

**评估**: ⚠️ 不推荐 - 代码冗余过高

---

### 方案B: 共享核心库(推荐)

```
目标结构:
.claude/skills/aigc/
├── _shared/                        # 新增共享目录
│   ├── README.md                   # 说明共享库用途
│   ├── banana_api_core.py          # 核心API类
│   ├── plan_executor.py            # 计划执行器
│   └── models/
│       └── execution_plan.py       # 数据模型
│
├── text-to-image/
│   ├── SKILL.md                    # 更新import路径
│   └── scripts/
│       └── api_wrapper.py          # 轻量级包装器
│
├── image-to-image/
│   ├── SKILL.md
│   └── scripts/
│       └── api_wrapper.py
│
├── image-recognition/
│   ├── SKILL.md
│   └── scripts/
│       └── api_wrapper.py
│
└── advanced-processing/
    ├── SKILL.md
    └── scripts/
        └── api_wrapper.py
```

**共享库使用方式**:
```python
# 各Skill的api_wrapper.py
import sys
from pathlib import Path

# 添加共享库路径
shared_lib = Path(__file__).parent.parent.parent / "_shared"
sys.path.insert(0, str(shared_lib))

from banana_api_core import NanoBananaAPI
from plan_executor import execute_plan

# Skill特定的便捷函数
def generate_image(prompt, design_type):
    api = NanoBananaAPI()
    return api.generate_text_to_image(prompt, design_type)
```

**优点**:
- ✅ 代码不重复(共享核心)
- ✅ 维护成本低(修改一处生效)
- ✅ 版本一致性保证
- ✅ 仍然自包含(整个aigc/目录)

**缺点**:
- ⚠️ 需要重构代码结构
- ⚠️ Skills间有内部依赖(_shared)

**评估**: ✅ 推荐 - 平衡了自包含和代码复用

---

### 方案C: 混合模式(渐进迁移)

保留 `api/projects/` 作为开发仓库,Skills通过拷贝获取稳定版本:

```
开发流程:
1. 在api/projects/开发和测试新功能
2. 稳定后发布到.claude/skills/aigc/_shared/
3. Skills引用_shared/中的稳定版本
```

**优点**:
- ✅ 开发和生产分离
- ✅ 代码质量可控
- ✅ 渐进迁移,风险低

**缺点**:
- ⚠️ 需要版本管理流程
- ⚠️ 两处代码存在(过渡期)

**评估**: ✅ 可选 - 适合渐进式迁移

---

## 📊 推荐方案详细设计

### 最终选择: 方案B(共享核心库)

#### 目录结构

```
.claude/skills/aigc/
├── README.md                       # AIGC Skills总览
├── ARCHITECTURE.md                 # 架构文档(已有)
├── INTEGRATION_SUMMARY.md          # 集成总结(已有)
│
├── _shared/                        # ⭐ 新增共享核心库
│   ├── README.md                   # 库说明文档
│   ├── __init__.py                 # Python包初始化
│   ├── banana_api_core.py          # 核心API类(重命名)
│   ├── plan_executor.py            # 计划执行器(重命名)
│   ├── config.py                   # 配置管理
│   └── models/
│       ├── __init__.py
│       └── execution_plan.py       # 数据模型
│
├── text-to-image/
│   ├── SKILL.md                    # 更新import示例
│   ├── reference.md
│   └── scripts/
│       ├── __init__.py
│       └── text_to_image_api.py    # Skill专用API(新增)
│
├── image-to-image/
│   ├── SKILL.md
│   ├── reference.md
│   └── scripts/
│       ├── __init__.py
│       └── image_to_image_api.py   # Skill专用API
│
├── image-recognition/
│   ├── SKILL.md
│   ├── reference.md
│   └── scripts/
│       ├── __init__.py
│       └── image_recognition_api.py
│
└── advanced-processing/
    ├── SKILL.md
    ├── reference.md
    └── scripts/
        ├── __init__.py
        └── advanced_processing_api.py
```

#### 代码重构方案

##### 1. 共享核心库 (_shared/)

**_shared/README.md**:
```markdown
# AIGC共享核心库

本目录包含所有AIGC Skills共享的核心执行引擎代码。

## 核心组件

- `banana_api_core.py`: NanoBananaAPI核心类
- `plan_executor.py`: JSON计划执行器
- `config.py`: 配置管理(API密钥、模型等)
- `models/`: 数据模型定义

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
```

**_shared/config.py** (新增):
```python
"""AIGC API配置管理"""
import os
from pathlib import Path

class AIGCConfig:
    """统一配置管理"""

    # OpenRouter配置
    API_KEY = "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"
    BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
    MODEL = "google/gemini-2.5-flash-image-preview"

    # 项目根目录
    PROJECT_ROOT = Path(__file__).parent.parent.parent.parent

    # 输出路径
    OUTPUT_BASE = PROJECT_ROOT / "output"
    IMAGES_DIR = OUTPUT_BASE / "images"
    PROMPTS_DIR = OUTPUT_BASE / "prompts"

    @classmethod
    def get_output_path(cls, agent_id: str, operation_type: str):
        """获取指定智能体的输出路径"""
        return cls.IMAGES_DIR / f"{agent_id}-{operation_type}"
```

**_shared/banana_api_core.py** (从banana-all-in-one.py重构):
```python
"""
Nano Banana API核心引擎
- 从原banana-all-in-one.py重构
- 移除硬编码配置,使用config.py
- 保持所有E1-E9方法
"""
import requests
import json
import base64
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any

from .config import AIGCConfig

class NanoBananaAPI:
    """Nano Banana API核心类"""

    def __init__(self):
        self.config = AIGCConfig()
        self.api_key = self.config.API_KEY
        self.base_url = self.config.BASE_URL
        self.model = self.config.MODEL

        # 初始化输出目录
        self.config.IMAGES_DIR.mkdir(parents=True, exist_ok=True)
        self.config.PROMPTS_DIR.mkdir(parents=True, exist_ok=True)

    # ... 保留所有generate_*方法 ...
```

##### 2. Skill专用API包装器

**text-to-image/scripts/text_to_image_api.py** (新增):
```python
"""
E1 文生图 Skill专用API

提供便捷的文生图调用接口,封装共享核心库。
"""
import sys
from pathlib import Path

# 导入共享核心库
shared_lib = Path(__file__).parent.parent.parent / "_shared"
sys.path.insert(0, str(shared_lib))

from banana_api_core import NanoBananaAPI
from plan_executor import execute_plan

# Skill便捷函数
def generate_text_to_image(prompt: str, design_type: str, **kwargs):
    """
    便捷函数:生成文生图

    Args:
        prompt: 文字描述
        design_type: 设计类型(1-poster, 2-menu等)
        **kwargs: 其他参数

    Returns:
        结果字典
    """
    api = NanoBananaAPI()
    return api.generate_text_to_image(prompt, design_type, **kwargs)

def execute_plan_from_file(plan_path: str):
    """
    便捷函数:从JSON执行计划生成

    Args:
        plan_path: JSON计划文件路径

    Returns:
        结果字典
    """
    return execute_plan(plan_path)

# 导出主要接口
__all__ = ['generate_text_to_image', 'execute_plan_from_file', 'NanoBananaAPI']
```

##### 3. 更新SKILL.md

**text-to-image/SKILL.md** 示例更新:
```markdown
---
name: AIGC Text-to-Image Generator
description: Generate professional restaurant design images from text descriptions...
---

# AIGC Text-to-Image Generator

## Quick Start

### 方式1: 使用Skill便捷函数
```python
import sys
sys.path.append('./.claude/skills/aigc/text-to-image/scripts')
from text_to_image_api import generate_text_to_image

result = generate_text_to_image(
    prompt="Modern hotpot restaurant poster",
    design_type="1-poster"
)
```

### 方式2: 使用共享核心库
```python
import sys
from pathlib import Path

# 导入共享库
shared = Path('./.claude/skills/aigc/_shared')
sys.path.insert(0, str(shared))

from banana_api_core import NanoBananaAPI

api = NanoBananaAPI()
result = api.generate_text_to_image(
    prompt="...",
    design_type="1-poster"
)
```

### 方式3: 执行JSON计划
```python
from text_to_image_api import execute_plan_from_file

result = execute_plan_from_file(
    'api/plans/e1-text-to-image/task-001.json'
)
```

## Design Types
[保持现有内容...]
```

---

## 🔧 执行步骤

### Phase 1: 准备阶段

**步骤1.1: 创建共享目录结构**
```bash
mkdir -p .claude/skills/aigc/_shared/models
touch .claude/skills/aigc/_shared/__init__.py
touch .claude/skills/aigc/_shared/models/__init__.py
```

**步骤1.2: 复制核心代码到共享库**
```bash
# 复制并重命名核心文件
cp api/projects/nano-banana-api/banana-all-in-one.py \
   .claude/skills/aigc/_shared/banana_api_core.py

cp api/projects/nano-banana-api/execute_plan.py \
   .claude/skills/aigc/_shared/plan_executor.py

cp api/projects/nano-banana-api/models/execution_plan.py \
   .claude/skills/aigc/_shared/models/
```

**步骤1.3: 创建配置文件**
```bash
# 创建config.py(提取硬编码配置)
cat > .claude/skills/aigc/_shared/config.py << 'EOF'
[配置文件内容...]
EOF
```

**步骤1.4: 创建README文档**
```bash
cat > .claude/skills/aigc/_shared/README.md << 'EOF'
[README内容...]
EOF
```

### Phase 2: 代码重构

**步骤2.1: 重构banana_api_core.py**
- 移除硬编码配置,改用config.py
- 添加from .config import AIGCConfig
- 更新__init__方法

**步骤2.2: 重构plan_executor.py**
- 更新import路径(相对导入)
- 使用config.py配置

**步骤2.3: 创建Skill专用API**
```bash
# 为每个Skill创建专用API包装器
for skill in text-to-image image-to-image image-recognition advanced-processing
do
    skill_dir=".claude/skills/aigc/${skill}"
    mkdir -p "${skill_dir}/scripts"
    touch "${skill_dir}/scripts/__init__.py"

    # 创建专用API文件
    # (根据Skill类型定制内容)
done
```

### Phase 3: 更新Skills

**步骤3.1: 更新SKILL.md**
- 更新import示例
- 添加三种使用方式说明
- 更新Quick Start代码

**步骤3.2: 删除符号链接**
```bash
find .claude/skills/aigc -type l -delete
```

**步骤3.3: 验证导入路径**
```bash
# 测试各Skill的导入
python3 << 'EOF'
import sys
sys.path.insert(0, '.claude/skills/aigc/_shared')
from banana_api_core import NanoBananaAPI
print("✅ 导入成功")
EOF
```

### Phase 4: 测试验证

**步骤4.1: 单元测试**
```python
# 测试共享库导入
import sys
from pathlib import Path
sys.path.insert(0, '.claude/skills/aigc/_shared')

from banana_api_core import NanoBananaAPI
from plan_executor import execute_plan

api = NanoBananaAPI()
assert api.model == "google/gemini-2.5-flash-image-preview"
print("✅ 共享库测试通过")
```

**步骤4.2: 集成测试**
```python
# 测试text-to-image Skill
import sys
sys.path.append('./.claude/skills/aigc/text-to-image/scripts')
from text_to_image_api import generate_text_to_image

# 模拟生成(使用测试提示词)
result = generate_text_to_image(
    prompt="Test poster",
    design_type="1-poster"
)
print(f"✅ E1测试通过: {result}")
```

**步骤4.3: Claude Skills发现测试**
- 在Claude Code中测试:"生成一张测试海报"
- 验证Claude能否自动发现text-to-image Skill
- 验证Claude能否正确导入和执行

### Phase 5: 清理与归档

**步骤5.1: 归档旧代码**
```bash
mkdir -p archive/api-projects-backup-20251020
cp -r api/projects/nano-banana-api \
      archive/api-projects-backup-20251020/
```

**步骤5.2: 更新引用文档**
- 更新ARCHITECTURE.md
- 更新INTEGRATION_SUMMARY.md
- 添加迁移完成说明

**步骤5.3: Git提交**
```bash
git add .claude/skills/aigc/_shared
git add .claude/skills/aigc/*/scripts
git add .claude/skills/aigc/*/SKILL.md
git commit -m "迁移AIGC执行引擎到Skills自包含结构

- 创建共享核心库 .claude/skills/aigc/_shared/
- 重构banana-all-in-one.py为banana_api_core.py
- 为各Skill创建专用API包装器
- 更新所有SKILL.md的import示例
- 删除符号链接,实现真正的自包含

符合Claude Code官方Skills自包含规范"
```

---

## 📊 影响评估

### 正面影响

| 维度 | 改进 | 量化指标 |
|-----|------|---------|
| **规范性** | 符合官方标准 | 100%符合 |
| **可移植性** | Skills可独立使用 | 整个aigc/目录可复制 |
| **可维护性** | 单一代码源 | 维护点减少75%(4→1) |
| **可分发性** | 支持Plugin分发 | 可直接打包 |

### 风险评估

| 风险 | 级别 | 缓解措施 |
|-----|------|---------|
| **导入路径变更** | 🟡 中 | 更新SKILL.md示例,保留过渡期文档 |
| **现有计划失效** | 🟡 中 | api/plans/继续有效,向后兼容 |
| **测试不足** | 🟢 低 | Phase 4完整测试覆盖 |
| **回滚复杂** | 🟢 低 | 归档旧代码,Git可回滚 |

### 兼容性

- ✅ **向后兼容**: 旧的import路径仍可用(过渡期)
- ✅ **JSON计划**: api/plans/中的计划无需修改
- ✅ **Agents文档**: .claude/agents/无需修改
- ⚠️ **外部引用**: 如有外部脚本引用api/projects/,需更新

---

## 📅 执行时间表

### 总时长: 2-3小时

| 阶段 | 时长 | 关键产出 |
|-----|------|---------|
| Phase 1: 准备 | 30分钟 | 目录结构、初始文件 |
| Phase 2: 重构 | 60分钟 | 共享库、专用API |
| Phase 3: 更新 | 30分钟 | SKILL.md更新 |
| Phase 4: 测试 | 30分钟 | 测试报告 |
| Phase 5: 清理 | 20分钟 | Git提交、文档更新 |

---

## ✅ 验收标准

### 功能验收

- [ ] 共享库可正常导入
- [ ] 各Skill专用API功能完整
- [ ] E1-E9所有方法可调用
- [ ] JSON计划执行正常
- [ ] Claude Skills自动发现工作
- [ ] 图片生成和保存正常

### 质量验收

- [ ] 无硬编码路径
- [ ] 所有import路径正确
- [ ] 代码无重复(共享库单一源)
- [ ] 文档完整更新
- [ ] Git历史清晰

### 性能验收

- [ ] 执行速度无明显下降
- [ ] 内存占用无明显增加
- [ ] Skills加载时间<1秒

---

## 📚 参考文档

### 官方文档
- [Claude Code Skills Guide](https://docs.claude.com/zh-CN/docs/claude-code/skills)
- [Equipping Agents with Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

### 项目文档
- [AIGC架构文档](.claude/skills/aigc/ARCHITECTURE.md)
- [Skills创建工程师](.claude/agents/system/F5-Skills技能包创建工程师.md)

### 相关代码
- 当前位置: `api/projects/nano-banana-api/`
- 目标位置: `.claude/skills/aigc/_shared/`

---

## 🎯 后续优化

### 短期(1周内)
- [ ] 监控Skills使用情况
- [ ] 收集Claude使用反馈
- [ ] 优化导入性能

### 中期(1个月内)
- [ ] 考虑将_shared发布为独立Python包
- [ ] 添加版本管理机制
- [ ] 完善单元测试覆盖

### 长期(3个月内)
- [ ] 探索作为Plugin Skills发布
- [ ] 支持其他AI模型(如Claude自身)
- [ ] 建立Skills生态系统

---

**版本**: v1.0
**创建日期**: 2025-10-20
**作者**: ZTL数智化作战中心
**状态**: 待执行 → 执行中 → 已完成
