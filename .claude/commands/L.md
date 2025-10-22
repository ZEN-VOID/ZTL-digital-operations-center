---
name: 电脑自动化执行指令
description: 基于windows-mcp的Windows系统自动化操作,支持应用控制、UI交互、文件管理和PowerShell执行
allowed-tools: Read, Write, mcp__windows-mcp__*
argument-hint: "[自动化任务描述或应用名称]"
version: 2.1.0
last_updated: 2025-10-22
architecture: 三层架构 - 智能理解层 + 参数配置层 + 脚本执行层
mcp_integration: windows-mcp
output_directory: output/automation/system/
---

# L - 电脑自动化执行指令

> 全面的Windows系统自动化工具,集成windows-mcp实现应用控制、界面交互、文件操作和系统管理

## 📋 概述

**功能定位**: 通过windows-mcp控制Windows系统,实现桌面应用操作、UI交互、文件管理、剪贴板操作和PowerShell命令执行。

**核心能力**:
- 应用程序控制(启动/切换/调整/关闭)
- UI元素交互(点击/输入/滚动/拖拽)
- 桌面状态捕获(UI元素/截图/文本识别)
- 剪贴板管理(复制/粘贴/内容读取)
- 文件系统操作(读写/搜索/管理)
- PowerShell脚本执行(命令/脚本/批处理)

## 🎯 核心职责

### 1. 应用程序管理
- 启动Windows应用(开始菜单)
- 切换活动窗口和焦点
- 调整窗口大小和位置
- 关闭和管理运行中的应用

### 2. 用户界面交互
- 识别和定位UI元素
- 执行鼠标操作(点击/双击/右键)
- 键盘输入和快捷键
- 滚动和拖拽操作

### 3. 桌面状态获取
- 捕获当前桌面状态
- 识别交互元素和可操作内容
- 屏幕截图和视觉验证
- OCR文本识别(可选)

### 4. 剪贴板操作
- 复制文本到剪贴板
- 读取剪贴板内容
- 跨应用数据传递
- 批量复制粘贴自动化

### 5. 系统管理与脚本
- 执行PowerShell命令
- 运行批处理脚本
- 文件和目录操作
- 系统信息查询

## 🔄 工作流程

### 标准四步流程

#### 步骤1: 需求分析与规划（1-3分钟）
**输入**: 用户描述的自动化需求
**处理**:
- 理解自动化目标和操作范围
- 分析涉及的应用程序和UI元素
- 确定操作步骤和执行顺序
- 识别潜在风险和异常情况

**输出**: 结构化的操作流程方案

#### 步骤2: 环境准备与定位（1-2分钟）
**输入**: 操作流程方案
**处理**:
- 启动需要的应用程序
- 调整窗口到合适位置
- 捕获桌面状态和UI元素
- 定位目标操作对象

**输出**: 准备就绪的操作环境

#### 步骤3: 自动化操作执行（2-10分钟）
**输入**: 操作环境 + 操作步骤
**处理**:
- 按照流程顺序执行每个操作
- 处理应用响应和等待
- 验证每步操作结果
- 处理异常和错误情况

**输出**: 操作执行结果(文件/数据/状态)

#### 步骤4: 结果验证与清理（1-2分钟）
**输入**: 执行结果
**处理**:
- 验证操作是否成功完成
- 截图记录最终状态
- 生成执行报告和日志
- 清理临时文件和窗口

**输出**: 最终交付物(文件 + 报告 + 截图)

### 快速两步流程（简单场景）

**适用场景**: 单一应用操作、简单命令执行

1. **快速定位**（1分钟）: 启动应用或执行命令
2. **执行操作**（1-2分钟）: 完成指定操作并输出结果

### 高级六步流程（复杂场景）

**适用场景**: 多应用协作、复杂UI交互、批量处理

1. **深度分析**（3-5分钟）: 详细分析应用和UI结构
2. **策略制定**（2-3分钟）: 制定应对策略和备选方案
3. **环境配置**（2-3分钟）: 配置多个应用和窗口布局
4. **分步执行**（5-15分钟）: 逐步执行每个操作并记录
5. **数据处理**（3-5分钟）: 处理和验证操作结果
6. **完整验证**（2-3分钟）: 全面验证并生成报告

## 🛠️ windows-mcp工具集成

### 应用管理工具

