---
name: global-plugins-inspector
description: 全局插件可视化查询系统 - 自动扫描和索引全局Claude Code插件（~/.claude/plugins/），提供快速查询和变更检测。当用户询问"有哪些全局插件"、"全局技能包"、"可用的skills"时自动调用。
---

# 全局照见 (Global Plugins Inspector)

## 概述

**全局照见**是一个智能插件管理和查询系统，自动维护全局Claude Code插件的实时索引，提供：

1. **快速查询** - 即时查看所有可用的全局插件、技能包、智能体
2. **自动同步** - 检测全局配置变更，自动更新知识库
3. **结构化索引** - 为每个插件生成详细的元数据和能力清单
4. **智能推荐** - 根据用户需求推荐合适的插件和技能

**宣告语**: "我正在使用'全局照见'技能扫描全局插件配置..."

## 何时使用

**自动调用场景**:
- 用户询问："有哪些全局插件？"
- 用户询问："我能用哪些技能包？"
- 用户询问："全局安装了什么Skills？"
- 用户询问："Anthropic官方插件有哪些？"
- 用户询问："Superpowers Chrome怎么用？"

**手动调用场景**:
- 需要查看全局插件的详细信息
- 检查插件是否需要更新
- 验证插件安装状态
- 生成插件清单报告

## 核心功能

### 1. 插件扫描

扫描以下位置的全局插件：
- `~/.claude/settings.json` - 已启用的插件配置
- `~/.claude/plugins/marketplaces/` - Marketplace插件
- `~/.claude/plugins/cache/` - 缓存插件
- `~/.claude/plugins/installed_plugins.json` - 安装记录

### 2. 知识库管理

维护结构化的插件索引：
- **plugins_registry.json** - 插件注册表（版本、来源、安装路径）
- **skills_index.json** - 技能包索引（名称、描述、功能）
- **agents_index.json** - 智能体索引（如有）
- **last_sync.json** - 同步历史和变更日志

### 3. 智能查询

支持多种查询模式：
- 列出所有全局插件
- 查询特定插件的详细信息
- 搜索包含特定功能的技能包
- 生成插件使用报告

### 4. 自动同步

智能检测变更并更新索引：
- 检查配置文件修改时间
- 对比插件安装记录
- 增量更新知识库
- 记录同步历史

## 使用方法

### 快速查询

直接询问Claude：
```
"有哪些全局插件可用？"
"Anthropic官方Skills有哪些？"
"Superpowers Chrome能做什么？"
```

Claude会自动：
1. 调用全局照见技能
2. 检查知识库是否需要同步
3. 返回结构化的查询结果

### 强制同步

如果你刚刚安装/删除了插件，可以要求强制同步：
```
"同步全局插件配置"
"刷新插件索引"
"重新扫描全局技能包"
```

### 详细查询

查询特定插件的详细信息：
```
"Anthropic Agent Skills包含哪些技能？"
"document-skills能做什么？"
"browsing技能的完整功能列表"
```

## 工作流程

```
用户查询
  ↓
检查知识库是否需要同步
  ↓ YES (检测到变更)
扫描全局插件配置
  ├─ settings.json (启用状态)
  ├─ installed_plugins.json (安装记录)
  ├─ marketplaces/* (插件目录)
  └─ cache/* (缓存插件)
  ↓
提取插件元数据
  ├─ 插件名称、版本、来源
  ├─ 包含的技能包列表
  ├─ 每个技能的描述和功能
  └─ Git commit SHA (追溯性)
  ↓
更新知识库索引
  ├─ plugins_registry.json
  ├─ skills_index.json
  └─ last_sync.json
  ↓
生成查询结果
  ↓
返回给用户
```

## 输出格式

### 插件清单输出

```markdown
# 全局插件清单

## 已启用插件 (2个)

### 1. Anthropic Agent Skills
- **来源**: anthropics/skills (GitHub)
- **版本**: unknown
- **安装位置**: ~/.claude/plugins/marketplaces/anthropic-agent-skills/
- **最后更新**: 2025-10-24
- **包含技能**: 15个
  - example-skills (11个技能)
  - document-skills (4个技能)

**技能列表**:
1. algorithmic-art - 算法艺术生成
2. canvas-design - 视觉艺术设计
3. mcp-builder - MCP服务器开发
...

### 2. Superpowers Chrome
- **来源**: obra/superpowers-marketplace (GitHub)
- **版本**: 1.3.0
- **安装位置**: ~/.claude/plugins/cache/superpowers-chrome/
- **最后更新**: 2025-10-28
- **包含技能**: 1个

**技能列表**:
1. browsing - Chrome浏览器直接控制
   - 17个CLI命令
   - 支持多标签管理、表单自动化、内容提取
```

