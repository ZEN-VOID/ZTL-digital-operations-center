# 全局照见 - 技术参考文档

> 详细的技术实现、API文档和扩展指南

---

## 📚 目录

- [架构设计](#架构设计)
- [核心模块API](#核心模块api)
- [知识库结构](#知识库结构)
- [同步机制](#同步机制)
- [扩展开发](#扩展开发)
- [性能优化](#性能优化)
- [故障排查](#故障排查)

---

## 架构设计

### 三层架构

```
┌─────────────────────────────────────┐
│  用户交互层 (User Interaction)      │
│  - Claude对话接口                    │
│  - 自然语言查询                      │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  业务逻辑层 (Business Logic)        │
│  - KnowledgeBase (查询接口)         │
│  - SyncManager (同步管理)           │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  数据采集层 (Data Collection)       │
│  - PluginsScanner (插件扫描)        │
│  - 配置文件解析                      │
│  - 目录结构遍历                      │
└─────────────────────────────────────┘
```

### 数据流

```
全局配置文件
├─ ~/.claude/settings.json
├─ ~/.claude/plugins/installed_plugins.json
└─ ~/.claude/plugins/marketplaces/*
   └─ ~/.claude/plugins/cache/*
         ↓
   [PluginsScanner]
         ↓
   插件注册表 (JSON)
         ↓
   [KnowledgeBase]
         ↓
   结构化查询结果 (Markdown)
         ↓
   返回给用户
```

---

## 核心模块API

### PluginsScanner

**类**: `PluginsScanner`

#### 初始化

```python
from plugins_scanner import PluginsScanner

scanner = PluginsScanner()
```

#### 方法

**scan_all() -> Dict[str, Any]**

扫描所有全局插件，返回完整的插件注册表。

```python
result = scanner.scan_all()
# result = {
#     "scan_time": "2025-10-28T21:17:53.985908",
#     "total_plugins": 2,
#     "enabled_plugins": 2,
#     "total_skills": 12,
#     "total_agents": 0,
#     "plugins": {
#         "plugin-id": {
#             "plugin_id": str,
#             "enabled": bool,
#             "version": str,
#             "install_path": str,
#             "skills": List[Dict],
#             "agents": List[Dict],
#             ...
#         }
#     }
# }
```

**返回结构**:
- `scan_time`: ISO格式的扫描时间戳
- `total_plugins`: 插件总数
- `enabled_plugins`: 已启用的插件数
- `total_skills`: 技能包总数
- `total_agents`: 智能体总数
- `plugins`: 插件详细信息字典

---

### KnowledgeBase

**类**: `KnowledgeBase`

#### 初始化

```python
from knowledge_base import KnowledgeBase

kb = KnowledgeBase()  # 使用默认路径
# 或指定自定义路径
kb = KnowledgeBase(knowledge_dir=Path("/custom/path"))
```

#### 核心方法

**load_plugins_registry() -> Optional[Dict[str, Any]]**

加载插件注册表。

```python
registry = kb.load_plugins_registry()
if registry:
    print(f"Total plugins: {registry['total_plugins']}")
```

**save_plugins_registry(registry: Dict[str, Any])**

保存插件注册表。

```python
kb.save_plugins_registry(registry)
```

**build_skills_index(registry: Dict[str, Any]) -> Dict[str, Any]**

从插件注册表构建技能包索引。

```python
skills_index = kb.build_skills_index(registry)
# skills_index = {
#     "build_time": "2025-10-28T21:17:53.986457",
#     "total_skills": 12,
#     "skills": {
#         "skill-id": {
#             "skill_id": str,
#             "display_name": str,
#             "description": str,
#             "plugin_id": str,
#             ...
#         }
#     }
# }
```

#### 查询方法

**query_all_plugins() -> str**

查询所有插件，返回Markdown格式的报告。

```python
report = kb.query_all_plugins()
print(report)
```

**query_plugin_by_id(plugin_id: str) -> str**

查询特定插件的详细信息。

```python
details = kb.query_plugin_by_id("example-skills@anthropic-agent-skills")
print(details)
```

**query_skill_by_id(skill_id: str) -> str**

查询特定技能包的详细信息。

```python
skill_info = kb.query_skill_by_id("browsing")
print(skill_info)
```

**search_skills(keyword: str) -> str**

搜索包含特定关键词的技能包。

```python
results = kb.search_skills("browser")
print(results)
```

**generate_summary_report() -> str**

生成摘要报告。

```python
summary = kb.generate_summary_report()
print(summary)
```

---

### SyncManager

**类**: `SyncManager`

#### 初始化

```python
from sync_manager import SyncManager

manager = SyncManager()
```

#### 方法

**check_need_sync(force: bool = False) -> Tuple[bool, str]**

检查是否需要同步。

```python
need_sync, reason = manager.check_need_sync()
if need_sync:
    print(f"需要同步: {reason}")
```

**sync(force: bool = False) -> Dict[str, Any]**

执行同步。

```python
result = manager.sync(force=True)
if result["synced"]:
    print("同步成功")
    print(f"总技能包: {result['registry']['total_skills']}")
```

**get_sync_status() -> str**

获取同步状态的Markdown报告。

```python
status = manager.get_sync_status()
print(status)
```

---

## 知识库结构

### 文件组织

```
.claude/skills/全局照见/
├── SKILL.md                    # 技能包元数据
├── reference.md                # 本文档
├── scripts/                    # 执行引擎
│   ├── plugins_scanner.py      # 插件扫描器
│   ├── knowledge_base.py       # 知识库管理器
│   └── sync_manager.py         # 同步管理器
├── knowledge/                  # 知识库（动态生成）
│   ├── plugins_registry.json   # 插件注册表
│   ├── skills_index.json       # 技能包索引
│   └── last_sync.json         # 同步记录
└── examples/                   # 使用示例
    └── query_examples.md
```

### plugins_registry.json 结构

```json
{
  "scan_time": "2025-10-28T21:17:53.985908",
  "total_plugins": 2,
  "enabled_plugins": 2,
  "total_skills": 12,
  "total_agents": 0,
  "plugins": {
    "example-skills@anthropic-agent-skills": {
      "plugin_id": "example-skills@anthropic-agent-skills",
      "enabled": true,
      "version": "unknown",
      "install_path": "~/.claude/plugins/marketplaces/anthropic-agent-skills/",
      "installed_at": "2025-10-24T02:15:49.458Z",
      "last_updated": "2025-10-24T02:15:49.458Z",
      "git_commit_sha": "c74d647e56e6daa12029b6acb11a821348ad044b",
      "is_local": true,
      "source": "anthropic-agent-skills",
      "skills": [
        {
          "skill_id": "algorithmic-art",
          "display_name": "Algorithmic Art",
          "description": "Creating algorithmic art using p5.js...",
          "allowed_tools": "",
          "file_path": "~/.claude/plugins/.../algorithmic-art/SKILL.md",
          "skill_path": "~/.claude/plugins/.../algorithmic-art"
        }
      ],
      "agents": [],
      "commands": [],
      "metadata": {
        "readme_excerpt": "# Skills\nSkills are folders of instructions..."
      }
    }
  }
}
```

### skills_index.json 结构

```json
{
  "build_time": "2025-10-28T21:17:53.986457",
  "total_skills": 12,
  "skills": {
    "algorithmic-art": {
      "skill_id": "algorithmic-art",
      "display_name": "Algorithmic Art",
      "description": "Creating algorithmic art using p5.js...",
      "allowed_tools": "",
      "file_path": "~/.claude/plugins/.../algorithmic-art/SKILL.md",
      "skill_path": "~/.claude/plugins/.../algorithmic-art",
      "plugin_id": "example-skills@anthropic-agent-skills",
      "plugin_source": "anthropic-agent-skills"
    }
  }
}
```

### last_sync.json 结构

```json
{
  "sync_time": "2025-10-28T21:17:53.986457",
  "scan_duration_seconds": 0.0012,
  "trigger_reason": "用户强制同步",
  "total_plugins": 2,
  "total_skills": 12,
  "total_agents": 0,
  "git_commits": {
    "example-skills@anthropic-agent-skills": "c74d647e56e6daa12029b6acb11a821348ad044b",
    "superpowers-chrome@superpowers-marketplace": "5ba8f8b5031b76bbb6feec7a6714938618a9669c"
  }
}
```

---

## 同步机制

### 变更检测策略

**1. 文件修改时间检查**

```python
# 检查settings.json
settings_mtime = settings_file.stat().st_mtime
if datetime.fromtimestamp(settings_mtime) > last_sync_time:
    trigger_sync("settings.json已更新")

# 检查installed_plugins.json
installed_mtime = installed_file.stat().st_mtime
if datetime.fromtimestamp(installed_mtime) > last_sync_time:
    trigger_sync("installed_plugins.json已更新")
```

**2. Git Commit SHA比对**

```python
# 读取当前commit
current_sha = plugin_info.get("gitCommitSha")

# 与上次同步记录比对
previous_sha = sync_record["git_commits"].get(plugin_id)

if current_sha != previous_sha:
    trigger_sync("检测到Git commit变更")
```

**3. 首次运行检测**

```python
# 检查知识库是否存在
if not plugins_registry_file.exists():
    trigger_sync("知识库未初始化")
```

### 同步触发场景

| 场景 | 触发条件 | 同步类型 |
|------|---------|---------|
| 首次使用 | 知识库文件不存在 | 完整同步 |
| 安装新插件 | `installed_plugins.json`修改时间变更 | 完整同步 |
| 启用/禁用插件 | `settings.json`修改时间变更 | 完整同步 |
| 插件更新 | Git commit SHA变更 | 完整同步 |
| 强制同步 | 用户调用`--force` | 完整同步 |

### 同步性能

- **平均扫描时间**: 0.001-0.01秒（12个技能包）
- **知识库大小**: ~10-50KB（JSON文件）
- **内存占用**: <5MB（Python进程）
- **缓存命中率**: >95%（正常使用）

---

## 扩展开发

### 添加新的查询方法

在`knowledge_base.py`中添加自定义查询：

```python
def query_skills_by_category(self, category: str) -> str:
    """按分类查询技能包"""
    skills_index = self.load_skills_index()
    if not skills_index:
        return "⚠️ 技能包索引未初始化"

    matches = []
    for skill_id, skill in skills_index["skills"].items():
        # 自定义分类逻辑
        if category.lower() in skill.get("description", "").lower():
            matches.append(skill)

    # 生成Markdown报告
    output = [f"# {category} 类别的技能包\n"]
    for skill in matches:
        output.append(f"- **{skill['skill_id']}**: {skill['description']}")

    return "\n".join(output)
```

### 添加新的扫描规则

在`plugins_scanner.py`中扩展扫描逻辑：

```python
def _scan_custom_metadata(self, plugin_path: Path) -> Dict[str, Any]:
    """扫描自定义元数据"""
    metadata = {}

    # 示例：扫描plugin.json
    plugin_json = plugin_path / "plugin.json"
    if plugin_json.exists():
        with open(plugin_json, 'r') as f:
            data = json.load(f)
            metadata["plugin_version"] = data.get("version")
            metadata["plugin_author"] = data.get("author")

    return metadata
```

### 自定义同步策略

在`sync_manager.py`中添加自定义同步条件：

```python
def check_custom_condition(self) -> bool:
    """自定义同步条件检查"""
    # 示例：每天自动同步一次
    sync_record = self.kb.load_sync_record()
    if not sync_record:
        return True

    last_sync = datetime.fromisoformat(sync_record["sync_time"])
    now = datetime.now()

    if (now - last_sync).days >= 1:
        return True

    return False
```

---

## 性能优化

### 1. 渐进加载

技能包采用渐进披露原则：
- **Level 1**: 仅加载YAML frontmatter（~50 tokens）
- **Level 2**: 按需加载SKILL.md全文（~500-2000 tokens）
- **Level 3**: 仅在需要时加载reference.md（~1000-5000 tokens）

### 2. 缓存策略

```python
# 知识库文件缓存在磁盘
# 避免重复扫描
if not need_sync:
    return cached_registry  # 直接返回缓存
```

### 3. 并行扫描

可以改进为并行扫描多个插件（未来优化）：

```python
from concurrent.futures import ThreadPoolExecutor

def scan_all_parallel(self):
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(self._scan_plugin, plugin_id, install_info)
            for plugin_id, install_info in installed_plugins.items()
        ]
        results = [f.result() for f in futures]
    return results
```

### 4. 增量更新

检测变更后仅更新变更的插件（未来优化）：

```python
def sync_incremental(self):
    changed_plugins = self._detect_changes()
    for plugin_id in changed_plugins:
        self._update_plugin(plugin_id)
```

---

## 故障排查

### 问题1: 扫描不到某个插件

**症状**: `total_plugins`数量不对，或某个已安装插件未出现

**排查步骤**:

1. 检查插件是否在`installed_plugins.json`中
   ```bash
   cat ~/.claude/plugins/installed_plugins.json | jq '.plugins | keys'
   ```

2. 检查安装路径是否存在
   ```bash
   ls -la ~/.claude/plugins/marketplaces/
   ls -la ~/.claude/plugins/cache/
   ```

3. 手动运行扫描器查看详细日志
   ```bash
   cd .claude/skills/全局照见/scripts
   python3 plugins_scanner.py
   ```

### 问题2: 技能包数量不对

**症状**: `total_skills`数量少于预期

**排查步骤**:

1. 检查插件目录结构
   ```bash
   # Anthropic Agent Skills结构
   ls ~/.claude/plugins/marketplaces/anthropic-agent-skills/

   # 应该看到多个子目录，每个是一个skill
   # algorithmic-art/, canvas-design/, etc.
   ```

2. 检查SKILL.md文件是否存在
   ```bash
   find ~/.claude/plugins -name "SKILL.md"
   ```

3. 查看扫描器日志
   ```bash
   python3 plugins_scanner.py 2>&1 | grep "技能包:"
   ```

### 问题3: 同步不触发

**症状**: 安装新插件后，知识库未更新

**解决方案**:

1. 强制同步
   ```bash
   cd .claude/skills/全局照见/scripts
   python3 sync_manager.py --force
   ```

2. 检查同步状态
   ```bash
   python3 sync_manager.py --status
   ```

3. 清空知识库重新生成
   ```bash
   rm -rf ../knowledge/*.json
   python3 sync_manager.py --force
   ```

### 问题4: 知识库文件损坏

**症状**: JSON解析错误

**解决方案**:

```bash
# 备份现有文件
cd .claude/skills/全局照见/knowledge
cp plugins_registry.json plugins_registry.json.backup

# 验证JSON格式
python3 -m json.tool plugins_registry.json

# 如果损坏，删除并重新生成
cd ../scripts
rm -rf ../knowledge/*.json
python3 sync_manager.py --force
```

---

## 命令行工具

### plugins_scanner.py

**用法**:
```bash
python3 plugins_scanner.py
```

**输出**: JSON格式的完整插件注册表

### knowledge_base.py

**用法**:
```bash
python3 knowledge_base.py
```

**输出**: 所有插件的Markdown报告和摘要

### sync_manager.py

**用法**:
```bash
# 智能同步（仅在需要时）
python3 sync_manager.py

# 强制同步
python3 sync_manager.py --force

# 查看同步状态
python3 sync_manager.py --status
```

---

## 最佳实践

### 1. 定期同步

建议每周手动触发一次同步，确保知识库最新：

```bash
cd .claude/skills/全局照见/scripts
python3 sync_manager.py --force
```

### 2. 版本控制策略

知识库文件（`knowledge/*.json`）建议加入`.gitignore`：

```gitignore
# .gitignore
.claude/skills/全局照见/knowledge/*.json
```

原因：这些是动态生成的文件，每个开发者的全局插件配置不同。

### 3. CI/CD集成

如果需要在CI环境中使用，可以添加初始化步骤：

```yaml
# .github/workflows/test.yml
- name: Initialize Global Plugins Knowledge Base
  run: |
    cd .claude/skills/全局照见/scripts
    python3 sync_manager.py --force
```

### 4. 监控知识库健康度

定期检查知识库文件大小和完整性：

```bash
# 检查文件大小
du -h .claude/skills/全局照见/knowledge/

# 验证JSON格式
for file in .claude/skills/全局照见/knowledge/*.json; do
  echo "Validating $file..."
  python3 -m json.tool "$file" > /dev/null && echo "✅ OK" || echo "❌ INVALID"
done
```

---

## 未来改进

### 计划中的功能

- [ ] **插件依赖关系图** - 可视化插件之间的依赖关系
- [ ] **使用频率统计** - 追踪每个技能包的调用次数
- [ ] **智能推荐系统** - 根据用户查询推荐相关技能包
- [ ] **插件健康度检查** - 检测过期、损坏或不兼容的插件
- [ ] **自动更新通知** - 检测插件更新并通知用户
- [ ] **多语言支持** - 支持中英文双语查询

### 社区贡献

欢迎贡献代码和改进建议：
1. Fork项目
2. 创建功能分支
3. 提交Pull Request

---

**版本**: v1.0.0
**最后更新**: 2025-10-28
**维护者**: ZTL数智化作战中心
