---
name: ZTL数智化作战中心 Web-UI可视化界面
description: 基于Next.js 16构建赛博朋克风格的多智能体可视化操作平台,实现Claude Code项目的Web界面化
version: 1.0.0
created: 2025-11-01
status: Planning
priority: High
estimated_effort: 3-4周 (分阶段交付)
---

# ZTL数智化作战中心 Web-UI可视化界面

## 📋 功能概述

### 业务目标

将ZTL数智化作战中心从命令行工具转化为可视化Web应用,降低使用门槛,提升操作体验,实现:

- **降低学习曲线**: 从CLI命令行→可视化点选操作
- **增强用户体验**: 游戏化界面设计,赛博朋克视觉冲击
- **提升操作效率**: 快速切换智能体,可视化任务状态
- **扩展用户群体**: 从程序员→非技术团队成员

### 核心价值主张

1. **零学习成本**: 无需记忆60+智能体名称和命令语法
2. **沉浸式体验**: 游戏化设计,类似"拳皇选角"的视觉呈现
3. **实时反馈**: WebSocket实时通信,即时看到AI响应
4. **多模态交互**: 支持文字、语音、图片输入

### 应用场景

- **内部使用**: 团队成员快速调用智能体完成任务
- **客户演示**: 向客户展示AI能力和多智能体协作
- **新人培训**: 帮助新员工快速了解系统架构和功能
- **远程访问**: 通过浏览器随时随地访问作战中心

---

## 🔍 上下文与参考

### 文档引用

#### 官方文档

1. **Next.js 16 官方文档**
   - URL: https://nextjs.org/blog/next-16
   - 相关性: Next.js 16核心特性(Cache Components, React Compiler, Turbopack)
   - 重点章节: App Router, Server Components, Caching Strategy

2. **Next.js Best Practices 2025**
   - URL: https://www.raftlabs.com/blog/building-with-next-js-best-practices-and-benefits-for-performance-first-teams/
   - 相关性: 项目结构、性能优化、App Router最佳实践
   - 重点章节: Server Components First, Project Structure, Component Organization

3. **Framer Motion Scroll Animations**
   - URL: https://motion.dev/docs/react-scroll-animations
   - 相关性: 实现赛博朋克风格的滚动特效和页面转场
   - 重点章节: whileInView, useScroll, scroll() function

4. **shadcn/ui Dashboard Templates**
   - URL: https://www.shadcn.io/template/category/dashboard
   - 相关性: 高质量UI组件库,加速开发
   - 重点章节: Dashboard Components, Tailwind CSS v4, Radix UI

#### 设计参考

5. **Cyberpunk Neon CSS Design**
   - URL: https://www.cssscript.com/demo/cyberpunk-2077/
   - 相关性: 赛博朋克风格CSS实现
   - 关键技术: text-shadow霓虹效果, clip-path故障特效, 动态网格背景

6. **ARWES - Futuristic Sci-Fi UI Framework**
   - URL: https://github.com/arwes/arwes
   - 相关性: 科幻风格UI组件库
   - 关键特性: Sound effects, Animations, Futuristic design system

### 代码示例

#### 现有实现参考

**1. Cyberpunk风格实现** (`.claude/skills/特别拓展/html风格包/cyberpunk-neon/SKILL.md:19-141`)

```css
/* 核心赛博朋克色彩系统 */
:root {
    --neon-pink: #ff00ff;
    --neon-cyan: #00ffff;
    --neon-purple: #b000ff;
    --cyber-bg-primary: #0a0a0f;
    --cyber-bg-secondary: #0f0f23;
}

/* 霓虹发光效果 */
.neon-text {
    color: #00ffff;
    text-shadow:
        0 0 5px #00ffff,
        0 0 10px #00ffff,
        0 0 20px #00ffff,
        0 0 40px rgba(0, 255, 255, 0.5);
}

/* 动态网格背景 */
body::before {
    content: '';
    position: fixed;
    width: 100%;
    height: 100%;
    background:
        linear-gradient(0deg, transparent 24%, rgba(255, 0, 255, 0.05) 25%...);
    background-size: 50px 50px;
    animation: grid-move 20s linear infinite;
}

@keyframes grid-move {
    0% { transform: translateY(0); }
    100% { transform: translateY(50px); }
}
```

**2. 现有HTML原型** (`project/instructions-V2/ZTL数智化作战中心项目介绍.html:1-100`)

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>ZTL数智化作战中心 - Cyberpunk Edition</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Electrolize&display=swap" rel="stylesheet">
    <!-- 已有成熟的赛博朋克风格实现 -->
</head>
```

**分析**: 项目已有完整的HTML静态原型,实现了:
- ✅ Cyberpunk网格背景和扫描线效果
- ✅ Orbitron/Electrolize字体系统
- ✅ 霓虹色彩方案(粉/青/紫)
- ❌ 缺少交互逻辑和后端集成

**3. React前端设计师智能体** (`plugins/创意组/agents/X7-React前端设计师.md:1-885`)

```yaml
核心定位: UX/UI设计架构师
关键能力:
  - 活动页/详情页/数据看板/文档页设计
  - 自动整合artifacts-builder、theme-factory、html风格包
  - 输出路径规范: output/[项目名]/X6-React前端设计师/

输出产物:
  - plans/: 设计简报和需求规格(JSON/YAML)
  - results/: 设计交付物(HTML原型、Figma导出、截图)
  - logs/: 设计决策日志
  - metadata/: 版本历史和反馈
```

**分析**: 可直接调用该智能体生成设计方案和交互原型

**4. Next.js脚手架命令** (`plugins/开发组/commands/nextjs-scaffold.md:1-236`)

```yaml
命令功能: 创建Next.js应用脚手架
支持配置:
  - TypeScript: ✅ (强制启用)
  - Tailwind CSS: ✅
  - App Router: ✅ (Next.js 16默认)
  - ESLint/Prettier: ✅

项目结构:
  app/               # App Router
  components/        # 可复用组件
    └── ui/          # shadcn/ui组件
  lib/               # 工具和配置
  public/            # 静态资源
  types/             # TypeScript类型
