# Scripts 目录说明

核心Python脚本工具集,支持批量图片替换、URL管理和自动化工作流。

## ⚡ 核心设计理念

### 配置驱动,脚本复用 (Configuration-Driven, Script Reuse)

**关键原则**: 快捷键命令(`/1`, `/2`, `/3`, `/4`)的实现基于**生成新的配置文件**让**同一个核心脚本**来完成执行,而**不是每次都生成新的脚本**,避免资源浪费。

#### ❌ 错误模式 - 脚本重复生成(资源浪费)
```yaml
用户请求 → 生成新脚本 → 执行新脚本 → 丢弃脚本
用户请求 → 生成新脚本 → 执行新脚本 → 丢弃脚本
用户请求 → 生成新脚本 → 执行新脚本 → 丢弃脚本

问题:
  - 每次请求都生成相同逻辑的脚本
  - 造成大量冗余代码和维护负担
  - 脚本质量无法统一保证
  - 浪费计算资源和存储空间
```

#### ✅ 正确模式 - 配置驱动,脚本复用
```yaml
用户请求 → 生成配置文件 → 核心脚本读取配置 → 执行任务
用户请求 → 生成配置文件 → 核心脚本读取配置 → 执行任务
用户请求 → 生成配置文件 → 核心脚本读取配置 → 执行任务

优势:
  - 核心脚本经过充分测试,稳定可靠
  - 配置文件轻量化,易于管理和版本控制
  - 参数化设计,灵活应对不同场景
  - 资源高效,无冗余代码
```

### 快捷键命令的实现方式

| 命令 | 配置文件 | 核心脚本 | 功能说明 |
|------|----------|----------|----------|
| `/1` | `input/明红/图片URL/[模板]/cos-index.json` | `batch_extract_cos_urls.py` | 从腾讯云COS提取图片URL并生成索引 |
| `/2` | `input/明红/图片URL/随机组合/[模板]/random_*.json` | `batch_random_url_combination.py` | 批量生成随机URL组合配置 |
| `/3` | `scripts/configs/batch_replace/task_config.json` | `batch_replace_images.py` | 批量图片替换和截图 |
| `/4` | `library/figma-informations/[fileId]_[pageName]_raw.json` | `figma_to_next.py` | Figma设计稿转Next.js页面 |

### 工作流程图

```
┌──────────────┐
│ 用户输入     │ 例: /3 模板页面: three-day-tour, 处理 random_01 ~ random_50
└──────┬───────┘
       ↓
┌──────────────┐
│ AI意图理解   │ 解析: 页面=three-day-tour, 文件=random_01~50, 任务=批量替换
└──────┬───────┘
       ↓
┌──────────────┐
│ 生成配置文件 │ 创建: scripts/configs/batch_replace/task_config.json
└──────┬───────┘       (包含50个input_files配置项)
       ↓
┌──────────────┐
│ 复用核心脚本 │ 执行: python scripts/batch_replace_images.py
└──────┬───────┘       (读取配置,执行批量任务)
       ↓
┌──────────────┐
│ 输出结果     │ 生成: output/model/*.png (50张截图)
└──────────────┘
```

### 设计哲学总结

1. **一次编写,多次复用**: 核心脚本经过充分测试和优化,通过配置文件适配不同场景
2. **配置即文档**: 配置文件清晰记录每次任务的参数,可追溯、可复现
3. **关注点分离**: AI专注理解意图和生成配置,脚本专注稳定执行
4. **资源高效**: 避免生成大量功能相同的脚本,节省存储和维护成本

---

## 核心脚本

### 1. batch_replace_images.py ⭐⭐⭐⭐⭐
**批量图片替换核心引擎**

**功能**:
- 从配置文件读取任务参数,执行批量图片替换和截图
- 支持精确映射和通用选择器两种替换模式
- 自动化页面加载、图片替换、样式调整和精确截图

**使用方法**:
```bash
# 使用默认配置
python scripts/batch_replace_images.py

# 指定配置文件
python scripts/batch_replace_images.py scripts/configs/batch_replace/task_config.json
```

**配置文件**: `scripts/configs/batch_replace/task_config.json`

**输出**: `output/model/*.png`

**技术特性**:
- 基于Playwright的浏览器自动化
- 精确的CSS选择器定位
- 智能的背景图片加载验证
- 自动从CSS提取页面尺寸
- 支持并发控制(当前设为串行避免服务器过载)

### 2. batch_extract_cos_urls.py
**腾讯云COS URL批量提取工具**

**功能**:
- 从腾讯云COS存储桶指定目录提取所有图片URL
- 生成标准格式的JSON索引文件
- 支持目录递归遍历和URL签名

**使用方法**:
```bash
python scripts/batch_extract_cos_urls.py
```

**输出**: `input/明红/图片URL/[模板目录]/cos-index.json`

**配置**: 需要配置腾讯云COS环境变量(参考`.env.example`)

