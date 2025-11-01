# Commands - 开发组斜杠命令

本目录包含**6个专业命令**,提供Next.js和Supabase快速开发工具链。

## 📋 命令列表

### Next.js工具链 (4个)

| 命令 | 描述 | 使用场景 |
|------|------|----------|
| `/nextjs-scaffold` | Next.js项目脚手架生成器 | 创建新的Next.js项目,配置TypeScript、Tailwind CSS、ESLint |
| `/nextjs-component-generator` | React组件生成器 | 快速创建React组件、Hooks、TypeScript接口 |
| `/nextjs-api-tester` | Next.js API路由测试工具 | 测试API端点、验证请求/响应、调试API逻辑 |
| `/nextjs-performance-audit` | Next.js性能审计工具 | 分析包大小、检测性能瓶颈、优化建议 |

### Supabase工具链 (2个)

| 命令 | 描述 | 使用场景 |
|------|------|----------|
| `/supabase-data-explorer` | Supabase数据浏览器 | 查询数据库、管理表结构、执行SQL |
| `/supabase-performance-optimizer` | Supabase性能优化器 | 分析查询性能、优化索引、数据库调优 |

## 🚀 使用指南

### 命令格式

所有命令遵循标准格式:

```markdown
---
description: 命令描述
argument-hint: [可选参数]
allowed-tools: ["Tool1", "Tool2"]
---

# 命令内容
[提示词内容]
```

### 调用方式

在Claude Code中直接输入斜杠命令:

```
用户: /nextjs-scaffold my-app
→ 生成新的Next.js项目脚手架

用户: /nextjs-component-generator Button
→ 创建Button组件及相关文件

用户: /supabase-data-explorer users
→ 浏览users表数据
```

## 📚 详细文档

### Next.js工具链

#### `/nextjs-scaffold`
**功能**: 创建Next.js项目脚手架
**输出**:
- 完整的Next.js 14+ 项目结构
- TypeScript配置
- Tailwind CSS集成
- ESLint + Prettier配置
- 推荐的目录结构 (app/, components/, lib/)

**使用示例**:
```
/nextjs-scaffold my-restaurant-app
```

#### `/nextjs-component-generator`
**功能**: 生成React组件及相关文件
**输出**:
- 组件文件 (.tsx)
- 样式文件 (可选)
- 测试文件 (可选)
- TypeScript类型定义

**使用示例**:
```
/nextjs-component-generator RestaurantCard --with-tests
```

#### `/nextjs-api-tester`
**功能**: 测试Next.js API路由
**输出**:
- API测试报告
- 请求/响应示例
- 错误诊断建议

**使用示例**:
```
/nextjs-api-tester /api/restaurants
```

#### `/nextjs-performance-audit`
**功能**: 分析Next.js应用性能
**输出**:
- 包大小分析
- 组件渲染性能
- 图片优化建议
- 代码分割建议

**使用示例**:
```
/nextjs-performance-audit
```

### Supabase工具链

#### `/supabase-data-explorer`
**功能**: 浏览和管理Supabase数据
**输出**:
- 表结构信息
- 数据查询结果
- 关系图谱
- SQL执行记录

**使用示例**:
```
/supabase-data-explorer restaurants
```

#### `/supabase-performance-optimizer`
**功能**: 优化Supabase数据库性能
**输出**:
- 慢查询分析
- 索引优化建议
- 查询重写建议
- 性能基准测试

**使用示例**:
```
/supabase-performance-optimizer
```

## 🛠️ 开发新命令

### 命令文件结构

```markdown
---
description: 简短的命令描述
argument-hint: [参数1] [参数2] (可选)
allowed-tools: ["Read", "Write", "Bash"]
---

# 命令名称

## 功能说明
[描述命令的具体功能]

## 使用方法
[详细的使用说明]

## 示例
[实际使用示例]

[命令执行的提示词内容]
```

### 最佳实践

1. **清晰的描述**: description字段要简洁明了
2. **参数提示**: argument-hint提供清晰的参数说明
3. **工具限制**: allowed-tools只包含必需的工具
4. **实用性**: 命令应解决实际开发问题
5. **文档完整**: 提供充分的使用示例

## 🔗 相关资源

- **命令模板**: 参考`.claude/skills/元skills/commands/`
- **智能体**: 配合智能体使用,如F1-前端开发、F5-后端架构师
- **技能包**: 与技能包组合,如webapp-testing
- **主文档**: 返回[开发组主README](../README.md)

## 📊 命令统计

- **总命令数**: 6个
- **Next.js工具**: 4个
- **Supabase工具**: 2个
- **平均使用频率**: 高频工具(脚手架、组件生成)
- **维护状态**: 活跃维护

---

**提示**: 命令是一次性操作的快捷方式。对于复杂的多步骤工作流,建议使用技能包或智能体。