```

**分析**: 可复用该脚手架快速初始化项目

### 技术陷阱

#### Next.js 16 特定问题

1. **Cache Components陷阱** (来源: Next.js 16官方博客)
   ```yaml
   问题: Next.js 16的缓存机制从隐式变为显式opt-in
   影响: 默认情况下,所有动态代码在请求时执行,可能影响性能
   解决方案:
     - 使用cacheLife配置stale-while-revalidate行为
     - 合理使用Cache Components标记静态内容
     - 避免过度缓存导致数据不新鲜
   ```

2. **Server Actions安全问题** (来源: Next.js Best Practices)
   ```yaml
   问题: 在Client Component中直接定义Server Actions会泄露服务端代码
   影响: 服务端逻辑暴露在客户端bundle中
   解决方案:
     - Server Actions必须定义在单独文件(*.server.ts)
     - 在Client Component中import并调用
     - 使用"use server"指令明确标记
   ```

#### 赛博朋克风格性能问题

3. **霓虹发光效果性能开销** (来源: CSS Neon Animation实践)
   ```yaml
   问题: 多层text-shadow和box-shadow导致重绘开销大
   影响: 移动设备上可能出现卡顿
   解决方案:
     - 限制阴影层数≤4层
     - 使用will-change: transform提升至合成层
     - 移动端降级,减少动画复杂度
     - 使用CSS containment隔离渲染区域
   ```

4. **动态网格背景性能** (来源: Cyberpunk.css文档)
   ```yaml
   问题: 大面积::before伪元素动画消耗GPU
   影响: 低端设备帧率下降
   解决方案:
     - 使用transform代替background-position
     - 添加@media (prefers-reduced-motion)
     - 检测设备性能,动态启用/禁用特效
   ```

#### 多智能体交互复杂度

5. **60+智能体数据加载** (项目特定)
   ```yaml
   问题: 首页需要展示8个业务组 + 60+智能体信息
   影响: 首屏加载时间长,TTI(Time to Interactive)差
   解决方案:
     - 延迟加载(Lazy Loading): 只加载可视区域智能体卡片
     - 虚拟滚动(react-window): 大列表渲染优化
     - 数据预处理: 构建时生成plugins索引JSON
     - 增量加载: 点击业务组再加载该组智能体详情
   ```

6. **WebSocket实时通信** (技术栈集成)
   ```yaml
   问题: Next.js App Router中Server Components不支持WebSocket
   影响: 实时对话功能无法在RSC中实现
   解决方案:
     - 对话界面使用Client Component
     - 使用Socket.io或Pusher建立WebSocket连接
     - Server Actions作为fallback(轮询模式)
     - 考虑Server-Sent Events (SSE)作为轻量级替代
   ```

### 实现模式

#### 智能体卡片选择模式 (类"拳皇选角")

**参考**: 游戏角色选择界面 + project/instructions-V2/ZTL数智化作战中心项目介绍.html

```typescript
// 智能体卡片数据结构
interface AgentCard {
  id: string;              // 例: "G1", "X3", "E2"
  name: string;            // 例: "经营分析优化师"
  group: string;           // 例: "战略组"
  avatar: string;          // 头像URL
  description: string;     // 简短描述
  color: string;           // 主题色(霓虹色)
  stats: {                 // 游戏化属性
    expertise: string[];   // 专长领域
    tools: string[];       // 可用工具
    output: string;        // 输出类型
  };
}

// 交互状态机
enum CardState {
  Idle = 'idle',           // 默认状态
  Hover = 'hover',         // 悬停(放大+霓虹脉冲)
  Selected = 'selected',   // 选中(高亮+边框动画)
  Disabled = 'disabled',   // 不可用(灰度+降低透明度)
}
```

**悬停特效实现** (Framer Motion):

```typescript
// 组件: AgentCard.tsx
import { motion } from 'framer-motion';

const AgentCard = ({ agent }: { agent: AgentCard }) => {
  return (
    <motion.div
      className="agent-card"
      initial={{ scale: 1, boxShadow: '0 0 10px var(--neon-cyan)' }}
      whileHover={{
        scale: 1.05,
        boxShadow: '0 0 20px var(--neon-cyan), 0 0 40px var(--neon-cyan)',
        transition: { duration: 0.2 }
      }}
      whileTap={{ scale: 0.95 }}
    >
      {/* 卡片内容 */}
    </motion.div>
  );
};
```

**选中动画** (CSS + Framer Motion):

```css
/* 选中状态边框扫描动画 */
@keyframes border-scan {
  0%, 100% {
    clip-path: inset(0 100% 100% 0);
  }
  25% {
    clip-path: inset(0 0 100% 0);
  }
  50% {
    clip-path: inset(0 0 0 0);
  }
  75% {
    clip-path: inset(0 0 0 100%);
  }
}

.agent-card.selected::after {
  content: '';
  position: absolute;
  inset: -2px;
  border: 2px solid var(--neon-pink);
  animation: border-scan 2s linear infinite;
}
```

#### 对话界面模式 (参考Grok)

**参考**: https://grok.x.ai (X.AI的Grok界面)

```typescript
// 对话消息数据结构
interface ChatMessage {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: number;
  agent?: AgentCard;       // 如果是智能体回复,附带智能体信息
  attachments?: Attachment[]; // 多模态附件
  status: 'sending' | 'sent' | 'error';
}

// 消息渲染模式
interface MessageRenderer {
  text: (content: string) => JSX.Element;        // Markdown渲染
  code: (code: string, lang: string) => JSX.Element; // 代码高亮
  image: (url: string) => JSX.Element;          // 图片卡片
  file: (file: File) => JSX.Element;            // 文件卡片
  chart: (data: any) => JSX.Element;            // 数据图表
  table: (data: any[][]) => JSX.Element;        // 表格
}
```

**对话流式输出** (Server-Sent Events):

```typescript
// API Route: app/api/chat/route.ts
export async function POST(req: Request) {
  const { message, agentId } = await req.json();

  const stream = new ReadableStream({
    async start(controller) {
      // 调用Claude API获取流式响应
      const response = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
          'anthropic-version': '2023-06-01',
          'x-api-key': process.env.ANTHROPIC_API_KEY!,
        },
        body: JSON.stringify({
          model: 'claude-sonnet-4-5-20250929',
          messages: [{ role: 'user', content: message }],
          stream: true,
        }),
      });

      // 转发流式响应到客户端
      const reader = response.body!.getReader();
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        controller.enqueue(value);
      }
      controller.close();
    },
  });

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
    },
  });
}
```

**客户端消费流** (React Hook):

```typescript
// hooks/useStreamingChat.ts
import { useState, useCallback } from 'react';

