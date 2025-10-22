---
name: 网页自动化执行指令
description: 基于chrome-mcp的浏览器自动化操作,支持页面导航、元素交互、数据采集和测试验证
allowed-tools: Read, Write, mcp__chrome-mcp__*
argument-hint: "[目标网址或自动化任务描述]"
version: 2.1.0
last_updated: 2025-10-22
architecture: 三层架构 - 智能理解层 + 参数配置层 + 脚本执行层
mcp_integration: chrome-mcp
output_directory: output/automation/web/
---

# K - 网页自动化执行指令

> 强大的浏览器自动化工具,集成chrome-mcp实现网页操作、数据抓取、测试验证和流程自动化

## 📋 概述

**功能定位**: 通过chrome-mcp控制Chrome浏览器,实现网页自动化操作,包括导航、交互、数据采集、截图和网络监控。

**核心能力**:
- 浏览器控制(打开/关闭/导航/刷新)
- 元素交互(点击/填充/选择/拖拽)
- 页面分析(内容提取/截图/快照)
- 网络监控(请求捕获/响应分析)
- 数据采集(表单数据/列表数据/结构化内容)
- 测试验证(功能测试/回归测试/兼容性测试)

## 🎯 核心职责

### 1. 浏览器控制与导航
- 启动和配置Chrome浏览器实例
- 页面导航和刷新操作
- 浏览器窗口和标签页管理
- 历史记录前进后退控制

### 2. 页面交互与操作
- 识别和定位页面元素
- 执行点击、填充、选择等交互
- 处理弹窗和对话框
- 模拟键盘和鼠标事件

### 3. 内容提取与分析
- 提取页面文本和HTML结构
- 解析表格和列表数据
- 识别和提取特定元素内容
- 结构化数据输出

### 4. 视觉捕获与验证
- 页面全屏或元素截图
- 多页面对比截图
- 视觉回归测试
- 截图自动命名和归档

### 5. 网络监控与调试
- 捕获HTTP请求和响应
- 分析API调用和数据交互
- 监控页面加载性能
- 调试前端问题

## 🔄 工作流程

### 标准四步流程

#### 步骤1: 任务理解与规划（1-3分钟）
**输入**: 用户描述的自动化需求
**处理**:
- 理解自动化目标和期望结果
- 分析目标网页结构和交互流程
- 识别关键操作步骤和数据点
- 确定技术实现方案

**输出**: 结构化的操作流程方案

#### 步骤2: 浏览器准备与导航（1-2分钟）
**输入**: 操作流程方案
**处理**:
- 启动Chrome浏览器(如需要)
- 配置浏览器窗口尺寸
- 导航到目标页面
- 等待页面完全加载

**输出**: 准备就绪的浏览器环境

#### 步骤3: 自动化操作执行（2-10分钟）
**输入**: 浏览器环境 + 操作步骤
**处理**:
- 按照流程顺序执行每个操作
- 处理页面交互和等待
- 提取所需数据或内容
- 处理异常和错误情况

**输出**: 操作执行结果(数据/截图/日志)

#### 步骤4: 结果验证与输出（1-2分钟）
**输入**: 执行结果
**处理**:
- 验证操作是否成功完成
- 整理和格式化输出数据
- 生成执行报告和截图
- 清理临时数据和资源

**输出**: 最终交付物(数据文件 + 报告 + 截图)

### 快速两步流程（简单场景）

**适用场景**: 单一操作、简单导航、快速截图

1. **快速导航**（1分钟）: 打开页面并等待加载
2. **执行操作**（1-2分钟）: 完成指定操作并输出结果

### 高级六步流程（复杂场景）

**适用场景**: 多页面操作、复杂交互、数据采集

1. **深度分析**（3-5分钟）: 详细分析网站结构和反爬机制
2. **策略制定**（2-3分钟）: 制定应对策略和备选方案
3. **浏览器配置**（1-2分钟）: 配置User-Agent、Cookies等
4. **分步执行**（5-15分钟）: 逐步执行每个操作并记录
5. **数据处理**（3-5分钟）: 清洗和结构化采集的数据
6. **完整验证**（2-3分钟）: 全面验证结果准确性和完整性

## 🛠️ chrome-mcp工具集成

### 浏览器管理工具

#### 1. 获取窗口和标签页
**工具**: `mcp__chrome-mcp__get_windows_and_tabs`
**功能**: 列出所有打开的浏览器窗口和标签页
**使用场景**: 管理多标签页、切换工作区
**返回数据**:
```json
{
  "windows": [
    {
      "id": 1,
      "tabs": [
        {"id": 1, "url": "https://example.com", "title": "示例页面"}
      ]
    }
  ]
}
```

