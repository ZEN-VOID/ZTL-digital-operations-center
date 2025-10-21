# API Scripts

> 提供API服务启动、管理和运维工具脚本，支持多服务统一启动和健康检查。

## 📋 目录概述

API脚本工具目录，包含用于启动、管理和监控API服务的实用脚本。

## 📁 目录结构

```
api/scripts/
└── start_all.py    # 统一启动所有API服务
```

## 🎯 核心脚本

### start_all.py - 统一服务启动器

**功能描述**:
- 一键启动所有API项目服务
- 并行启动多个FastAPI应用
- 自动端口分配和冲突检测
- 健康检查和启动验证

**使用方法**:
```bash
# 启动所有API服务
python api/scripts/start_all.py

# 指定端口范围启动
python api/scripts/start_all.py --start-port 8000

# 调试模式启动
python api/scripts/start_all.py --debug
```

**支持的API项目**:
- `nano-banana-api`: E系列智能体统一执行器 (默认端口: 8001)
- `figma-rest-api`: Figma API服务 (默认端口: 8002)
- 其他API项目按需添加

**启动流程**:
```yaml
步骤1 - 扫描API项目:
  - 检查api/projects/目录下的所有项目
  - 识别包含main.py或app.py的FastAPI项目

步骤2 - 端口分配:
  - 根据配置或自动分配端口
  - 检测端口占用情况
  - 避免端口冲突

步骤3 - 并行启动:
  - 使用uvicorn启动FastAPI应用
  - 后台进程模式运行
  - 记录启动日志

步骤4 - 健康检查:
  - 检查服务是否成功启动
  - 验证健康检查端点
  - 输出启动状态报告
```

## 📝 使用场景

**开发环境**:
- 本地开发时一键启动所有依赖的API服务
- 快速重启服务进行调试
- 验证多服务协作场景

**测试环境**:
- 集成测试前统一启动服务
- 确保所有API服务正常运行
- 模拟生产环境的服务部署

**部署准备**:
- 验证服务启动脚本
- 检查端口配置
- 测试服务依赖关系

## 🔧 配置管理

### 环境变量

```bash
# .env文件配置示例
API_HOST=0.0.0.0
API_START_PORT=8000
API_RELOAD=true
LOG_LEVEL=info
```

### 服务配置

在`start_all.py`中配置各API项目:
```python
SERVICES = [
    {
        "name": "nano-banana-api",
        "path": "api/projects/nano-banana-api",
        "port": 8001,
        "module": "main:app"
    },
    {
        "name": "figma-rest-api",
        "path": "api/projects/figma-rest-api",
        "port": 8002,
        "module": "app:app"
    }
]
```

## 🚀 最佳实践

**启动前检查**:
- 确保所有依赖已安装 (`pip install -r requirements.txt`)
- 检查.env配置文件是否存在
- 验证端口是否被占用

**日志管理**:
- 启动日志保存在logs/api/目录
- 定期清理过期日志
- 使用日志轮转避免文件过大

**性能优化**:
- 开发环境使用`--reload`热重载
- 生产环境禁用reload提升性能
- 根据负载调整worker数量

**错误处理**:
- 启动失败时自动清理进程
- 记录详细错误信息
- 提供重试机制

## 🔗 相关文档

- [NanoBanana API文档](../projects/nano-banana-api/README.md)
- [Figma REST API文档](../projects/figma-rest-api/README.md)
- [API架构规范](../../.claude/agents/F7.md)

---

**脚本版本**: v1.0.0
**创建日期**: 2025-09-28
**Python版本**: 3.10+
**依赖框架**: uvicorn, FastAPI
