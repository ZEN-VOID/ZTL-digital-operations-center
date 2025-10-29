# ZTL数智化作战中心 - Plugins总览

> 完整的8个业务组插件，基于Claude Code Plugins规范v1.0构建
>
> **创建日期**: 2025-10-28
> **状态**: ✅ Production Ready

---

## 📦 插件清单

| # | 插件名称 | Plugin ID | Agents数量 | 业务领域 |
|---|---------|-----------|-----------|---------|
| 1 | 筹建组 | construction-team | 6 | 门店筹建、空间设计、BIM建模 |
| 2 | 创意组 | creative-team | 9 | 内容创意、广告设计、视频制作 |
| 3 | 供应组 | supply-chain-team | 7 | 供应链管理、采购、库存 |
| 4 | 开发组 | development-team | 11 | 全栈开发、AI集成、DevOps |
| 5 | 美团组 | meituan-ops-team | 6 | 美团平台运营、营销、报表 |
| 6 | 情报组 | intelligence-team | 8 | 市场调研、数据采集、分析 |
| 7 | 行政组 | admin-team | 9 | 财务、人事、法务、行政 |
| 8 | 战略组 | strategy-team | 9 | 战略规划、业务拓展、优化 |

**总计**: 8个插件 | 65个专业智能体

---

## 🏗️ 插件架构

每个插件都遵循标准的Claude Code Plugins结构：

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json              # 插件清单（必需）
│
├── agents/                      # 专业智能体（已配置）
│   └── *.md                     # N个领域专家agents
│
├── commands/                    # 斜杠命令（预留）
│   └── README.md
│
├── skills/                      # 技能包（预留）
│   └── README.md
│
├── hooks/                       # 事件钩子（预留）
│   └── hooks.json
│
├── scripts/                     # 脚本目录（预留）
│
├── .mcp.json                   # MCP服务器配置（预留）
├── README.md                   # 完整使用文档
├── CHANGELOG.md                # 版本历史
└── LICENSE                     # MIT许可证
```

---

## 📋 各组详细信息

### 1. 筹建组 (Construction Team)

**Plugin ID**: `construction-team`

**核心能力**: 餐饮门店从需求分析到落地交付的完整筹建流程

**智能体清单** (6个):
- Z0 - 筹建项目需求分析师
- Z1 - 平面图设计师
- Z2 - 空间设计师
- Z3 - BIM建模师
- Z4 - 建筑动画师
- ZZ - 筹建组组长（协调者）

**典型工作流**:
```
Z0需求分析 → Z1平面图 → Z2空间设计 → Z3 BIM建模 → Z4动画展示
```

---

### 2. 创意组 (Creative Team)

**Plugin ID**: `creative-team`

**核心能力**: 营销内容创意、设计、拍摄、剪辑全流程

**智能体清单** (9个):
- X0 - 内容创意需求分析师
- X1 - 广告策划师
- X2 - 文案创作师
- X3 - 平面设计师
- X4 - 图文排版师
- X5 - 短视频脚本创作师
- X6 - 摄影师
- X7 - 剪辑师
- XX - 创意组组长（协调者）

**典型工作流**:
```
X0需求分析 → X1广告策划 → X2文案 + X3设计 → X6拍摄 → X7剪辑
```

---

### 3. 供应组 (Supply Chain Team)

**Plugin ID**: `supply-chain-team`

**核心能力**: 采购、库存、成本、供应商、分账管理

**智能体清单** (7个):
- S0 - 供应需求分析师
- S1 - 采购执行经理
- S2 - 库存管理员
- S3 - 成本卡管理员
- S4 - 供应商管理员
- S5 - 分账管理员
- SS - 供应组组长（协调者）

**典型工作流**:
```
S0需求分析 → S1采购执行 → S2库存入库 → S3成本核算 → S5分账结算
```

---

### 4. 开发组 (Development Team)

**Plugin ID**: `development-team`

**核心能力**: 全栈开发、AI集成、测试、部署

**智能体清单** (11个):
- F0 - 产品经理
- F1 - 前端开发
- F2 - 组件开发
- F3 - 数据库开发
- F4 - API开发
- F5 - 后端开发
- F6 - AI集成开发
- F7 - 测试性能工程师
- F8 - 版本控制助手
- F9 - 云部署管理
- FF - 开发团队组长（协调者）

**典型工作流**:
```
F0产品设计 → F1前端 + F5后端 + F3数据库 → F7测试 → F9部署
```

---

### 5. 美团组 (Meituan Ops Team)

**Plugin ID**: `meituan-ops-team`

**核心能力**: 美团平台运营、营销、报表、自动化

**智能体清单** (6个):
- V0 - 办公业务需求分析员
- V1 - 运营管理员
- V2 - 营销管理员
- V4 - 报表管理员
- V5 - 网页自动化
- VV - 美团组组长（协调者）

**典型工作流**:
```
V0需求分析 → V1运营执行 + V2营销活动 → V4报表分析
```

---

### 6. 情报组 (Intelligence Team)

**Plugin ID**: `intelligence-team`

**核心能力**: 市场调研、数据采集、深度分析、存储管理

**智能体清单** (8个):
- E0 - 情报需求分析师
- E1 - 深度调研员
- E2 - Chrome网页采集
- E3 - 深度爬虫
- E4 - 深度情报分析
- E5 - COS存储管理
- E6 - Supabase数据库管理
- EE - 情报组组长（协调者）

**典型工作流**:
```
E0需求分析 → E1/E2/E3数据采集 → E4深度分析 → E5/E6存储管理
```

---

### 7. 行政组 (Admin Team)

**Plugin ID**: `admin-team`

**核心能力**: 财务、人事、法务、办公协同、文件管理

**智能体清单** (9个):
- R0 - 办公业务需求分析员
- R1 - 财务管理员
- R2 - 人事管理员
- R3 - 法务专家
- R4 - 秘书
- R5 - 飞书管理员
- R6 - 文件管理员
- R7 - 腾讯云COS存储管理员
- RR - 行政组组长（协调者）

**典型工作流**:
```
R0需求分析 → R1财务/R2人事/R3法务处理 → R6归档 + R7备份
```

---

### 8. 战略组 (Strategy Team)

**Plugin ID**: `strategy-team`

**核心能力**: 战略规划、业务拓展、数字化转型、精细化管理

**智能体清单** (9个):
- G0 - 战略需求解析师
- G1 - 经营分析优化师
- G2 - 产品力打造专家
- G3 - 区域扩张策略师
- G4 - 商业模式设计师
- G5 - 连锁复制专家
- G6 - 数字化转型架构师
- G7 - 精细化管理专家
- GG - 战略规划总监（协调者）

**典型工作流**:
```
G0需求解析 → G1经营分析 → G2/G3/G4战略设计 → G6数字化实施
```

---

## 🚀 安装与使用

### 全局安装（推荐）

将所有插件安装到用户级插件目录：

```bash
# 批量复制所有插件
for plugin in 筹建组 创意组 供应组 开发组 美团组 情报组 行政组 战略组; do
  cp -r "plugins/${plugin}" ~/.claude/plugins/