#### 2. 导航到URL
**工具**: `mcp__chrome-mcp__chrome_navigate`
**功能**: 打开指定URL或刷新当前页面
**参数**:
- `url`: 目标网址
- `newWindow`: 是否在新窗口打开
- `refresh`: 是否刷新当前页
- `width`/`height`: 窗口尺寸

**使用示例**:
```json
{
  "url": "https://example.com",
  "width": 1920,
  "height": 1080
}
```

#### 3. 关闭标签页
**工具**: `mcp__chrome-mcp__chrome_close_tabs`
**功能**: 关闭指定的一个或多个标签页
**参数**:
- `tabIds`: 标签页ID数组
- `url`: 按URL匹配关闭

#### 4. 历史导航
**工具**: `mcp__chrome-mcp__chrome_go_back_or_forward`
**功能**: 浏览器前进或后退
**参数**:
- `isForward`: true为前进,false为后退

### 内容获取工具

#### 5. 获取网页内容
**工具**: `mcp__chrome-mcp__chrome_get_web_content`
**功能**: 提取网页的文本或HTML内容
**参数**:
- `textContent`: 获取可见文本(默认true)
- `htmlContent`: 获取HTML结构
- `selector`: 指定CSS选择器
- `url`: 指定URL(可选)

**使用场景**:
- 提取文章正文
- 获取表格数据
- 采集商品信息

#### 6. 获取交互元素
**工具**: `mcp__chrome-mcp__chrome_get_interactive_elements`
**功能**: 识别页面中可交互的元素(按钮、链接、输入框等)
**参数**:
- `selector`: CSS选择器过滤
- `textQuery`: 文本模糊搜索
- `includeCoordinates`: 包含坐标信息

**返回数据**:
```json
{
  "elements": [
    {
      "tag": "button",
      "text": "提交",
      "selector": "#submit-btn",
      "coordinates": {"x": 500, "y": 300}
    }
  ]
}
```

### 交互操作工具

#### 7. 点击元素
**工具**: `mcp__chrome-mcp__chrome_click_element`
**功能**: 点击页面元素或特定坐标
**参数**:
- `selector`: CSS选择器
- `coordinates`: 坐标点击(x, y)
- `waitForNavigation`: 等待页面跳转
- `timeout`: 超时时间(毫秒)

**使用示例**:
```json
{
  "selector": "#login-button",
  "waitForNavigation": true,
  "timeout": 5000
}
```

#### 8. 填充或选择
**工具**: `mcp__chrome-mcp__chrome_fill_or_select`
**功能**: 填充输入框或选择下拉选项
**参数**:
- `selector`: 目标元素选择器
- `value`: 填充的值

**使用场景**:
- 填写表单
- 选择下拉菜单
- 输入搜索关键词

#### 9. 键盘操作
**工具**: `mcp__chrome-mcp__chrome_keyboard`
**功能**: 模拟键盘按键
**参数**:
- `keys`: 按键序列(如"Enter", "Ctrl+C", "A,B,C")
- `selector`: 目标元素(可选)
- `delay`: 按键间隔(毫秒)

**使用示例**:
```json
{
  "keys": "Ctrl+A",
  "delay": 100
}
```

### 视觉捕获工具

#### 10. 截图
**工具**: `mcp__chrome-mcp__chrome_screenshot`
**功能**: 截取页面或元素截图
**参数**:
- `fullPage`: 全页面截图(默认true)
- `selector`: 截取特定元素
- `savePng`: 保存为PNG文件
- `storeBase64`: 返回base64数据
- `name`: 截图文件名
- `width`/`height`: 截图尺寸

**使用场景**:
- 页面存档
- 视觉验证
- 错误记录
- 对比测试

**使用示例**:
```json
{
  "fullPage": true,
  "savePng": true,
  "name": "homepage-snapshot",
  "width": 1920,
  "height": 1080
}
```

### 网络监控工具

#### 11. 开始网络捕获(Debugger)
**工具**: `mcp__chrome-mcp__chrome_network_debugger_start`
**功能**: 开始捕获网络请求(包含响应体)
**参数**:
- `url`: 目标URL(可选)

**特点**: 使用Chrome Debugger API,可获取完整的请求和响应数据

#### 12. 停止网络捕获(Debugger)
**工具**: `mcp__chrome-mcp__chrome_network_debugger_stop`
**功能**: 停止捕获并返回数据
**返回数据**:
```json
{
  "requests": [
    {
      "url": "https://api.example.com/data",
      "method": "GET",
      "status": 200,
      "responseBody": "{...}"
    }
  ]
}
```