### 3. batch_random_url_combination.py
**随机URL组合批量生成器**

**功能**:
- 从多个cos-index.json文件中随机抽取图片URL
- 批量生成多组随机组合配置
- 支持自定义组合数量和输出目录

**使用方法**:
```bash
python scripts/batch_random_url_combination.py
```

**输出**: `input/明红/图片URL/随机组合/[模板目录]/random_*.json`

**参数**:
- 组合数量: 默认50组
- 输出目录: 自动创建时间戳目录
- 索引文件: 自动搜索所有模板的cos-index.json

### 4. random_image_combiner.py
**单次随机图片组合生成器**

**功能**:
- 生成单组随机URL组合
- 适合快速测试或单次使用场景

**使用方法**:
```bash
python scripts/random_image_combiner.py
```

**输出**: `input/明红/图片URL/随机组合/模板[X]/random_[timestamp].json`

### 5. check-dependencies.sh
**项目依赖检查脚本**

**功能**:
- 检查Python版本和环境
- 验证必需的Python包
- 检查系统依赖(Playwright浏览器)

**使用方法**:
```bash
bash scripts/check-dependencies.sh
```

## 工作流程

### 完整的图片批量替换流程

```
1. 提取COS URL
   ├─> batch_extract_cos_urls.py
   └─> 生成 cos-index.json

2. 生成随机组合
   ├─> batch_random_url_combination.py
   └─> 生成 random_*.json (50组)

3. 批量替换和截图
   ├─> batch_replace_images.py
   └─> 生成 output/model/*.png (50张)
```

### 配置驱动的执行流程

```yaml
配置文件 (task_config.json):
  - task_name: 任务名称
  - page_config: 页面和替换配置
  - input_files: 输入JSON文件列表
  - output_config: 输出目录和格式
  - execution_config: 执行参数

执行引擎 (batch_replace_images.py):
  - 加载配置 → 验证参数
  - 读取输入JSON → 提取URL
  - 启动浏览器 → 导航到页面
  - 批量替换 → 等待加载
  - 精确截图 → 保存输出
```

## 配置文件

详细配置说明请参考: [configs/README.md](configs/README.md)

核心配置文件:
- `configs/batch_replace/task_config.json` - 主任务配置
- `configs/batch_replace/task_config.schema.json` - JSON Schema验证

## 依赖要求

### Python环境
- Python 3.10+
- asyncio (标准库)
- json, re, pathlib (标准库)

### 第三方包
```bash
pip install playwright jsonschema
playwright install chromium
```

### 云服务(可选)
- 腾讯云COS: 用于URL提取功能
- 环境变量配置参考`.env.example`

## 归档脚本

历史版本和过程性脚本已归档至`archived/`目录:
- `archived/deprecated/` - 已废弃的旧版本脚本
- `archived/process-scripts/` - 临时和一次性使用脚本
- `archived/test-scripts/` - 开发测试脚本

详细归档说明: [archived/README.md](archived/README.md)

## 最佳实践

### 1. 配置管理
- 为不同任务创建专用配置文件
- 使用描述性的task_name和task_id
- 配置文件版本控制(Git)

### 2. 性能优化
- 并发数设置: 根据服务器性能调整`CONCURRENT_TASKS`
- 等待时间: 根据网络状况调整`wait_after_replace`
- 无头模式: 生产环境使用`headless: true`

### 3. 错误处理
- 检查输入JSON文件是否存在
- 验证URL的有效性(签名未过期)
- 监控浏览器控制台输出

### 4. 输出管理
- 定期清理output目录旧文件
- 使用时间戳和任务ID标识输出
- 保留输出文件的任务配置副本

## 故障排查

### 常见问题

**1. 图片替换失败**
```bash
# 检查CSS选择器是否正确
# 检查URL是否有效(COS签名是否过期)
# 检查页面是否正常加载
```

**2. 截图尺寸不对**
```bash
# 检查page.module.css中的容器尺寸
# 验证auto_dimensions配置
# 查看container_box日志输出
```

**3. 浏览器启动失败**
```bash
# 重新安装Playwright浏览器
playwright install chromium

# 检查系统依赖
bash scripts/check-dependencies.sh
```

## 开发指南

### 创建新脚本
1. 遵循现有脚本的命名规范
2. 添加完整的docstring和类型提示
3. 支持命令行参数
4. 提供使用示例

### 代码规范
- 遵循PEP8
- 使用类型提示
- UTF-8编码
- 详细的错误处理

## 与快捷键系统的关系

### 核心集成架构

scripts目录是ZTL项目**快捷键系统**的底层执行引擎，与`.claude/commands/`和`.claude/agents/`形成完整的三层协作架构:

