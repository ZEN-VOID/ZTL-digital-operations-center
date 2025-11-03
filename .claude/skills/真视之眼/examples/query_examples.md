# 全局照见 - 查询示例集

> 实用的查询示例和最佳实践

---

## 📋 目录

- [基础查询](#基础查询)
- [高级查询](#高级查询)
- [插件管理](#插件管理)
- [报告生成](#报告生成)
- [命令行使用](#命令行使用)

---

## 基础查询

### 示例1: 列出所有全局插件

**用户提问**:
```
"有哪些全局插件可用？"
```

**Claude响应**:
```markdown
# 全局插件清单

**扫描时间**: 2025-10-28T21:17:53.985908
**总插件数**: 2
**已启用**: 2
**总技能包**: 12
**总智能体**: 0

## 1. example-skills@anthropic-agent-skills
- **状态**: ✅ 已启用
- **版本**: unknown
- **来源**: anthropic-agent-skills
- **技能包** (11个)

## 2. superpowers-chrome@superpowers-marketplace
- **状态**: ✅ 已启用
- **版本**: 1.3.0
- **来源**: superpowers-marketplace
- **技能包** (1个)
```

---

### 示例2: 查询特定插件详情

**用户提问**:
```
"Anthropic Agent Skills包含哪些技能？"
```

**Claude响应**:
```markdown
# example-skills@anthropic-agent-skills

**状态**: ✅ 已启用
**版本**: unknown
**来源**: anthropic-agent-skills

## 技能包 (11个)

### algorithmic-art
**ID**: `algorithmic-art`
**描述**: Creating algorithmic art using p5.js...

### canvas-design
**ID**: `canvas-design`
**描述**: Create beautiful visual art in .png and .pdf...

... (更多技能包)
```

---

### 示例3: 搜索特定功能

**用户提问**:
```
"有没有关于浏览器自动化的技能包？"
```

**Claude响应**:
```markdown
# 搜索结果: 'browser'

找到 1 个匹配的技能包:

## browsing
**ID**: `browsing`
**插件**: superpowers-chrome@superpowers-marketplace
**描述**: Use when you need direct browser control...
```

---

## 高级查询

### 示例4: 按关键词搜索

**用户提问**:
```
"搜索所有与艺术设计相关的技能包"
```

**Claude行为**:
1. 调用`search_skills("art")`
2. 返回匹配结果：
   - algorithmic-art
   - canvas-design
   - artifacts-builder
   - theme-factory

---

### 示例5: 查询特定技能的详细信息

**用户提问**:
```
"browsing技能的完整功能列表"
```

**Claude响应**:
```markdown
# browsing (Superpowers Chrome)

**描述**: Chrome DevTools Protocol直接控制

**功能**:
- 标签管理: tabs, new, close
- 导航: navigate, wait-for, wait-text
- 交互: click, fill, select
- 提取: eval, extract, attr, html
- 导出: screenshot, markdown

**工具**: mcp__chrome__use_browser
```

---

## 插件管理

### 示例6: 检查同步状态

**用户提问**:
```
"全局插件配置是否是最新的？"
```

**Claude行为**:
1. 调用`check_need_sync()`
2. 检查配置文件修改时间
3. 返回同步状态报告

---

### 示例7: 强制同步

**用户提问**:
```
"刷新全局插件索引"
"同步全局插件配置"
"重新扫描全局技能包"
```

**Claude行为**:
1. 调用`sync(force=True)`
2. 重新扫描所有插件
3. 更新知识库
4. 返回同步结果

---

## 报告生成

### 示例8: 生成摘要报告

**用户提问**:
```
"生成全局插件摘要报告"
```

**Claude响应**:
```markdown
# 全局插件摘要报告

## 📊 统计信息

- **总插件数**: 2
- **已启用**: 2
- **总技能包**: 12
- **总智能体**: 0
- **扫描时间**: 2025-10-28T21:17:53.985908

## 📦 已安装插件

- ✅ **example-skills@anthropic-agent-skills** (vunknown) - 11 个技能包
- ✅ **superpowers-chrome@superpowers-marketplace** (v1.3.0) - 1 个技能包

## 🎯 技能包分类

共 12 个技能包:
- **algorithmic-art** (example-skills@anthropic-agent-skills)
- **canvas-design** (example-skills@anthropic-agent-skills)
- **browsing** (superpowers-chrome@superpowers-marketplace)
...
```

---

### 示例9: 导出插件清单

**用户提问**:
```
"为项目文档生成全局插件清单"
```

**Claude行为**:
1. 调用`query_all_plugins()`
2. 格式化为项目文档格式
3. 包含每个插件的详细信息
4. 可选：保存为Markdown文件

---

## 命令行使用

### 示例10: 直接扫描插件

```bash
cd .claude/skills/全局照见/scripts

# 运行扫描器
python3 plugins_scanner.py
```

**输出**: JSON格式的完整插件注册表

---

### 示例11: 智能同步

```bash
# 仅在需要时同步
python3 sync_manager.py
```

**输出示例**:
```
✅ 知识库已是最新，无需同步
```

或

```
🔄 开始同步: settings.json已更新
🔍 开始扫描全局插件...
✅ 同步完成，耗时 0.01 秒
```

---

### 示例12: 强制同步

```bash
# 忽略检查，强制同步
python3 sync_manager.py --force
```

**输出**:
```
🔄 开始同步: 用户强制同步
🔍 开始扫描全局插件...
   已启用插件: 2 个
   已安装插件: 2 个

   📦 扫描: example-skills@anthropic-agent-skills
      技能包: 11 个

   📦 扫描: superpowers-chrome@superpowers-marketplace
      技能包: 1 个

✅ 扫描完成:
   总插件数: 2
   已启用: 2
   总技能包: 12

✅ 同步完成，耗时 0.01 秒
```

---

### 示例13: 查看同步状态

```bash
python3 sync_manager.py --status
```

**输出**:
```markdown
# 同步状态

**最后同步**: 2025-10-28T21:17:53.986457
**触发原因**: 用户强制同步
**扫描耗时**: 0.01 秒
**插件数量**: 2
**技能包数量**: 12
**智能体数量**: 0

**当前状态**: ✅ 已是最新
```

---

## Python API使用

### 示例14: 查询所有插件

```python
from knowledge_base import KnowledgeBase

kb = KnowledgeBase()
report = kb.query_all_plugins()
print(report)
```

---

### 示例15: 搜索技能包

```python
from knowledge_base import KnowledgeBase

kb = KnowledgeBase()

# 搜索关键词
results = kb.search_skills("design")
print(results)

# 查询特定技能
skill_info = kb.query_skill_by_id("canvas-design")
print(skill_info)
```

---

### 示例16: 执行同步

```python
from sync_manager import SyncManager

manager = SyncManager()

# 检查是否需要同步
need_sync, reason = manager.check_need_sync()
print(f"需要同步: {need_sync}, 原因: {reason}")

# 执行同步
result = manager.sync(force=False)
if result["synced"]:
    print(f"同步成功，共 {result['registry']['total_skills']} 个技能包")
```

---

## 最佳实践

### 实践1: 安装新插件后立即查询

```
用户操作: 使用 /plugin install xxx 安装新插件
用户提问: "新安装的插件包含哪些技能？"
Claude行为:
  1. 检测到需要同步（installed_plugins.json变更）
  2. 自动执行同步
  3. 返回新插件的详细信息
```

---

### 实践2: 定期生成配置报告

**建议频率**: 每周一次

```bash
# 创建定时任务
crontab -e

# 添加每周一上午9点执行
0 9 * * 1 cd ~/.claude/skills/全局照见/scripts && python3 sync_manager.py --force
```

---

### 实践3: 在项目文档中引用

**项目README.md**:
```markdown
# 项目依赖的全局技能包

本项目依赖以下Claude Code全局技能包：

- **browsing** (superpowers-chrome) - 浏览器自动化
- **canvas-design** (example-skills) - 视觉设计
- **mcp-builder** (example-skills) - MCP服务器开发

查看完整清单: 询问Claude "生成全局插件清单"
```

---

### 实践4: CI/CD集成

```yaml
# .github/workflows/test.yml
- name: Check Global Plugins
  run: |
    cd .claude/skills/全局照见/scripts
    python3 sync_manager.py --force
    python3 -c "
    from knowledge_base import KnowledgeBase
    kb = KnowledgeBase()
    registry = kb.load_plugins_registry()
    print(f'✅ 检测到 {registry[\"total_skills\"]} 个技能包')
    "
```

---

## 常见问题

### Q1: 如何确认技能包是否已加载？

**A**: 询问Claude "browsing技能是否可用？"，Claude会查询知识库并确认。

---

### Q2: 新安装的插件没有出现在清单中？

**A**: 手动触发同步：
```bash
cd .claude/skills/全局照见/scripts
python3 sync_manager.py --force
```

---

### Q3: 如何查看某个技能包的使用示例？

**A**: 询问Claude：
```
"canvas-design技能的使用示例"
```

Claude会：
1. 读取SKILL.md
2. 提取示例部分
3. 返回格式化的示例代码

---

## 总结

**全局照见**技能包提供了强大的插件查询和管理能力：

✅ **自动化** - 无需手动维护插件清单
✅ **实时性** - 智能检测配置变更
✅ **灵活性** - 支持自然语言和命令行查询
✅ **扩展性** - 易于添加自定义查询逻辑

---

**更多示例**: 参考[reference.md](../reference.md)的扩展开发章节
