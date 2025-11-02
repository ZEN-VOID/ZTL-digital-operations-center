# [功能名称] PRP文档

**项目名称**: [项目名称]
**创建时间**: [YYYY-MM-DD]
**负责人**: F0-需求分析师
**PRP版本**: 开发组专属模板 v1.0

---

## 🎯 Goal / Why / What

### 目标 (Goal)
[一句话描述本功能要实现什么目标]

### 为什么 (Why)
[说明为什么需要这个功能，解决什么问题，带来什么价值]

### 是什么 (What)
[详细描述功能的范围和核心内容]

---

## 🔍 All Needed Context

### 1. 代码库深度分析

#### 1.1 现有模式识别
```
相关文件:
  - [文件路径:行号] - [模式描述]
  - [文件路径:行号] - [模式描述]

可复用代码:
  - [组件/函数名称] @ [文件路径]
    作用: [描述]
    复用方式: [如何复用]
```

#### 1.2 技术栈现状
```yaml
当前使用:
  - Next.js版本: [版本号]
  - Supabase配置: [配置详情]
  - 相关依赖: [npm包列表]

需要新增:
  - [新依赖1]
  - [新依赖2]
```

### 2. 外部研究与知识整合

#### 2.1 官方文档
- **Next.js 16文档**: [具体章节URL]
  - 关键要点: [摘要]
  - 最佳实践: [摘要]

- **Supabase文档**: [具体章节URL]
  - 关键要点: [摘要]
  - 最佳实践: [摘要]

#### 2.2 技术陷阱与注意事项
⚠️ **陷阱1**: [描述]
  - 原因: [说明]
  - 规避方法: [方案]

⚠️ **陷阱2**: [描述]
  - 原因: [说明]
  - 规避方法: [方案]

### 3. 用户需求澄清（如适用）

**原始需求**: [用户原始描述]

**澄清问题**:
- Q1: [问题]
  - A1: [答案]
- Q2: [问题]
  - A2: [答案]

**最终需求**: [澄清后的明确需求]

---

## 🎯 推荐执行角色

### Phase 1: 架构设计 (预计X天)

**并行执行**:
- **[F6-数据库架构师]** (X天)
  - 任务: [具体任务描述]
  - 命令: `/supabase-data-explorer`
  - 输出:
    - `[文件路径1]`
    - `[文件路径2]`
  - 关键考虑:
    - [考虑点1]
    - [考虑点2]
  - 依赖: 无

- **[F5-后端架构师]** (X天)
  - 任务: [具体任务描述]
  - 技术栈: [技术选型]
  - 输出:
    - `[文件路径]`
  - 关键考虑:
    - [考虑点1]
    - [考虑点2]
  - 依赖: 可与F6并行

- **[F8-云架构师]** (X天)
  - 任务: [具体任务描述]
  - 平台: Vercel Edge + Supabase
  - 输出:
    - `[文件路径]`
  - 关键考虑:
    - [考虑点1]
  - 依赖: 可与F5/F6并行

**串行执行**:
- **[F9-架构评审]** (0.5天)
  - 依赖: F5/F6/F8完成后
  - 任务: 评审架构方案合理性
  - 输出: `architecture/review-report.md`

### Phase 2: 功能实现 (预计X天)

**主力开发**:
- **[F1-前端开发]** (X天)
  - 任务: [具体任务描述]
  - 命令: `/nextjs-component-generator`
  - 输出:
    - `app/[路径]/page.tsx`
    - `app/components/[组件名].tsx`
  - 技术要点:
    - [要点1]
    - [要点2]

**专家支持**:
- **[F11-TypeScript专家]** (X天)
  - 任务: 设计类型系统和Zod schema
  - 输出:
    - `types/[类型文件].ts`
    - `schemas/[验证文件].ts`
  - 技术要点:
    - [要点1]

- **[F10-Python专家]** (X天, 可与F1并行)
  - 任务: [Python相关任务]
  - 输出: `supabase/functions/[函数名]/`
  - 技术要点:
    - [要点1]

### Phase 3: 测试验证 (预计X天)

- **[F14-测试工程师]** (X天)
  - 任务: 编写单元测试和E2E测试
  - 命令: `/nextjs-api-tester [API路径]`
  - 技能: `skills/webapp-testing`
  - 输出:
    - `tests/unit/[测试文件].test.ts`
    - `tests/e2e/[测试文件].spec.ts`
    - `coverage/` (测试覆盖率报告)
  - 验证标准:
    - 单元测试覆盖率 ≥80%
    - E2E测试覆盖核心用户路径
    - 所有API端点响应时间 <200ms