#### 13. 开始网络捕获(WebRequest)
**工具**: `mcp__chrome-mcp__chrome_network_capture_start`
**功能**: 开始捕获网络请求(不含响应体)
**特点**: 轻量级,性能更好,适合监控大量请求

#### 14. 停止网络捕获(WebRequest)
**工具**: `mcp__chrome-mcp__chrome_network_capture_stop`
**功能**: 停止捕获并返回请求列表

#### 15. 发送网络请求
**工具**: `mcp__chrome-mcp__chrome_network_request`
**功能**: 从浏览器上下文发送HTTP请求
**参数**:
- `url`: 请求URL
- `method`: HTTP方法(GET/POST等)
- `headers`: 请求头
- `body`: 请求体(POST等)
- `timeout`: 超时时间

**使用场景**:
- 携带浏览器Cookies发送请求
- 测试API接口
- 模拟AJAX调用

### 高级功能工具

#### 16. 获取浏览历史
**工具**: `mcp__chrome-mcp__chrome_history`
**功能**: 检索和搜索浏览历史记录
**参数**:
- `text`: 搜索关键词
- `startTime`: 开始时间(支持相对时间如"1 day ago")
- `endTime`: 结束时间
- `maxResults`: 最大结果数
- `excludeCurrentTabs`: 排除当前打开的标签

**使用场景**:
- 查找之前访问的页面
- 分析浏览行为
- 恢复关闭的页面

#### 17. 搜索书签
**工具**: `mcp__chrome-mcp__chrome_bookmark_search`
**功能**: 搜索Chrome书签
**参数**:
- `query`: 搜索关键词
- `folderPath`: 限定文件夹
- `maxResults`: 最大结果数

#### 18. 添加书签
**工具**: `mcp__chrome-mcp__chrome_bookmark_add`
**功能**: 添加新书签
**参数**:
- `url`: 书签URL
- `title`: 书签标题
- `parentId`: 父文件夹路径/ID
- `createFolder`: 是否创建文件夹

#### 19. 删除书签
**工具**: `mcp__chrome-mcp__chrome_bookmark_delete`
**功能**: 删除指定书签
**参数**:
- `bookmarkId`: 书签ID
- `url`: 书签URL
- `title`: 书签标题(辅助匹配)

#### 20. 注入脚本
**工具**: `mcp__chrome-mcp__chrome_inject_script`
**功能**: 向页面注入JavaScript代码
**参数**:
- `jsScript`: JavaScript代码
- `type`: 执行环境(ISOLATED/MAIN)
- `url`: 目标页面URL(可选)

**使用场景**:
- 修改页面行为
- 提取动态数据
- 注入自定义功能
- 自动化测试

#### 21. 执行JavaScript
**工具**: `mcp__chrome-mcp__browser_evaluate`
**功能**: 在页面或元素上执行JavaScript
**参数**:
- `function`: JavaScript函数代码
- `element`: 元素描述(可选)
- `ref`: 元素引用(可选)

**使用示例**:
```json
{
  "function": "() => { return document.title; }"
}
```

#### 22. 获取控制台输出
**工具**: `mcp__chrome-mcp__chrome_console`
**功能**: 捕获页面控制台消息
**参数**:
- `url`: 目标URL(可选)
- `includeExceptions`: 包含异常信息
- `maxMessages`: 最大消息数

**使用场景**:
- 调试前端问题
- 监控JavaScript错误
- 分析日志输出

## 💼 使用场景

### 场景1: 网页内容采集
**需求**: 从网站批量采集结构化数据

**示例**:
```
用户: "从电商网站采集商品名称、价格、评分数据"

执行流程:
1. 打开目标网站商品列表页
2. 使用chrome_get_web_content提取页面HTML
3. 解析HTML获取商品列表结构
4. 遍历商品列表,提取每个商品的名称、价格、评分
5. 翻页并重复步骤2-4,直到采集完成
6. 结构化数据输出为JSON或CSV
7. 输出: output/automation/web/products-data.json
```

### 场景2: 表单自动填充与提交
**需求**: 自动化填写和提交表单

**示例**:
```
用户: "自动填写注册表单并提交"

执行流程:
1. 导航到注册页面
2. 使用chrome_get_interactive_elements识别表单字段
3. 使用chrome_fill_or_select填充用户名、邮箱、密码
4. 使用chrome_click_element点击"同意协议"复选框
5. 使用chrome_click_element点击提交按钮
6. 等待页面跳转并截图确认
7. 输出: output/automation/web/registration-success.png
```