export function useStreamingChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);

  const sendMessage = useCallback(async (content: string, agentId: string) => {
    setIsStreaming(true);
    const response = await fetch('/api/chat', {
      method: 'POST',
      body: JSON.stringify({ message: content, agentId }),
    });

    const reader = response.body!.getReader();
    const decoder = new TextDecoder();
    let accumulatedText = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      accumulatedText += decoder.decode(value);

      // 实时更新UI
      setMessages(prev => {
        const last = prev[prev.length - 1];
        if (last?.role === 'assistant' && last.status === 'sending') {
          return [...prev.slice(0, -1), { ...last, content: accumulatedText }];
        }
        return [...prev, { role: 'assistant', content: accumulatedText, status: 'sending' }];
      });
    }

    setIsStreaming(false);
  }, []);

  return { messages, isStreaming, sendMessage };
}
```

---

## 🎯 实现蓝图

### 技术架构

#### 技术栈选型

```yaml
前端框架:
  核心: Next.js 16 (App Router)
  理由:
    - ✅ Next.js 16稳定版,Cache Components, React Compiler
    - ✅ App Router成熟,Server Components减少客户端JS
    - ✅ Turbopack加速开发构建
    - ✅ 优秀的SEO和性能

UI库:
  核心: shadcn/ui + Tailwind CSS v4
  理由:
    - ✅ Radix UI基础,无障碍性优秀
    - ✅ 无框架锁定,组件可定制
    - ✅ Tailwind v4性能提升
    - ✅ 成熟的Dashboard模板可参考

动画库:
  核心: Framer Motion 11
  理由:
    - ✅ 声明式API,易于维护
    - ✅ 原生支持scroll-linked动画
    - ✅ 性能优化(hybrid engine, ScrollTimeline API)
    - ✅ 游戏化特效(弹性、惯性、手势)

状态管理:
  核心: Zustand + React Query
  理由:
    - ✅ Zustand轻量级全局状态
    - ✅ React Query处理服务端状态和缓存
    - ✅ 避免Redux复杂度

实时通信:
  核心: Socket.io (WebSocket) + Server-Sent Events (SSE)
  理由:
    - ✅ Socket.io成熟可靠,自动降级
    - ✅ SSE简单高效,适合单向推送
    - ✅ 两种方案互为备份

代码质量:
  核心: TypeScript + ESLint + Prettier
  理由:
    - ✅ TypeScript类型安全
    - ✅ ESLint捕获潜在问题
    - ✅ Prettier统一代码风格
