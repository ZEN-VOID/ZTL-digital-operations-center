# HTML Design Styles Collection

> 7种现代HTML设计风格技能包，提供从iOS液态玻璃到赛博朋克霓虹的完整设计系统

## 📦 技能包列表

### 1. iOS Liquid Glass (iOS液态玻璃风格)
**路径**: `ios-liquid-glass/`

**特征**:
- iOS风格的液态玻璃效果
- Frosted glass外观
- Backdrop blur和透明度
- 层次深度设计

**应用场景**:
- 模态框和对话框
- 导航栏
- 卡片组件
- iOS风格应用

**关键技术**:
- `backdrop-filter: blur(20px) saturate(180%)`
- `rgba()` 透明度控制
- 多层阴影
- 渐进增强支持

**浏览器支持**: Safari 14+, Chrome 76+, Firefox 103+

---

### 2. Glassmorphism (玻璃拟态)
**路径**: `glassmorphism/`

**特征**:
- 磨砂玻璃表面效果
- 透明度和背景模糊
- 分层设计
- 边框高光

**应用场景**:
- SaaS平台仪表盘
- 现代网站设计
- 卡片布局
- 定价表格

**关键技术**:
- `backdrop-filter: blur(10px)`
- 半透明背景
- 柔和阴影
- 边框渐变

**浏览器支持**: 全现代浏览器 (Chrome 76+)

---

### 3. Neumorphism (新拟物化)
**路径**: `neumorphism/`

**特征**:
- 柔软的浮雕元素
- 双向阴影技术
- 触感式设计
- 更好的对比度和可访问性

**应用场景**:
- 极简工具应用
- 健康和健身应用
- 按钮和表单
- 设置面板

**关键技术**:
- 双阴影 (明+暗)
- 内嵌阴影 (按下状态)
- 单色背景配色
- 柔和圆角

**浏览器支持**: 所有现代浏览器 (基础CSS)

**可访问性**: 改进的对比度设计，符合WCAG AA标准

---

### 4. Neubrutalism (新野兽派)
**路径**: `neubrutalism/`

**特征**:
- 大胆色彩和粗体字
- 锋利线条 (无圆角)
- 粗黑边框
- 偏移阴影

**应用场景**:
- 创意工作室网站
- 艺术平台
- 品牌展示页
- 音乐和活动页面

**关键技术**:
- `border-radius: 0` (尖角)
- 粗边框 (3-5px)
- 偏移阴影 `box-shadow: 8px 8px 0 #000`
- 高对比度配色

**浏览器支持**: 所有浏览器 (简单CSS)

**性能**: 极佳 (无复杂效果)

---

### 5. Dark Mode Premium (高级暗黑模式)
**路径**: `dark-mode-premium/`

**特征**:
- 精致的暗色主题
- 保持品牌识别
- 减少眼疲劳
- 战略性点缀色

**应用场景**:
- 所有类型网站/应用
- SaaS仪表盘
- 开发者工具
- 内容管理系统

**关键技术**:
- CSS变量系统
- 分层背景 (`#0f0f0f → #1a1a1a → #242424`)
- 微妙渐变
- 系统偏好检测 `@media (prefers-color-scheme: dark)`

**浏览器支持**: 全现代浏览器

**可访问性**: WCAG AA合规，13.5:1对比度

---

### 6. Cyberpunk Neon (赛博朋克霓虹)
**路径**: `cyberpunk-neon/`

**特征**:
- 霓虹色彩 (粉/紫/青)
- 暗背景
- 发光效果
- 复古未来主义动画

**应用场景**:
- 科技网站
- 游戏界面
- 音乐平台
- 沉浸式体验

**关键技术**:
- 多层文字阴影发光
- 网格背景动画
- 扫描线效果
- 故障艺术 (glitch effect)

**浏览器支持**: 现代浏览器 (部分效果需Chrome 55+)

**性能考虑**: 限制动画层数，使用GPU加速

---

### 7. Minimalist Gradient (极简渐变)
**路径**: `minimalist-gradient/`

**特征**:
- 简洁布局
- 柔和渐变
- 柔和色板
- 战略性粗体点缀

**应用场景**:
- 企业网站
- 产品展示
- 创业公司主页
- 专业服务网站

**关键技术**:
- CSS渐变 (无图片)
- 文字渐变 `background-clip: text`
- 8px网格系统
- 大量留白

**浏览器支持**: 所有现代浏览器

**性能**: 优秀 (纯CSS，无资源加载)

---

## 🎨 快速对比

