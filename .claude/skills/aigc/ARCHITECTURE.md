# AIGC智能体与Skills架构详解

> 详细说明AIGC智能体、Skills模块、API执行的完整技术架构和内部流程

---

## 📋 目录

1. [整体架构概览](#整体架构概览)
2. [智能体与Skills关系](#智能体与Skills关系)
3. [三层架构设计](#三层架构设计)
4. [API任务执行流程](#API任务执行流程)
5. [Claude自动发现机制](#Claude自动发现机制)
6. [完整执行示例](#完整执行示例)
7. [技术栈与文件组织](#技术栈与文件组织)

---

## 整体架构概览

### 核心组件关系

```
┌─────────────────────────────────────────────────────────────┐
│                        用户请求                              │
│              "帮我生成一张火锅店开业海报"                     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Claude Sonnet 4.5                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  1. 意图识别: "生成海报" → text-to-image           │  │
│  │  2. 关键词匹配: "生成", "海报" → Skill Discovery  │  │
│  │  3. 智能体选择: V3-AIGC文生图设计师               │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Skills自动发现与加载 (渐进式)                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Level 1: 读取 text-to-image/SKILL.md (~500 tokens) │  │
│  │  - YAML frontmatter识别                             │  │
│  │  - description匹配确认                              │  │
│  │  - 快速开始示例                                     │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Level 2: (按需)读取 reference.md (~2000 tokens)   │  │
│  │  - 完整API参数说明                                  │  │
│  │  - 9种设计类型详解                                  │  │
│  │  - 错误处理策略                                     │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   智能体执行层                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  智能体: V3-AIGC文生图设计师.md                     │  │
│  │  - 分析用户需求: "火锅店开业海报"                   │  │
│  │  - 识别设计类型: "1-poster"                         │  │
│  │  - 增强提示词: 整合餐饮语料库                       │  │
│  │  - 生成执行计划: JSON配置                           │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    API执行引擎                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  执行路径1: 直接方法调用                            │  │
│  │  api = NanoBananaAPI()                              │  │
│  │  result = api.generate_text_to_image(              │  │
│  │      prompt="...",                                  │  │
│  │      design_type="1-poster"                         │  │
│  │  )                                                   │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  执行路径2: JSON计划执行                            │  │
│  │  python plan_executor.py \                          │  │
│  │    --plan api/plans/e1-text-to-image/task.json     │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              OpenRouter API调用                              │
│  Model: google/gemini-2.5-flash-image-preview               │
│  - 接收增强后的提示词                                       │
│  - 执行图像生成                                             │
│  - 返回Base64图片数据                                       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     结果处理与返回                           │
│  - 解码Base64图片                                           │
│  - 保存到 output/images/e1-text-to-image/                  │
│  - 保存提示词到 output/prompts/                             │
│  - 返回结果给Claude                                         │
│  - Claude展示给用户                                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 智能体与Skills关系

### 一对一映射关系

| 智能体 | Agent文件 | Skills模块 | 核心能力 |
|--------|-----------|-----------|---------|
| **V3-AIGC文生图设计师** | `.claude/agents/创意组/V3-AIGC文生图设计师.md` | `.claude/skills/aigc/text-to-image/` | 9种餐饮设计类型的文生图 |
| **V4-AIGC图生图设计师** | `.claude/agents/创意组/V4-AIGC图生图设计师.md` | `.claude/skills/aigc/image-to-image/` | 5种图片处理类型 |
| **V5-AIGC图片识别分析师** | `.claude/agents/创意组/V5-AIGC图片识别分析师.md` | `.claude/skills/aigc/image-recognition/` | 5种分析类型、120+维度 |
| **V6-AIGC高级图片处理师** | `.claude/agents/创意组/V6-AIGC高级图片处理师.md` | `.claude/skills/aigc/advanced-processing/` | E4-E9共6大高级能力 |

### 职责分工

#### 智能体文档 (Agent.md) 负责：
- ✅ **业务逻辑** - 定义业务目标、价值定位、使用场景
- ✅ **领域知识** - 餐饮行业专业知识、设计理论、美学原则
- ✅ **工作流程** - 需求分析 → 参数提取 → 计划生成 → 执行调度
- ✅ **规范标准** - 设计类型规范、质量标准、输出要求
- ✅ **执行编排** - 决定何时调用哪个API、如何组合多个API

**示例（V3智能体文档片段）**:
```markdown
### 主要设计类型

#### 🎨 **1. 海报设计 (Poster)**
- **比例**: 2:3纵向
- **目录**: 1-poster
- **场景**: 开业庆典、促销活动、节日营销

#### 📋 **2. 菜单设计 (Menu)**
- **比例**: 3:4纵向
- **目录**: 2-menu
- **场景**: 正餐菜单、饮品单、外卖菜单
```

#### Skills文档 (SKILL.md) 负责：
- ✅ **技术实现** - API调用方式、参数说明、代码示例
- ✅ **快速开始** - 最小化的上手示例、常见任务
- ✅ **API参考** - 完整的方法签名、参数类型、返回值
- ✅ **错误处理** - 常见错误、调试指南、最佳实践
- ✅ **工具发现** - 通过description让Claude自动发现

**示例（text-to-image/SKILL.md片段）**:
```markdown
---
name: AIGC Text-to-Image Generator
description: Generate professional restaurant design images from text descriptions.
Supports 9 design types (poster, menu, storefront...). Use when generating
restaurant visuals, marketing materials, or when user mentions text-to-image,
design generation, or restaurant graphics.
---

## Quick Start
```python
api = NanoBananaAPI()
result = api.generate_text_to_image(
    prompt="Create a modern hotpot poster",
    design_type="1-poster"
)
```
```

### 协作模式

```
用户请求: "生成火锅店开业海报"
    │
    ▼
┌─────────────────────────────────────┐
│  Claude读取智能体文档               │
│  - 理解业务目标                     │
│  - 学习餐饮设计知识                 │
│  - 掌握9种设计类型                  │
│  - 了解海报设计规范                 │
└──────────────┬──────────────────────┘
               │ 决策: 需要文生图能力
               ▼
┌─────────────────────────────────────┐
│  Claude发现text-to-image Skill      │
│  - 匹配关键词: "generate", "poster" │
│  - 读取SKILL.md获取技术细节         │
│  - 学习API调用方式                  │
└──────────────┬──────────────────────┘
               │ 组合知识
               ▼
┌─────────────────────────────────────┐
│  Claude综合决策                     │
│  - 业务知识(智能体) + 技术知识(Skill)│
│  - 生成执行代码                     │
│  - 调用API执行                      │
└─────────────────────────────────────┘
```

---

## 三层架构设计

### Layer 1: 规范层 (Rules Layer)

**位置**: `.claude/agents/创意组/V{3-6}*.md`

**职责**:
- 定义智能体的业务目标和价值定位
- 描述领域知识和专业理论
- 规定工作流程和决策逻辑
- 设定质量标准和输出规范

**示例结构**:
```markdown
# V3-AIGC文生图设计师

## 🎯 概念与价值定义
- 核心目标: 生成符合餐饮行业标准的专业级平面设计
- 业务价值: 流程自动化、品牌一致性、质量提升

## 🤖 角色与交互设计
- 智能体身份: 餐饮行业全类型平面设计专家
- 交互模式: RequestResponse + HumanInTheLoop
- 自主级别: ModelDrivenWorkflow

## ⚙️ 架构与核心组件
- 大语言模型: google/gemini-2.5-flash-image-preview
- 工具集: 三层架构 + Skills集成
- 外部资源: library/prompts/ 餐饮语料库
```

**智能体如何使用规范层**:
1. Claude读取智能体文档
2. 理解业务目标和领域知识
3. 学习9种设计类型的规范
4. 掌握质量标准和输出要求

---

### Layer 2: 计划层 (Plan Layer)

**位置**: `api/plans/e{1-9}-{operation-name}/`

**职责**:
- 存储结构化的任务执行计划（JSON格式）
- 分离配置与代码，实现可复用性
- 支持版本控制和任务追溯
- 标准化不同智能体的执行接口

**执行计划标准格式**:
```json
{
  "agent_id": "E1",
  "task_description": "生成火锅店开业海报",
  "input_data": {
    "text_prompt": "火锅店开业庆典海报，喜庆红色背景，火锅食材...",
    "design_type": "1-poster",
    "design_requirements": [
      "保持品牌红色色调",
      "突出开业优惠信息",
      "适合印刷输出300 DPI"
    ]
  },
  "output_settings": {
    "save_path": "output/images/e1-text-to-image/",
    "format": "png"
  },
  "metadata": {
    "created_at": "2025-10-20T10:30:00",
    "created_by": "V3-AIGC文生图设计师",
    "version": "1.0"
  }
}
```

**执行方式**:
```bash
# 使用plan_executor.py执行JSON计划
python .claude/skills/aigc/_shared/plan_executor.py \
  --plan api/plans/e1-text-to-image/hotpot-opening.json
```

**优势**:
- ✅ **配置与代码分离** - 修改参数无需改代码
- ✅ **任务可复用** - 相同配置可重复执行
- ✅ **版本可控** - JSON文件可纳入Git管理
- ✅ **流程可追溯** - 保留完整执行历史

---

### Layer 3: 执行层 (Execution Layer)

**位置**: `.claude/skills/aigc/_shared/`

**核心文件**:

#### 1. `banana_api_core.py` - 统一API客户端

**职责**:
- 封装E1-E9所有智能体的API调用
- 统一OpenRouter接口
- 处理提示词增强和语料库集成
- 图片保存和元数据管理

**核心类结构**:
```python
class NanoBananaAPI:
    def __init__(self):
        self.api_key = "sk-or-v1-..."
        self.model = "google/gemini-2.5-flash-image-preview"
        self.design_types = {...}  # E1: 9种设计类型
        self.processing_types = {...}  # E2: 5种处理类型
        self.analysis_types = {...}  # E3: 5种分析类型
        # ... E4-E9的类型映射

    # E1: 文生图
    def generate_text_to_image(self, prompt, design_type):
        """生成餐饮设计图片"""
        pass

    # E2: 图生图
    def generate_image_to_image(self, prompt, image_urls, processing_type):
        """基于现有图片进行优化"""
        pass

    # E3: 图片识别
    def generate_image_recognition(self, image_url, analysis_type):
        """分析图片内容和质量"""
        pass

    # E4-E9: 高级处理方法
    def generate_smart_repair(self, image_url, repair_prompt, repair_type):
        """智能修复与扩展"""
        pass

    # 计划层执行入口
    def execute_from_plan(self, plan_file_path):
        """从JSON执行计划生成"""
        pass
```

#### 2. `plan_executor.py` - 通用执行器

**职责**:
- 读取JSON执行计划
- 提取agent_id识别智能体
- 路由到对应的API方法
- 统一错误处理和结果输出

**方法路由表**:
```python
AGENT_METHOD_MAP = {
    "E1": "generate_text_to_image",
    "E2": "generate_image_to_image",
    "E3": "generate_image_recognition",
    "E4": "generate_smart_repair",
    "E5": "generate_structure_control",
    "E6": "generate_image_fusion",
    "E7": "generate_character_consistency",
    "E8": "generate_design_iteration",
    "E9": "generate_super_resolution"
}
```

**执行流程**:
```python
def execute_plan(plan_path):
    # 1. 加载JSON计划
    plan = load_execution_plan(plan_path)

    # 2. 识别智能体
    agent_id = plan["agent_id"]  # "E1"

    # 3. 提取参数
    params = extract_api_params(plan)  # 根据agent_id提取

    # 4. 路由到方法
    method_name = AGENT_METHOD_MAP[agent_id]  # "generate_text_to_image"
    api = NanoBananaAPI()
    method = getattr(api, method_name)

    # 5. 执行调用
    result = method(**params)

    # 6. 返回结果
    return result
```

---

## API任务执行流程

### 完整执行链路（以E1文生图为例）

#### 阶段1: 用户请求与意图识别

```
用户输入: "帮我生成一张火锅店开业海报，要喜庆的红色风格"
    │
    ▼
Claude分析:
  - 关键词提取: "生成", "海报", "火锅店", "开业", "红色"
  - 任务类型: 图像生成 (text-to-image)
  - 设计类型: 海报 (poster)
  - 风格要求: 喜庆、红色
```

#### 阶段2: Skills自动发现

```
Claude执行Skills Discovery:
  1. 扫描 .claude/skills/aigc/ 目录
  2. 读取各Skill的YAML frontmatter:
     - text-to-image: description包含 "text-to-image", "generate", "poster"
     - image-to-image: description包含 "edit", "modify"
     - ... (其他Skills)

  3. 关键词匹配:
     用户词: ["生成", "海报"]
     ↓ 匹配
     text-to-image description: "Generate professional restaurant design
     images... Supports 9 design types (poster, menu...)..."

  4. 匹配成功! 发现 text-to-image Skill
```

#### 阶段3: 渐进式信息加载

```
Level 1 - 读取 SKILL.md (~500 tokens):
  ┌────────────────────────────────────────┐
  │ name: AIGC Text-to-Image Generator     │
  │ description: Generate professional ... │
  │                                        │
  │ ## Quick Start                         │
  │ api = NanoBananaAPI()                  │
  │ result = api.generate_text_to_image(   │
  │     prompt="...",                      │
  │     design_type="1-poster"             │
  │ )                                      │
  │                                        │
  │ ## Design Types                        │
  │ | Poster | 1-poster | 2:3 | ...       │
  │ | Menu   | 2-menu   | 3:4 | ...       │
  └────────────────────────────────────────┘

Claude获得:
  - 基本调用方式
  - 9种设计类型代码
  - 快速示例

Level 2 - (按需)读取 reference.md (~2000 tokens):
  ┌────────────────────────────────────────┐
  │ ## API Methods                         │
  │                                        │
  │ ### generate_text_to_image()           │
  │ **Parameters**:                        │
  │   - prompt (str): 详细的文字描述       │
  │   - design_type (str): 设计类型        │
  │     - "1-poster": 海报 (2:3)           │
  │     - "2-menu": 菜单 (3:4)             │
  │   - design_requirements (list): 可选   │
  │                                        │
  │ **Returns**:                           │
  │   {                                    │
  │     "success": bool,                   │
  │     "image_paths": [str],              │
  │     "prompt_used": str                 │
  │   }                                    │
  └────────────────────────────────────────┘

Claude获得:
  - 完整参数说明
  - 返回值结构
  - 错误处理策略
```

#### 阶段4: 智能体业务逻辑处理

```
Claude读取智能体文档:
  .claude/agents/创意组/V3-AIGC文生图设计师.md

  提取业务知识:
  ┌────────────────────────────────────────┐
  │ ### 主要设计类型                       │
  │ #### 🎨 1. 海报设计 (Poster)           │
  │ - 比例: 2:3纵向                        │
  │ - 目录: 1-poster                       │
  │ - 场景: 开业庆典、促销活动             │
  │ - 设计要点:                            │
  │   - 主题突出、信息层次清晰             │
  │   - 视觉冲击力强                       │
  │   - 品牌元素统一                       │
  └────────────────────────────────────────┘

  整合餐饮语料库:
  ┌────────────────────────────────────────┐
  │ library/prompts/                       │
  │ ├── color-theory.json                  │
  │ │   → 火锅: 暖色系、红橙配色           │
  │ ├── design-masters.json                │
  │ │   → 海报: 斯图亚特·戴维斯风格         │
  │ ├── typography.json                    │
  │ │   → 标题: 粗体、醒目、居中           │
  └────────────────────────────────────────┘

Claude生成增强提示词:
  原始: "火锅店开业海报，喜庆的红色风格"
  ↓ 增强
  最终: "专业级火锅店开业庆典海报设计，采用中国传统喜庆配色方案，
        以暖红色(#D4332A)为主色调，金黄色(#FDB913)为辅助色，
        融合斯图亚特·戴维斯的现代平面设计风格，
        突出'开业大吉'主题文字，包含火锅食材视觉元素，
        版式采用中心对称构图，300 DPI印刷级质量，2:3纵向海报比例"
```

#### 阶段5: API调用执行

```
执行路径1: 直接方法调用
┌────────────────────────────────────────┐
│ import sys                             │
│ sys.path.append('./api/projects/...')  │
│ from banana_all_in_one import NanoB... │
│                                        │
│ api = NanoBananaAPI()                  │
│ result = api.generate_text_to_image(   │
│     prompt="专业级火锅店开业庆典...",  │
│     design_type="1-poster"             │
│ )                                      │
└────────────────────────────────────────┘

执行路径2: JSON计划执行
┌────────────────────────────────────────┐
│ # 1. Claude生成执行计划JSON             │
│ plan = {                               │
│   "agent_id": "E1",                    │
│   "input_data": {                      │
│     "text_prompt": "专业级火锅店...",  │
│     "design_type": "1-poster"          │
│   }                                    │
│ }                                      │
│                                        │
│ # 2. 保存到文件                         │
│ with open("task.json", "w") as f:      │
│     json.dump(plan, f)                 │
│                                        │
│ # 3. 执行计划                           │
│ python plan_executor.py --plan task.json│
└────────────────────────────────────────┘
```

#### 阶段6: OpenRouter API交互

```
NanoBananaAPI内部处理:
┌────────────────────────────────────────────────────────┐
│ def generate_text_to_image(self, prompt, design_type): │
│     # 1. 构建API请求                                   │
│     payload = {                                        │
│         "model": "google/gemini-2.5-flash-image-...",  │
│         "messages": [{                                 │
│             "role": "user",                            │
│             "content": prompt                          │
│         }]                                             │
│     }                                                  │
│                                                        │
│     # 2. 调用OpenRouter                                │
│     response = requests.post(                          │
│         "https://openrouter.ai/api/v1/chat/...",      │
│         headers={                                      │
│             "Authorization": f"Bearer {self.api_key}", │
│             "HTTP-Referer": self.site_url              │
│         },                                             │
│         json=payload                                   │
│     )                                                  │
│                                                        │
│     # 3. 提取图片数据                                  │
│     image_base64 = response.json()["data"][0]["..."]  │
│                                                        │
│     # 4. 解码并保存                                    │
│     image_data = base64.b64decode(image_base64)        │
│     timestamp = datetime.now().strftime("%Y%m%d_...")  │
│     filename = f"text_to_image_{timestamp}_1.png"      │
│     save_path = self.output_base / "images" / "e1-..." │
│     with open(save_path / filename, "wb") as f:        │
│         f.write(image_data)                            │
│                                                        │
│     # 5. 返回结果                                      │
│     return {                                           │
│         "success": True,                               │
│         "image_paths": [str(save_path / filename)],    │
│         "prompt_used": prompt                          │
│     }                                                  │
└────────────────────────────────────────────────────────┘
```

#### 阶段7: 结果处理与返回

```
输出文件结构:
output/
├── images/
│   └── e1-text-to-image/
│       └── text_to_image_20251020_103000_1.png  ← 生成的海报
└── prompts/
    └── e1-text-to-image/
        └── text_to_image_20251020_103000_prompt.json  ← 提示词记录

Claude返回给用户:
┌────────────────────────────────────────┐
│ ✅ 已成功生成火锅店开业海报！          │
│                                        │
│ 📁 文件位置:                           │
│ output/images/e1-text-to-image/        │
│ text_to_image_20251020_103000_1.png    │
│                                        │
│ 🎨 设计特点:                           │
│ - 喜庆红色主色调                       │
│ - 2:3海报比例                          │
│ - 300 DPI印刷级质量                    │
│ - 突出开业主题                         │
│                                        │
│ 📋 提示词已保存到:                     │
│ output/prompts/...prompt.json          │
└────────────────────────────────────────┘
```

---

## Claude自动发现机制

### Skills Discovery原理

#### 1. YAML Frontmatter识别

每个Skill的SKILL.md开头包含元数据：

```yaml
---
name: AIGC Text-to-Image Generator
description: Generate professional restaurant design images from text descriptions.
Supports 9 design types (poster, menu, storefront, panel, magazine, icon,
typography, main-image, detail). Use when generating restaurant visuals,
marketing materials, or when user mentions text-to-image, design generation,
or restaurant graphics. Requires OpenRouter API key.
---
```

**关键字段**:
- `name`: Skill的规范名称
- `description`: 详细描述，包含触发关键词

#### 2. 关键词匹配策略

Claude使用语义理解匹配用户意图与description：

```
用户请求分析:
  "帮我生成一张火锅店开业海报"
  ↓ 提取关键词
  ["生成", "海报", "火锅店", "开业"]
  ↓ 意图识别
  任务类型: 图像生成
  设计类型: 海报
  行业: 餐饮

Skills扫描:
  text-to-image/SKILL.md:
    description关键词:
      - "Generate" ✓ (匹配 "生成")
      - "poster" ✓ (匹配 "海报")
      - "restaurant" ✓ (匹配 "火锅店")
      - "design images" ✓ (匹配意图)

    匹配度: 高 ✓✓✓

  image-to-image/SKILL.md:
    description关键词:
      - "edit", "modify" ✗ (不匹配 "生成")
      - "enhance", "improve" ✗

    匹配度: 低 ✗

  → 选择: text-to-image Skill
```

#### 3. 触发时机

Claude在以下情况会触发Skills发现：

```
触发场景1: 用户明确提到技术术语
  用户: "用text-to-image生成海报"
  → 直接匹配 "text-to-image" 关键词

触发场景2: 用户描述功能需求
  用户: "帮我生成一张海报"
  → 语义匹配 "generate" + "poster"

触发场景3: 用户询问能力
  用户: "你能帮我设计餐厅菜单吗？"
  → 匹配 "design" + "menu" + "restaurant"

触发场景4: 上下文推断
  用户上一轮: "我想做火锅店营销"
  用户当前轮: "生成开业海报"
  → 结合上下文，匹配餐饮+海报设计
```

#### 4. 渐进式加载决策

```
Claude决策树:
┌─────────────────────────────────────┐
│ 发现相关Skill                       │
│ (text-to-image)                     │
└──────────────┬──────────────────────┘
               │
               ▼
        [是否需要详细API信息?]
               │
       ┌───────┴───────┐
       │ 是            │ 否
       ▼               ▼
 读取reference.md   只用SKILL.md
 (~2000 tokens)     (~500 tokens)
       │               │
       └───────┬───────┘
               ▼
        [组合智能体知识]
               │
               ▼
        [生成执行代码]
```

**加载Level 2的场景**:
- ❌ 简单任务: "生成海报" → 只需SKILL.md的快速示例
- ✅ 复杂任务: "生成3种尺寸的海报，要求300 DPI" → 需要reference.md的参数详解
- ✅ 错误排查: API调用失败 → 需要reference.md的错误处理说明
- ✅ 参数优化: 用户要求调整细节 → 需要reference.md的完整参数列表

---

## 完整执行示例

### 示例1: 简单文生图任务

**用户请求**: "生成一张咖啡店Logo"

**执行流程**:

```python
# 步骤1: Claude发现text-to-image Skill
# 步骤2: 读取SKILL.md (Level 1)
# 步骤3: 读取智能体文档理解Logo设计规范
# 步骤4: 生成代码并执行

import sys
sys.path.append('./api/projects/nano-banana-api')
from banana_all_in_one import NanoBananaAPI

api = NanoBananaAPI()
result = api.generate_text_to_image(
    prompt="Modern coffee shop logo with artisanal elements, minimalist design, warm brown tones",
    design_type="6-icon"  # Logo类型
)

if result["success"]:
    print(f"✅ Logo生成成功: {result['image_paths'][0]}")
    # output/images/e1-text-to-image/text_to_image_20251020_103000_1.png
```

**输出**:
- `output/images/e1-text-to-image/text_to_image_20251020_103000_1.png` - 1:1正方形Logo
- `output/prompts/e1-text-to-image/text_to_image_20251020_103000_prompt.json` - 提示词记录

---

### 示例2: 复杂图生图任务

**用户请求**: "这张菜品照片需要优化，增强色彩和光线"

**执行流程**:

```python
# 步骤1: Claude发现image-to-image Skill
# 步骤2: 读取SKILL.md + reference.md (需要详细参数)
# 步骤3: 读取V4智能体文档理解图片优化规范
# 步骤4: 生成代码并执行

import sys
sys.path.append('./.claude/skills/aigc/_shared')
from banana_api_core import NanoBananaAPI

api = NanoBananaAPI()
result = api.generate_image_to_image(
    prompt="Enhance food colors and lighting, improve appetite appeal",
    image_urls=["output/images/original_dish_photo.jpg"],
    processing_type="local_optimization"  # 局部优化类型
)

if result["success"]:
    print(f"✅ 图片优化完成: {result['image_paths'][0]}")
```

---

### 示例3: 综合分析任务

**用户请求**: "分析这张餐厅环境照片的质量，给出改进建议"

**执行流程**:

```python
# 步骤1: Claude发现image-recognition Skill
# 步骤2: 读取SKILL.md
# 步骤3: 读取V5智能体文档理解120+维度分析体系
# 步骤4: 生成代码并执行

import sys
sys.path.append('./.claude/skills/aigc/_shared')
from banana_api_core import NanoBananaAPI

api = NanoBananaAPI()
result = api.generate_image_recognition(
    image_url="output/images/restaurant_interior.jpg",
    analysis_type="comprehensive_analysis",  # 综合分析
    analysis_dimensions=[
        "lighting_quality",  # 光线质量
        "composition",       # 构图
        "color_harmony",     # 色彩和谐度
        "cleanliness",       # 环境整洁度
        "atmosphere"         # 氛围营造
    ]
)

if result["success"]:
    analysis = result["analysis_result"]
    print(f"📊 分析报告:")
    print(f"  整体评分: {analysis['overall_score']}/10")
    print(f"  光线质量: {analysis['lighting_quality']}")
    print(f"  改进建议: {analysis['improvement_suggestions']}")
```

---

### 示例4: JSON计划执行

**用户请求**: "我要批量生成10张不同菜品的主图"

**执行流程**:

```python
# 步骤1: Claude发现text-to-image Skill
# 步骤2: 读取智能体文档理解批量任务规范
# 步骤3: 生成JSON执行计划
# 步骤4: 使用plan_executor.py批量执行

# 生成执行计划
plan = {
    "agent_id": "E1",
    "task_description": "批量生成菜品主图摄影",
    "input_data": {
        "batch_tasks": [
            {
                "text_prompt": "Professional food photography of Kung Pao Chicken",
                "design_type": "8-main-image"
            },
            {
                "text_prompt": "Professional food photography of Mapo Tofu",
                "design_type": "8-main-image"
            },
            # ... 10个任务
        ]
    },
    "output_settings": {
        "save_path": "output/images/e1-text-to-image/batch/",
        "format": "png"
    }
}

# 保存计划
import json
with open("api/plans/e1-text-to-image/batch-dishes.json", "w") as f:
    json.dump(plan, f, indent=2, ensure_ascii=False)

# 执行计划
import subprocess
subprocess.run([
    "python",
    ".claude/skills/aigc/_shared/plan_executor.py",
    "--plan", "api/plans/e1-text-to-image/batch-dishes.json"
])
```

---

## 技术栈与文件组织

### 技术栈

```
┌─────────────────────────────────────────────┐
│          Claude Sonnet 4.5 (主控)          │
│  - 意图识别                                 │
│  - Skills发现                               │
│  - 代码生成                                 │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│         Skills系统 (知识库)                 │
│  - SKILL.md: 快速开始                       │
│  - reference.md: API参考                    │
│  - scripts/: 可执行脚本                     │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│    NanoBananaAPI (执行引擎)                 │
│  - Language: Python 3.10+                   │
│  - HTTP Client: requests                    │
│  - Data Model: pydantic                     │
│  - Config: python-dotenv                    │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│       OpenRouter API Gateway                │
│  - Endpoint: https://openrouter.ai/api/v1   │
│  - Model: google/gemini-2.5-flash-image-... │
│  - Auth: Bearer Token                       │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│      Google Gemini 2.5 Flash Image          │
│  - 多模态理解                               │
│  - 图像生成                                 │
│  - 图像分析                                 │
└─────────────────────────────────────────────┘
```

### 文件组织结构

```
项目根目录/
├── .claude/
│   ├── agents/
│   │   └── 创意组/
│   │       ├── V3-AIGC文生图设计师.md          # 规范层 - E1
│   │       ├── V4-AIGC图生图设计师.md          # 规范层 - E2
│   │       ├── V5-AIGC图片识别分析师.md        # 规范层 - E3
│   │       └── V6-AIGC高级图片处理师.md        # 规范层 - E4-E9
│   │
│   └── skills/
│       └── aigc/
│           ├── README.md                       # Skills总览
│           ├── ARCHITECTURE.md                 # 本文档
│           ├── INTEGRATION_SUMMARY.md          # 集成总结
│           │
│           ├── text-to-image/                  # E1 Skill
│           │   ├── SKILL.md                    # Level 1: 快速开始
│           │   ├── reference.md                # Level 2: API参考
│           │   └── scripts/                    # Level 3: 可执行代码
│           │       ├── banana_api_core.py → (符号链接)
│           │       └── plan_executor.py → (符号链接)
│           │
│           ├── image-to-image/                 # E2 Skill
│           │   ├── SKILL.md
│           │   └── scripts/
│           │
│           ├── image-recognition/              # E3 Skill
│           │   ├── SKILL.md
│           │   └── scripts/
│           │
│           └── advanced-processing/            # E4-E9 Skill
│               ├── SKILL.md
│               └── scripts/
│
├── .claude/
│   └── skills/
│       └── aigc/
│           └── _shared/                        # 执行层 - 统一API
│               ├── banana_api_core.py          # 核心API客户端
│               ├── plan_executor.py            # 通用执行器
│               ├── models/
│               │   └── execution_plan.py       # 数据模型
│               └── tests/
│                   └── test_plan_executor.py   # 测试脚本
│
├── api/
│   └── plans/                                  # 计划层 - JSON执行计划
│       ├── e1-text-to-image/
│       │   ├── template.json                   # 执行计划模板
│       │   ├── task-001-poster.json            # 海报任务
│       │   ├── task-002-menu.json              # 菜单任务
│       │   └── ...
│       ├── e2-image-to-image/
│       ├── e3-image-recognition/
│       └── e4-e9-*/
│
├── library/
│   └── prompts/                                # 餐饮专业语料库
│       ├── aesthetic-principles.json           # 美学原理
│       ├── color-theory.json                   # 色彩理论
│       ├── design-masters.json                 # 设计大师
│       └── ...
│
└── output/                                     # 输出目录
    ├── images/
    │   ├── e1-text-to-image/                   # E1生成的图片
    │   ├── e2-image-to-image/                  # E2处理的图片
    │   └── ...
    └── prompts/
        ├── e1-text-to-image/                   # E1提示词记录
        └── ...
```

---

## 总结

### 核心设计原则

1. **职责分离**
   - 智能体文档 → 业务逻辑和领域知识
   - Skills文档 → 技术实现和API调用
   - 执行计划 → 任务配置和参数
   - API客户端 → 统一执行引擎

2. **渐进式披露**
   - Level 1 (SKILL.md) → 快速开始，最小化上下文
   - Level 2 (reference.md) → 详细文档，按需加载
   - Level 3 (scripts/) → 可执行代码，不占用上下文

3. **自动发现机制**
   - YAML frontmatter → 元数据标识
   - description关键词 → 语义匹配
   - Claude智能路由 → 无需手动指定

4. **配置与代码分离**
   - JSON执行计划 → 可复用、可版本控制
   - Python API客户端 → 稳定、统一接口
   - execute_plan.py → 通用执行器

### 关键优势

- ✅ **低上下文消耗** - 渐进式加载，只读取必要信息
- ✅ **高可维护性** - 清晰的职责分离和模块化设计
- ✅ **强可扩展性** - 新增智能体只需添加对应Skill
- ✅ **智能路由** - Claude自动发现，无需手动配置
- ✅ **统一执行** - E1-E9共享执行引擎，代码复用
- ✅ **任务追溯** - JSON计划可版本控制和审计

---

**文档版本**: v1.0.0
**最后更新**: 2025-10-20
**维护者**: ZTL数智化作战中心
**参考规范**: Anthropic Agent Skills Design (2025)