```

#### 系统架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                     Browser (Client)                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐  │
│  │   主页 (/)     │  │  对话页        │  │  资源页        │  │
│  │                │  │  (/chat)       │  │  (/resources)  │  │
│  │ - 指挥部展示   │  │ - AI对话界面   │  │ - Output目录   │  │
│  │ - 8大业务组    │  │ - 智能体切换   │  │ - COS云存储    │  │
│  │ - 60+智能体    │  │ - 多模态输入   │  │ - Supabase DB  │  │
│  │ - 卡片选择     │  │ - 实时响应     │  │                │  │
│  └────────────────┘  └────────────────┘  └────────────────┘  │
│           │                    │                     │          │
│           └────────────────────┼─────────────────────┘          │
│                                │                                │
│                    ┌───────────▼──────────┐                     │
│                    │  Framer Motion       │                     │
│                    │  (动画引擎)           │                     │
│                    └──────────────────────┘                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                               │
                               │ HTTP/WebSocket/SSE
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│                     Next.js 16 Server                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐   │
│  │              App Router (app/)                          │   │
│  │                                                          │   │
│  │  app/                                                    │   │
│  │  ├── page.tsx              (主页 Server Component)      │   │
│  │  ├── chat/                                               │   │
│  │  │   └── page.tsx          (对话页 Client Component)    │   │
│  │  ├── resources/                                          │   │
│  │  │   └── page.tsx          (资源页 Server Component)    │   │
│  │  ├── api/                                                │   │
│  │  │   ├── agents/           (智能体API)                  │   │
│  │  │   │   └── route.ts      (GET /api/agents)            │   │
│  │  │   ├── chat/             (对话API)                     │   │
│  │  │   │   └── route.ts      (POST /api/chat)             │   │
│  │  │   └── files/            (文件管理API)                │   │
│  │  │       └── route.ts      (GET /api/files)             │   │
│  │  ├── layout.tsx            (根布局)                      │   │
│  │  └── globals.css           (全局样式)                    │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐   │
│  │              Components (components/)                    │   │
│  │                                                          │   │
│  │  components/                                             │   │
│  │  ├── ui/                   (shadcn/ui基础组件)          │   │
│  │  │   ├── button.tsx                                     │   │
│  │  │   ├── card.tsx                                       │   │
│  │  │   ├── input.tsx                                      │   │
│  │  │   └── ...                                            │   │
│  │  ├── agents/               (智能体相关组件)             │   │
│  │  │   ├── AgentCard.tsx     (智能体卡片)                │   │
│  │  │   ├── AgentGrid.tsx     (智能体网格)                │   │
│  │  │   └── GroupSelector.tsx (业务组选择器)              │   │
│  │  ├── chat/                 (对话相关组件)               │   │
│  │  │   ├── ChatInput.tsx     (输入框)                     │   │
│  │  │   ├── MessageList.tsx   (消息列表)                   │   │
│  │  │   └── MessageCard.tsx   (消息卡片)                   │   │
│  │  └── layout/               (布局组件)                    │   │
│  │      ├── Header.tsx        (顶部导航)                    │   │
│  │      ├── Sidebar.tsx       (侧边栏)                      │   │
│  │      └── Footer.tsx        (底部)                        │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐   │
│  │              Services (lib/)                             │   │
│  │                                                          │   │
│  │  lib/                                                    │   │
│  │  ├── agents/               (智能体服务)                  │   │
│  │  │   ├── parser.ts         (解析plugins目录)            │   │
│  │  │   └── index.json        (构建时生成的索引)           │   │
│  │  ├── claude/               (Claude API集成)             │   │
│  │  │   └── client.ts         (API客户端)                  │   │
│  │  ├── storage/              (存储服务)                    │   │
│  │  │   ├── cos.ts            (COS集成)                     │   │
│  │  │   └── supabase.ts       (Supabase集成)               │   │
│  │  └── utils/                (工具函数)                    │   │
│  │      ├── cn.ts             (className合并)              │   │
│  │      └── format.ts         (格式化)                      │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                               │
                               │ File System / API Calls
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│                     External Systems                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │ plugins/     │  │ Claude API   │  │ COS/Supabase │        │
│  │ (本地文件)   │  │ (外部API)    │  │ (云存储)      │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 项目结构

```
ztl-web-ui/                           # 项目根目录
├── app/                              # Next.js App Router
│   ├── (main)/                       # 主应用路由组
│   │   ├── page.tsx                  # 主页 (/)
│   │   ├── chat/
│   │   │   └── page.tsx              # 对话页 (/chat)
│   │   └── resources/
│   │       └── page.tsx              # 资源页 (/resources)
│   ├── api/                          # API路由
│   │   ├── agents/
│   │   │   └── route.ts              # GET /api/agents
│   │   ├── chat/
│   │   │   └── route.ts              # POST /api/chat (SSE)
│   │   └── files/
│   │       └── route.ts              # GET /api/files
│   ├── layout.tsx                    # 根布局
│   ├── globals.css                   # 全局样式
│   └── not-found.tsx                 # 404页面
│
├── components/                       # 组件目录
│   ├── ui/                           # shadcn/ui组件
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── input.tsx
│   │   ├── dialog.tsx
│   │   └── ...
│   ├── agents/                       # 智能体组件
│   │   ├── AgentCard.tsx             # 智能体卡片
│   │   ├── AgentGrid.tsx             # 智能体网格布局
│   │   ├── GroupSelector.tsx         # 业务组选择器
│   │   └── AgentDetail.tsx           # 智能体详情
│   ├── chat/                         # 对话组件
│   │   ├── ChatInput.tsx             # 输入框(多模态)
│   │   ├── MessageList.tsx           # 消息列表
│   │   ├── MessageCard.tsx           # 消息卡片
│   │   ├── StreamingText.tsx         # 流式文本渲染
│   │   └── TypingIndicator.tsx       # 输入中指示器
│   ├── layout/                       # 布局组件
│   │   ├── Header.tsx                # 顶部导航
│   │   ├── Sidebar.tsx               # 侧边栏
│   │   ├── Footer.tsx                # 底部
│   │   └── MobileMenu.tsx            # 移动端菜单
│   └── effects/                      # 特效组件
│       ├── CyberpunkGrid.tsx         # 赛博朋克网格背景
│       ├── ScanlineEffect.tsx        # 扫描线效果
│       └── NeonGlow.tsx              # 霓虹发光容器
│
├── lib/                              # 业务逻辑
│   ├── agents/                       # 智能体服务
│   │   ├── parser.ts                 # 解析plugins/目录
│   │   ├── types.ts                  # 类型定义
│   │   └── index.json                # 构建时生成的智能体索引
│   ├── claude/                       # Claude API
│   │   ├── client.ts                 # API客户端
│   │   └── types.ts                  # 类型定义
│   ├── storage/                      # 存储服务
│   │   ├── cos.ts                    # COS云存储
│   │   └── supabase.ts               # Supabase数据库
│   └── utils/                        # 工具函数
│       ├── cn.ts                     # className合并
│       ├── format.ts                 # 格式化
│       └── colors.ts                 # 赛博朋克色彩工具
│
├── hooks/                            # React Hooks
│   ├── useStreamingChat.ts           # 流式对话Hook
│   ├── useAgents.ts                  # 智能体数据Hook
│   ├── useMediaQuery.ts              # 响应式Hook
│   └── useKeyboardShortcut.ts        # 键盘快捷键Hook
│
├── types/                            # TypeScript类型
│   ├── agents.ts                     # 智能体类型
│   ├── chat.ts                       # 对话类型
│   └── api.ts                        # API类型
│
├── public/                           # 静态资源
│   ├── images/
│   │   ├── logo.svg                  # Logo
│   │   └── avatars/                  # 智能体头像
│   ├── fonts/                        # 字体文件
│   │   ├── orbitron/
│   │   └── electrolize/
│   └── sounds/                       # 音效(可选)
│       └── ui-beep.mp3
│
├── styles/                           # 样式文件
│   ├── cyberpunk.css                 # 赛博朋克主题
│   ├── animations.css                # 动画定义
│   └── themes.css                    # 主题变量
│
├── scripts/                          # 构建脚本
│   └── generate-agent-index.ts       # 生成智能体索引JSON
│
├── .env.local                        # 环境变量
├── .env.example                      # 环境变量模板
├── next.config.js                    # Next.js配置
├── tailwind.config.ts                # Tailwind配置
├── tsconfig.json                     # TypeScript配置
├── package.json                      # 依赖管理
└── README.md                         # 项目文档
```

### 核心实现伪代码

#### 1. 主页 - 智能体选择界面

```typescript
// app/page.tsx
import { AgentGrid } from '@/components/agents/AgentGrid';
import { GroupSelector } from '@/components/agents/GroupSelector';
import { getAllAgents, getGroups } from '@/lib/agents/parser';

export default async function HomePage() {
  // Server Component: 构建时读取plugins/目录
  const groups = await getGroups(); // ['战略组', '创意组', '情报组', ...]
  const agents = await getAllAgents(); // 60+智能体数据

  return (
    <main className="cyberpunk-container">
      {/* 赛博朋克背景特效 */}
      <CyberpunkGrid />
      <ScanlineEffect />

      {/* 标题 */}
      <h1 className="neon-text text-6xl font-orbitron">
        ZTL数智化作战中心
      </h1>

      {/* 业务组选择器 */}
      <GroupSelector groups={groups} />

      {/* 智能体网格 */}
      <AgentGrid agents={agents} />
    </main>
  );
}
```

**AgentGrid组件** (关键交互逻辑):

```typescript
// components/agents/AgentGrid.tsx
'use client';

import { motion, AnimatePresence } from 'framer-motion';
import { useState } from 'react';
import { AgentCard } from './AgentCard';
import type { Agent } from '@/types/agents';

interface AgentGridProps {
  agents: Agent[];
}