done

# 在全局settings.json中启用
cat >> ~/.claude/settings.json <<EOF
{
  "enabledPlugins": [
    "construction-team",
    "creative-team",
    "supply-chain-team",
    "development-team",
    "meituan-ops-team",
    "intelligence-team",
    "admin-team",
    "strategy-team"
  ]
}
EOF

# 重启Claude Code（完全退出并重启）
```

### 项目级安装（选择性启用）

在项目级只启用需要的插件：

```bash
# 在项目.claude/settings.json中配置
cat >> .claude/settings.json <<EOF
{
  "enabledPlugins": [
    "./plugins/筹建组",
    "./plugins/创意组"
  ]
}
EOF
```

---

## 🎯 使用场景

### 场景1: 新店筹建项目

**涉及插件**: 筹建组 + 战略组 + 供应组

```yaml
战略组(G3): 区域选址和定位分析
  ↓
筹建组(Z0-Z4): 完整的设计和建模
  ↓
供应组(S1-S4): 材料采购和成本管理
```

### 场景2: 营销活动策划

**涉及插件**: 创意组 + 美团组 + 情报组

```yaml
情报组(E1-E4): 市场调研和竞品分析
  ↓
创意组(X1-X7): 创意策划和内容制作
  ↓
美团组(M1-M2): 平台运营和效果跟踪
```

### 场景3: 系统开发项目

**涉及插件**: 开发组 + 行政组

```yaml
开发组(F0): 产品需求分析
  ↓
开发组(F1-F9): 全栈开发和部署
  ↓
行政组(R7): 云存储和备份管理
```

---

## 🔧 扩展建议

每个插件都预留了扩展空间，可以根据实际需要添加：

### 1. Commands (斜杠命令)

在`commands/`目录下添加`.md`文件，创建快捷命令：

```markdown
---
description: 启动新店筹建项目
argument-hint: [店铺名称] [面积] [业态]
---

