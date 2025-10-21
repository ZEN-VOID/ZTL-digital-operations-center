# API服务架构

## 📋 目录概述
API服务架构是ZTL餐饮数智化平面设计工作台的核心服务层，提供完整的API网关、项目特定服务、共享组件等企业级API解决方案。

## 📁 目录结构

```text
api/
├── 📁 plans/                       # E系列智能体JSON执行计划 (E1-E9)
│   ├── 📁 e1-text-to-image/       # E1文生图智能体计划
│   ├── 📁 e2-image-to-image/      # E2图生图智能体计划
│   ├── 📁 e3-image-recognition/   # E3图片识别智能体计划
│   ├── 📁 e4-smart-repair/        # E4智能修复智能体计划
│   ├── 📁 e5-structure-control/   # E5结构控制智能体计划
│   ├── 📁 e6-creative-combination/ # E6多图融合智能体计划
│   ├── 📁 e7-character-consistency/ # E7角色一致性智能体计划
│   ├── 📁 e8-design-iteration/    # E8设计迭代智能体计划
│   └── 📁 e9-super-resolution/    # E9超分增强智能体计划
├── 📁 projects/                    # 多个API项目的根目录
│   ├── 📁 figma-rest-api/         # Figma REST API项目 - 设计工具集成
│   │   ├── 📁 app/
│   │   │   ├── 📁 api/v1/endpoints/  # API端点
│   │   │   ├── 📁 core/           # 核心业务逻辑
│   │   │   │   ├── 📁 models/     # 数据模型
│   │   │   │   ├── 📁 schemas/    # Pydantic模式
│   │   │   │   └── 📁 services/   # 业务服务
│   │   │   └── 📁 tests/          # 项目测试
│   │   ├── requirements.txt       # 项目依赖
│   │   ├── .env.example          # 环境变量示例
│   │   ├── README.md             # 项目说明文档
│   │   ├── SETUP_GUIDE.md        # 设置指南
│   │   └── COMPLETE_API_OVERVIEW.md  # 完整API概览
│   └── 📁 nano-banana-api/        # NanoBanana AI API项目 - AIGC服务
│       ├── execute_plan.py        # E系列智能体统一执行器
│       ├── main.py               # FastAPI主入口
│       └── requirements.txt       # 项目依赖
├── 📁 shared/                     # 共享组件 (规划中)
│   ├── 📁 middleware/             # 中间件
│   ├── 📁 utils/                  # 工具函数
│   ├── 📁 exceptions/             # 异常处理
│   └── 📁 models/                 # 共享模型
├── 📁 gateway/                    # API网关 (规划中)
├── 📁 scripts/                    # 管理脚本
├── 📁 docs/                       # 文档 (规划中)
├── 📁 tests/                      # 全局测试
├── requirements-shared.txt        # 共享依赖 (规划中)
└── docker-compose.yml            # Docker编排 (规划中)
```

## 🚀 快速开始

### 1. E系列智能体JSON执行计划使用

```bash
# 查看某个智能体的模板
cat plans/e1-text-to-image/template.json

# 基于模板创建任务
cp plans/e1-text-to-image/template.json \
   plans/e1-text-to-image/my-task.json

# 编辑任务配置 (修改 input_data 和 output_settings)
# 示例: 生成一张火锅店海报

# 执行任务计划
python projects/nano-banana-api/execute_plan.py \
  --plan plans/e1-text-to-image/my-task.json
```

### 2. 安装API项目依赖

```bash
# 安装Figma REST API依赖
pip install -r projects/figma-rest-api/requirements.txt

# 安装NanoBanana AI API依赖
pip install -r projects/nano-banana-api/requirements.txt
```

### 3. 配置环境

```bash
# Figma REST API配置
cp projects/figma-rest-api/.env.example projects/figma-rest-api/.env

# 编辑配置文件
# 根据需要修改Figma Access Token、腾讯云COS配置等
```