export function AgentGrid({ agents }: AgentGridProps) {
  const [selectedGroup, setSelectedGroup] = useState<string | null>(null);
  const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null);

  // 过滤当前选中业务组的智能体
  const filteredAgents = selectedGroup
    ? agents.filter(a => a.group === selectedGroup)
    : agents;

  return (
    <div className="agent-grid-container">
      {/* 网格布局 */}
      <motion.div
        className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6"
        layout
      >
        <AnimatePresence mode="popLayout">
          {filteredAgents.map((agent) => (
            <motion.div
              key={agent.id}
              layout
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.8 }}
              transition={{ type: 'spring', stiffness: 300, damping: 30 }}
            >
              <AgentCard
                agent={agent}
                isSelected={selectedAgent?.id === agent.id}
                onSelect={() => setSelectedAgent(agent)}
              />
            </motion.div>
          ))}
        </AnimatePresence>
      </motion.div>

      {/* 智能体详情弹窗 */}
      {selectedAgent && (
        <AgentDetailModal
          agent={selectedAgent}
          onClose={() => setSelectedAgent(null)}
          onStartChat={() => {
            // 跳转到对话页并带上智能体ID
            window.location.href = `/chat?agent=${selectedAgent.id}`;
          }}
        />
      )}
    </div>
  );
}
```

**AgentCard组件** (游戏化卡片):

```typescript
// components/agents/AgentCard.tsx
'use client';

import { motion } from 'framer-motion';
import type { Agent } from '@/types/agents';

interface AgentCardProps {
  agent: Agent;
  isSelected: boolean;
  onSelect: () => void;
}

export function AgentCard({ agent, isSelected, onSelect }: AgentCardProps) {
  return (
    <motion.div
      className="agent-card"
      style={{
        '--neon-color': agent.color, // CSS变量: 动态霓虹色
      } as React.CSSProperties}
      whileHover={{ scale: 1.05, rotateY: 5 }} // 3D倾斜效果
      whileTap={{ scale: 0.95 }}
      onClick={onSelect}
    >
      {/* 霓虹边框 */}
      <div className={`neon-border ${isSelected ? 'selected' : ''}`} />

      {/* 头像 */}
      <div className="agent-avatar">
        <img src={agent.avatar} alt={agent.name} />
      </div>

      {/* 智能体信息 */}
      <div className="agent-info">
        <h3 className="text-lg font-orbitron neon-text">{agent.name}</h3>
        <p className="text-sm text-gray-400">{agent.id}</p>
        <p className="text-xs mt-2">{agent.description}</p>
      </div>

      {/* 属性条 (游戏化) */}
      <div className="agent-stats">
        {agent.stats.expertise.map((exp) => (
          <span key={exp} className="stat-badge">{exp}</span>
        ))}
      </div>

      {/* 选中扫描动画 */}
      {isSelected && (
        <motion.div
          className="scan-line"
          animate={{ y: ['-100%', '100%'] }}
          transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
        />
      )}
    </motion.div>
  );
}
```

#### 2. 对话页 - AI聊天界面

```typescript
// app/chat/page.tsx
'use client';

import { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import { ChatInput } from '@/components/chat/ChatInput';
import { MessageList } from '@/components/chat/MessageList';
import { AgentSwitcher } from '@/components/chat/AgentSwitcher';
import { useStreamingChat } from '@/hooks/useStreamingChat';

export default function ChatPage() {
  const searchParams = useSearchParams();
  const initialAgentId = searchParams.get('agent') || 'QQ'; // 默认总指挥官

  const [currentAgentId, setCurrentAgentId] = useState(initialAgentId);
  const { messages, isStreaming, sendMessage } = useStreamingChat(currentAgentId);

  return (
    <div className="chat-container h-screen flex">
      {/* 侧边栏: 智能体/指令/技能选择器 (类WoW界面) */}
      <aside className="w-64 bg-cyber-secondary border-r border-neon-cyan">
        <AgentSwitcher
          currentAgentId={currentAgentId}
          onSwitch={setCurrentAgentId}
        />
        <CommandPalette />
        <SkillPanel />
      </aside>

      {/* 主聊天区域 */}
      <main className="flex-1 flex flex-col">
        {/* 顶部状态栏 */}
        <header className="h-16 border-b border-neon-purple px-4 flex items-center">
          <AgentAvatar agentId={currentAgentId} />
          <div className="ml-4">
            <h2 className="font-orbitron neon-text">当前智能体: {currentAgentId}</h2>
            <StatusIndicator isOnline />
          </div>
        </header>

        {/* 消息列表 */}
        <div className="flex-1 overflow-y-auto p-4">
          <MessageList messages={messages} />
        </div>

        {/* 输入区域 */}
        <div className="border-t border-neon-cyan p-4">
          <ChatInput
            onSend={(content) => sendMessage(content)}
            isDisabled={isStreaming}
          />
        </div>
      </main>
    </div>
  );
}
```

**流式聊天Hook** (核心):

```typescript
// hooks/useStreamingChat.ts
import { useState, useCallback } from 'react';
import type { ChatMessage } from '@/types/chat';

export function useStreamingChat(agentId: string) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);

  const sendMessage = useCallback(async (content: string) => {
    // 1. 添加用户消息
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: Date.now(),
      status: 'sent',
    };
    setMessages(prev => [...prev, userMessage]);

    // 2. 创建占位助手消息
    const assistantMessageId = (Date.now() + 1).toString();
    const assistantMessage: ChatMessage = {
      id: assistantMessageId,
      role: 'assistant',
      content: '',
      timestamp: Date.now(),
      status: 'sending',
      agentId,
    };
    setMessages(prev => [...prev, assistantMessage]);

    // 3. 调用SSE流式API
    setIsStreaming(true);
    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: content, agentId }),
      });

      const reader = response.body!.getReader();
      const decoder = new TextDecoder();
      let accumulatedText = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        accumulatedText += decoder.decode(value, { stream: true });

        // 实时更新助手消息
        setMessages(prev => prev.map(msg =>
          msg.id === assistantMessageId
            ? { ...msg, content: accumulatedText }
            : msg
        ));
      }

      // 4. 标记消息完成
      setMessages(prev => prev.map(msg =>
        msg.id === assistantMessageId
          ? { ...msg, status: 'sent' }
          : msg
      ));
    } catch (error) {
      console.error('Chat error:', error);
      setMessages(prev => prev.map(msg =>
        msg.id === assistantMessageId
          ? { ...msg, status: 'error', content: '发送失败,请重试' }
          : msg
      ));
    } finally {
      setIsStreaming(false);
    }
  }, [agentId]);

  return { messages, isStreaming, sendMessage };
}
```

#### 3. 智能体数据解析器

```typescript
// lib/agents/parser.ts
import fs from 'fs/promises';
import path from 'path';
import matter from 'gray-matter';
import type { Agent, Group } from '@/types/agents';

