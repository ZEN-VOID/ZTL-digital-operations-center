# AIGC技能包重构方案：提示词整合与路径规范

**生成时间**: 2025-10-28
**影响范围**: plugins/创意组/skills/aigc/ 和 plugins/创意组/agents/*prompt*.md
**优化目标**:
1. 将独立的提示词agents整合到AIGC skills中作为中间层
2. 修复所有路径引用问题
3. 统一输出路径规范

---

## 📊 当前状况分析

### 1. 提示词Agents现状

| Agent文件 | 功能定位 | 问题 |
|----------|---------|------|
| `kling-prompt-generator.md` | Kling AI视频生成提示词工程 | ❌ 独立agent，应整合到Kling skill |
| `nano-banana-prompt-engineer.md` | Nano Banana图像变体提示词工程 | ❌ 独立agent，应整合到Nano-banana skill |
| `wan-prompt-generator.md` | 通义万相图像生成提示词工程 | ❌ 独立agent，应整合到Wan skill |

**核心问题**：
- 这些提示词agents本质上是AIGC skills的**提示词优化中间层**
- 当前作为独立agents存在，导致架构不清晰
- 用户需要显式调用两次（先生成提示词，再执行创作）
- 无法形成完整的"需求→提示词优化→执行创作"工作流

### 2. AIGC Skills路径问题

#### Kling Skill路径分析

```yaml
# SKILL.md中的路径引用
❌ 错误引用1: `.claude/agents/提词组/kling-prompt-generator.md`
   正确路径: `plugins/创意组/agents/kling-prompt-generator.md`

❌ 错误引用2: `.claude/skills/执行引擎/API/aigc/Kling/scripts/`
   正确路径: `plugins/创意组/skills/aigc/Kling/scripts/`

# kling_api_core.py中的硬编码注释
❌ 错误注释: `从 .claude/skills/执行引擎/API/aigc/Kling/scripts/ 上溯到项目根目录`
   正确路径: `从 plugins/创意组/skills/aigc/Kling/scripts/ 上溯到项目根目录`
```

#### 输出路径对比

| Skill | 当前输出路径 | 符合规范 | 建议修改 |
|-------|------------|---------|---------|
| **Kling** | `output/{project-name}/kling/` | ✅ 符合 | 无需修改 |
| **Nano-banana** | `output/nano-banana/` | ❌ 缺少项目名 | 改为 `output/{project-name}/nano-banana/` |
| **Wan** | `output/tongyi-wanxiang/` | ❌ 缺少项目名 | 改为 `output/{project-name}/wan/` |

**标准格式** (参考全局CLAUDE.md 第4.5章):
```
output/[项目名]/[skill-name]/
├── plans/          # 执行计划(JSON)
├── results/        # 最终输出
├── logs/           # 执行日志
└── metadata/       # 元数据
```

### 3. Agents引用skill的方式

发现的积极做法（Kling skill已部分体现）：
- Kling agent中第18-40行定义了"执行模式"机制
- 自由/独立模式：生成提示词后询问是否执行
- 批量/工作流模式：自动执行无需确认

**这是正确的设计方向**，需要在整合时保留并优化。

---

## 🎯 重构目标

### 核心理念

```
传统架构（问题）:
用户请求 → 提示词Agent → Markdown文档 → (手动) → Skill执行 → 结果

优化后架构（目标）:
用户请求 → Skill自动发现 → 内置提示词优化层 → 执行引擎 → 结果
          ↓
       可选中间输出：优化后的提示词文档
```

### 三层架构优化

```yaml
Layer 1 - 规范层 (SKILL.md):
  - 业务逻辑和领域知识
  - 提示词工程规范（整合原agent的expertise）
  - 工作流程定义

Layer 1.5 - 提示词优化层 (prompt_engineering.md):
  - 原agent的prompt工程知识
  - 智能补全策略
  - 质量验证标准
  - 作为内部文档，Claude按需加载

Layer 2 - 计划层 (JSON):
  - 结构化任务配置
  - 包含优化后的提示词
  - 批量任务编排

Layer 3 - 执行层 (scripts/):
  - API调用和任务执行
  - 进度追踪和错误处理
  - 结果输出和元数据生成
```

---

## 📋 详细重构方案

### 方案A: 提示词agents整合到skills

#### 目标结构

```
plugins/创意组/skills/aigc/
├── Kling/
│   ├── SKILL.md                    # 核心skill文档
│   ├── prompt_engineering.md       # 新增：提示词工程知识（原kling-prompt-generator内容）
│   ├── reference.md                # 扩展文档
│   ├── camera_control.md
│   ├── motion_brush.md
│   └── scripts/
│       ├── prompt_optimizer.py     # 新增：提示词优化脚本
│       ├── kling_api_core.py
│       └── kling_executor.py
│
├── Nano-banana/
│   ├── SKILL.md
│   ├── prompt_engineering.md       # 新增：提示词工程知识（原nano-banana-prompt-engineer内容）
│   ├── reference.md
│   └── scripts/
│       ├── prompt_optimizer.py     # 新增
│       ├── api_client.py
│       └── nano-banana-execute.py
│
└── Wan/
    ├── SKILL.md
    ├── prompt_engineering.md       # 新增：提示词工程知识（原wan-prompt-generator内容）
    ├── reference.md
    ├── composer.md
    ├── qwen_image.md
    └── scripts/
        ├── prompt_optimizer.py     # 新增
        ├── wan-base.py
        └── wan-execute.py
```

#### 整合策略

**Step 1: 提取提示词agents的核心知识**

从agents中提取：
- 提示词结构模板
- 智能补全策略
- 质量验证标准
- 领域专业知识

**Step 2: 转化为prompt_engineering.md**

格式规范：
```markdown
---
# Metadata (Progressive Disclosure - Level 1.5)
name: [Skill Name] Prompt Engineering
description: 提示词优化中间层，智能补全和质量验证
---

# [Skill Name] Prompt Engineering

## Core Prompt Structure

## Intelligent Completion Strategy

## Quality Validation Standards

## Best Practices

## Output Format
```

**Step 3: 更新SKILL.md引用**

在SKILL.md中添加章节：
```markdown
## Prompt Optimization Layer

This skill includes an intelligent prompt optimization layer that:

1. **Auto-enhances user inputs**: Expands brief descriptions into complete prompts
2. **Validates quality**: Ensures character count, structure, and language requirements
3. **Applies best practices**: Leverages domain-specific prompt engineering techniques

**Documentation**: See [prompt_engineering.md](prompt_engineering.md) for detailed specifications.

**Usage**:
- **Implicit Mode** (默认): Skill自动优化用户输入的提示词
- **Explicit Mode**: 用户可选择输出优化后的提示词文档到 `output/[项目名]/[skill-name]/prompts/`
```

**Step 4: 实现prompt_optimizer.py脚本**

```python
# scripts/prompt_optimizer.py

class PromptOptimizer:
    """提示词智能优化引擎"""

    def __init__(self, rules_path: Path):
        """加载提示词工程规范"""
        pass

    def optimize(self, user_input: str, context: Dict) -> Dict:
        """
        优化用户输入的提示词

        Returns:
            {
                "optimized_prompt": str,
                "validation_passed": bool,
                "suggestions": List[str],
                "metadata": Dict
            }
        """
        pass

    def validate(self, prompt: str) -> Dict:
        """验证提示词质量"""
        pass
```

#### 删除独立agents

执行后删除以下文件：
- `plugins/创意组/agents/kling-prompt-generator.md`
- `plugins/创意组/agents/nano-banana-prompt-engineer.md`
- `plugins/创意组/agents/wan-prompt-generator.md`

---

### 方案B: 路径引用修复

#### Kling Skill路径修复

**1. SKILL.md路径修复**

| 行号/位置 | 当前路径 | 修正路径 |
|----------|---------|---------|
| 第59行 | `.claude/agents/提词组/kling-prompt-generator.md` | `plugins/创意组/skills/aigc/Kling/prompt_engineering.md` |
| 第164行 | `.claude/skills/执行引擎/API/aigc/Kling/scripts/` | `plugins/创意组/skills/aigc/Kling/scripts/` |
| 第635行 | `.claude/skills/执行引擎/API/aigc/Kling/scripts/` | `plugins/创意组/skills/aigc/Kling/scripts/` |
| 第652行 | `.claude/agents/提词组/kling-prompt-generator.md` | `plugins/创意组/skills/aigc/Kling/prompt_engineering.md` |

**2. kling_api_core.py路径修复**

```python
# 第67行注释修复
# 修复前
# 从 .claude/skills/执行引擎/API/aigc/Kling/scripts/ 上溯到项目根目录

# 修复后
# 从 plugins/创意组/skills/aigc/Kling/scripts/ 上溯到项目根目录
```

#### Nano-banana Skill路径修复

**1. SKILL.md路径修复**

```markdown
# 第253行
- [三层架构API规范](../../../../.claude/agents/system/Api-Creator.md)

# 修复为（根据实际文件存在情况）
- [三层架构API规范](../../../README.md#三层架构规范)
```

**2. 输出路径修复**

```python
# scripts/config_template.json
"base_path": "output/nano-banana"  # 修复前

"base_path": "output/{project_name}/nano-banana"  # 修复后

# scripts/nano-banana-execute.py
base_path = Path(output_config.get("base_path", "output/temp"))  # 修复前

project_name = plan.get("project_name", "temp-project")
base_path = Path(output_config.get("base_path", f"output/{project_name}/nano-banana"))  # 修复后
```

#### Wan Skill路径修复

**1. SKILL.md路径修复**

```markdown
# 第52行
- **计划层**: JSON配置文件 (`output/tongyi-wanxiang/plans/`)

# 修复为
- **计划层**: JSON配置文件 (`output/[项目名]/wan/plans/`)

# 第313-314行
- **三层架构规范**: `.claude/agents/system/Api-Creator.md`
- **智能体创建**: `.claude/agents/system/Agent-Creator.md`

# 修复为（根据实际情况调整）
- **三层架构规范**: 参见项目CLAUDE.md
- **技能包创建**: 参见 .claude/skills/meta/
```

**2. 输出路径修复**

```python
# scripts/wan-execute.py
base_path = Path(output_config.get("base_path", "output/temp"))  # 修复前

project_name = plan.get("project_name", "temp-project")
base_path = Path(output_config.get("base_path", f"output/{project_name}/wan"))  # 修复后

# scripts/test_t2i.py
output_dir = Path("output/images/tongyi-wanxiang")  # 修复前

project_name = "test-project"  # 或从配置读取
output_dir = Path(f"output/{project_name}/wan")  # 修复后
```

**3. 全局搜索替换**

```bash
# 在Wan目录下批量替换
grep -rl "output/tongyi-wanxiang" plugins/创意组/skills/aigc/Wan/ | \
  xargs sed -i '' 's|output/tongyi-wanxiang|output/{project_name}/wan|g'

grep -rl "\.claude/agents/system" plugins/创意组/skills/aigc/Wan/ | \
  xargs sed -i '' 's|\.claude/agents/system|plugins/创意组/skills/meta|g'
```

---

## 🚀 执行计划

### Phase 1: 提示词整合（高优先级）

**任务1.1: 创建prompt_engineering.md文件**

对每个AIGC skill：
1. 复制对应的prompt generator agent内容
2. 提取核心提示词工程知识
3. 转换为skills文档格式
4. 保存到 `plugins/创意组/skills/aigc/[skill-name]/prompt_engineering.md`

**预计时间**: 2-3小时

**任务1.2: 实现prompt_optimizer.py脚本**

为每个skill创建提示词优化脚本：
- 加载prompt_engineering.md规范
- 实现智能补全逻辑
- 实现质量验证
- 集成到执行流程

**预计时间**: 3-4小时

**任务1.3: 更新SKILL.md**

- 添加"Prompt Optimization Layer"章节
- 更新Quick Start示例
- 更新工作流程说明
- 添加prompt_engineering.md引用

**预计时间**: 1-2小时

**任务1.4: 删除独立agents**

确认整合完成后：
```bash
git mv plugins/创意组/agents/kling-prompt-generator.md \
      _deprecated/agents/kling-prompt-generator.md.backup

git mv plugins/创意组/agents/nano-banana-prompt-engineer.md \
      _deprecated/agents/nano-banana-prompt-engineer.md.backup

git mv plugins/创意组/agents/wan-prompt-generator.md \
      _deprecated/agents/wan-prompt-generator.md.backup

# 验证无误后删除
git rm _deprecated/agents/*prompt*.md.backup
```

**预计时间**: 30分钟

### Phase 2: 路径修复（中优先级）

**任务2.1: Kling路径修复**

- 修复SKILL.md中的4处路径引用
- 修复kling_api_core.py中的注释
- 搜索其他潜在的旧路径引用

**预计时间**: 1小时

**任务2.2: Nano-banana路径修复**

- 修复SKILL.md中的路径引用
- 修复输出路径配置
- 更新所有scripts中的硬编码路径

**预计时间**: 1-2小时

**任务2.3: Wan路径修复**

- 修复SKILL.md中的路径引用
- 批量替换"tongyi-wanxiang" → "{project_name}/wan"
- 修复所有test scripts中的路径

**预计时间**: 1-2小时

**任务2.4: 全局验证**

```bash
# 检查是否还有遗漏的旧路径
grep -r "\.claude/skills/执行引擎" plugins/创意组/skills/aigc/
grep -r "\.claude/agents/提词组" plugins/创意组/skills/aigc/
grep -r "output/tongyi-wanxiang" plugins/创意组/skills/aigc/
grep -r "output/nano-banana" plugins/创意组/skills/aigc/
```

**预计时间**: 30分钟

### Phase 3: 文档更新（低优先级）

**任务3.1: 更新README和reference文档**

- 更新skills/aigc/README.md（如存在）
- 更新各skill的reference.md
- 确保示例代码使用新路径

**预计时间**: 1-2小时

**任务3.2: 更新其他引用**

检查是否有其他agents或commands引用这些prompt agents：
```bash
grep -r "kling-prompt-generator" plugins/创意组/
grep -r "nano-banana-prompt-engineer" plugins/创意组/
grep -r "wan-prompt-generator" plugins/创意组/
```

如有，更新为新的skill引用方式。

**预计时间**: 1小时

**任务3.3: 生成迁移指南**

创建 `plugins/创意组/skills/aigc/MIGRATION_GUIDE.md`，说明：
- 旧agents如何映射到新skills
- 用户如何迁移现有工作流
- 新旧API对比

**预计时间**: 1小时

### Phase 4: 测试验证（必需）

**任务4.1: 功能测试**

- 测试Kling skill的完整工作流
- 测试Nano-banana skill的完整工作流
- 测试Wan skill的完整工作流
- 验证提示词优化层是否正常工作

**预计时间**: 2-3小时

**任务4.2: 路径测试**

- 验证所有输出文件保存到正确位置
- 验证所有import和引用路径正确
- 运行示例脚本确认无错误

**预计时间**: 1-2小时

**任务4.3: 文档验证**

- 确保所有SKILL.md中的示例可运行
- 确保所有路径引用正确
- 确保prompt_engineering.md可被Claude正确加载

**预计时间**: 1小时

---

## 📊 影响评估

### 破坏性变更

| 变更 | 影响范围 | 风险等级 |
|------|---------|---------|
| 删除独立prompt agents | 任何显式调用这些agents的代码/配置 | 🔴 高 |
| 修改输出路径 | 依赖旧路径的脚本和配置 | 🟡 中 |
| 修改skills内部路径 | skills内部引用 | 🟢 低 |

### 兼容性措施

**向后兼容方案**：
```python
# 在skills的SKILL.md中添加"已弃用agents"说明
## Deprecated: Independent Prompt Agents

⚠️ **重要通知**: 以下agents已整合到本skill中作为内置提示词优化层：

- ❌ `kling-prompt-generator` → ✅ 现在是本skill的一部分
- ❌ `nano-banana-prompt-engineer` → ✅ 现在是本skill的一部分
- ❌ `wan-prompt-generator` → ✅ 现在是本skill的一部分

**迁移指南**: 原来需要两步（生成提示词 + 执行）的工作流，现在只需一步即可完成。
Skill会自动优化提示词，无需显式调用独立agents。
```

### 用户体验提升

**重构前**:
```
用户: "用Kling生成一个赛博朋克场景视频"
Claude: "我先调用kling-prompt-generator生成提示词..."
         [生成提示词文档]
         "提示词已生成。是否需要执行视频生成？"
用户: "是的"
Claude: "现在调用Kling skill执行..."
         [执行视频生成]
```

**重构后**:
```
用户: "用Kling生成一个赛博朋克场景视频"
Claude: "正在调用Kling skill..."
         [自动优化提示词 → 执行视频生成]
         "视频已生成！同时已保存优化后的提示词文档供参考。"
```

**优势**:
- ✅ 减少交互步骤：从2步变为1步
- ✅ 自动化优化：无需用户关心提示词细节
- ✅ 保留透明性：可选输出提示词文档
- ✅ 支持高级用户：仍可显式要求生成提示词

---

## 🎯 成功标准

### 功能标准

- [ ] 所有AIGC skills包含prompt_engineering.md
- [ ] 所有skills可自动优化用户输入的提示词
- [ ] 提示词优化层可选输出Markdown文档
- [ ] 独立prompt agents已删除且无破坏性影响

### 质量标准

- [ ] 所有路径引用正确（无`.claude/skills/执行引擎`等旧路径）
- [ ] 输出路径符合规范（`output/[项目名]/[skill-name]/`）
- [ ] 所有示例代码可正常运行
- [ ] 文档清晰准确无误导性内容

### 性能标准

- [ ] 提示词优化不显著增加执行时间（<5秒）
- [ ] Claude加载prompt_engineering.md符合渐进披露原则
- [ ] 批量任务执行效率不下降

---

## 📝 变更日志模板

```markdown
## [3.0.0] - 2025-10-28

### 🔄 Breaking Changes
- 移除独立提示词agents（kling-prompt-generator, nano-banana-prompt-engineer, wan-prompt-generator）
- 修改输出路径格式：`output/[项目名]/[skill-name]/` 取代旧的固定路径

### ✨ New Features
- 为所有AIGC skills添加内置提示词优化层（prompt_engineering.md）
- 自动化提示词优化和质量验证
- 支持单步式工作流（无需手动生成提示词）

### 🐛 Bug Fixes
- 修复Kling skill中的旧路径引用（.claude/skills/执行引擎 → plugins/创意组/skills）
- 修复Nano-banana和Wan的输出路径不符合规范的问题
- 统一所有skills的路径引用标准

### 📚 Documentation
- 更新所有SKILL.md文档以反映新架构
- 添加MIGRATION_GUIDE.md迁移指南
- 添加prompt_engineering.md详细说明

### 🔧 Maintenance
- 清理已弃用的agent文件
- 统一代码中的输出路径配置
- 优化skills的渐进披露结构
```

---

## 🔗 相关资源

- **全局规范**: ~/.claude/CLAUDE.md (第4.5章：输出路径规范，第5章：三层架构)
- **Skills元文档**: .claude/skills/meta/
- **当前AIGC skills**: plugins/创意组/skills/aigc/
- **待删除agents**: plugins/创意组/agents/*prompt*.md

---

## 🤝 建议的执行顺序

```
1️⃣ Phase 1: 提示词整合 (6-9小时)
   ├── 创建prompt_engineering.md
   ├── 实现prompt_optimizer.py
   ├── 更新SKILL.md
   └── 备份并删除独立agents

2️⃣ Phase 4: 测试验证 (4-6小时)
   ├── 功能测试
   ├── 路径测试
   └── 文档验证

3️⃣ Phase 2: 路径修复 (3-5小时)
   ├── Kling路径修复
   ├── Nano-banana路径修复
   ├── Wan路径修复
   └── 全局验证

4️⃣ Phase 3: 文档更新 (3-4小时)
   ├── 更新README
   ├── 更新引用
   └── 生成迁移指南

总预计时间: 16-24小时（分2-3个工作日完成）
```

---

**报告生成者**: Claude Code
**审核建议**: 建议由创意组负责人审核并批准执行
**风险评估**: 中等风险（需要充分测试以避免破坏现有工作流）
