# Hooks系统快速开始

> 5分钟快速上手Claude Code Hooks自动化工作流

## 🎯 什么是Hooks？

Hooks是在Claude Code特定事件发生时自动执行的脚本，实现零人工干预的智能化工作流。

### 核心价值

- ✅ **自动保存上下文** - Compact时不再丢失信息
- ✅ **并行工作能力** - 一个任务，两个实例同时处理
- ✅ **无缝任务衔接** - 自动启动新实例继续工作
- ✅ **零人工干预** - 全程自动化，专注核心工作

## 🚀 3步启用

### 步骤1: 验证权限（30秒）

```bash
# 确保hook脚本可执行
chmod +x .claude/hooks/parallel-claude-after-compact.sh

# 验证权限
ls -la .claude/hooks/
# 应该看到: -rwxr-xr-x ... parallel-claude-after-compact.sh
```

### 步骤2: 配置iTerm权限（1分钟）

1. 打开 **系统偏好设置**
2. 进入 **安全性与隐私** → **隐私** → **辅助功能**
3. 点击左下角 🔒 解锁
4. 添加或勾选 **iTerm.app**
5. 点击 🔒 锁定

### 步骤3: 测试hook（1分钟）

```bash
# 测试hook执行
echo '{"context": "测试内容", "reason": "test"}' | \
  .claude/hooks/parallel-claude-after-compact.sh

# 查看执行日志
cat .claude/logs/parallel-claude-after-compact.log

# 应该看到: "Hook Triggered", "Lock acquired", "Parallel Claude launch initiated"
```

✅ **完成！** Hooks系统已启用。

## 💡 工作原理

### 场景：对话上下文太长

**无Hooks**:
```
对话超限 → 提示Compact → 确认 → 部分上下文丢失 → 需要重新提供背景
```

**有Hooks**:
```
对话超限 → 触发PreCompact Hook
           ↓
    自动保存完整上下文
           ↓
    新iTerm窗口自动打开
           ↓
    新Claude实例自动启动
           ↓
    上下文自动注入
           ↓
原实例继续工作 + 新实例接手任务
```

**结果**: 零上下文丢失，零人工干预，两个实例并行工作！

## 📊 实际效果对比

| 指标 | 无Hooks | 有Hooks |
|------|---------|---------|
| 上下文保留 | ❌ 部分丢失 | ✅ 100%保留 |
| 人工操作 | ❌ 需要手动 | ✅ 全自动 |
| 任务连续性 | ❌ 中断 | ✅ 无缝 |
| 并行能力 | ❌ 不支持 | ✅ 支持 |
| 启动时间 | 🐢 ~2分钟 | ⚡ ~25秒 |

## 🎨 使用示例

### 示例1: 长对话自动衔接

```
你: 帮我开发一个复杂功能A
Claude: [工作中...]
Claude: [上下文接近限制]
→ Hook自动触发 →
新窗口自动打开，新Claude接手继续开发
原窗口继续处理其他任务
```

### 示例2: 并行探索多方案

```
你: 探索3种架构方案
Claude: [开始分析...]
→ Hook触发 →
窗口1: 方案A深入分析
窗口2: 方案B和C并行探索
→ 效率提升3倍
```

## 🔍 监控和调试

### 查看Hook日志

```bash
# 实时监控
tail -f .claude/logs/parallel-claude-after-compact.log

# 查看完整日志
cat .claude/logs/parallel-claude-after-compact.log

# 查找错误
grep ERROR .claude/logs/parallel-claude-after-compact.log
```

### 查看上下文快照

```bash
# 列出所有快照
ls -lt context/snapshots/

# 查看最新快照
cat context/snapshots/last-compact-context.txt
```

### 检查窗口状态

```bash
# 使用深渊凝视查询iTerm窗口
python3 .claude/skills/深渊凝视/scripts/abyss_gaze.py list_windows
```

## ⚙️ 高级配置

### 启用调试模式

```bash
# 临时启用
DEBUG=true .claude/hooks/parallel-claude-after-compact.sh

# 永久启用（添加到 ~/.zshrc）
export DEBUG=true
```

### 调整超时时间

编辑 `.claude/hooks/parallel-claude-after-compact.sh`:

```bash
# 修改等待Claude启动的时间（默认20秒）
sleep 20  →  sleep 30
```

### 禁用特定Hook

```bash
# 临时禁用
export SKIP_PARALLEL_CLAUDE=true

# 永久禁用：移除执行权限
chmod -x .claude/hooks/parallel-claude-after-compact.sh
```

## ❓ 常见问题

### Q1: Hook没有触发？

**检查清单**:
- [ ] 脚本有执行权限: `ls -la .claude/hooks/`
- [ ] iTerm有辅助功能权限: 系统偏好设置 → 辅助功能
- [ ] 日志文件存在: `ls .claude/logs/`

### Q2: 新窗口打开但Claude没启动？

**可能原因**:
- Claude未安装: `which claude`
- PATH未配置: `echo $PATH`
- 等待时间不够: 增加sleep时间

**解决方案**:
```bash
# 手动测试Claude命令
claude --version

# 添加到PATH（如需要）
export PATH="/path/to/claude:$PATH"
```

### Q3: 上下文注入失败？

**检查日志**:
```bash
grep "Send result" .claude/logs/parallel-claude-after-compact.log
```

**常见问题**:
- iTerm权限不足
- 窗口索引错误
- 深渊凝视脚本路径错误

## 📚 深入学习

- **完整文档**: `.claude/hooks/README.md`
- **深渊凝视Skill**: `.claude/skills/深渊凝视/SKILL.md`
- **集成报告**: `reports/hooks-system-integration-20251030.md`
- **项目配置**: `CLAUDE.md` → "Hooks System"

## 🆘 获取帮助

### 问题排查流程

```
1. 查看日志
   tail -f .claude/logs/parallel-claude-after-compact.log

2. 测试hook手动执行
   echo '{"context": "test"}' | .claude/hooks/parallel-claude-after-compact.sh

3. 验证深渊凝视
   python3 .claude/skills/深渊凝视/scripts/abyss_gaze.py list_windows

4. 检查权限
   ls -la .claude/hooks/
   系统偏好设置 → 辅助功能 → iTerm

5. 查看完整文档
   cat .claude/hooks/README.md
```

### 联系方式

- **GitHub Issues**: [项目仓库]/issues
- **文档**: `.claude/hooks/README.md`

---

**版本**: v1.0.0
**更新日期**: 2025-10-30
**维护**: ZTL Team

🎉 **恭喜！** 你已经掌握了Hooks系统的基础使用。现在开始享受自动化工作流带来的效率提升吧！