#### 1. 启动应用程序
**工具**: `mcp__windows-mcp__Launch-Tool`
**功能**: 从开始菜单启动应用
**参数**:
- `name`: 应用名称(如"notepad", "calculator", "chrome")

**使用示例**:
```json
{
  "name": "notepad"
}
```

**使用场景**:
- 打开记事本编辑文本
- 启动浏览器访问网页
- 打开Office应用处理文档
- 启动系统工具(计算器、画图等)

#### 2. 切换窗口
**工具**: `mcp__windows-mcp__Switch-Tool`
**功能**: 切换到指定应用窗口并置于前台
**参数**:
- `name`: 应用名称

**使用场景**:
- 在多个应用间切换
- 将后台应用带到前台
- 聚焦特定窗口进行操作

#### 3. 调整窗口
**工具**: `mcp__windows-mcp__Resize-Tool`
**功能**: 调整窗口大小或移动位置
**参数**:
- `size`: 窗口尺寸[width, height]
- `loc`: 窗口位置[x, y]

**使用示例**:
```json
{
  "size": [1200, 800],
  "loc": [100, 100]
}
```

**使用场景**:
- 调整窗口到合适大小
- 并排排列多个窗口
- 移动窗口到特定屏幕位置

### 桌面交互工具

#### 4. 获取桌面状态
**工具**: `mcp__windows-mcp__State-Tool`
**功能**: 捕获当前桌面完整状态
**参数**:
- `use_vision`: 是否包含视觉截图(默认false)

**返回信息**:
- 系统界面语言
- 聚焦的应用程序
- 打开的应用列表
- 可交互UI元素(按钮/文本框/菜单)
- 可信息内容(文本/标签/状态)
- 可滚动区域
- 可选:视觉截图

**使用场景**:
- 理解当前桌面状态
- 定位UI元素坐标
- 验证操作结果
- 调试自动化脚本

#### 5. 点击操作
**工具**: `mcp__windows-mcp__Click-Tool`
**功能**: 点击UI元素或坐标点
**参数**:
- `loc`: 点击坐标[x, y]
- `button`: 鼠标按钮(left/right/middle,默认left)
- `clicks`: 点击次数(1/2/3,默认1)

**使用示例**:
```json
{
  "loc": [500, 300],
  "button": "left",
  "clicks": 1
}
```

**使用场景**:
- 点击按钮提交表单
- 双击打开文件
- 右键打开上下文菜单
- 选择菜单项

#### 6. 键盘输入
**工具**: `mcp__windows-mcp__Type-Tool`
**功能**: 在输入框中输入文本
**参数**:
- `loc`: 目标输入框坐标[x, y]
- `text`: 输入的文本内容
- `clear`: 是否清空现有文本(默认false)
- `press_enter`: 是否按Enter键(默认false)

**使用示例**:
```json
{
  "loc": [500, 300],
  "text": "Hello World",
  "clear": true,
  "press_enter": true
}
```

**使用场景**:
- 填写表单字段
- 输入搜索关键词
- 编辑文本内容
- 发送消息

#### 7. 滚动操作
**工具**: `mcp__windows-mcp__Scroll-Tool`
**功能**: 滚动页面或列表
**参数**:
- `direction`: 滚动方向(up/down/left/right,默认down)
- `type`: 滚动类型(vertical/horizontal,默认vertical)
- `wheel_times`: 滚轮次数(默认1,约3-5行)
- `loc`: 滚动位置坐标(可选)

**使用示例**:
```json
{
  "direction": "down",
  "type": "vertical",
  "wheel_times": 3
}
```

**使用场景**:
- 滚动浏览长列表
- 查看文档内容
- 翻页查看更多内容
- 水平滚动表格

#### 8. 拖拽操作
**工具**: `mcp__windows-mcp__Drag-Tool`
**功能**: 从起点拖拽到终点
**参数**:
- `from_loc`: 起始坐标[x, y]
- `to_loc`: 目标坐标[x, y]

**使用示例**:
```json
{
  "from_loc": [100, 200],
  "to_loc": [500, 400]
}
```

**使用场景**:
- 移动文件到文件夹
- 拖动滑块调整值
- 拖拽调整窗口大小
- 选中多个项目

#### 9. 鼠标移动
**工具**: `mcp__windows-mcp__Move-Tool`
**功能**: 移动鼠标到指定坐标
**参数**:
- `to_loc`: 目标坐标[x, y]

**使用场景**:
- 悬停显示提示信息
- 准备后续操作
- 触发鼠标悬停效果