# 新店筹建快速启动

调用ZZ组长编排Z0-Z4完成完整筹建流程...
```

### 2. Skills (技能包)

在`skills/`目录下创建技能包目录：

```
skills/
├── cost-estimation/
│   ├── SKILL.md
│   └── scripts/
│       └── calculate_cost.py
```

### 3. Hooks (事件钩子)

在`hooks/hooks.json`中添加自动化流程：

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write",
      "hooks": [{
        "type": "command",
        "command": "./scripts/backup.sh",
        "description": "自动备份重要文件"
      }]
    }]
  }
}
```

### 4. MCP Servers (外部工具集成)

在`.mcp.json`中配置外部服务：

```json
{
  "mcpServers": {
    "meituan-api": {
      "type": "stdio",
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/scripts/meituan-mcp.js"]
    }
  }
}
```

---

## 📊 技术规格

### 符合标准

- ✅ Claude Code Plugins Reference v1.0
- ✅ Claude Code v1.0.124+
- ✅ 基于 `.claude/skills/元skills/plugins` 规范
- ✅ Sonnet 4.5 模型兼容

### 文件统计

```
总插件数: 8
总智能体数: 65
总文件数: 130+
总代码行数: 15,000+
许可证: MIT License
```

### 目录结构统计

每个插件包含：
- 1个 plugin.json（配置清单）
- N个 agents/*.md（智能体定义）
- 1个 README.md（使用文档）
- 1个 CHANGELOG.md（版本历史）
- 1个 LICENSE（MIT许可证）
- 4个预留目录（commands, skills, hooks, scripts）
- 2个配置文件（hooks.json, .mcp.json）

---

## 📝 版本信息

| 插件 | 版本 | 状态 | 最后更新 |
|------|------|------|---------|
| 筹建组 | 1.0.0 | Production | 2025-10-28 |
| 创意组 | 1.0.0 | Production | 2025-10-28 |
| 供应组 | 1.0.0 | Production | 2025-10-28 |
| 开发组 | 1.0.0 | Production | 2025-10-28 |
| 美团组 | 1.0.0 | Production | 2025-10-28 |
| 情报组 | 1.0.0 | Production | 2025-10-28 |
| 行政组 | 1.0.0 | Production | 2025-10-28 |
| 战略组 | 1.0.0 | Production | 2025-10-28 |

---

## 🤝 贡献指南

### 添加新插件

1. 复制现有插件作为模板
2. 修改`plugin.json`中的元数据
3. 在`agents/`目录添加智能体定义
4. 更新`README.md`和`CHANGELOG.md`
5. 测试插件加载和agents调用

### 扩展现有插件

1. 在对应目录添加commands/skills/hooks
2. 更新`plugin.json`中的版本号
3. 在`CHANGELOG.md`中记录变更
4. 测试新功能兼容性

### 提交规范

```bash
git add plugins/[组名]
git commit -m "feat(plugins): 添加[组名]新功能"
git push
```

---

## 🔗 相关资源

### 官方文档

- [Claude Code Plugins Reference](https://docs.claude.com/zh-CN/docs/claude-code/plugins-reference)
- [Claude Code Agents](https://docs.claude.com/zh-CN/docs/claude-code/sub-agents)
- [Claude Code Skills](https://docs.claude.com/zh-CN/docs/claude-code/skills)

### 项目文档

- `.claude/skills/元skills/plugins/` - Plugins创建指南
- `.claude/skills/元skills/agents/` - Agents创建指南
- `.claude/skills/元skills/skills/` - Skills创建指南
- `.claude/skills/元skills/commands/` - Commands创建指南
- `.claude/skills/元skills/hooks/` - Hooks创建指南

### 工具脚本

- `scripts/create_plugins_batch.py` - 批量创建插件脚本

---

## 📞 支持

**问题反馈**:
- 在对应插件的GitHub Issues提交

**文档更新**:
- 所有插件文档都在各自的README.md中维护

**技术支持**:
- 参考各插件的agents文档获取详细使用说明

---

**创建者**: ZTL Digital Intelligence Operations Center
**创建日期**: 2025-10-28
**插件版本**: v1.0.0 (全系列)
**状态**: ✅ Production Ready

**总结**: 8个专业业务组插件，覆盖餐饮企业从战略规划、门店筹建、内容创意、供应链管理、平台运营、市场情报、软件开发到行政管理的全业务流程，共计65个专业智能体，形成完整的数智化作战体系。