const PLUGINS_DIR = path.join(process.cwd(), '../plugins');

// 解析单个智能体Markdown文件
async function parseAgentFile(filePath: string): Promise<Agent | null> {
  try {
    const content = await fs.readFile(filePath, 'utf-8');
    const { data, content: body } = matter(content);

    // 从文件名提取ID (例: "G1-经营分析优化师.md" => "G1")
    const fileName = path.basename(filePath, '.md');
    const [id] = fileName.split('-');

    return {
      id,
      name: data.name || fileName,
      description: data.description || '',
      group: path.basename(path.dirname(path.dirname(filePath))),
      avatar: `/images/avatars/${id}.png`,
      color: data.color || '#00ffff', // 默认青色
      stats: {
        expertise: data.expertise || [],
        tools: data.tools || [],
        output: data.output || 'text',
      },
      markdown: body,
    };
  } catch (error) {
    console.error(`Failed to parse agent file: ${filePath}`, error);
    return null;
  }
}

// 获取所有智能体
export async function getAllAgents(): Promise<Agent[]> {
  const pluginDirs = await fs.readdir(PLUGINS_DIR);
  const agents: Agent[] = [];

  for (const pluginDir of pluginDirs) {
    const agentsDir = path.join(PLUGINS_DIR, pluginDir, 'agents');

    try {
      const files = await fs.readdir(agentsDir);

      for (const file of files) {
        if (file.endsWith('.md') && !file.includes('README')) {
          const filePath = path.join(agentsDir, file);
          const agent = await parseAgentFile(filePath);
          if (agent) agents.push(agent);
        }
      }
    } catch (error) {
      // 目录不存在,跳过
    }
  }

  return agents;
}

// 获取所有业务组
export async function getGroups(): Promise<Group[]> {
  const pluginDirs = await fs.readdir(PLUGINS_DIR);
  const groups: Group[] = [];

  for (const pluginDir of pluginDirs) {
    const pluginJsonPath = path.join(PLUGINS_DIR, pluginDir, 'plugin.json');

    try {
      const content = await fs.readFile(pluginJsonPath, 'utf-8');
      const pluginData = JSON.parse(content);

      groups.push({
        id: pluginDir,
        name: pluginData.name || pluginDir,
        description: pluginData.description || '',
        color: pluginData.color || '#ff00ff',
      });
    } catch (error) {
      // plugin.json不存在,使用默认值
      groups.push({
        id: pluginDir,
        name: pluginDir,
        description: '',
        color: '#ff00ff',
      });
    }
  }

  return groups;
}

// 构建时生成JSON索引 (优化性能)
export async function generateAgentIndex() {
  const agents = await getAllAgents();
  const groups = await getGroups();

  const index = { agents, groups, timestamp: Date.now() };

  await fs.writeFile(
    path.join(process.cwd(), 'lib/agents/index.json'),
    JSON.stringify(index, null, 2)
  );

  console.log(`✅ Generated agent index: ${agents.length} agents, ${groups.length} groups`);
}
```

**构建时调用** (package.json):

```json
{
  "scripts": {
    "prebuild": "tsx scripts/generate-agent-index.ts",
    "build": "next build",
    "dev": "next dev"
  }
}
```

#### 4. 赛博朋克样式系统

```css
/* styles/cyberpunk.css */

/* 色彩变量 */
:root {
  --neon-pink: #ff00ff;
  --neon-cyan: #00ffff;
  --neon-purple: #b000ff;
  --neon-yellow: #ffff00;
  --neon-green: #00ff00;
  --neon-orange: #ff8800;

  --cyber-bg-primary: #0a0a0f;
  --cyber-bg-secondary: #0f0f23;
  --cyber-bg-tertiary: #1a0a2e;

  --cyber-text-primary: #ffffff;
  --cyber-text-secondary: #a8a8ff;
  --cyber-text-muted: #737373;
}

/* 霓虹文字 */
.neon-text {
  color: var(--neon-cyan);
  text-shadow:
    0 0 5px var(--neon-cyan),
    0 0 10px var(--neon-cyan),
    0 0 20px var(--neon-cyan),
    0 0 40px rgba(0, 255, 255, 0.5);
}

.neon-text-pink {
  color: var(--neon-pink);
  text-shadow:
    0 0 5px var(--neon-pink),
    0 0 10px var(--neon-pink),
    0 0 20px var(--neon-pink),
    0 0 40px rgba(255, 0, 255, 0.5);
}

/* 霓虹边框 */
.neon-border {
  border: 2px solid var(--neon-color, var(--neon-cyan));
  box-shadow:
    0 0 5px var(--neon-color, var(--neon-cyan)),
    0 0 10px var(--neon-color, var(--neon-cyan)),
    0 0 20px rgba(var(--neon-color-rgb, 0, 255, 255), 0.5),
    inset 0 0 10px rgba(var(--neon-color-rgb, 0, 255, 255), 0.1);
}

.neon-border.selected {
  border: 3px solid var(--neon-pink);
  animation: border-scan 2s linear infinite;
}

/* 边框扫描动画 */
@keyframes border-scan {
  0%, 100% {
    clip-path: inset(0 100% 100% 0);
  }
  25% {
    clip-path: inset(0 0 100% 0);
  }
  50% {
    clip-path: inset(0 0 0 0);
  }
  75% {
    clip-path: inset(0 0 0 100%);
  }
}

/* 赛博朋克网格背景 */
.cyberpunk-grid {
  position: fixed;
  width: 100%;
  height: 100%;
  background:
    linear-gradient(0deg, transparent 24%, rgba(255, 0, 255, 0.05) 25%, rgba(255, 0, 255, 0.05) 26%, transparent 27%, transparent 74%, rgba(255, 0, 255, 0.05) 75%, rgba(255, 0, 255, 0.05) 76%, transparent 77%, transparent),
    linear-gradient(90deg, transparent 24%, rgba(255, 0, 255, 0.05) 25%, rgba(255, 0, 255, 0.05) 26%, transparent 27%, transparent 74%, rgba(255, 0, 255, 0.05) 75%, rgba(255, 0, 255, 0.05) 76%, transparent 77%, transparent);
  background-size: 50px 50px;
  background-color: var(--cyber-bg-primary);
  animation: grid-move 20s linear infinite;
  z-index: 0;
  pointer-events: none;
}