### 4. 启动服务

```bash
# 启动Figma REST API项目
cd projects/figma-rest-api
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

# 启动NanoBanana AI API项目
cd projects/nano-banana-api
uvicorn main:app --reload --host 0.0.0.0 --port 8002

# 访问API文档
# Figma API: http://localhost:8001/docs
# NanoBanana API: http://localhost:8002/docs
```

## 📐 E系列智能体三层架构

本项目基于**规范·计划·执行**三层架构实现E系列智能体(E1-E9)的标准化工作流:

```
规范层 (.claude/agents/E[X].md)
    ↓
计划层 (api/plans/e[x]-*/*.json)  ← plans/目录
    ↓
执行层 (api/projects/nano-banana-api/execute_plan.py)
```

**核心设计原则**:
- ✅ 配置与代码完全分离
- ✅ 标准化JSON格式 (5个顶层字段)
- ✅ 统一执行器 (单一入口点)
- ✅ 模板化与可复用性

**标准JSON格式**:
```json
{
  "agent_id": "E[X]",
  "task_description": "任务的自然语言描述",
  "input_data": { /* 智能体特定参数 */ },
  "output_settings": {
    "save_path": "output/images/e[x]-*/",
    "format": "png"
  },
  "metadata": {
    "created_at": "2025-10-11T10:30:00",
    "created_by": "用户名",
    "version": "1.0"
  }
}
```

详细架构文档参见: [E系列智能体三层架构](./.claude/CLAUDE.md#3-e系列智能体三层架构标准化流程)

---

## 📋 开发规范

### 目录结构规范

- **plans/**: E系列智能体JSON执行计划配置
- **projects/**: 存放独立的API项目
- **shared/**: 存放可复用的共享组件 (规划中)
- **gateway/**: API网关相关代码 (规划中)
- **scripts/**: 项目管理和部署脚本

### 代码规范

- 使用Python 3.11+
- 遵循PEP8代码规范
- 使用类型注解
- 编写完整的文档字符串 (Google风格)
- 使用black进行代码格式化

### API规范

- 使用FastAPI框架
- 遵循RESTful API设计原则
- 使用Pydantic进行数据验证
- 实现完整的错误处理和日志记录

## 🔧 扩展指南

### 添加新的API项目

1. 在 `projects/` 目录下创建新项目文件夹
2. 复制现有项目的基础结构
3. 修改项目配置和依赖
4. 更新 `docker-compose.yml` 添加新服务 (规划中)
5. 在 `scripts/start_all.py` 中注册新项目 (规划中)

### 扩展E系列智能体 (E10+)

1. 在 `.claude/agents/` 创建智能体文档 (规范层)
2. 在 `plans/` 创建新目录 (如e10-new-agent/)
3. 编写 `template.json` (基于标准5字段格式)
4. 在 `projects/nano-banana-api/execute_plan.py` 添加路由映射

## 📚 相关文档

### 核心文档

- [plans/README.md](./plans/README.md) - JSON执行计划详细规范
- [projects/README.md](./projects/README.md) - FastAPI子项目说明
- [projects/figma-rest-api/README.md](./projects/figma-rest-api/README.md) - Figma API完整文档
- [projects/nano-banana-api/README.md](./projects/nano-banana-api/README.md) - NanoBanana API文档

### 架构文档

- [E系列智能体三层架构](../.claude/CLAUDE.md#3-e系列智能体三层架构标准化流程) - 完整架构说明
- [开发物料管理规范](../.claude/CLAUDE.md#1-开发物料管理规范) - 目录组织规范

### API文档 (在线)

- Figma REST API: http://localhost:8001/docs (启动服务后访问)
- NanoBanana AI API: http://localhost:8002/docs (启动服务后访问)

---

**最后更新**: 2025-10-11
**文档版本**: v2.0.0
**维护者**: ZTL项目团队