### Phase 4: 性能优化 (预计X天)

- **[F15-性能优化专家]** (X天)
  - 任务: Core Web Vitals优化
  - 命令:
    - `/nextjs-performance-audit`
    - `/supabase-performance-optimizer`
  - 输出: `performance/audit-report.md`
  - 优化目标:
    - LCP (Largest Contentful Paint) <2.5s
    - FID (First Input Delay) <100ms
    - CLS (Cumulative Layout Shift) <0.1
  - 关键优化:
    - [优化点1]
    - [优化点2]

### Phase 5: 最终审查 (预计0.5天)

- **[F13-代码审查专家]** (0.5天)
  - 任务: 全面Code Review
  - 输出: `code-review/report.md`
  - 审查清单:
    - TypeScript类型安全
    - Supabase RLS策略正确性
    - Server Components/Client Components划分合理性
    - 错误处理完整性

---

## ⚙️ 技术栈约束

### 强制约束 (不可替代)

- ✅ **前端框架**: Next.js 16 App Router
  - 原因: 开发组标准技术栈
  - 要求: 优先使用Server Components，减少客户端JS

- ✅ **后端服务**: Supabase
  - PostgreSQL数据库 (托管)
  - Realtime订阅 (WebSocket)
  - Auth认证 (Row Level Security)
  - Edge Functions (Deno运行时)

- ✅ **类型系统**: TypeScript 5.x 严格模式
  - 原因: 类型安全和代码质量
  - 要求: 所有文件必须有类型定义

- ✅ **样式方案**: Tailwind CSS + shadcn/ui
  - 原因: 开发组UI标准
  - 要求: 使用shadcn/ui组件库

- ✅ **状态管理**:
  - Server State: TanStack Query (React Query)
  - Client State: Zustand
  - URL State: Next.js searchParams

- ✅ **部署平台**: Vercel Edge Network
  - 原因: Next.js最佳部署平台
  - 要求: 利用Edge Functions减少延迟

### 禁止使用 (会导致PRP评分降低)

- ❌ **Pages Router**: 已废弃，必须使用App Router
- ❌ **Express.js/Koa.js**: 使用Server Actions和Route Handlers代替
- ❌ **MongoDB/MySQL**: 必须使用Supabase PostgreSQL
- ❌ **Firebase**: 必须使用Supabase
- ❌ **Redux**: 使用TanStack Query + Zustand代替
- ❌ **CSS Modules/Styled Components**: 使用Tailwind CSS

### 推荐但非强制

- 🟡 **测试框架**: Vitest (推荐) 或 Jest
- 🟡 **E2E测试**: Playwright (推荐) 或 Cypress
- 🟡 **表单验证**: Zod (推荐) 或 Yup
- 🟡 **HTTP客户端**: Fetch API (推荐) 或 Axios

---

## 🛠️ 推荐Commands

### 初始化阶段 (Phase 0-1)
```bash
# 创建Next.js 16项目脚手架
/nextjs-scaffold [project-name] --typescript --tailwind --app-router

# 说明:
# - 自动配置TypeScript严格模式
# - 自动安装Tailwind CSS
# - 创建App Router目录结构
# - 配置ESLint + Prettier
```

### 数据建模阶段 (Phase 1)
```bash
# 可视化Supabase数据库设计
/supabase-data-explorer

# 功能:
# - 可视化设计表结构
# - 生成RLS策略
# - 创建索引建议
# - 导出SQL migration文件
```

### 开发阶段 (Phase 2)
```bash
# 生成标准化Next.js组件
/nextjs-component-generator [ComponentName] --server-component

# 说明:
# - --server-component: 生成Server Component
# - --client-component: 生成Client Component
# - 自动生成TypeScript类型
```

### 测试阶段 (Phase 3)
```bash
# API端点测试
/nextjs-api-tester [API路径]

# 测试内容:
# - 请求/响应格式验证
# - 错误处理测试
# - 性能基准测试
# - 生成测试报告
```

### 优化阶段 (Phase 4)
```bash
# Next.js性能审计
/nextjs-performance-audit

# 检查项:
# - Core Web Vitals指标
# - Bundle Size分析
# - 图片优化建议
# - 代码分割检查

# Supabase性能优化
/supabase-performance-optimizer

# 检查项:
# - 慢查询识别
# - 索引建议
# - RLS策略性能影响
# - 连接池配置
```