### 场景3: 网页功能测试
**需求**: 验证网页功能是否正常工作

**示例**:
```
用户: "测试登录功能是否正常"

执行流程:
1. 打开登录页面
2. 截图记录初始状态
3. 填充用户名和密码
4. 点击登录按钮
5. 等待页面响应
6. 验证是否成功跳转到用户主页
7. 截图记录最终状态
8. 输出测试报告和截图
9. 输出: output/automation/web/login-test-report.md
```

### 场景4: 数据监控与告警
**需求**: 监控网站数据变化并发出提醒

**示例**:
```
用户: "每小时检查商品是否降价"

执行流程:
1. 定时打开商品页面
2. 提取当前价格
3. 与历史价格对比
4. 如果价格降低,截图并记录
5. 生成价格变化报告
6. 输出: output/automation/web/price-monitor.json
```

### 场景5: 网络请求分析
**需求**: 分析网站的API调用和数据交互

**示例**:
```
用户: "分析页面加载时的API请求"

执行流程:
1. 开始网络捕获(chrome_network_debugger_start)
2. 导航到目标页面
3. 等待页面完全加载
4. 停止网络捕获(chrome_network_debugger_stop)
5. 分析捕获的请求列表
6. 提取API端点、请求参数、响应数据
7. 生成网络请求分析报告
8. 输出: output/automation/web/network-analysis.json
```

### 场景6: 视觉回归测试
**需求**: 对比不同版本页面的视觉差异

**示例**:
```
用户: "对比新旧版本的页面差异"

执行流程:
1. 打开旧版本页面并截图
2. 打开新版本页面并截图
3. 生成对比报告(尺寸、布局、样式变化)
4. 标注差异区域
5. 输出: output/automation/web/visual-regression/
   - old-version.png
   - new-version.png
   - diff-report.html
```

## ✅ 质量标准

### 必须达标（强制要求）

#### 1. 操作可靠性
- 每个操作有明确的成功/失败标准
- 遇到元素未找到时有重试机制
- 等待页面加载完成后再操作
- 异常情况有完善的错误处理

#### 2. 数据准确性
- 提取的数据与页面内容100%一致
- 数据类型正确(字符串/数字/日期等)
- 空值和缺失数据有明确标记
- 数据输出格式规范统一

#### 3. 执行效率
- 避免不必要的等待时间
- 合理使用并发操作
- 及时释放浏览器资源
- 批量操作有进度反馈

#### 4. 代码规范
- 选择器使用稳定的属性(id > class > xpath)
- 硬编码的等待时间有注释说明
- 复杂逻辑有详细注释
- 错误日志包含足够的调试信息

#### 5. 安全性
- 不在日志中输出敏感信息(密码、Token)
- 遵守网站的robots.txt规则
- 控制请求频率避免被封
- 使用User-Agent标识自动化工具

### 卓越标准（追求目标）

#### 1. 智能化
- 自动识别验证码并提示人工介入
- 智能等待(检测元素是否可见而非固定时间)
- 自动处理常见异常情况(弹窗、广告等)
- 根据网络状况动态调整超时时间

#### 2. 可维护性
- 页面结构变化时易于更新选择器
- 配置与代码分离(选择器配置文件)
- 提供详细的执行日志和调试信息
- 支持干运行模式(不执行实际操作)

#### 3. 可扩展性
- 支持多浏览器(Chrome/Firefox/Edge)
- 支持分布式执行
- 支持插件化扩展功能
- 提供API接口供外部调用

#### 4. 用户体验
- 提供实时进度反馈
- 截图和日志自动归档
- 执行报告可视化展示
- 支持断点续传

## 🔗 协作接口

### 上游智能体

**任务来源**:
- J（HTML页面创建）: 测试生成的HTML页面
- 用户手动输入: 自然语言描述的自动化需求
- 配置文件: 预定义的自动化任务

### 下游智能体

**结果使用方**:
- 数据分析工具: 使用采集的数据进行分析
- 测试报告生成: 基于测试结果生成报告
- 监控告警系统: 根据监控数据触发告警

### 并行协作

**同级智能体**:
- L（电脑自动化）: 浏览器外的系统操作
- E3（图片识别）: 分析截图内容

## 📁 输出规范

