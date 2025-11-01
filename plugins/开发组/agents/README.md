# 开发组智能体 (Development Agents)

> 全栈开发、架构设计、质量保障的专业智能体团队

[![Agents](https://img.shields.io/badge/agents-19-blue)]()
[![Status](https://img.shields.io/badge/status-active-green)]()
[![Updated](https://img.shields.io/badge/updated-2025--11--01-brightgreen)]()

## 📋 Overview

开发组负责数智化协作平台的全栈开发、架构设计、质量保障和系统优化。团队包含产品经理、前后端开发、架构师、测试工程师等19个专业智能体,覆盖完整的软件开发生命周期。

**Total: 19 agents**

## 🗂️ Organizational Structure

### 产品与设计 (Product & Design)
- **F0-产品经理**: 需求分析、产品规划、用户故事
- **F2-UI设计师**: UI/UX设计、交互设计

### 前端开发 (Frontend Development)
- **F1-前端开发**: Next.js 16 + React + TypeScript
- **F11-TypeScript专家**: TypeScript深度优化
- **F12-JavaScript专家**: Modern JavaScript (ES2024+)

### 后端开发 (Backend Development)
- **F5-后端架构师**: FastAPI + Supabase后端架构
- **F6-数据库架构师**: PostgreSQL数据库设计
- **F10-Python专家**: Python后端深度优化

### 全栈与架构 (Full-Stack & Architecture)
- **F3-全栈开发**: 端到端全栈开发
- **F8-云架构师**: 腾讯云基础设施
- **F9-架构评审**: 架构审查与优化

### 质量保障 (Quality Assurance)
- **F13-代码审查专家**: 代码质量审查
- **F14-测试工程师**: 测试自动化
- **F15-性能优化专家**: 性能优化与监控
- **F16-调试专家**: 系统级调试
- **F17-错误侦探**: 错误分析与诊断

### 文档与协作 (Documentation & Collaboration)
- **F4-文档报告生成**: 技术文档生成
- **F7-API文档生成**: API文档自动化

### 团队管理 (Team Management)
- **FF-开发组组长**: 团队协调与项目管理

## 🤖 Detailed Agent Documentation

### F0-产品经理 (Product Manager)

**Description**: 产品经理专家,负责需求分析、产品规划、用户故事编写、功能优先级排序和产品路线图制定。深谙数智化协作平台产品特性和技术栈(Next.js 16+Supabase+FastAPI)约束。主动用于需求澄清、PRD文档编写、用户体验优化和产品决策。

**When to use**:
- 需求分析和澄清
- 产品规划和路线图制定
- 用户故事和PRD编写
- 功能优先级排序

**Invocation**:
```python
Task(subagent_type="F0-产品经理",
     prompt="分析这个功能需求并编写PRD文档")
```

---

### F1-前端开发 (Frontend Developer)

**Description**: Frontend development expert specialized in Next.js 16 App Router, Supabase integration, React Server Components, and responsive design for digital intelligence platforms. Masters state management, performance optimization, and mobile-first development.

**When to use**:
- Next.js 16 App Router开发
- React组件开发
- 响应式设计实现
- 前端性能优化

**Invocation**:
```python
Task(subagent_type="F1-前端开发",
     prompt="实现任务管理页面的前端组件")
```

---

### F2-UI设计师 (UI Designer)

**Description**: UI/UX design specialist for digital intelligence platforms, focusing on user-centered design and interaction patterns.

**When to use**:
- UI/UX设计
- 交互设计
- 视觉设计优化
- 用户体验改进

**Invocation**:
```python
Task(subagent_type="F2-UI设计师",
     prompt="设计任务管理界面的交互流程")
```

---

### F3-全栈开发 (Full-Stack Developer)

**Description**: Full-stack development expert for digital intelligence collaboration platforms, mastering Next.js 16 App Router + FastAPI + Supabase architecture, end-to-end development, API integration, and complete feature delivery.

**When to use**:
- 端到端功能开发
- 前后端集成
- 完整功能交付
- 全栈架构设计

**Invocation**:
```python
Task(subagent_type="F3-全栈开发",
     prompt="实现完整的用户认证功能")
```

---

### F4-文档报告生成 (Documentation Generator)

**Description**: Technical documentation and report generation specialist for digital intelligence collaboration platforms. Creates technical docs, API documentation, user guides, architecture diagrams, and data analysis reports.

**When to use**:
- 技术文档编写
- API文档生成
- 用户手册制作
- 数据分析报告

**Invocation**:
```python
Task(subagent_type="F4-文档报告生成",
     prompt="生成系统架构文档")
```

---

### F5-后端架构师 (Backend Architect)

**Description**: Backend architecture specialist for digital intelligence collaboration platform using FastAPI + Supabase. Expert in RESTful API design, authentication, real-time updates, and scalable architecture patterns.

**When to use**:
- 后端架构设计
- API设计与实现
- 数据库集成
- 性能优化

**Invocation**:
```python
Task(subagent_type="F5-后端架构师",
     prompt="设计任务管理API架构")
```

---

### F6-数据库架构师 (Database Architect)

**Description**: Supabase PostgreSQL database architect for digital intelligence collaboration platform. Expert in multi-tenant data modeling, RLS policies, real-time subscriptions, and query optimization.

**When to use**:
- 数据库设计
- 数据模型优化
- RLS策略配置
- 查询性能优化

**Invocation**:
```python
Task(subagent_type="F6-数据库架构师",
     prompt="设计多租户数据模型")
```

---

### F7-API文档生成 (API Documentation)

**Description**: API documentation specialist for digital intelligence collaboration platform. Specializes in FastAPI OpenAPI schema generation, interactive API documentation, SDK generation, and API versioning.

**When to use**:
- API文档自动化
- OpenAPI规范生成
- SDK文档编写
- API版本管理

**Invocation**:
```python
Task(subagent_type="F7-API文档生成",
     prompt="生成FastAPI的OpenAPI文档")
```

---

### F8-云架构师 (Cloud Architect)

**Description**: Tencent Cloud infrastructure specialist for digital intelligence collaboration platform. Specializes in COS storage, CDN, cloud functions, monitoring, and cost optimization.

**When to use**:
- 云基础设施设计
- COS存储配置
- CDN加速优化
- 云监控部署

**Invocation**:
```python
Task(subagent_type="F8-云架构师",
     prompt="设计文件存储方案")
```

---

### F9-架构评审 (Architecture Reviewer)

**Description**: Architecture reviewer for digital intelligence collaboration platform. Reviews code changes through architectural lens, evaluates design patterns, ensures scalability, and validates technical decisions.

**When to use**:
- 架构审查
- 设计模式评估
- 可扩展性验证
- 技术决策审核

**Invocation**:
```python
Task(subagent_type="F9-架构评审",
     prompt="审查这个架构设计方案")
```

---

### F10-Python专家 (Python Expert)

**Description**: FastAPI backend specialist with Pydantic V2, AsyncIO, and Supabase integration. Implements digital intelligence platform APIs, optimizes async performance, and ensures type safety.

**When to use**:
- Python深度优化
- FastAPI开发
- 异步编程
- 类型安全增强

**Invocation**:
```python
Task(subagent_type="F10-Python专家",
     prompt="优化这段Python异步代码")
```

---

### F11-TypeScript专家 (TypeScript Expert)

**Description**: Next.js 16 + React + TypeScript expert for multi-agent collaboration platforms. Masters App Router, Server Components, type-safe API integration, and advanced TypeScript patterns.

**When to use**:
- TypeScript深度优化
- 类型系统设计
- Next.js类型安全
- 复杂类型推导

**Invocation**:
```python
Task(subagent_type="F11-TypeScript专家",
     prompt="优化组件的类型定义")
```

---

### F12-JavaScript专家 (JavaScript Expert)

**Description**: Modern JavaScript (ES2024+) expert with deep browser API knowledge. Masters async patterns, functional programming, performance optimization, and cross-browser compatibility.

**When to use**:
- 现代JavaScript优化
- 浏览器API应用
- 性能调优
- 跨浏览器兼容

**Invocation**:
```python
Task(subagent_type="F12-JavaScript专家",
     prompt="优化这段JavaScript性能")
```

---

### F13-代码审查专家 (Code Reviewer)

**Description**: Senior code review specialist for quality, security, and maintainability. Expert in SOLID principles, design patterns, security best practices, and technical debt management.

**When to use**:
- 代码质量审查
- 安全漏洞检测
- 设计模式评估
- 技术债务分析

**Invocation**:
```python
Task(subagent_type="F13-代码审查专家",
     prompt="审查这段代码的质量和安全性")
```

---

### F14-测试工程师 (Test Engineer)

**Description**: Test automation and quality assurance specialist. Use PROACTIVELY for test strategy, test automation implementation, coverage analysis, and quality metrics tracking.

**When to use**:
- 测试策略制定
- 测试自动化
- 覆盖率分析
- 质量度量

**Invocation**:
```python
Task(subagent_type="F14-测试工程师",
     prompt="为这个功能编写测试用例")
```

---

### F15-性能优化专家 (Performance Optimizer)

**Description**: Performance optimization specialist for web applications. Expert in Core Web Vitals, bundle optimization, caching strategies, and real-user monitoring.

**When to use**:
- 性能优化
- Core Web Vitals改进
- Bundle优化
- 缓存策略设计

**Invocation**:
```python
Task(subagent_type="F15-性能优化专家",
     prompt="优化页面加载性能")
```

---

### F16-调试专家 (Debugging Expert)

**Description**: System-level debugging and problem diagnosis expert. Use PROACTIVELY for debugging complex issues, analyzing stack traces, reproducing bugs, and root cause analysis.

**When to use**:
- 系统级调试
- 问题诊断
- Bug重现
- 根因分析

**Invocation**:
```python
Task(subagent_type="F16-调试专家",
     prompt="调试这个复杂的系统问题")
```

---

### F17-错误侦探 (Error Detective)

**Description**: Error analysis and root cause diagnosis expert. Use PROACTIVELY for error pattern detection, log analysis, crash investigation, and preventive error handling strategies.

**When to use**:
- 错误模式分析
- 日志分析
- 崩溃调查
- 错误预防策略

**Invocation**:
```python
Task(subagent_type="F17-错误侦探",
     prompt="分析这些错误日志的模式")
```

---

### FF-开发组组长 (Development Team Leader)

**Description**: 开发组组长,负责统筹协调开发组全部智能体(F0-F17),制定开发计划,分配任务,质量把控,进度管理和团队协作。主动用于复杂开发项目、多智能体协作和全流程开发管理。

**When to use**:
- 复杂开发项目协调
- 多智能体任务分配
- 开发进度管理
- 质量把控

**Invocation**:
```python
Task(subagent_type="FF-开发组组长",
     prompt="协调团队完成这个复杂功能")
```

---

## 🚀 Usage Guide

### Auto-Delegation

Claude会根据任务类型自动委派给合适的智能体:

```
User: "实现用户登录功能"
→ Claude识别为全栈开发任务
→ 自动委派给F3-全栈开发
```

### Explicit Invocation

对于复杂任务,可以显式调用特定智能体:

```python
# 产品需求分析
Task(subagent_type="F0-产品经理",
     prompt="分析用户认证需求并编写PRD")

# 前端开发
Task(subagent_type="F1-前端开发",
     prompt="实现登录页面UI组件")

# 后端API
Task(subagent_type="F5-后端架构师",
     prompt="设计认证API架构")

# 质量保障
Task(subagent_type="F14-测试工程师",
     prompt="编写认证功能测试用例")
```

### Team Coordination

使用组长协调复杂项目:

```python
Task(subagent_type="FF-开发组组长",
     prompt="协调团队实现完整的任务管理系统,包括前端、后端、数据库、测试")
```

## 🎯 Best Practices

1. **选择合适的智能体**: 根据任务性质选择最匹配的专业智能体
2. **利用自动委派**: 简单任务让Claude自动分配,提高效率
3. **显式调用专家**: 复杂任务显式调用专业智能体,确保质量
4. **团队协作**: 大型项目使用组长协调多个智能体
5. **质量优先**: 开发完成后主动调用测试、审查、调试智能体
6. **文档同步**: 功能完成后使用文档智能体生成文档

## 🔗 Related Resources

- [开发组 Plugin README](../README.md) - 开发组插件总览
- [项目主 README](../../../README.md) - 项目完整文档
- [Global CLAUDE.md](../../../CLAUDE.md) - 全局配置规范

---

**Last Updated**: 2025-11-01
**Maintained by**: ZTL Digital Intelligence Operations Center
**Status**: ✅ Active (19 agents)