```
┌─────────────────────────────────────────────────────────────┐
│  用户交互层 (.claude/commands/ & .claude/agents/)           │
│  - 自然语言理解                                              │
│  - 智能参数推断                                              │
│  - 任务编排和调度                                            │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  配置管理层 (scripts/configs/)                               │
│  - JSON配置文件                                              │
│  - Schema验证                                                │
│  - 任务参数存储                                              │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  执行引擎层 (scripts/*.py)                                   │
│  - 核心业务逻辑                                              │
│  - 浏览器自动化                                              │
│  - 云服务集成                                                │
└─────────────────────────────────────────────────────────────┘
```

### 关联的快捷键和智能体

#### 1. `/3` 命令 - Next.js页面图片批量替换

**文档位置**: `.claude/commands/3.md`

**调用关系**:
```yaml
/3 命令:
  功能: 智能理解用户意图,生成配置,执行批量替换

  执行流程:
    第1步 - 智能理解层:
      - 解析用户自然语言输入
      - 推断页面路径、JSON文件、替换参数

    第2步 - 配置生成:
      - 生成 scripts/configs/batch_replace/task_config.json
      - 验证配置完整性和合法性

    第3步 - 脚本调用:
      - 执行 python scripts/batch_replace_images.py
      - 批量替换图片并截图
      - 输出到 output/model/

  核心脚本: batch_replace_images.py
  配置文件: configs/batch_replace/task_config.json
```

**使用示例**:
```bash
# 用户输入自然语言
/3 模板页面：three-day-tour，处理 random_01 到 random_50

# AI执行流程
1. 解析意图 → 页面=three-day-tour, 范围=01~50
2. 生成配置 → task_config.json (50个input_files)
3. 调用脚本 → python scripts/batch_replace_images.py
4. 批量执行 → 生成50张截图到output/model/
```

#### 2. `/R3` 智能体 - Figma批量替换专家

**文档位置**: `.claude/agents/R3.md`

**调用关系**:
```yaml
/R3 智能体:
  定位: Figma批量替换专家
  核心能力: 大规模内容批量替换和自动化更新

  与scripts的关系:
    - 提供高层次的智能化包装
    - 理解业务场景和替换逻辑
    - 生成适合batch_replace_images.py的配置
    - 监控执行过程和结果验证

  典型场景:
    场景1 - 餐饮菜品图片批量更新:
      1. R3分析菜单模板结构
      2. R3准备替换映射关系
      3. R3生成task_config.json
      4. R3调用batch_replace_images.py执行
      5. R3验证替换效果

    场景2 - 品牌素材批量替换:
      1. R3识别品牌元素节点
      2. R3准备素材和映射
      3. R3配置精确节点映射
      4. R3执行批量替换
      5. R3导出更新后的设计
```

### 配置驱动的设计哲学

**为什么采用"快捷键 + 配置 + 脚本"三层架构？**

1. **关注点分离**
   - 快捷键层: 专注用户交互和意图理解
   - 配置层: 专注参数管理和任务追溯
   - 脚本层: 专注业务逻辑和技术实现

2. **可复用性**
   - 同一个脚本可以通过不同配置处理不同任务
   - 配置文件可以保存、复用、版本控制
   - 脚本独立于交互方式,可被其他工具调用

3. **可维护性**
   - 单一职责原则,每层逻辑清晰
   - 独立测试,质量保证
   - 易于扩展和优化

4. **智能化**
   - AI在快捷键层理解自然语言
   - AI在配置层生成标准化参数
   - 脚本在执行层保证稳定性和效率

### 开发新功能的标准流程

当需要添加新的批量处理功能时,遵循以下步骤:

```yaml
步骤1 - 创建核心脚本:
  位置: scripts/new_feature.py
  职责: 实现核心业务逻辑
  要求: 支持配置文件驱动

步骤2 - 定义配置Schema:
  位置: scripts/configs/new_feature/config.schema.json
  职责: 定义配置文件结构和验证规则

步骤3 - 创建快捷键命令:
  位置: .claude/commands/[X].md
  职责: 智能理解用户意图,生成配置,调用脚本

步骤4 - (可选)创建专家智能体:
  位置: .claude/agents/[RX].md
  职责: 提供场景化的高层次封装
```

## 相关文档

### 核心文档

- [项目开发规范](../.claude/CLAUDE.md) - 完整的开发规范和快捷键系统说明
- [快捷键系统总览](../.claude/CLAUDE.md#项目专属能力接口) - 所有快捷键和智能体的索引
- [开发物料管理规范](../.claude/CLAUDE.md#开发物料管理规范) - scripts目录的组织规范

### 快捷键和智能体

- `/3 命令文档` - Next.js页面图片批量替换指令
- `/R3 智能体文档` - Figma批量替换专家
- `/R4 智能体文档` - Figma工作流编排专家

### 技术文档

- [API文档](../api/README.md) - FastAPI服务接口说明
- [配置文件文档](configs/README.md) - 详细的配置文件说明

---

**维护者**: ZTL项目团队
**最后更新**: 2025-10-06
**版本**: v1.2.0 (新增配置驱动设计理念说明,强调脚本复用模式)