---

## 🔗 Skills依赖声明

### skills/figma/ (UI设计转代码)

**依赖场景**: F2-UI设计师需要将Figma设计稿转换为代码时

**使用时机**: Phase 2前端实现阶段

**典型用法**:
```bash
# F2-UI设计师调用
使用skills/figma解析Figma设计稿URL
生成Tailwind CSS + shadcn/ui代码
输出到 app/components/
```

**输出示例**:
- `app/components/[组件名].tsx`
- `styles/figma-tokens.css` (设计令牌)

**前置条件**:
- 需要Figma文件共享链接
- 设计稿必须使用Auto Layout
- 组件命名规范

### skills/webapp-testing/ (Web应用自动化测试)

**依赖场景**: F14-测试工程师编写E2E测试时

**使用时机**: Phase 3测试验证阶段

**典型用法**:
```bash
# F14-测试工程师调用
使用skills/webapp-testing创建测试套件
针对核心流程
输出Playwright测试脚本
```

**测试覆盖**:
- [核心流程1]
- [核心流程2]
- 错误状态处理

**输出示例**:
- `tests/e2e/[flow-name].spec.ts`
- `playwright-report/` (测试报告)

---

## 📋 Implementation Blueprint

### 高层架构设计

```
[绘制架构图或描述]
├── 前端层: Next.js 16 App Router
│   ├── Server Components: [组件列表]
│   └── Client Components: [组件列表]
├── API层: Server Actions + Route Handlers
│   ├── Server Actions: [动作列表]
│   └── Route Handlers: [端点列表]
└── 数据层: Supabase
    ├── Tables: [表列表]
    ├── RLS Policies: [策略列表]
    └── Edge Functions: [函数列表]
```

### 数据模型设计

```sql
-- [表名1]
CREATE TABLE [表名] (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  [字段1] [类型] [约束],
  [字段2] [类型] [约束],
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS策略
ALTER TABLE [表名] ENABLE ROW LEVEL SECURITY;
CREATE POLICY "[策略名]" ON [表名]
  FOR SELECT USING (auth.uid() = user_id);
```

### 核心流程伪代码

```typescript
// 伪代码示例 (Phase 2)
// app/[路径]/page.tsx

export default async function Page() {
  // Server Component - 服务端数据获取
  const data = await fetchData();

  return (
    <div>
      {/* 静态内容 */}
      <ServerComponent data={data} />

      {/* 需要交互的Client Component */}
      <ClientComponent initialData={data} />
    </div>
  );
}

// Server Action (在Server Component中)
async function fetchData() {
  const supabase = createServerClient();
  const { data, error } = await supabase
    .from('[表名]')
    .select('*')
    .eq('[字段]', '[值]');

  if (error) throw error;
  return data;
}
```

### 文件结构规划

```
[项目根目录]/
├── app/
│   ├── [路由1]/
│   │   ├── page.tsx
│   │   └── loading.tsx
│   ├── components/
│   │   ├── [组件1].tsx
│   │   └── [组件2].tsx
│   └── api/
│       └── [端点名]/
│           └── route.ts
├── lib/
│   ├── supabase/
│   │   └── client.ts
│   └── utils/
├── types/
│   └── [类型文件].ts
└── schemas/
    └── [验证文件].ts
```

### Task Checklist (按完成顺序)

```yaml
Phase 1: 架构设计
  ☐ 1.1: F6 - 设计数据库Schema
  ☐ 1.2: F6 - 配置RLS策略
  ☐ 1.3: F5 - 设计Server Actions架构
  ☐ 1.4: F8 - 规划Vercel部署配置
  ☐ 1.5: F9 - 架构评审

Phase 2: 功能实现
  ☐ 2.1: F1 - 实现[组件1]
  ☐ 2.2: F1 - 实现[组件2]
  ☐ 2.3: F11 - 定义TypeScript类型
  ☐ 2.4: F1 - 实现Server Actions
  ☐ 2.5: F13 - Code Review

Phase 3: 测试验证
  ☐ 3.1: F14 - 编写单元测试
  ☐ 3.2: F14 - 编写E2E测试
  ☐ 3.3: F14 - 执行测试并生成报告

Phase 4: 性能优化
  ☐ 4.1: F15 - 性能审计
  ☐ 4.2: F15 - 优化Core Web Vitals
  ☐ 4.3: F15 - Supabase查询优化

Phase 5: 最终审查
  ☐ 5.1: F13 - 最终Code Review
  ☐ 5.2: F9 - 架构合规检查
  ☐ 5.3: 准备上线检查清单
```

