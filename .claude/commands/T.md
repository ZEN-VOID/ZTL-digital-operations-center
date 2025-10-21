---
name: 任务拆解与执行系统
description: 对指定内容启用TodoWrite工具进行任务拆解和执行,配合日志监控和Hooks自动化,确保每一步都细致完成
version: 1.0.0
last_updated: 2025-10-01
---

# 任务拆解与执行监控系统

> 基于TodoWrite工具的智能任务拆解和执行监控系统,配合日志监控和Hooks自动化,确保复杂任务的高质量完成

## 系统概述

### 核心能力
- **智能任务拆解**: 将复杂任务分解为可执行的细粒度步骤
- **TodoWrite集成**: 使用Claude Code内置的TodoWrite工具进行任务跟踪
- **日志监控**: 基于.claude/logs的任务进度实时监控
- **Hooks自动化**: 对话结束时自动检查并继续未完成任务
- **防偷懒机制**: 确保每个步骤都细致完成,避免快速敷衍

### 设计原则

SMART原则:
- Specific (具体): 每个任务步骤明确具体
- Measurable (可衡量): 有明确的完成标准
- Achievable (可实现): 步骤难度适中,可在单轮对话完成
- Relevant (相关): 步骤与总体目标直接相关
- Time-bound (有时限): 每个步骤有预期执行时间

质量保证:
- 任务粒度: 单个步骤不超过5分钟,复杂任务进一步拆解
- 执行标准: 每个步骤必须满足验证标准才能标记完成
- 进度跟踪: 实时记录执行状态和遇到的问题
- 自动继续: 未完成任务在下次对话自动恢复

## 五步工作流

### 步骤1: 任务意图解析与拆解

**目标**: 理解用户任务需求,拆解为结构化的执行步骤

**执行示例**:

用户输入: "帮我创建一个Figma批量替换的API端点"

拆解结果:
1. 分析需求与设计API接口 (3-5分钟)
2. 创建Pydantic数据模型 (5-8分钟)
3. 实现API端点逻辑 (10-15分钟)
4. 编写单元测试 (8-10分钟)
5. 更新API文档 (3-5分钟)

### 步骤2: TodoWrite任务创建与管理

**目标**: 使用TodoWrite工具创建任务列表并实时更新状态

**TodoWrite调用示例**:

初始任务列表创建:
```python
TodoWrite(todos=[
    {
        "content": "分析需求与设计API接口",
        "activeForm": "正在分析需求与设计API接口",
        "status": "pending"
    },
    {
        "content": "创建Pydantic数据模型",
        "activeForm": "正在创建Pydantic数据模型",
        "status": "pending"
    }
])
```

开始执行第一步:
```python
TodoWrite(todos=[
    {
        "content": "分析需求与设计API接口",
        "activeForm": "正在分析需求与设计API接口",
        "status": "in_progress"
    },
    {
        "content": "创建Pydantic数据模型",
        "activeForm": "正在创建Pydantic数据模型",
        "status": "pending"
    }
])
```

**状态管理规范**:

状态转换规则:
- pending → in_progress: 开始执行步骤时立即更新,只能有一个任务为in_progress
- in_progress → completed: 步骤完成并通过验证后更新,检查是否满足最小执行时间要求
- in_progress → failed: 遇到无法解决的错误时标记,记录失败原因和恢复建议

### 步骤3: 日志监控机制设计

**目标**: 在.claude/logs目录下建立任务执行日志,实时监控进度

**日志结构**:
- 日志目录: .claude/logs/tasks/
- 日志格式: JSON Lines
- 文件命名: task_{task_id}_{timestamp}.jsonl

日志内容示例:
```json
{
  "timestamp": "2025-10-01T10:30:45.123Z",
  "task_id": "task_20251001_103045",
  "event_type": "step_start|step_complete|step_failed",
  "step_id": 1,
  "step_description": "分析需求与设计API接口",
  "status": "in_progress",
  "complexity": "medium",
  "estimated_time": 300,
  "actual_time": null
}
```

### 步骤4: Hooks自动化执行机制

**目标**: 配合.claude/hooks系统,实现对话结束时的任务检查和自动继续

**Hooks脚本: conversation-end.sh**

