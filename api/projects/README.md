# FastAPI子项目集合

> **API服务架构的核心**: 存储所有独立的FastAPI应用项目,每个项目提供特定的API服务能力,形成模块化的API生态系统。

## 📋 目录说明

本目录包含ZTL餐饮数智化平台的所有FastAPI子项目,每个项目都是独立可运行的API服务,具有完整的配置、文档和测试体系。

## 🎯 核心理念

**模块化API架构,独立部署,统一管理**
- ✅ 独立服务: 每个项目独立运行,互不干扰
- ✅ 标准化: 所有项目遵循统一的FastAPI开发规范
- ✅ 可扩展: 新增API服务只需创建新的子项目
- ✅ 易维护: 每个项目有独立的依赖和配置管理
- ✅ 清晰职责: 每个项目专注于特定的业务领域

## 📂 目录结构

```
api/projects/
├── figma-rest-api/         # Figma REST API项目
│   ├── app/                # FastAPI应用代码
│   │   ├── api/v1/         # API端点
│   │   ├── core/           # 核心业务逻辑
│   │   └── tests/          # 项目测试
│   ├── requirements.txt    # 项目依赖
│   ├── .env.example        # 环境变量示例
│   └── README.md           # 项目文档
│
├── nano-banana-api/        # NanoBanana AI API项目
│   ├── execute_plan.py     # E系列智能体统一执行器
│   ├── main.py             # FastAPI主入口
│   └── requirements.txt    # 项目依赖
│
└── README.md               # 本文档
```

## 🚀 子项目概览

### 1. Figma REST API (figma-rest-api/)

**项目定位**: Figma设计工具集成服务
**核心功能**:
- Figma文件管理(读取、解析、版本控制)
- 设计元素批量导出(SVG、PNG、JPG)
- 图片批量替换与自动化处理
- 腾讯云COS存储集成
- 完整的API文档和测试用例

**技术栈**:
- FastAPI + Uvicorn
- Figma REST API SDK
- 腾讯云COS SDK
- Pydantic数据验证

**快速启动**:
```bash
cd api/projects/figma-rest-api
pip install -r requirements.txt
cp .env.example .env  # 配置Figma Access Token和COS凭证
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

**API文档**: http://localhost:8001/docs (启动服务后访问)

**详细文档**: 查看 [figma-rest-api/README.md](./figma-rest-api/README.md)

### 2. NanoBanana AI API (nano-banana-api/)

**项目定位**: AIGC智能体执行引擎
**核心功能**:
- E系列智能体(E1-E9)统一执行器
- JSON执行计划解析与路由
- OpenRouter AI服务调用
- 图片生成、处理、识别等AIGC任务
- 任务结果存储与状态管理

**技术栈**:
- FastAPI + Uvicorn
- OpenRouter API SDK
- Pydantic数据验证
- JSON配置驱动

**快速启动**:
```bash
cd api/projects/nano-banana-api
pip install -r requirements.txt
# 配置OpenRouter API密钥
uvicorn main:app --reload --host 0.0.0.0 --port 8002
```

**执行器使用**:
```bash
# 执行E系列智能体任务计划
python execute_plan.py --plan ../../plans/e1-text-to-image/my-task.json
```

**API文档**: http://localhost:8002/docs (启动服务后访问)

## 🔄 项目间协作

### 工作流集成示例

**场景1: Figma批量替换 + AI图片生成**
```bash
# Step 1: 使用E1智能体生成图片
python api/projects/nano-banana-api/execute_plan.py \
  --plan api/plans/e1-text-to-image/hotpot-images.json

# Step 2: 使用Figma API批量替换到模板
curl -X POST http://localhost:8001/api/v1/figma/batch-replace \
  -H "Content-Type: application/json" \
  -d @api/plans/figma-batch-replace-config.json
```

**场景2: Figma导出 + AI图片增强**
```bash
# Step 1: 从Figma导出图片
curl -X GET http://localhost:8001/api/v1/figma/export?file_id=xxx&node_id=xxx

# Step 2: 使用E9智能体超分增强
python api/projects/nano-banana-api/execute_plan.py \
  --plan api/plans/e9-super-resolution/enhance-exported.json