### 错误处理策略

```typescript
// 统一错误处理模式
try {
  const result = await dangerousOperation();
  return { success: true, data: result };
} catch (error) {
  // 1. 日志记录
  console.error('[模块名]:', error);

  // 2. 用户友好提示
  if (error instanceof SupabaseError) {
    return { success: false, error: '数据库操作失败，请稍后重试' };
  }

  // 3. 回退方案
  return { success: false, error: '未知错误' };
}
```

---

## ✅ 验证门控

### Gate 1: 数据库Schema验证

```bash
# 验证RLS策略
supabase test policies

# 验证索引优化
/supabase-performance-optimizer
```

- **责任人**: F6-数据库架构师
- **验证时机**: Phase 1完成后
- **通过标准**:
  - 所有表启用RLS
  - 所有RLS策略测试通过
  - 查询性能 <100ms

### Gate 2: TypeScript类型安全验证

```bash
# TypeScript类型检查
tsc --noEmit

# Zod schema验证
npm run validate-schemas
```

- **责任人**: F11-TypeScript专家
- **验证时机**: Phase 2完成后
- **通过标准**:
  - 无TypeScript编译错误
  - 所有API输入输出有Zod验证

### Gate 3: 测试覆盖率验证

```bash
# 单元测试
npm run test:unit

# E2E测试
npm run test:e2e

# 覆盖率报告
npm run test:coverage
```

- **责任人**: F14-测试工程师
- **验证时机**: Phase 3完成后
- **通过标准**:
  - 单元测试覆盖率 ≥80%
  - E2E测试覆盖核心路径
  - 所有测试通过

### Gate 4: 性能指标验证

```bash
# 性能审计
/nextjs-performance-audit

# Lighthouse CI
npm run lighthouse
```

- **责任人**: F15-性能优化专家
- **验证时机**: Phase 4完成后
- **通过标准**:
  - LCP <2.5s
  - FID <100ms
  - CLS <0.1
  - Lighthouse分数 ≥90

### Gate 5: Code Review验证

```bash
# 代码规范检查
npm run lint

# 格式化检查
npm run format:check
```

- **责任人**: F13-代码审查专家
- **验证时机**: Phase 5最终审查
- **通过标准**:
  - 无ESLint错误
  - 代码格式化一致
  - 架构符合PRP要求

---

## 🚨 Anti-Patterns (避免这些错误)

### 反模式1: [描述]

```yaml
❌ 错误做法:
  [描述错误做法]

✅ 正确做法:
  [描述正确做法]

原因:
  [说明为什么错误]
```

### 反模式2: [描述]

```yaml
❌ 错误做法:
  [描述错误做法]

✅ 正确做法:
  [描述正确做法]

原因:
  [说明为什么错误]
```

---

## 📊 PRP质量评分

### 自评分

```yaml
维度1: 上下文完整性 (25%)
  - 代码库分析: [X/10]
  - 外部研究: [X/10]
  - 技术陷阱: [X/5]
  小计: [X/25]

维度2: 实现路径清晰度 (25%)
  - 蓝图逻辑: [X/10]
  - 任务分解: [X/10]
  - 依赖关系: [X/5]
  小计: [X/25]

维度3: 生态契合度 (30%)
  - 角色分配: [X/10]
  - 技术约束: [X/10]
  - Commands推荐: [X/5]
  - Skills依赖: [X/5]
  小计: [X/30]

维度4: 验证可执行性 (20%)
  - 验证命令: [X/10]
  - 责任人明确: [X/5]
  - 自动化程度: [X/5]
  小计: [X/20]

总分: [X/100] → [X/10]
```

**评分标准**:
- 9-10分: 优秀，可直接执行
- 8-8.9分: 良好，稍作调整即可
- 7-7.9分: 及格，需要补充完善
- <7分: 不合格，需要重新生成

**目标评分**: ≥8.0/10

---

## 📝 更新日志

- [YYYY-MM-DD] v1.0 - 初始版本创建
- [YYYY-MM-DD] v1.1 - [更新内容]

---

**生成by**: F0-需求分析师
**模板版本**: 开发组专属 v1.0
**质量承诺**: 本PRP评分≥8.0/10，可作为实施的唯一指南