```bash
#!/bin/bash
# .claude/hooks/conversation-end.sh
# 对话结束时检查任务完成情况

LATEST_TASK_LOG=$(ls -t .claude/logs/tasks/task_*.jsonl 2>/dev/null | head -1)

if [ -z "$LATEST_TASK_LOG" ]; then
    exit 0
fi

# 检查是否有未完成的任务
INCOMPLETE_COUNT=$(grep -c '"status":"pending\|in_progress"' "$LATEST_TASK_LOG" 2>/dev/null || echo "0")

if [ "$INCOMPLETE_COUNT" -gt 0 ]; then
    cat > ".claude/logs/tasks/continue_prompt.txt" << EOF
检测到未完成的任务 ($INCOMPLETE_COUNT 个步骤待完成)

任务日志: $LATEST_TASK_LOG

请在下次对话开始时自动执行:
1. 读取任务日志
2. 识别未完成的步骤
3. 从断点继续执行
4. 使用TodoWrite更新任务状态

继续执行命令: /T continue
EOF

    cat ".claude/logs/tasks/continue_prompt.txt"
fi

exit 0
```

### 步骤5: 质量保证与防偷懒机制

**目标**: 确保每个步骤都细致完成,避免快速敷衍了事

**防偷懒规则**:

最小执行时间要求(秒):
- trivial: 30秒 (简单任务至少30秒)
- simple: 60秒 (普通任务至少1分钟)
- medium: 180秒 (中等任务至少3分钟)
- complex: 300秒 (复杂任务至少5分钟)

质量检查逻辑:
```python
def validate_step_quality(step, execution_time):
    required_time = MIN_EXECUTION_TIME.get(step.complexity, 60)

    if execution_time < required_time:
        return False, f"执行时间过短,可能偷懒"

    return True, "质量检查通过"
```

**细致完成检查清单**:

每个步骤完成前必须确认:
- [ ] 执行时间 >= 最小要求时间
- [ ] 所有工具调用都有明确目的和结果
- [ ] 文件修改符合任务要求
- [ ] 代码更改包含必要的注释和文档
- [ ] 测试已执行并通过
- [ ] 错误处理已添加
- [ ] 满足所有验证标准

如果以上任一项未满足,步骤不应标记为completed

## 使用流程

### 1. 启动任务拆解

用户: /T <任务描述>

示例:
- /T 创建一个新的Figma API端点,用于批量替换图片
- /T 优化云存储模块的上传性能,支持并发上传
- /T 为E系列智能体添加缓存机制,减少API调用

### 2. 系统自动执行

步骤1: 解析任务意图
- 分析用户输入
- 评估任务复杂度
- 拆解为具体步骤

步骤2: 创建任务列表
- 调用TodoWrite创建todos
- 展示完整任务列表
- 等待用户确认

步骤3: 逐步执行
- 标记当前步骤为in_progress
- 执行具体操作
- 记录执行日志
- 验证步骤质量
- 标记为completed或failed

步骤4: 质量检查
- 检查执行时间
- 验证工具调用
- 确认文件修改
- 通过则继续,否则重做

步骤5: 完成或继续
- 所有步骤完成: 输出任务总结
- 对话中断: conversation-end hook触发
- 下次对话: 自动提示继续未完成任务

### 3. 继续未完成任务

场景1: 对话自然结束
- conversation-end.sh自动检查任务状态
- 发现未完成任务,生成continue_prompt.txt
- 下次对话开始时自动提示

场景2: 手动继续
- 用户: /T continue
- 系统读取最新任务日志
- 识别未完成步骤
- 从断点继续执行
- 更新TodoWrite状态

## 日志查看与分析

### 查看任务日志

查看最新任务日志:
```bash
cat $(ls -t .claude/logs/tasks/task_*.jsonl | head -1)
```

统计任务完成情况:
```bash
grep -c '"status":"completed"' .claude/logs/tasks/task_*.jsonl
```

## 相关文档

- **TodoWrite工具文档**: Claude Code内置工具说明
- **Hooks系统文档**: `.claude/hooks/README.md`
- **日志规范**: `.claude/logs/README.md`

## 总结

`/T` 命令提供了一套完整的任务拆解与执行监控系统,通过:

1. **智能拆解**: 将复杂任务分解为可管理的步骤
2. **TodoWrite集成**: 实时跟踪任务状态
3. **日志监控**: 详细记录执行过程
4. **Hooks自动化**: 自动检查和继续未完成任务
5. **质量保证**: 防止快速敷衍,确保细致完成

确保每个任务都能高质量地完成,同时支持跨对话的任务持续性

---
**版本**: 1.0.0
**最后更新**: 2025-10-01
**作者**: Claude Code Framework Team
