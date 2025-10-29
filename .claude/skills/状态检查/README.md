# 状态检查技能包目录

这个目录包含用于系统状态检查和健康验证的技能包。

## 技能包列表

### plugin-status
**项目插件状态检查**

自动化验证ZTL数智化作战中心的多智能体插件生态系统。

**核心功能**:
- ✅ 验证 `.claude/settings.json` 配置
- ✅ 检查 `.claude-plugin/marketplace.json` 定义
- ✅ 校验8个业务组插件目录结构
- ✅ 统计62+个专业智能体
- ✅ 生成综合状态报告

**使用方法**:
```
"检查所有插件是否正确启用"
"验证插件系统完整性"
"显示当前插件状态"
```

**详细文档**: [plugin-status/README.md](./plugin-status/README.md)

---

## 技能包开发规范

遵循Claude Code技能包标准结构：

```
技能包名称/
├── SKILL.md              # 必需: 元数据 + 使用说明
│   ├── YAML frontmatter  # name + description
│   └── 使用指南          # Quick Start + API Reference
├── scripts/              # 推荐: 执行引擎
│   └── core_engine.py    # 核心逻辑
├── reference.md          # 可选: 扩展文档
└── README.md             # 可选: 项目说明
```

### 渐进披露原则
- **Level 1**: YAML frontmatter (~50 tokens) - 能力发现
- **Level 2**: SKILL.md核心指令 (~500-2000 tokens) - 使用说明
- **Level 3**: reference.md扩展文档 (~1000-5000 tokens) - 深度专业知识
- **Level 4**: scripts/可执行代码 - 真实执行引擎

## 未来计划

待添加的状态检查技能包：
- [ ] **mcp-status** - MCP服务器连接状态检查
- [ ] **agent-health** - 智能体健康度评估
- [ ] **system-performance** - 系统性能监控
- [ ] **config-validator** - 配置文件语法验证
- [ ] **dependency-checker** - 依赖关系完整性检查

---

## 参考资源

- [Claude Code Skills文档](https://docs.claude.com/en/docs/claude-code/skills.md)
- [全局CLAUDE.md配置](@/.claude/CLAUDE.md) - Skills vs Commands vs Subagents
- [项目CLAUDE.md](@/CLAUDE.md) - ZTL项目特定配置
