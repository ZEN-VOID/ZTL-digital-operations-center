# 全局照见 (Global Plugins Inspector)

> 智能全局插件可视化查询系统 - 自动扫描、索引和查询Claude Code全局插件

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Status](https://img.shields.io/badge/status-production-green)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)

---

## 🌟 核心特性

- ✅ **自动扫描** - 实时检测全局插件配置变更
- ✅ **智能索引** - 结构化技能包、智能体、命令清单
- ✅ **快速查询** - Markdown格式的即时查询结果
- ✅ **自动同步** - 智能变更检测，按需更新知识库
- ✅ **零配置** - 开箱即用，无需手动设置

---

## 📦 扫描范围

| 配置项 | 路径 | 说明 |
|--------|------|------|
| 启用插件 | `~/.claude/settings.json` | 当前启用的插件列表 |
| 安装记录 | `~/.claude/plugins/installed_plugins.json` | 插件安装信息和版本 |
| Marketplace插件 | `~/.claude/plugins/marketplaces/*` | 官方市场插件 |
| 缓存插件 | `~/.claude/plugins/cache/*` | 第三方缓存插件 |

---

## 🚀 快速开始

### 自动使用（推荐）

直接询问Claude：

```
"有哪些全局插件可用？"
"Anthropic官方Skills有哪些？"
"browsing技能能做什么？"
```

Claude会自动：
1. 调用**全局照见**技能
2. 检查知识库是否需要同步
3. 返回结构化查询结果

### 手动同步

如果刚安装/删除了插件：

```bash
cd .claude/skills/全局照见/scripts
python3 sync_manager.py --force
```

---

## 📊 当前扫描结果

**最后同步**: 2025-10-28 21:17:53

**统计信息**:
- 📦 总插件数: 2
- ✅ 已启用: 2
- 🎯 总技能包: 12
- 🤖 总智能体: 0

**已安装插件**:
1. **example-skills@anthropic-agent-skills** (11个技能包)
   - Anthropic官方示例技能集
   - 包含：algorithmic-art, canvas-design, mcp-builder等

2. **superpowers-chrome@superpowers-marketplace** (1个技能包)
   - Chrome浏览器控制工具
   - 包含：browsing (17个CLI命令)

---

## 🎯 使用场景

### 1. 插件发现

**场景**: 刚开始使用Claude Code，想了解有哪些可用工具

**提问**: "我能用哪些全局插件和技能包？"

**返回**: 完整的插件清单，包括每个技能包的描述和功能

### 2. 功能查询

**场景**: 需要某个特定功能，不确定是否有现成技能包

**提问**: "有没有关于浏览器自动化的技能？"

**返回**: 搜索结果显示`browsing`技能，包含完整功能说明

### 3. 配置审计

**场景**: 检查当前全局配置状态

**提问**: "生成全局插件摘要报告"

**返回**: 统计信息、插件列表、同步状态

### 4. 文档生成

**场景**: 为项目生成插件清单文档

**提问**: "导出所有全局插件的详细信息"

**返回**: 可用于项目文档的完整Markdown报告

---

## 📁 目录结构

```
.claude/skills/全局照见/
├── SKILL.md                    # 技能包元数据和使用指南
├── README.md                   # 本文档
├── reference.md                # 技术参考文档
│
├── scripts/                    # 执行引擎
│   ├── __init__.py
│   ├── plugins_scanner.py      # 插件扫描器
│   ├── knowledge_base.py       # 知识库管理器
│   └── sync_manager.py         # 同步管理器
│
├── knowledge/                  # 知识库（动态生成）
│   ├── plugins_registry.json   # 插件注册表
│   ├── skills_index.json       # 技能包索引
│   └── last_sync.json         # 同步记录
│
└── examples/                   # 使用示例
    └── query_examples.md
```

---

## 🔧 技术架构

### 三层架构

```
用户交互层 (Claude对话)
    ↓
业务逻辑层 (KnowledgeBase + SyncManager)
    ↓
数据采集层 (PluginsScanner)
```

### 同步机制

| 触发条件 | 检测方式 | 同步类型 |
|----------|---------|---------|
| 首次使用 | 知识库不存在 | 完整同步 |
| 安装新插件 | `installed_plugins.json`修改时间 | 完整同步 |
| 启用/禁用插件 | `settings.json`修改时间 | 完整同步 |
| 插件更新 | Git commit SHA变更 | 完整同步 |
| 强制同步 | 用户调用`--force` | 完整同步 |

---

## 📚 文档索引

- **SKILL.md** - 快速使用指南（Claude自动加载）
- **README.md** - 本文档（项目概览）
- **reference.md** - 技术参考文档（API、扩展开发）
- **examples/query_examples.md** - 查询示例集合

---

## 🛠️ 命令行工具

### 同步管理

```bash
# 智能同步（仅在需要时）
python3 scripts/sync_manager.py

# 强制同步（忽略检查）
python3 scripts/sync_manager.py --force

# 查看同步状态
python3 scripts/sync_manager.py --status
```

### 直接扫描

```bash
# 扫描并输出JSON
python3 scripts/plugins_scanner.py

# 查询并输出Markdown
python3 scripts/knowledge_base.py
```

---

## 🔍 查询示例

### 基础查询

```python
from knowledge_base import KnowledgeBase

kb = KnowledgeBase()

# 查询所有插件
print(kb.query_all_plugins())

# 查询特定插件
print(kb.query_plugin_by_id("example-skills@anthropic-agent-skills"))

# 搜索技能包
print(kb.search_skills("browser"))

# 生成摘要报告
print(kb.generate_summary_report())
```

### 通过Claude查询

```
# 列出所有插件
"有哪些全局插件？"

# 查询特定插件
"Anthropic Agent Skills包含哪些技能？"

# 搜索功能
"有没有设计相关的技能包？"

# 生成报告
"生成全局插件摘要报告"
```

---

## ⚙️ 配置选项

### 自定义知识库路径

```python
from pathlib import Path
from knowledge_base import KnowledgeBase

custom_kb = KnowledgeBase(knowledge_dir=Path("/custom/path"))
```

### 扩展扫描规则

编辑`scripts/plugins_scanner.py`，添加自定义扫描逻辑：

```python
def _scan_custom_metadata(self, plugin_path: Path):
    # 自定义元数据提取
    pass
```

---

## 🐛 故障排查

### 问题：扫描不到某个插件

**解决方案**:
```bash
# 检查安装记录
cat ~/.claude/plugins/installed_plugins.json | jq '.plugins | keys'

# 强制重新扫描
python3 scripts/sync_manager.py --force
```

### 问题：知识库未同步

**解决方案**:
```bash
# 清空并重新生成
rm -rf knowledge/*.json
python3 scripts/sync_manager.py --force
```

---

## 🚧 路线图

### v1.1.0 (计划中)

- [ ] 插件依赖关系图
- [ ] 使用频率统计
- [ ] 智能推荐系统
- [ ] 插件健康度检查

### v1.2.0 (未来)

- [ ] 自动更新通知
- [ ] 多语言支持
- [ ] Web UI界面
- [ ] 批量插件管理

---

## 📄 许可证

MIT License

---

## 🤝 贡献

欢迎提交Issue和Pull Request！

**开发指南**:
1. Fork项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

---

## 📞 支持

- **Issue反馈**: GitHub Issues
- **文档**: [reference.md](reference.md)
- **示例**: [examples/](examples/)

---

**创建者**: ZTL数智化作战中心
**版本**: v1.0.0
**创建日期**: 2025-10-28
**状态**: ✅ Production Ready

**适用场景**: 全局插件管理、技能发现、配置审计、文档生成