```

## 📋 开发规范

### 项目创建规范

**1. 目录结构**:
```
new-project-api/
├── app/
│   ├── api/v1/endpoints/   # API端点实现
│   ├── core/               # 核心业务逻辑
│   │   ├── models/         # 数据模型
│   │   ├── schemas/        # Pydantic模式
│   │   └── services/       # 业务服务
│   ├── main.py             # FastAPI应用入口
│   └── config.py           # 配置管理
├── tests/                  # 测试用例
├── requirements.txt        # 项目依赖
├── .env.example            # 环境变量示例
└── README.md               # 项目文档
```

**2. 必备文件**:
- `requirements.txt`: 项目依赖清单
- `.env.example`: 环境变量模板
- `README.md`: 项目说明文档
  - 项目定位和核心功能
  - 快速启动指南
  - API端点说明
  - 配置说明

**3. 代码规范**:
- 遵循PEP8代码规范
- 使用类型提示(Type Hints)
- 编写Google风格的docstring
- 使用black进行代码格式化

### 端口分配规范

| 项目 | 端口 | 用途 |
|------|------|------|
| figma-rest-api | 8001 | Figma设计工具集成 |
| nano-banana-api | 8002 | AIGC智能体执行引擎 |
| [预留] | 8003+ | 未来新增项目 |

### 环境变量管理

**原则**: 所有敏感配置通过环境变量管理,不得提交到Git

**标准模式**:
1. 创建`.env.example`模板文件(提交到Git)
2. 本地复制为`.env`文件(添加到.gitignore)
3. 在`.env`文件中填写实际凭证

**示例**:
```bash
# .env.example (模板)
FIGMA_ACCESS_TOKEN=your_figma_token_here
COS_SECRET_ID=your_cos_secret_id_here
OPENROUTER_API_KEY=your_openrouter_key_here

# .env (实际配置,不提交)
FIGMA_ACCESS_TOKEN=figd_xxxxxxxxxxx
COS_SECRET_ID=AKIDxxxxxxxxxxx
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxx
```

## 🔧 常用操作

### 启动所有服务

**方式1: 手动启动**
```bash
# 终端1: 启动Figma REST API
cd api/projects/figma-rest-api && uvicorn app.main:app --reload --port 8001

# 终端2: 启动NanoBanana AI API
cd api/projects/nano-banana-api && uvicorn main:app --reload --port 8002
```

**方式2: 并行启动(未来实现)**
```bash
# 使用docker-compose统一管理
docker-compose up -d
```

### 依赖管理

**安装所有项目依赖**:
```bash
# Figma REST API
pip install -r api/projects/figma-rest-api/requirements.txt

# NanoBanana AI API
pip install -r api/projects/nano-banana-api/requirements.txt
```

**更新依赖清单**:
```bash
cd api/projects/{project-name}
pip freeze > requirements.txt
```

### 测试运行

**单元测试**:
```bash
cd api/projects/figma-rest-api
pytest app/tests/
```

**API集成测试**:
```bash
# 启动服务后访问
curl http://localhost:8001/health
curl http://localhost:8002/health
```

## 📚 相关文档

### 项目文档
- [figma-rest-api/README.md](./figma-rest-api/README.md) - Figma API完整文档
- [figma-rest-api/SETUP_GUIDE.md](./figma-rest-api/SETUP_GUIDE.md) - 配置指南
- [figma-rest-api/COMPLETE_API_OVERVIEW.md](./figma-rest-api/COMPLETE_API_OVERVIEW.md) - API概览

### 架构文档
- [api/README.md](../README.md) - API服务架构总览
- [api/plans/README.md](../plans/README.md) - JSON执行计划规范
- [.claude/CLAUDE.md](../../.claude/CLAUDE.md) - E系列智能体三层架构

## 🔮 扩展指南

### 添加新的API项目

**步骤1: 创建项目目录**
```bash
mkdir -p api/projects/new-project-api/app/api/v1/endpoints
mkdir -p api/projects/new-project-api/app/core/{models,schemas,services}
mkdir -p api/projects/new-project-api/tests
```

**步骤2: 创建必备文件**
```bash
# FastAPI入口
touch api/projects/new-project-api/app/main.py

# 配置文件
touch api/projects/new-project-api/app/config.py

# 依赖清单
touch api/projects/new-project-api/requirements.txt

# 环境变量模板
touch api/projects/new-project-api/.env.example

# 项目文档
touch api/projects/new-project-api/README.md
```

**步骤3: 编写FastAPI应用**
```python
# app/main.py
from fastapi import FastAPI

app = FastAPI(
    title="New Project API",
    description="New API service description",
    version="1.0.0"
)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# 导入API路由
# from app.api.v1 import router
# app.include_router(router, prefix="/api/v1")
```

**步骤4: 更新本README**
- 在"子项目概览"章节添加新项目说明
- 在"端口分配规范"表格添加端口号
- 更新目录结构图

**步骤5: 测试与文档**
```bash
# 启动服务测试
cd api/projects/new-project-api
uvicorn app.main:app --reload --port 8003

# 访问API文档
curl http://localhost:8003/docs
```

## 💡 最佳实践

### 项目独立性
- 每个项目应能独立运行,不依赖其他项目
- 共享逻辑应提取到`api/shared/`目录
- 避免项目间的硬依赖

### API版本管理
- 使用`/api/v1/`前缀进行版本控制
- 重大变更时创建新版本(v2, v3...)
- 保持旧版本向后兼容

### 文档完整性
- 每个项目必须有README.md
- 使用FastAPI自动生成的OpenAPI文档
- 提供完整的配置说明和示例

### 错误处理
- 统一错误响应格式
- 提供清晰的错误信息和错误码
- 记录详细的错误日志

---

**文档版本**: v1.0.0
**创建日期**: 2025-10-11
**最后更新**: 2025-10-11
**维护标准**: 遵循FastAPI最佳实践和项目规范