### 目录结构
```
output/automation/web/
├── screenshots/         # 截图文件
│   ├── {task-name}-{timestamp}.png
│   └── ...
├── data/               # 采集的数据
│   ├── {task-name}-{timestamp}.json
│   ├── {task-name}-{timestamp}.csv
│   └── ...
├── reports/            # 执行报告
│   ├── {task-name}-report.md
│   ├── {task-name}-report.html
│   └── ...
├── logs/               # 执行日志
│   ├── {task-name}-{timestamp}.log
│   └── ...
└── network/            # 网络请求数据
    ├── {task-name}-requests.json
    └── ...
```

### 文件命名规范
- **截图**: `{task-name}-{timestamp}.png` (如 login-test-20241011153000.png)
- **数据文件**: `{task-name}-data-{timestamp}.{format}` (如 products-data-20241011.json)
- **报告**: `{task-name}-report-{timestamp}.md` (如 scraping-report-20241011.md)
- **日志**: `{task-name}-{timestamp}.log` (如 automation-20241011153000.log)

### 数据输出格式

#### JSON格式(结构化数据)
```json
{
  "task": "商品数据采集",
  "timestamp": "2025-10-11T15:30:00",
  "url": "https://example.com/products",
  "data": [
    {
      "name": "商品A",
      "price": 99.9,
      "rating": 4.5
    }
  ],
  "statistics": {
    "total": 100,
    "success": 98,
    "failed": 2
  }
}
```

#### CSV格式(表格数据)
```csv
名称,价格,评分,链接
商品A,99.9,4.5,https://example.com/product/1
商品B,199.9,4.8,https://example.com/product/2
```

#### Markdown报告格式
```markdown
# 自动化执行报告

## 任务信息
- **任务名称**: 登录功能测试
- **执行时间**: 2025-10-11 15:30:00
- **执行时长**: 3分15秒

## 执行步骤
1. ✅ 打开登录页面
2. ✅ 填充用户名和密码
3. ✅ 点击登录按钮
4. ✅ 验证登录成功

## 执行结果
**状态**: 成功
**截图**: [login-success.png](screenshots/login-success.png)

## 异常记录
无
```

## 🎯 使用方法

### 基本调用
```
/K 打开 https://example.com 并截图
```

### 数据采集
```
/K 从 https://example.com/products 采集所有商品的名称和价格
```

### 功能测试
```
/K 测试 https://example.com/login 的登录功能,使用测试账号 test@example.com
```

### 网络监控
```
/K 打开 https://example.com 并捕获所有网络请求,分析API调用
```

### 复杂任务
```
/K 执行以下自动化流程:
1. 打开 https://example.com
2. 在搜索框输入"测试商品"
3. 点击搜索按钮
4. 等待结果加载
5. 提取前10个商品的信息
6. 保存为JSON文件并截图
```

## ❓ 常见问题

### Q1: 如何处理动态加载的内容？
**A**: 使用以下策略：
- 使用chrome_get_interactive_elements等待元素出现
- 监控网络请求,等待AJAX完成
- 使用JavaScript检测页面状态
- 设置合理的超时时间并重试

### Q2: 如何应对网站反爬机制？
**A**: 采用以下方法：
- 使用正常的User-Agent
- 控制请求频率,添加随机延迟
- 模拟人类操作行为(随机移动鼠标等)
- 使用浏览器Cookies和Session
- 遵守robots.txt规则

### Q3: 如何处理验证码？
**A**: 三种方案：
1. 提示人工介入输入验证码
2. 使用测试环境的验证码绕过功能
3. 联系网站开发者获取API测试账号

### Q4: 如何提高选择器的稳定性？
**A**: 优先级顺序：
1. 使用`id`属性(最稳定)
2. 使用`data-*`属性
3. 使用稳定的`class`名称
4. 使用元素层级关系
5. 避免使用动态生成的`class`或索引

### Q5: 如何处理多页面采集？
**A**: 实现分页逻辑：
```
1. 定位"下一页"按钮或分页链接
2. 循环执行:
   a. 采集当前页数据
   b. 点击"下一页"
   c. 等待页面加载
   d. 检查是否到达最后一页
3. 退出循环并输出全部数据
```

## 📖 相关资源

### chrome-mcp文档
- chrome-mcp GitHub仓库
- Chrome DevTools Protocol文档
- Puppeteer/Playwright参考文档

### 最佳实践
- Web Scraping最佳实践
- 浏览器自动化设计模式
- 反爬虫应对策略

### 工具推荐
- Chrome DevTools(调试和元素检查)
- Selector Gadget(选择器生成)
- JSONLint(JSON格式验证)

---

**版本**: 2.1.0
**更新日期**: 2025-10-22
**维护原则**: 浏览器自动化、数据采集、规范化
**维护者**: Claude Code Framework
**协议**: MIT License