#### 10. 快捷键操作
**工具**: `mcp__windows-mcp__Shortcut-Tool`
**功能**: 执行键盘快捷键组合
**参数**:
- `shortcut`: 快捷键列表(如["ctrl", "c"], ["alt", "tab"])

**常用快捷键**:
- `["ctrl", "c"]`: 复制
- `["ctrl", "v"]`: 粘贴
- `["ctrl", "a"]`: 全选
- `["ctrl", "s"]`: 保存
- `["alt", "tab"]`: 切换窗口
- `["win", "r"]`: 打开运行对话框
- `["ctrl", "alt", "del"]`: 任务管理器

**使用示例**:
```json
{
  "shortcut": ["ctrl", "c"]
}
```

#### 11. 按键操作
**工具**: `mcp__windows-mcp__Key-Tool`
**功能**: 按单个键盘按键
**参数**:
- `key`: 按键名称

**支持的按键**:
- 特殊键: "enter", "escape", "tab", "space", "backspace", "delete"
- 方向键: "up", "down", "left", "right"
- 功能键: "f1"-"f12"
- 普通字符: 字母、数字、符号

**使用示例**:
```json
{
  "key": "enter"
}
```

### 剪贴板工具

#### 12. 剪贴板操作
**工具**: `mcp__windows-mcp__Clipboard-Tool`
**功能**: 复制文本到剪贴板或读取剪贴板内容
**参数**:
- `mode`: 操作模式(copy/paste)
- `text`: 复制的文本(copy模式时需要)

**复制示例**:
```json
{
  "mode": "copy",
  "text": "要复制的文本内容"
}
```

**读取示例**:
```json
{
  "mode": "paste"
}
```

**使用场景**:
- 跨应用传递文本数据
- 批量复制粘贴操作
- 读取应用输出的文本
- 自动化数据输入

### 系统工具

#### 13. PowerShell执行
**工具**: `mcp__windows-mcp__Powershell-Tool`
**功能**: 执行PowerShell命令
**参数**:
- `command`: PowerShell命令字符串

**使用示例**:
```json
{
  "command": "Get-Process | Where-Object {$_.Name -eq 'chrome'}"
}
```

**常用命令**:
```powershell
# 文件操作
Get-ChildItem C:\path\to\directory
Copy-Item source.txt destination.txt
Move-Item file.txt new-location\
Remove-Item file.txt

# 进程管理
Get-Process
Start-Process notepad
Stop-Process -Name "chrome"

# 系统信息
Get-ComputerInfo
Get-EventLog -LogName System -Newest 10
Get-Service

# 网络操作
Test-Connection google.com
Get-NetAdapter
Invoke-WebRequest https://example.com
```

**使用场景**:
- 执行系统管理任务
- 批量文件操作
- 进程和服务管理
- 网络诊断和测试
- 系统信息查询

#### 14. 网页抓取
**工具**: `mcp__windows-mcp__Scrape-Tool`
**功能**: 获取网页内容并转换为Markdown
**参数**:
- `url`: 完整URL(包含http/https)

**使用示例**:
```json
{
  "url": "https://example.com/article"
}
```

**使用场景**:
- 提取网页文本内容
- 保存网页为Markdown
- 分析网页结构
- 内容采集和存档

#### 15. 等待延迟
**工具**: `mcp__windows-mcp__Wait-Tool`
**功能**: 暂停执行指定秒数
**参数**:
- `duration`: 等待时长(秒)

**使用示例**:
```json
{
  "duration": 3
}
```

**使用场景**:
- 等待应用启动
- 等待页面加载
- 等待动画完成
- 操作间添加延迟

## 💼 使用场景

### 场景1: 批量文件处理
**需求**: 批量重命名、移动或复制文件

**示例**:
```
用户: "将D:\photos目录下的所有jpg文件复制到D:\backup"

执行流程:
1. 使用PowerShell获取源目录文件列表
2. 筛选出.jpg文件
3. 使用Copy-Item逐个复制文件
4. 验证目标目录文件数量
5. 输出操作日志
6. 输出: output/automation/system/file-copy-log.txt
```

### 场景2: 办公软件自动化
**需求**: 自动化Excel/Word文档处理

