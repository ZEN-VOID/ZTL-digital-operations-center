# MCP输出路径规范说明

## 🎯 问题说明

**原配置问题**:
```json
"MINIMAX_MCP_BASE_PATH": "/Users/vincentlee/Desktop/AIGC数字游牧派影视文化公司/output"
```

这是**绝对路径**,会导致以下问题:
- ❌ 所有项目都输出到同一个目录
- ❌ 多项目输出混杂,难以管理
- ❌ 配置文件不可移植
- ❌ 不符合项目输出路径规范

## ✅ 修正后的配置

**新配置** (相对路径):
```json
"MINIMAX_MCP_BASE_PATH": "output"
```

这是**相对路径**,相对于**当前工作目录** (Claude Code的工作目录),优势:
- ✅ 每个项目输出到自己的output目录
- ✅ 多项目完全隔离
- ✅ 配置文件可移植
- ✅ 符合项目标准化规范

---

## 📁 输出路径规范

根据全局CLAUDE.md定义的标准化输出路径规范:

### 标准路径格式

```
output/[项目名]/[agent-or-skill-name]/
├── plans/      # 执行计划配置 (JSON/YAML)
├── results/    # 实际输出结果
├── logs/       # 执行日志
└── metadata/   # 元数据和追溯信息
```

### 应用到MiniMax

**在当前项目中** (ZTL数智化作战中心):
```
output/
├── [项目名1]/
│   └── minimax/
│       ├── videos/      # 视频生成
│       ├── audios/      # 音频合成
│       ├── images/      # 图像生成
│       └── metadata/    # 元数据
├── [项目名2]/
│   └── minimax/
│       └── ...
```

**在其他项目中** (如AIGC数字游牧派):
```
/Users/vincentlee/Desktop/AIGC数字游牧派影视文化公司/
└── output/
    └── [项目名]/
        └── minimax/
            ├── videos/
            ├── audios/
            └── images/
```

### 使用示例

**项目A - ZTL数智化作战中心**:
```bash
cd "/Users/vincentlee/Desktop/ZTL数智化作战中心"

# 用户请求: "用MiniMax生成火锅店宣传视频"
# 输出路径: output/火锅店开业筹备/minimax/videos/
```

**项目B - AIGC数字游牧派**:
```bash
cd "/Users/vincentlee/Desktop/AIGC数字游牧派影视文化公司"

# 用户请求: "用MiniMax生成影视海报"
# 输出路径: output/影视项目筹备/minimax/images/
```

**完全隔离**: 两个项目的输出互不影响!

---

## 🔧 工作原理

### MiniMax MCP的路径解析

MiniMax MCP服务器在运行时会:

1. **读取环境变量**:
   ```
   MINIMAX_MCP_BASE_PATH = "output"
   ```

2. **获取当前工作目录**:
   ```python
   import os
   cwd = os.getcwd()
   # 例如: /Users/vincentlee/Desktop/ZTL数智化作战中心
   ```

3. **拼接完整路径**:
   ```python
   full_path = os.path.join(cwd, "output")
   # 结果: /Users/vincentlee/Desktop/ZTL数智化作战中心/output
   ```

4. **按项目名和agent名创建子目录**:
   ```python
   project_name = "火锅店开业筹备"  # 由Claude或用户指定
   agent_name = "minimax"

   output_dir = os.path.join(full_path, project_name, agent_name)
   # 结果: .../output/火锅店开业筹备/minimax/
   ```

### Claude Code的工作目录

**重要**: Claude Code的当前工作目录是:
- 用户明确打开的项目目录
- 或用户通过 `cd` 命令切换到的目录

**示例**:
```bash
# 在Claude Code中
pwd
# 输出: /Users/vincentlee/Desktop/ZTL数智化作战中心

# 使用MiniMax生成内容
# 输出: /Users/vincentlee/Desktop/ZTL数智化作战中心/output/[项目名]/minimax/
```

---

## 📊 路径对比

### 使用绝对路径 (原配置 - 错误)

| 项目 | 工作目录 | 输出路径 |
|------|---------|---------|
| ZTL数智化作战中心 | `/Users/vincentlee/Desktop/ZTL数智化作战中心` | ❌ `/Users/vincentlee/Desktop/AIGC数字游牧派影视文化公司/output` |
| AIGC数字游牧派 | `/Users/vincentlee/Desktop/AIGC数字游牧派影视文化公司` | ❌ `/Users/vincentlee/Desktop/AIGC数字游牧派影视文化公司/output` |
| 其他任意项目 | `/path/to/any/project` | ❌ `/Users/vincentlee/Desktop/AIGC数字游牧派影视文化公司/output` |

**问题**: 所有项目都输出到同一个目录!

### 使用相对路径 (新配置 - 正确)

| 项目 | 工作目录 | 输出路径 |
|------|---------|---------|
| ZTL数智化作战中心 | `/Users/vincentlee/Desktop/ZTL数智化作战中心` | ✅ `/Users/vincentlee/Desktop/ZTL数智化作战中心/output/[项目名]/minimax/` |
| AIGC数字游牧派 | `/Users/vincentlee/Desktop/AIGC数字游牧派影视文化公司` | ✅ `/Users/vincentlee/Desktop/AIGC数字游牧派影视文化公司/output/[项目名]/minimax/` |
| 其他任意项目 | `/path/to/any/project` | ✅ `/path/to/any/project/output/[项目名]/minimax/` |

