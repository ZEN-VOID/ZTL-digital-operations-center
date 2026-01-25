# ZTL数智化作战中心 Web-UI

> **Cyberpunk Multi-Agent Orchestration Platform**
> 基于Next.js 16 + React 19的赛博朋克风格智能体编排平台

## 🎯 项目概述

ZTL数智化作战中心Web-UI是一个可视化智能体编排平台,旨在将CLI命令行工具转化为沉浸式的Web应用,降低使用门槛,提升操作体验。

### 核心特性

- ✨ **赛博朋克视觉风格**: 霓虹灯光效、全息投影、数字雨特效
- 🤖 **60+智能体**: 覆盖8大业务组的专业智能体系统
- 🚀 **实时流式响应**: SSE协议实现AI响应流式输出
- 📱 **完全响应式**: 支持桌面/平板/手机全场景
- 🎨 **游戏化交互**: 类似"拳皇选角"的智能体选择体验
- 🔐 **企业级安全**: API密钥认证、速率限制、输入验证

## 🛠️ 技术栈

### 核心框架

- **Next.js 16**: 采用App Router,支持Server Components和Edge Runtime
- **React 19**: 最新版本,改进的并发特性和性能优化
- **TypeScript 5.3+**: 严格类型检查,提供更好的开发体验

### UI & 样式

- **Tailwind CSS v4**: 原子化CSS框架,自定义赛博朋克主题
- **Google Fonts**: Orbitron(标题字体) + Electrolize(正文字体)
- **自定义动画**: 网格移动、全息投影、霓虹脉冲等特效

### 开发工具

- **ESLint**: 代码质量检查
- **Prettier**: 代码格式化
- **TypeScript**: 静态类型检查

## 📦 安装与启动

### 环境要求

- Node.js 18.x 或更高版本
- npm 9.x 或更高版本

### 安装依赖

\`\`\`bash
npm install
\`\`\`

### 配置环境变量

复制 `.env.example` 为 `.env.local` 并填入实际配置:

\`\`\`bash
cp .env.example .env.local
\`\`\`

必需配置:
- `ANTHROPIC_API_KEY`: Claude API密钥

可选配置:
- `COS_*`: 腾讯云COS配置(文件存储)
- `SUPABASE_*`: Supabase配置(数据库+对象存储)

### 启动开发服务器

\`\`\`bash
npm run dev
\`\`\`

访问 http://localhost:3000 查看应用。

### 构建生产版本

\`\`\`bash
npm run build
npm run start
\`\`\`

## 📁 项目结构

\`\`\`
projects/web-ui/
├── app/                    # Next.js App Router
│   ├── layout.tsx         # 根布局
│   ├── page.tsx           # 首页
│   ├── globals.css        # 全局样式
│   └── api/               # API路由
├── components/            # React组件
│   └── ui/               # UI基础组件
├── lib/                  # 工具函数和配置
│   └── utils/            # 通用工具
├── public/               # 静态资源
│   └── images/           # 图片资源
├── types/                # TypeScript类型定义
├── next.config.ts        # Next.js配置
├── tailwind.config.ts    # Tailwind CSS配置
├── tsconfig.json         # TypeScript配置
└── package.json          # 项目依赖
\`\`\`

## 🎨 设计系统

### 色彩方案

\`\`\`css
--neon-pink: #ff00ff      /* 霓虹粉 */
--neon-cyan: #00ffff      /* 霓虹青 */
--neon-purple: #b000ff    /* 霓虹紫 */
--neon-green: #00ff00     /* 霓虹绿 */

--cyber-bg-primary: #0a0a0f    /* 主背景 */
--cyber-bg-secondary: #0f0f23  /* 次背景 */
--cyber-bg-tertiary: #1a0a2e   /* 三级背景 */
\`\`\`

### 字体系统

- **标题字体**: Orbitron (科幻感强)
- **正文字体**: Electrolize (未来主义)

### 动画效果

- `grid-move`: 网格背景移动 (20s)
- `holographic-shine`: 全息投影闪光 (3s)
- `neon-pulse`: 霓虹脉冲 (2s)
- `message-appear`: 消息出现动画 (0.3s)
- `streaming-pulse`: 流式响应脉冲 (1.4s)

## 🔧 开发脚本

\`\`\`bash
npm run dev          # 启动开发服务器
npm run build        # 构建生产版本
npm run start        # 启动生产服务器
npm run lint         # 运行ESLint检查
npm run lint:fix     # 修复ESLint问题
npm run type-check   # TypeScript类型检查
npm run format       # 格式化代码
npm run format:check # 检查代码格式
\`\`\`

## 📚 开发指南

### 添加新页面

在 `app/` 目录下创建新文件夹:

\`\`\`typescript
// app/new-page/page.tsx
export default function NewPage() {
  return <div>New Page Content</div>;
}
\`\`\`

### 添加API端点

在 `app/api/` 目录下创建路由:

\`\`\`typescript
// app/api/hello/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  return NextResponse.json({ message: 'Hello World' });
}
\`\`\`

### 使用赛博朋克样式

应用内置的Tailwind工具类:

\`\`\`tsx
<div className="neon-glow-cyan p-6 rounded-lg">
  <h2 className="neon-text-pink font-orbitron">Cyberpunk Title</h2>
</div>
\`\`\`

## 🧪 测试

### 类型检查

\`\`\`bash
npm run type-check
\`\`\`

### 代码质量检查

\`\`\`bash
npm run lint
\`\`\`

### 构建验证

\`\`\`bash
npm run build
\`\`\`

## 🚀 部署

### Vercel部署(推荐)

1. 将项目推送到GitHub
2. 在Vercel导入项目
3. 配置环境变量
4. 点击部署

### 自托管部署

\`\`\`bash
npm run build
npm run start
\`\`\`

或使用PM2:

\`\`\`bash
pm2 start npm --name "web-ui" -- start
\`\`\`

## 📖 相关文档

- [Next.js 16 文档](https://nextjs.org/docs)
- [React 19 文档](https://react.dev)
- [Tailwind CSS v4 文档](https://tailwindcss.com/docs)
- [TypeScript 文档](https://www.typescriptlang.org/docs)

## 🤝 贡献指南

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 📝 开发日志

### Phase 1 - 项目初始化 (当前)

- [x] Next.js 16项目脚手架
- [x] TypeScript配置
- [x] Tailwind CSS配置
- [x] 赛博朋克设计系统
- [x] 基础页面和布局
- [ ] 智能体解析器
- [ ] API路由实现
- [ ] 组件库开发

### Phase 2 - 核心功能开发

- [ ] 智能体主页
- [ ] 对话界面
- [ ] 资源管理
- [ ] SSE流式响应

### Phase 3 - 集成与优化

- [ ] Claude API集成
- [ ] 云存储集成
- [ ] 性能优化
- [ ] 响应式适配

### Phase 4 - 测试与部署

- [ ] 单元测试
- [ ] E2E测试
- [ ] 生产环境部署
- [ ] 文档完善

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 👥 团队

ZTL开发组 - 全栈开发团队

---

**技术支持**: [GitHub Issues](https://github.com/yourusername/ztl-web-ui/issues)