@keyframes grid-move {
  0% { transform: translateY(0); }
  100% { transform: translateY(50px); }
}

/* 扫描线效果 */
.scanline-effect {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: repeating-linear-gradient(
    0deg,
    rgba(0, 0, 0, 0.15),
    rgba(0, 0, 0, 0.15) 1px,
    transparent 1px,
    transparent 2px
  );
  pointer-events: none;
  z-index: 9999;
  animation: scanline 8s linear infinite;
}

@keyframes scanline {
  0% { transform: translateY(0); }
  100% { transform: translateY(100%); }
}

/* 霓虹脉冲动画 */
@keyframes neon-pulse {
  0%, 100% {
    box-shadow:
      0 0 5px var(--neon-cyan),
      0 0 10px var(--neon-cyan),
      0 0 20px rgba(0, 255, 255, 0.5);
  }
  50% {
    box-shadow:
      0 0 10px var(--neon-cyan),
      0 0 20px var(--neon-cyan),
      0 0 40px rgba(0, 255, 255, 0.8);
  }
}

.neon-pulse {
  animation: neon-pulse 2s ease-in-out infinite;
}

/* 故障效果 */
@keyframes glitch {
  0% {
    clip-path: inset(40% 0 61% 0);
    transform: translate(0);
  }
  20% {
    clip-path: inset(92% 0 1% 0);
    transform: translate(-5px, 5px);
  }
  40% {
    clip-path: inset(43% 0 1% 0);
    transform: translate(5px, -5px);
  }
  60% {
    clip-path: inset(25% 0 58% 0);
    transform: translate(-5px, 0);
  }
  80% {
    clip-path: inset(54% 0 7% 0);
    transform: translate(5px, 5px);
  }
  100% {
    clip-path: inset(58% 0 43% 0);
    transform: translate(0);
  }
}

.glitch-effect::before,
.glitch-effect::after {
  content: attr(data-text);
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.glitch-effect::before {
  color: var(--neon-pink);
  animation: glitch 0.3s infinite;
}

.glitch-effect::after {
  color: var(--neon-cyan);
  animation: glitch 0.3s infinite reverse;
}

/* 性能优化 */
@media (prefers-reduced-motion: reduce) {
  * {
    animation: none !important;
    transition: none !important;
  }
}

/* GPU加速 */
.gpu-accelerated {
  will-change: transform;
  transform: translateZ(0);
}

/* 容器隔离 */
.contain-layout {
  contain: layout;
}

.contain-paint {
  contain: paint;
}
```

### 错误处理策略

#### 前端错误

```typescript
// app/error.tsx (Next.js错误边界)
'use client';

import { useEffect } from 'react';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error('Application error:', error);
  }, [error]);

  return (
    <div className="error-container">
      <h2 className="neon-text-pink">系统故障</h2>
      <p className="text-cyber-text-secondary">
        {error.message || '发生未知错误,请刷新页面重试'}
      </p>
      <button onClick={reset} className="neon-button">
        重试
      </button>
    </div>
  );
}
```

#### API错误

```typescript
// lib/utils/error-handler.ts
export class APIError extends Error {
  constructor(
    message: string,
    public status: number,
    public code: string
  ) {
    super(message);
    this.name = 'APIError';
  }
}

export function handleAPIError(error: unknown): Response {
  if (error instanceof APIError) {
    return Response.json(
      { error: error.message, code: error.code },
      { status: error.status }
    );
  }

  console.error('Unhandled API error:', error);
  return Response.json(
    { error: '服务器内部错误', code: 'INTERNAL_ERROR' },
    { status: 500 }
  );
}
```

### 任务清单

#### Phase 1: 基础搭建 (Week 1)

- [ ] **项目初始化**
  - [ ] 使用`/nextjs-scaffold`命令创建Next.js 16项目
  - [ ] 安装核心依赖(shadcn/ui, Framer Motion, Zustand)
  - [ ] 配置TypeScript, ESLint, Prettier
  - [ ] 设置Git仓库和分支策略

- [ ] **基础架构**
  - [ ] 创建项目目录结构
  - [ ] 配置Tailwind CSS v4 + 自定义主题
  - [ ] 实现赛博朋克样式系统(cyberpunk.css)
  - [ ] 创建基础布局组件(Header, Footer, Sidebar)

- [ ] **智能体数据层**
  - [ ] 实现`lib/agents/parser.ts`解析plugins目录
  - [ ] 创建构建脚本`scripts/generate-agent-index.ts`
  - [ ] 定义TypeScript类型(agents.ts, groups.ts)
  - [ ] 测试数据解析和索引生成

#### Phase 2: 主页开发 (Week 2)

- [ ] **UI组件开发**
  - [ ] `AgentCard`组件(霓虹卡片+3D倾斜效果)
  - [ ] `AgentGrid`组件(响应式网格+过滤动画)
  - [ ] `GroupSelector`组件(业务组选择器)
  - [ ] `AgentDetailModal`组件(智能体详情弹窗)

- [ ] **交互特效**
  - [ ] 实现Framer Motion悬停动画(scale, rotateY)
  - [ ] 实现选中状态边框扫描动画
  - [ ] 实现智能体切换过渡动画(布局动画)
  - [ ] 添加赛博朋克背景特效(网格+扫描线)

- [ ] **响应式优化**
  - [ ] 移动端适配(单列布局)
  - [ ] 平板适配(双列布局)
  - [ ] 桌面适配(四列布局)
  - [ ] 触控手势支持(移动端)

#### Phase 3: 对话页开发 (Week 3)

- [ ] **对话基础**
  - [ ] `ChatInput`组件(多模态输入框)
  - [ ] `MessageList`组件(消息列表+虚拟滚动)
  - [ ] `MessageCard`组件(用户/助手消息卡片)
  - [ ] `TypingIndicator`组件(输入中指示器)

- [ ] **实时通信**
  - [ ] 实现`/api/chat` SSE端点
  - [ ] 实现`useStreamingChat` Hook
  - [ ] 实现流式文本渲染(打字机效果)
  - [ ] 添加断线重连机制

- [ ] **高级功能**
  - [ ] `AgentSwitcher`组件(智能体切换器)
  - [ ] `CommandPalette`组件(命令面板)
  - [ ] `SkillPanel`组件(技能面板)
  - [ ] 多模态输入(图片、文件上传)

#### Phase 4: 资源页开发 (Week 4)

- [ ] **文件浏览**
  - [ ] 实现`/api/files` API (读取output目录)
  - [ ] `FileExplorer`组件(文件树)
  - [ ] `FilePreview`组件(预览不同文件类型)
  - [ ] 文件搜索和过滤

- [ ] **云存储集成**
  - [ ] COS云存储集成(`lib/storage/cos.ts`)
  - [ ] Supabase数据库集成(`lib/storage/supabase.ts`)
  - [ ] 上传/下载功能
  - [ ] 云存储入口链接(跳转到外部管理界面)

#### Phase 5: 优化与部署 (Week 4末)

- [ ] **性能优化**
  - [ ] 图片优化(Next.js Image组件)
  - [ ] 代码分割(动态import)
  - [ ] 路由预加载(Link prefetch)
  - [ ] 霓虹特效性能优化(GPU加速, containment)

- [ ] **测试**
  - [ ] 单元测试(组件测试)
  - [ ] 集成测试(API测试)
  - [ ] E2E测试(Playwright)
  - [ ] 可访问性测试(WCAG AA)

- [ ] **部署**
  - [ ] Vercel部署配置
  - [ ] 环境变量配置
  - [ ] CI/CD流程
  - [ ] 监控和日志(Sentry/LogRocket)

---

## ✅ 验证门控

### 自动化验证命令

```bash
# 1. 类型检查
npm run type-check