**优势**: 每个项目输出到自己的目录!

---

## 🎯 项目名称管理

根据输出路径规范,**项目名称** 是动态的,由以下方式确定:

### 1. 用户显式指定

```
使用MiniMax为"火锅店开业筹备"项目生成宣传视频
```

Claude会提取项目名: `火锅店开业筹备`

### 2. 从上下文推断

```
# 当前正在讨论火锅店开业相关话题
使用MiniMax生成宣传视频
```

Claude根据对话上下文推断项目名

### 3. 使用默认项目名

```
# 无明确项目上下文
使用MiniMax生成一张图片
```

使用默认项目名,例如: `临时生成` 或 `未命名项目`

### 命名建议

**好的项目名**:
- ✅ "火锅店开业筹备"
- ✅ "美团营业额提升计划"
- ✅ "2025Q1产品宣传"
- ✅ "影视项目筹备"

**不好的项目名**:
- ❌ "20250129任务"
- ❌ "test"
- ❌ "临时"

---

## 🔍 验证配置

### 检查当前配置

```bash
# 查看MiniMax配置
cat "/Library/Application Support/ClaudeCode/managed-mcp.json" | \
  python3 -c "import sys, json; \
  config = json.load(sys.stdin); \
  print('MINIMAX_MCP_BASE_PATH:', config['mcpServers']['minimax-mcp']['env']['MINIMAX_MCP_BASE_PATH'])"
```

**预期输出**:
```
MINIMAX_MCP_BASE_PATH: output
```

### 测试输出路径

**在ZTL项目中**:
```bash
cd "/Users/vincentlee/Desktop/ZTL数智化作战中心"
pwd
# 输出: /Users/vincentlee/Desktop/ZTL数智化作战中心

# 在Claude Code中使用MiniMax
# 输出路径: output/[项目名]/minimax/
```

**在AIGC项目中**:
```bash
cd "/Users/vincentlee/Desktop/AIGC数字游牧派影视文化公司"
pwd
# 输出: /Users/vincentlee/Desktop/AIGC数字游牧派影视文化公司

# 在Claude Code中使用MiniMax
# 输出路径: output/[项目名]/minimax/
```

---

## 📝 最佳实践

### 1. 始终使用相对路径

**MCP配置**:
```json
{
  "env": {
    "MINIMAX_MCP_BASE_PATH": "output",  // ✅ 相对路径
    "SOME_OTHER_PATH": "output/custom"  // ✅ 相对路径
  }
}
```

**避免**:
```json
{
  "env": {
    "MINIMAX_MCP_BASE_PATH": "/absolute/path/output",  // ❌ 绝对路径
  }
}
```

### 2. 明确项目名称

在使用MiniMax时,明确指定项目名:
```
使用MiniMax为"火锅店开业筹备"项目生成:
- 开业海报
- 宣传视频
- 欢迎语音
```

### 3. 遵循目录结构

按照标准化规范组织输出:
```
output/
└── [项目名]/
    └── minimax/
        ├── videos/      # 视频文件
        ├── audios/      # 音频文件
        ├── images/      # 图像文件
        └── metadata/    # 元数据
```

### 4. 及时清理

定期清理旧的输出文件:
```bash
# 清理30天前的文件
find output -type f -mtime +30 -delete

# 或按项目清理
rm -rf "output/旧项目名"
```

---

## 🎯 总结

### 关键变更

**修改前**:
```json
"MINIMAX_MCP_BASE_PATH": "/Users/vincentlee/Desktop/AIGC数字游牧派影视文化公司/output"
```

**修改后**:
```json
"MINIMAX_MCP_BASE_PATH": "output"
```

### 优势

- ✅ **多项目隔离**: 每个项目独立输出目录
- ✅ **可移植性**: 配置在任何机器上都能工作
- ✅ **符合规范**: 遵循项目标准化路径规范
- ✅ **便于管理**: 项目文件集中在项目目录下

### 实际效果

**ZTL数智化作战中心项目**:
```
/Users/vincentlee/Desktop/ZTL数智化作战中心/
├── output/
│   ├── 火锅店开业筹备/
│   │   └── minimax/
│   │       ├── videos/
│   │       ├── audios/
│   │       └── images/
│   └── 美团营业额提升/
│       └── minimax/
│           └── ...
```

**AIGC数字游牧派项目**:
```
/Users/vincentlee/Desktop/AIGC数字游牧派影视文化公司/
├── output/
│   ├── 影视项目筹备/
│   │   └── minimax/
│   │       ├── videos/
│   │       └── images/
│   └── 短视频创作/
│       └── minimax/
│           └── ...
```

**完美隔离**: 两个项目互不干扰!

---

## 🚀 下一步

1. **重启Claude Code**: 使新配置生效
2. **测试验证**: 在不同项目中测试MiniMax输出
3. **更新文档**: 其他文档引用已同步更新

**配置修正时间**: 2025-10-29
**修正状态**: ✅ 完成
**符合规范**: ✅ 遵循项目标准化输出路径规范