| 风格 | 视觉风格 | 复杂度 | 性能 | 可访问性 | 适用场景 |
|-----|---------|-------|------|---------|---------|
| **iOS Liquid Glass** | 现代、透明 | 中 | 良好 | AA | 模态框、导航栏 |
| **Glassmorphism** | 时尚、磨砂 | 中 | 良好 | AA | SaaS平台、卡片 |
| **Neumorphism** | 柔和、触感 | 低 | 优秀 | AA | 极简工具、表单 |
| **Neubrutalism** | 大胆、原始 | 低 | 优秀 | AAA | 创意工作室 |
| **Dark Mode Premium** | 精致、暗色 | 中 | 优秀 | AA/AAA | 所有应用 |
| **Cyberpunk Neon** | 炫酷、霓虹 | 高 | 中等 | 需注意 | 游戏、科技网站 |
| **Minimalist Gradient** | 简洁、专业 | 低 | 优秀 | AA | 企业、产品页 |

## 🚀 使用指南

### 基础使用

每个技能包都包含：

1. **SKILL.md** - 完整文档
   - Quick Start 快速开始
   - 核心CSS原理
   - 自定义选项
   - 浏览器兼容性
   - 可访问性指南

2. **templates/** - 示例模板
   - `complete.html` - 完整页面
   - `components.html` - 组件库
   - `minimal.html` - 最小实现

3. **scripts/** (可选) - Python生成器

### Claude Code集成

这些技能包已集成到Claude Code系统，可通过关键词自动触发：

```
"设计一个iOS风格的模态框" → ios-liquid-glass
"创建玻璃拟态卡片" → glassmorphism
"制作赛博朋克风格页面" → cyberpunk-neon
"生成极简渐变网站" → minimalist-gradient
```

### 自定义建议

1. **颜色**: 调整CSS变量中的颜色值
2. **间距**: 修改padding/margin遵循8px网格
3. **圆角**: 根据品牌调整border-radius
4. **阴影**: 根据需要增减box-shadow层数

## ✅ 技术标准

所有技能包遵循：

- ✅ **响应式设计** - Mobile-first approach
- ✅ **可访问性** - WCAG 2.1 AA标准
- ✅ **浏览器兼容** - 现代浏览器全支持
- ✅ **性能优化** - GPU加速，减少重绘
- ✅ **渐进增强** - 优雅降级fallback
- ✅ **减少动画** - `prefers-reduced-motion` 支持

## 📚 设计参考

### 灵感来源

- **iOS Liquid Glass**: Apple iOS 15+ 设计语言
- **Glassmorphism**: Dribbble 2020-2023 流行趋势
- **Neumorphism**: 2019-2020 UI设计运动
- **Neubrutalism**: 野兽派建筑 + 瑞士设计
- **Dark Mode Premium**: Material Design 3, GitHub Dark
- **Cyberpunk Neon**: 赛博朋克2077, Blade Runner
- **Minimalist Gradient**: Apple产品页, Stripe

### 推荐工具

- **渐变生成**: [uigradients.com](https://uigradients.com)
- **配色工具**: [coolors.co](https://coolors.co)
- **对比度检查**: [contrast-ratio.com](https://contrast-ratio.com)
- **阴影生成**: [shadows.brumm.af](https://shadows.brumm.af)

## 🔗 相关技能包

- **AIGC图像生成**: `.claude/skills/aigc/text-to-image/`
- **Figma设计**: `.claude/skills/figma/`
- **数据可视化**: 使用 `/J` 命令

## 📝 版本历史

**v1.0.0** (2025-10-21)
- ✅ 创建7个完整HTML设计风格技能包
- ✅ 每个包含SKILL.md + templates/
- ✅ 符合F5-Skills创建工程师标准
- ✅ 遵循渐进披露原则
- ✅ 自包含设计，无外部依赖

## 🤝 贡献指南

添加新设计风格时：

1. 遵循kebab-case命名
2. 创建SKILL.md（包含YAML frontmatter）
3. 提供至少3个HTML模板
4. 确保WCAG AA可访问性
5. 测试跨浏览器兼容性
6. 更新本README

## 📄 许可证

MIT License - 可自由用于商业和个人项目

---

**创建日期**: 2025-10-21
**技术栈**: HTML5 + CSS3 + Pure CSS (无JavaScript依赖)
**兼容性**: Chrome 76+, Safari 14+, Firefox 103+, Edge 79+
**维护者**: ZTL数智化作战中心 F5-Skills工程师