# 2. 代码质量
npm run lint

# 3. 构建测试
npm run build

# 4. 单元测试
npm run test

# 5. E2E测试
npm run test:e2e

# 6. 性能测试 (Lighthouse CI)
npm run lighthouse

# 7. 可访问性测试
npm run test:a11y
```

### 验证标准

#### 功能验证

- ✅ 主页能展示所有8个业务组和60+智能体
- ✅ 智能体卡片悬停和选中特效正常工作
- ✅ 点击智能体能打开详情弹窗并跳转对话页
- ✅ 对话页能实时接收流式响应
- ✅ 可以切换智能体并保持对话历史
- ✅ 资源页能浏览output目录文件
- ✅ COS/Supabase入口能正常跳转

#### 性能验证

- ✅ Lighthouse Performance Score ≥ 90
- ✅ First Contentful Paint (FCP) < 1.5s
- ✅ Largest Contentful Paint (LCP) < 2.5s
- ✅ Time to Interactive (TTI) < 3.5s
- ✅ Total Blocking Time (TBT) < 300ms
- ✅ Cumulative Layout Shift (CLS) < 0.1

#### 可访问性验证

- ✅ WCAG 2.1 AA合规(axe-core扫描)
- ✅ 键盘导航完整支持(Tab, Enter, Esc)
- ✅ 屏幕阅读器兼容(NVDA/VoiceOver测试)
- ✅ 色彩对比度≥4.5:1(文本)
- ✅ 焦点指示器清晰可见

#### 兼容性验证

- ✅ Chrome/Edge 最新版
- ✅ Firefox 最新版
- ✅ Safari 最新版
- ✅ iOS Safari (iPhone 12+)
- ✅ Android Chrome (Android 10+)

---

## 📈 质量标准

### 代码质量

```yaml
TypeScript覆盖率: 100% (所有文件必须类型化)
ESLint通过率: 100% (零警告零错误)
Prettier格式化: 100% (自动格式化)
单元测试覆盖率: ≥80%
E2E测试覆盖率: 核心流程100%
```

### 用户体验

```yaml
首屏加载: <2秒(3G网络)
交互响应: <100ms(视觉反馈)
动画流畅度: 60fps(关键动画)
错误恢复: 自动重试+友好提示
多设备适配: 完美支持移动/平板/桌面
```

### 可维护性

```yaml
文档完整性: README + 组件文档 + API文档
代码注释: 复杂逻辑必须注释
组件复用性: 所有UI组件可独立复用
依赖管理: 定期更新依赖,无安全漏洞
```

---

## 🎯 成功标准

### MVP验收

1. ✅ **功能完整性**: 主页、对话页、资源页三大页面完整实现
2. ✅ **视觉还原度**: 赛博朋克风格100%还原设计稿
3. ✅ **交互流畅性**: 所有动画60fps,无卡顿
4. ✅ **性能达标**: Lighthouse ≥90分
5. ✅ **可访问性**: WCAG AA合规

### 用户反馈

- ✅ 非技术人员能在5分钟内上手使用
- ✅ 智能体选择体验符合"拳皇选角"直觉
- ✅ 对话界面媲美Grok的流畅度
- ✅ 移动端体验不逊色于桌面端

---

## 📝 附录

### 依赖版本

```json
{
  "dependencies": {
    "next": "^16.0.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "framer-motion": "^11.0.0",
    "zustand": "^5.0.0",
    "@tanstack/react-query": "^5.0.0",
    "socket.io-client": "^4.7.0",
    "gray-matter": "^4.0.3"
  },
  "devDependencies": {
    "typescript": "^5.5.0",
    "tailwindcss": "^4.0.0",
    "@types/node": "^22.0.0",
    "@types/react": "^19.0.0",
    "eslint": "^9.0.0",
    "eslint-config-next": "^16.0.0",
    "prettier": "^3.3.0",
    "playwright": "^1.48.0"
  }
}
```

### 参考资源

- **Next.js 16文档**: https://nextjs.org/docs
- **Framer Motion文档**: https://motion.dev/docs
- **shadcn/ui文档**: https://ui.shadcn.com
- **Cyberpunk.css**: https://www.cssscript.com/cyberpunk-2077/
- **ARWES框架**: https://github.com/arwes/arwes
- **WoW游戏界面参考**: https://wowpedia.fandom.com/wiki/Interface_customization

---

**PRP版本**: v1.0.0
**创建日期**: 2025-11-01
**预计完成日期**: 2025-11-29 (4周)
**评估信心等级**: 8.5/10

**评估理由**:
- ✅ 技术栈成熟稳定(Next.js 16, React 19)
- ✅ 已有完整的HTML原型作为参考
- ✅ 智能体数据结构清晰,解析逻辑简单
- ✅ 赛博朋克风格实现方案明确
- ⚠️ WebSocket实时通信需要额外调试
- ⚠️ 60+智能体性能优化需要仔细测试
- ⚠️ 多模态输入功能可能需要额外时间

**风险因素**:
- **中等风险**: Claude API流式响应稳定性
- **中等风险**: 移动端霓虹特效性能
- **低风险**: 文件系统访问权限问题