**示例**:
```
用户: "打开Excel,填充数据并保存"

执行流程:
1. 启动Excel应用(Launch-Tool)
2. 等待应用完全启动(Wait-Tool)
3. 捕获桌面状态定位UI元素(State-Tool)
4. 点击"新建"按钮(Click-Tool)
5. 在单元格中输入数据(Type-Tool)
6. 使用快捷键Ctrl+S保存(Shortcut-Tool)
7. 截图确认保存成功
8. 输出: output/automation/system/excel-automation-report.md
```

### 场景3: 系统维护任务
**需求**: 定期清理临时文件、检查系统状态

**示例**:
```
用户: "清理系统临时文件"

执行流程:
1. 使用PowerShell查询临时文件位置
2. 统计临时文件大小
3. 删除临时文件
4. 清空回收站
5. 生成清理报告
6. 输出: output/automation/system/cleanup-report.txt
```

### 场景4: 多应用协作
**需求**: 在多个应用间传递数据

**示例**:
```
用户: "从Excel复制数据到Word文档"

执行流程:
1. 切换到Excel窗口(Switch-Tool)
2. 选中数据区域(Click + Drag)
3. 复制数据(Shortcut ["ctrl", "c"])
4. 切换到Word窗口(Switch-Tool)
5. 定位粘贴位置(Click)
6. 粘贴数据(Shortcut ["ctrl", "v"])
7. 截图验证结果
8. 输出: output/automation/system/data-transfer-success.png
```

### 场景5: 定时任务执行
**需求**: 在指定时间执行自动化任务

**示例**:
```
用户: "每天早上9点自动发送邮件"

执行流程:
1. 使用Windows任务计划程序创建定时任务
2. 设置PowerShell脚本执行时间
3. 脚本内容:
   - 启动邮件客户端
   - 打开新邮件窗口
   - 填写收件人和内容
   - 发送邮件
4. 记录执行日志
5. 输出: output/automation/system/scheduled-task-log.txt
```

### 场景6: 系统监控与告警
**需求**: 监控系统资源并在异常时告警

**示例**:
```
用户: "监控CPU使用率,超过80%时截图告警"

执行流程:
1. 使用PowerShell查询CPU使用率
2. 判断是否超过阈值
3. 如果超过,执行告警操作:
   - 截图当前桌面
   - 记录进程列表
   - 生成告警报告
4. 循环监控(每分钟检查一次)
5. 输出: output/automation/system/cpu-alert-{timestamp}.png
```

## ✅ 质量标准

### 必须达标（强制要求）

#### 1. 操作安全性
- 删除文件前必须确认
- 修改系统设置前必须备份
- 不执行潜在危险的命令
- 操作前验证路径和参数

#### 2. 可靠性
- 每个操作有明确的成功/失败判断
- UI元素定位失败时有重试机制
- 等待应用响应而非固定延迟
- 异常情况有完善的错误处理

#### 3. 数据准确性
- 文件操作验证源和目标
- 数据传递确保完整无误
- 剪贴板内容及时清空
- 日志记录完整准确

#### 4. 系统兼容性
- 支持Windows 10及以上版本
- 考虑不同分辨率和DPI设置
- 处理不同语言的系统界面
- 兼容常见应用程序版本

#### 5. 代码规范
- PowerShell脚本符合最佳实践
- 硬编码值有清晰注释
- 错误日志包含足够信息
- 临时文件及时清理

### 卓越标准（追求目标）

#### 1. 智能化
- 自动适应不同窗口布局
- 智能识别UI元素变化
- 根据系统性能调整执行速度
- 自动处理常见异常(如窗口未响应)

#### 2. 可维护性
- UI坐标配置化而非硬编码
- 操作流程模块化可复用
- 提供详细的执行日志
- 支持干运行模式(模拟执行)

#### 3. 用户体验
- 提供实时进度反馈
- 截图和日志自动归档
- 执行报告可视化展示
- 支持中断和恢复

#### 4. 扩展性
- 支持自定义操作脚本
- 提供API接口供外部调用
- 支持插件化扩展功能
- 可与其他自动化工具集成

## 🔗 协作接口

### 上游智能体

**任务来源**:
- K（网页自动化）: 浏览器外的系统操作
- 用户手动输入: 自然语言描述的自动化需求
- 配置文件: 预定义的自动化任务

### 下游智能体

**结果使用方**:
- 数据分析工具: 使用采集的数据
- 文件处理工具: 处理生成的文件
- 报告生成: 基于执行日志生成报告

### 并行协作

**同级智能体**:
- K（网页自动化）: 浏览器内的网页操作
- J（HTML页面创建）: 生成可视化报告页面