### 详细技能信息

```markdown
# browsing (Superpowers Chrome)

**描述**: Chrome DevTools Protocol直接控制

**功能**:
- 标签管理: tabs, new, close
- 导航: navigate, wait-for, wait-text
- 交互: click, fill, select
- 提取: eval, extract, attr, html
- 导出: screenshot, markdown

**使用场景**:
- 控制已认证的浏览器会话
- 多标签管理
- 表单自动化
- 内容提取和数据采集

**工具**: mcp__chrome__use_browser
```

## 技术实现

### 核心脚本

- **scripts/plugins_scanner.py** - 插件扫描引擎
  - 读取全局配置文件
  - 遍历插件目录
  - 提取元数据和技能列表

- **scripts/knowledge_base.py** - 知识库管理器
  - 加载/保存索引文件
  - 提供查询接口
  - 生成Markdown报告

- **scripts/sync_manager.py** - 同步管理器
  - 检测配置变更
  - 触发增量更新
  - 记录同步历史

### 知识库结构

```
knowledge/
├── plugins_registry.json    # 插件注册表
├── skills_index.json         # 技能索引
├── agents_index.json         # 智能体索引（预留）
└── last_sync.json           # 同步历史
```

### 变更检测机制

1. **文件修改时间检查**
   - 对比 `settings.json` 的 mtime
   - 对比 `installed_plugins.json` 的 mtime

2. **Git commit SHA比对**
   - 读取 `installed_plugins.json` 中的 gitCommitSha
   - 与知识库中的记录比对

3. **智能增量更新**
   - 仅重新扫描发生变更的插件
   - 保留未变更插件的缓存数据

## 最佳实践

### 何时调用

✅ **推荐调用**:
- 用户明确询问全局插件信息
- 需要推荐合适的技能包
- 生成项目配置文档时

❌ **避免调用**:
- 查询项目级插件（使用项目目录扫描）
- 执行具体的插件功能（直接调用对应技能）
- 修改插件配置（使用 /plugin 命令）

### 性能优化

- 首次调用会进行完整扫描（~2-3秒）
- 后续调用使用缓存索引（<100ms）
- 仅当检测到变更时才重新扫描
- 知识库文件小（通常<50KB）

### 维护建议

- 安装/卸载插件后，下次查询会自动同步
- 可定期手动触发同步确保数据新鲜度
- 知识库文件建议加入 .gitignore（动态生成）

## 故障排除

### 问题：知识库未同步最新插件

**解决方案**:
```
"强制同步全局插件配置"
```
这会忽略缓存，重新扫描所有插件。

### 问题：找不到某个已安装的插件

**检查清单**:
1. 插件是否在 `~/.claude/settings.json` 中启用？
2. 插件目录是否存在？
3. 插件是否有有效的 `plugin.json` 或 SKILL.md？

### 问题：扫描速度慢

**优化方法**:
- 知识库会自动缓存，第二次查询会很快
- 仅在检测到变更时才重新扫描
- 可以查询特定插件而非列出全部

## 扩展性

### 未来功能

- [ ] 插件依赖关系图
- [ ] 插件使用频率统计
- [ ] 自动推荐相关技能包
- [ ] 插件健康度检查
- [ ] 与Claude Code /plugin 命令集成

### 自定义查询

可以在 `scripts/knowledge_base.py` 中添加自定义查询方法，如：
- 按功能分类查询
- 按作者/来源筛选
- 按安装时间排序
- 按更新频率排序

## 参考资源

- **SKILL.md** (本文件) - 快速使用指南
- **reference.md** - 技术实现细节和API文档
- **scripts/README.md** - 脚本使用说明
- **examples/** - 查询示例和输出模板

---

**创建者**: ZTL数智化作战中心
**创建日期**: 2025-10-28
**版本**: v1.0.0
**状态**: ✅ Production Ready

**适用场景**: 全局插件管理、技能发现、配置审计、文档生成