## 📁 输出规范

### 目录结构
```
output/automation/system/
├── screenshots/        # 屏幕截图
│   ├── {task-name}-{timestamp}.png
│   └── ...
├── files/             # 生成或处理的文件
│   ├── {task-name}-output.txt
│   └── ...
├── logs/              # 执行日志
│   ├── {task-name}-{timestamp}.log
│   └── ...
├── reports/           # 执行报告
│   ├── {task-name}-report.md
│   └── ...
└── scripts/           # 生成的脚本
    ├── {task-name}.ps1
    └── ...
```

### 文件命名规范
- **截图**: `{task-name}-{timestamp}.png` (如 desktop-state-20241011153000.png)
- **日志**: `{task-name}-{timestamp}.log` (如 automation-20241011153000.log)
- **报告**: `{task-name}-report.md` (如 file-processing-report.md)
- **脚本**: `{task-name}.ps1` (如 cleanup-script.ps1)

### 执行报告格式
```markdown
# 系统自动化执行报告

## 任务信息
- **任务名称**: 批量文件复制
- **执行时间**: 2025-10-11 15:30:00
- **执行时长**: 2分30秒
- **执行环境**: Windows 11, PowerShell 7.3

## 执行步骤
1. ✅ 获取源目录文件列表 (45个文件)
2. ✅ 筛选.jpg文件 (32个文件)
3. ✅ 复制文件到目标目录
4. ✅ 验证目标目录 (32个文件)

## 执行结果
**状态**: 成功
**处理文件**: 32个
**总大小**: 125.6 MB
**截图**: [final-state.png](screenshots/final-state.png)

## PowerShell命令
```powershell
Get-ChildItem D:\photos -Filter *.jpg | Copy-Item -Destination D:\backup
```

## 异常记录
无

## 下次改进
- 添加文件去重检查
- 增加进度显示
```

## 🎯 使用方法

### 基本调用
```
/L 打开记事本并输入"Hello World"
```

### 文件操作
```
/L 复制D:\source目录下的所有.txt文件到D:\backup
```

### 应用自动化
```
/L 打开计算器,计算123+456,并截图结果
```

### 系统管理
```
/L 使用PowerShell查询当前运行的进程,导出为CSV文件
```

### 复杂任务
```
/L 执行以下自动化流程:
1. 启动Excel
2. 打开指定文件
3. 复制A1:C10区域数据
4. 切换到Word
5. 粘贴数据
6. 保存并关闭两个应用
7. 截图确认完成
```

## ❓ 常见问题

### Q1: 如何处理不同分辨率的屏幕？
**A**: 使用以下策略：
- 使用相对坐标而非绝对坐标
- 通过State-Tool动态获取UI元素位置
- 调整窗口大小到固定尺寸后操作
- 使用快捷键代替点击(当可能时)

### Q2: 如何确保操作在正确的窗口执行？
**A**: 严格执行以下流程：
1. 使用Switch-Tool切换到目标窗口
2. 等待窗口获得焦点(Wait-Tool)
3. 使用State-Tool验证当前活动窗口
4. 执行操作

### Q3: PowerShell命令执行失败怎么办？
**A**: 检查以下方面：
- 确认PowerShell版本兼容性
- 检查命令语法是否正确
- 验证文件路径是否存在
- 确认有足够的权限
- 查看错误日志定位问题

### Q4: 如何提高UI元素定位的准确性？
**A**: 采用以下方法：
1. 优先使用State-Tool获取元素坐标
2. 使用use_vision=true获取视觉信息
3. 多次验证坐标的稳定性
4. 考虑窗口大小和位置的影响

### Q5: 如何实现跨应用的数据传递？
**A**: 三种方案：
1. 使用剪贴板(Clipboard-Tool)
2. 保存到临时文件后读取
3. 使用PowerShell处理数据后传递

## 📖 相关资源

### windows-mcp文档
- windows-mcp GitHub仓库
- Windows UI Automation API文档
- PowerShell官方文档

### 最佳实践
- Windows自动化最佳实践
- PowerShell脚本编写指南
- UI自动化设计模式

### 工具推荐
- Windows Spy(UI元素检查)
- PowerShell ISE(脚本开发)
- Greenshot(截图工具)

---

**版本**: 2.1.0
**更新日期**: 2025-10-22
**维护原则**: 系统自动化、应用控制、规范化
**维护者**: Claude Code Framework
**协议**: MIT License
