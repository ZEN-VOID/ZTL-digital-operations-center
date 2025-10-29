# 筹建组agents重构方案：从CAD/BIM理想化转向AIGC工具体系

> **文档版本**: v1.0.0
> **创建时间**: 2025-10-28
> **状态**: 设计方案
> **目的**: 将筹建组agents从不切实际的CAD/BIM工具属性，转向实际可行的AIGC创作工具体系

---

## 📋 目录

- [1. 问题诊断](#1-问题诊断)
- [2. 重构目标](#2-重构目标)
- [3. 整体架构设计](#3-整体架构设计)
- [4. 详细重构方案](#4-详细重构方案)
  - [4.1 Z1-平面图设计师](#41-z1-平面图设计师)
  - [4.2 Z2-空间设计师](#42-z2-空间设计师)
  - [4.3 Z3-BIM建模师](#43-z3-bim建模师)
  - [4.4 Z4-建筑动画师](#44-z4-建筑动画师)
- [5. Skills改造方案](#5-skills改造方案)
- [6. 实施计划](#6-实施计划)
- [7. 验证测试](#7-验证测试)
- [8. 风险与对策](#8-风险与对策)

---

## 1. 问题诊断

### 1.1 现状分析

**当前筹建组agents定位**:

| Agent | 当前定位 | 核心问题 |
|-------|---------|---------|
| Z1-平面图设计师 | CAD技术专家 (AutoCAD) | ❌ Claude Code无法操作CAD软件 |
| Z2-空间设计师 | 室内设计专家 (手工设计方案) | ❌ 输出形式过于传统，缺少AIGC能力 |
| Z3-BIM建模师 | BIM专家 (Revit/Navisworks) | ❌ Claude Code无法操作BIM软件 |
| Z4-建筑动画师 | 建筑动画专家 (Lumion/3ds Max) | ❌ Claude Code无法操作3D渲染软件 |

**核心矛盾**:
- Agents定义的能力与Claude Code的实际执行能力不匹配
- 理想化的工具属性（CAD/BIM/Lumion）无法在当前技术栈中实现
- 缺少可执行的Skills支持，导致agents变成"空壳"

### 1.2 技术能力边界

**Claude Code实际可行能力**:
- ✅ 生成结构化文档（Markdown/JSON）
- ✅ 调用外部API（AIGC图像生成、视频生成）
- ✅ 编写和执行Python脚本
- ✅ 生成HTML/CSS/JavaScript代码
- ❌ 操作本地GUI软件（CAD/BIM/3D渲染）
- ❌ 直接生成DWG/RVT等专业格式文件

**已有资源**:
- ✅ Nano-banana (图像生成API)
- ✅ Wan (通义万相图像生成)
- ✅ canvas-design (PNG/PDF视觉艺术设计)
- ✅ algorithmic-art (p5.js算法艺术)
- ✅ .env配置文件（KLING_JWT_TOKEN, MINIMAX_API_KEY, ALIYUN_API_KEY等）

---

## 2. 重构目标

### 2.1 核心原则

**从工具操作者 → 提示词工程师 + 执行引擎调度者**

**三层架构强化**:
```
Layer 1: 规范层 (Agent.md)
  ↓ 领域专业知识 + AIGC提示词工程规范
Layer 2: 计划层 (配置.md / JSON)
  ↓ 结构化提示词 + API参数配置
Layer 3: 执行层 (Skills)
  ↓ AIGC API调用 + 图像/视频生成
```

### 2.2 重构后的agents定位

| Agent | 新定位 | 核心能力 |
|-------|--------|---------|
| Z1-平面图计划师 | 平面图创意规划专家 | 生成"平面图配置.md" → 调用canvas-design创作平面图 |
| Z2-空间设计AIGC助手 | AIGC空间设计专家 | 构建高质量建筑提示词 → 调用Nano-banana生成空间设计图 |
| Z3-3D可视化师 | 3D模拟可视化专家 | 生成"3D建模和细节表现.md" → 调用algorithmic-art/three.js模拟建模 |
| Z4-建筑动画AIGC助手 | AIGC建筑动画专家 | 构建高质量建筑动画提示词 → 调用Wan生成建筑动画视频 |

### 2.3 成功指标

**必达指标**:
- ✅ 每个agent能够生成结构化的配置文档/提示词
- ✅ 每个agent能够成功调用对应的Skills执行引擎
- ✅ 生成的图像/视频符合基本的建筑/室内设计标准
- ✅ 完整的输出路径规范 (`output/[项目名]/[agent-name]/`)

**卓越指标**:
- ✅ AIGC生成的图像质量达到专业设计水准
- ✅ 提示词工程规范形成可复用的模板
- ✅ Skills执行引擎稳定可靠（成功率≥90%）
- ✅ 建立筹建组专用的提示词知识库

---

## 3. 整体架构设计

### 3.1 筹建组AIGC工作流

```
┌─────────────────────────────────────────────────────────────┐
│                    Z0-筹建项目需求分析师                      │
│                  (输入需求分析和任务分配)                      │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┬─────────────────┐
        ↓                ↓                ↓                 ↓
┌───────────────┐ ┌────────────────┐ ┌──────────────┐ ┌──────────────────┐
│ Z1-平面图计划师│ │Z2-空间设计助手  │ │Z3-3D可视化师 │ │Z4-建筑动画助手    │
│               │ │                │ │              │ │                  │
│ 生成平面图配置 │ │ 构建空间设计   │ │ 生成3D建模   │ │ 构建建筑动画      │
│   .md提示词   │ │   提示词       │ │   配置.md    │ │   提示词          │
└───────┬───────┘ └────────┬───────┘ └──────┬───────┘ └─────────┬────────┘
        │                  │                │                   │
        ↓                  ↓                ↓                   ↓
┌───────────────┐ ┌────────────────┐ ┌──────────────┐ ┌──────────────────┐
│canvas-design  │ │ Nano-banana    │ │algorithmic   │ │ Wan              │
│ 平面图生成    │ │ 空间设计图生成 │ │ -art/three   │ │ 建筑动画生成      │
│  (PNG/PDF)    │ │   (PNG)        │ │  (HTML/JS)   │ │  (MP4)           │
└───────┬───────┘ └────────┬───────┘ └──────┬───────┘ └─────────┬────────┘
        │                  │                │                   │
        └──────────────────┴────────────────┴───────────────────┘
                                    ↓
                    output/[项目名]/[agent-name]/
                      plans/ | results/ | logs/ | metadata/
```

### 3.2 输出路径规范

**统一路径结构**:
```
output/
├── [项目名]/                  # 动态项目名称（如"火锅店开业筹备"）
│   ├── Z1-平面图计划师/
│   │   ├── plans/            # 平面图配置.md提示词
│   │   ├── results/          # canvas-design生成的PNG/PDF平面图
│   │   ├── logs/             # 执行日志
│   │   └── metadata/         # 元数据（生成时间、参数等）
│   ├── Z2-空间设计AIGC助手/
│   │   ├── plans/            # 空间设计提示词JSON
│   │   ├── results/          # Nano-banana生成的空间设计图
│   │   ├── logs/
│   │   └── metadata/
│   ├── Z3-3D可视化师/
│   │   ├── plans/            # 3D建模配置.md
│   │   ├── results/          # algorithmic-art生成的HTML/JS模拟
│   │   ├── logs/
│   │   └── metadata/
│   └── Z4-建筑动画AIGC助手/
│       ├── plans/            # 建筑动画提示词JSON
│       ├── results/          # Wan生成的建筑动画MP4
│       ├── logs/
│       └── metadata/
```

---

## 4. 详细重构方案

### 4.1 Z1-平面图设计师

#### 4.1.1 重构定位

**从**: CAD技术专家（AutoCAD绘图）
**到**: 平面图创意规划专家 + canvas-design提示词工程师

#### 4.1.2 核心职责

**规范层（Agent.md）**:
- 建筑平面图设计规范和最佳实践
- 餐饮空间平面布局专业知识（功能分区、动线设计、家具布置标准）
- canvas-design提示词工程规范（如何用自然语言描述平面图需求）

**计划层（平面图配置.md）**:
生成结构化的平面图描述文档，包含：
- 空间尺寸和比例
- 功能分区描述（前厅、就餐区、包间、厨房、卫生间等）
- 动线设计要求（顾客动线、服务动线、后勤动线）
- 家具布置规范（桌椅尺寸、间距、数量）
- 视觉风格要求（线条风格、配色方案）

**执行层（Skills）**:
调用改造后的canvas-design技能包生成PNG/PDF平面图

#### 4.1.3 输出示例

**平面图配置.md**:
```markdown
# 火锅店平面图设计配置

## 基础信息
- **项目名称**: 火锅店开业筹备
- **空间尺寸**: 300㎡ (长20m × 宽15m)
- **层高**: 3.6m
- **风格**: 现代简约 + 工业风

## 功能分区布局

### 入口区域 (10㎡)
- 位置: 建筑左侧主入口
- 元素: 接待台、等候区、品牌展示
- 设计要点: 开阔视野、品牌形象强化

### 开放就餐区 (150㎡)
- 位置: 中央主区域
- 座位数: 60人（2人桌×10，4人桌×10）
- 桌椅规格: 2人桌 600×700mm，4人桌 800×800mm
- 间距要求: 主通道≥1400mm，桌间≥600mm

### 包间区域 (60㎡)
- 位置: 右侧靠窗区域
- 包间数: 3间（6人×2，8人×1）
- 隔断: 玻璃+窗帘，保持通透性

### 厨房区域 (60㎡)
- 位置: 后方独立区域
- 动线: 独立出入口、与就餐区明确分离
- 功能: 备菜区、烹饪区、洗碗区、仓储区

### 卫生间 (20㎡)
- 位置: 就餐区右后方
- 配置: 男女分离、无障碍设施

## 动线设计

### 顾客动线
入口 → 等候区 → 就餐区 → 卫生间 → 收银 → 出口

### 服务动线
厨房 → 传菜通道 → 就餐区 → 回收通道 → 洗碗区

### 后勤动线
后门 → 仓储区 → 厨房（避免与顾客动线交叉）

## 视觉风格要求

### 线条风格
- 墙体: 粗实线 (3px黑色)
- 门窗: 中等线 (1.5px黑色)
- 家具: 细线 (0.8px灰色)
- 尺寸标注: 细线 (0.5px蓝色)

### 配色方案
- 背景: 浅灰 (#F5F5F5)
- 墙体: 深灰 (#333333)
- 功能区: 不同色块区分（就餐区浅蓝、厨房浅绿、卫生间浅黄）

### 图例要求
- 比例尺: 1:100
- 指北针: 右上角
- 图例: 左下角（包含所有符号说明）

## canvas-design调用参数

**创作风格**: architectural_floor_plan
**输出格式**: PNG (4K分辨率) + PDF (矢量格式)
**画布尺寸**: 1920×1440 (适合A3打印)
```

#### 4.1.4 Agent改造清单

**文件**: `plugins/筹建组/agents/Z1-平面图计划师.md`

**改造内容**:
1. 更新YAML frontmatter
   ```yaml
   ---
   name: Z1-平面图计划师
   description: 专注于餐饮空间平面图创意规划,根据功能需求生成结构化的平面图配置文档,调用canvas-design技能包生成专业平面图。适用于新店筹建、空间改造的平面布局规划。
   model: sonnet
   color: blue
   tools: [Read, Write, Edit, Bash, Skill]
   ---
   ```

2. 重写核心身份定位
   - 移除CAD技术专家相关内容
   - 强化平面图规划和提示词工程能力
   - 新增canvas-design调用规范

3. 更新工作流程
   ```
   Step 1: 需求分析（接收Z0的项目需求）
   Step 2: 平面图规划（功能分区、动线设计、家具布置）
   Step 3: 生成配置文档（output/[项目名]/Z1-平面图计划师/plans/平面图配置.md）
   Step 4: 调用canvas-design（传递配置文档作为提示词）
   Step 5: 质量验证（检查生成的平面图是否符合规范）
   Step 6: 交付成果（保存到results/目录，通知Z2和ZZ）
   ```

4. 新增canvas-design调用规范章节
   - 如何将平面图配置.md转化为canvas-design可理解的自然语言提示词
   - 常见平面图类型的提示词模板（开放式布局、包间为主布局、混合布局）
   - 质量标准（尺寸准确性、动线合理性、视觉清晰度）

---

### 4.2 Z2-空间设计师

#### 4.2.1 重构定位

**从**: 传统室内设计专家（手工设计方案）
**到**: AIGC空间设计专家 + Nano-banana提示词工程师

#### 4.2.2 核心职责

**规范层（Agent.md）**:
- 建筑/室内/空间设计行业标准和规范
- 高质量建筑设计的视觉要素（构图、光影、材质、色彩）
- Nano-banana AIGC提示词工程最佳实践
- 多种需求类型的处理策略（严格按规划、图生图、局部修改等）

**计划层（空间设计提示词JSON）**:
生成标准化的Nano-banana API配置文件，包含：
- 核心提示词（主体描述、风格、氛围）
- 保持不变元素（keep_consistent）
- 需要改变元素（change_elements）
- 参考图路径（如基于平面图配置.md生成）
- API参数（strength、resolution、model等）

**执行层（Skills）**:
调用改造后的Nano-banana技能包生成空间设计图

#### 4.2.3 多场景支持

**场景1: 严格按照平面配置.md的规划基础生成**
```json
{
  "task_type": "text_to_image",
  "reference_base": "output/火锅店开业筹备/Z1-平面图计划师/plans/平面图配置.md",
  "prompt": "根据平面图配置,生成300㎡现代简约工业风火锅店室内空间概念图。开放就餐区60人座位,包间区3间,整体色调灰色+木色,工业吊灯,裸露红砖墙,水泥地面,绿植点缀。广角视角,温暖自然光,下午2点光线。",
  "style": "architectural_interior",
  "resolution": "1024x1024"
}
```

**场景2: 多视角创作中基于图生图保持一致性**
```json
{
  "task_type": "image_to_image",
  "reference_image": "output/火锅店开业筹备/Z2-空间设计AIGC助手/results/view-01-entrance.png",
  "keep_consistent": [
    "工业风格",
    "灰色墙面",
    "木质家具",
    "吊灯设计",
    "整体色调"
  ],
  "change_elements": [
    "视角: 从入口视角变为就餐区俯视视角",
    "焦点: 从接待台变为餐桌布局"
  ],
  "strength": 0.65
}
```

**场景3: 局部修改中基于图生图**
```json
{
  "task_type": "image_to_image",
  "reference_image": "output/火锅店开业筹备/Z2-空间设计AIGC助手/results/view-02-dining.png",
  "keep_consistent": [
    "整体空间布局",
    "墙面装饰",
    "地面材质",
    "家具位置"
  ],
  "change_elements": [
    "吊灯: 将工业吊灯更换为更柔和的球形吊灯",
    "墙面: 增加一面绿植墙"
  ],
  "strength": 0.50
}
```

**场景4: 用户单独指定使用skills时的智能分析**
- Agent需要智能分析用户意图（是全新创作还是基于已有图修改）
- 自动检测是否有参考图（平面图、已生成的空间图）
- 根据用户描述的详细程度选择合适的strength值
- 提供多个方案供用户选择

#### 4.2.4 Agent改造清单

**文件**: `plugins/筹建组/agents/Z2-空间设计AIGC助手.md`

**改造内容**:
1. 更新YAML frontmatter
   ```yaml
   ---
   name: Z2-空间设计AIGC助手
   description: AIGC空间设计专家,根据高质量建筑/室内/空间设计标准构建专业提示词,调用Nano-banana生成概念图、场景渲染图等。支持多种模式：严格按规划生成、图生图保持一致性、局部修改、多视角创作。
   model: sonnet
   color: blue
   tools: [Read, Write, Edit, Bash, Skill, Grep, Glob]
   ---
   ```

2. 重写核心身份定位
   - 从传统设计师 → AIGC提示词工程师
   - 强化高质量建筑设计规范知识
   - 新增Nano-banana API调用专业能力

3. 新增四大场景处理章节
   - 场景1: 严格按规划生成（文生图模式）
   - 场景2: 多视角一致性（图生图模式，高一致性）
   - 场景3: 局部修改（图生图模式，低strength）
   - 场景4: 智能分析用户意图（决策树）

4. 新增Nano-banana提示词工程规范
   - 核心提示词构建原则（主体、风格、氛围、细节）
   - keep_consistent和change_elements的选择策略
   - strength参数的选择标准（0.4-0.5轻微/0.6-0.7中等/0.75-0.8较大）
   - 常见空间类型的提示词模板

5. 更新工作流程
   ```
   Step 1: 需求分析（接收Z0或Z1的规划文档）
   Step 2: 场景类型判断（4种场景分类）
   Step 3: 构建提示词JSON（根据场景类型生成配置）
   Step 4: 调用Nano-banana（执行API调用）
   Step 5: 质量验证（检查一致性、美观度、专业性）
   Step 6: 迭代优化（如不满意，调整strength或提示词）
   Step 7: 交付成果（保存到results/，通知Z3和ZZ）
   ```

---

### 4.3 Z3-BIM建模师

#### 4.3.1 重构定位

**从**: BIM专家（Revit/Navisworks建模）
**到**: 3D可视化模拟专家 + algorithmic-art/three.js提示词工程师

#### 4.3.2 核心职责

**规范层（Agent.md）**:
- 3D建模的基础原理和视觉表现标准
- algorithmic-art (p5.js)和three.js的能力边界
- 如何用算法艺术模拟建筑3D效果（等轴测图、线框图、体块分析）
- 3D可视化的输出规范（HTML交互演示）

**计划层（3D建模和细节表现.md）**:
生成结构化的3D可视化需求文档，包含：
- 3D表现形式（等轴测图/透视图/线框图/体块分析）
- 空间结构描述（基于Z1的平面图和Z2的空间设计）
- 视觉风格要求（线条、色彩、材质模拟）
- 交互需求（旋转、缩放、视角切换）

**执行层（Skills）**:
调用改造后的algorithmic-art (p5.js)或新建three.js技能包生成3D可视化

#### 4.3.3 3D表现形式

**等轴测图（Isometric View）**:
- 用途: 展示整体空间布局和功能分区
- 技术: p5.js 2D绘图模拟3D投影
- 优势: 简洁清晰，适合快速理解空间关系

**线框图（Wireframe）**:
- 用途: 展示空间结构和尺寸关系
- 技术: p5.js或three.js线条绘制
- 优势: 强调结构，技术感强

**体块分析图（Massing Diagram）**:
- 用途: 展示空间体量和层次关系
- 技术: three.js 3D几何体渲染
- 优势: 立体感强，适合理解空间体量

**交互3D模型**:
- 用途: 允许用户自由旋转、缩放、切换视角
- 技术: three.js + OrbitControls
- 优势: 沉浸式体验，全方位理解空间

#### 4.3.4 输出示例

**3D建模和细节表现.md**:
```markdown
# 火锅店3D可视化模拟配置

## 基础信息
- **项目名称**: 火锅店开业筹备
- **参考文档**:
  - 平面图配置: output/火锅店开业筹备/Z1-平面图计划师/plans/平面图配置.md
  - 空间设计图: output/火锅店开业筹备/Z2-空间设计AIGC助手/results/view-01-entrance.png

## 3D表现形式

### 主要输出: 等轴测图 (Isometric View)
- 视角: 45度俯视
- 展示内容: 整体空间布局、功能分区、家具布置
- 层级: 3层楼板（地面、吊顶、设备层）

### 辅助输出: 体块分析图 (Massing Diagram)
- 视角: 透视图
- 展示内容: 各功能区体块、空间高度关系
- 交互: 支持旋转、缩放

## 空间结构描述

### 地面层
- 入口区域: 矩形体块 10㎡
- 开放就餐区: 大矩形体块 150㎡
- 包间区域: 3个独立小体块 60㎡
- 厨房区域: 后方矩形体块 60㎡
- 卫生间: 右后方矩形体块 20㎡

### 吊顶层
- 高度: 3.6m
- 工业风吊灯分布: 开放区6盏，包间区各2盏
- 管道布局: 暴露式管道沿墙走向

### 设备层（可选）
- HVAC系统: 天花板上方设备层
- 消防系统: 喷淋头分布

## 视觉风格要求

### 线条风格
- 墙体: 粗线条 (4px, 深灰 #333)
- 家具: 中等线条 (2px, 灰 #666)
- 细节: 细线条 (1px, 浅灰 #999)

### 色彩方案
- 墙面: 浅灰 (#CCCCCC)
- 地面: 水泥灰 (#999999)
- 家具: 木色 (#8B6F47)
- 点缀: 绿植 (#4CAF50)

### 材质模拟
- 墙面: 平面填充
- 地面: 网格纹理模拟水泥
- 家具: 木纹理模拟（简化版）

## 交互需求

### 基础交互（p5.js）
- 鼠标滚轮: 缩放
- 拖拽: 平移视角

### 高级交互（three.js）
- 鼠标拖拽: 旋转模型
- 滚轮: 缩放
- 按钮: 切换视角（正面/侧面/俯视）
- 图层控制: 显示/隐藏地面层、吊顶层、设备层

## algorithmic-art/three.js调用参数

### p5.js模式（快速生成）
- 输出格式: HTML + JavaScript
- 画布尺寸: 1200×900
- 渲染方式: 静态等轴测图

### three.js模式（高级交互）
- 输出格式: HTML + JavaScript (three.js库)
- 画布尺寸: 全屏自适应
- 渲染方式: WebGL 3D渲染 + OrbitControls
- 性能优化: LOD (Level of Detail)
```

#### 4.3.5 Agent改造清单

**文件**: `plugins/筹建组/agents/Z3-3D可视化师.md`

**改造内容**:
1. 更新文件名和YAML frontmatter
   ```yaml
   ---
   name: Z3-3D可视化师
   description: 3D可视化模拟专家,基于平面图和空间设计图生成3D可视化表现（等轴测图、线框图、体块分析、交互3D模型）。使用algorithmic-art(p5.js)或three.js技术栈,输出HTML交互演示。
   model: sonnet
   color: blue
   tools: [Read, Write, Edit, Bash, Skill, Grep, Glob]
   ---
   ```

2. 重写核心身份定位
   - 从BIM建模专家 → 3D可视化模拟专家
   - 移除Revit/Navisworks相关内容
   - 新增p5.js和three.js能力说明

3. 新增四种3D表现形式章节
   - 等轴测图（适合快速理解）
   - 线框图（适合结构展示）
   - 体块分析图（适合体量展示）
   - 交互3D模型（适合沉浸式体验）

4. 新增algorithmic-art和three.js调用规范
   - p5.js: 快速生成静态等轴测图和线框图
   - three.js: 高级交互3D模型
   - 两种技术的选择策略（根据需求复杂度）

5. 更新工作流程
   ```
   Step 1: 需求分析（接收Z1的平面图和Z2的空间设计图）
   Step 2: 3D表现形式选择（等轴测图/线框图/体块分析/交互3D）
   Step 3: 生成配置文档（output/[项目名]/Z3-3D可视化师/plans/3D建模和细节表现.md）
   Step 4: 选择技术栈（p5.js快速模式 或 three.js高级模式）
   Step 5: 调用Skills（执行代码生成和渲染）
   Step 6: 质量验证（检查准确性、视觉效果、交互流畅度）
   Step 7: 交付成果（保存HTML到results/，通知Z4和ZZ）
   ```

---

### 4.4 Z4-建筑动画师

#### 4.4.1 重构定位

**从**: 建筑动画专家（Lumion/3ds Max渲染）
**到**: AIGC建筑动画专家 + Wan提示词工程师

#### 4.4.2 核心职责

**规范层（Agent.md）**:
- 建筑动画的行业标准（镜头运动、节奏、叙事）
- 空间动画、动线展示动画、场景分析动画的设计原则
- Wan (通义万相) AIGC视频生成能力和限制
- 高质量建筑动画的提示词工程规范

**计划层（建筑动画提示词JSON）**:
生成标准化的Wan API配置文件，包含：
- 核心提示词（镜头描述、空间特征、运动路径）
- 参考图（基于Z2的空间设计图或Z3的3D可视化）
- 生成模式（文生视频 或 图生视频）
- API参数（duration、resolution、camera_movement等）

**执行层（Skills）**:
调用改造后的Wan技能包生成建筑动画视频

#### 4.4.3 多场景支持

**场景1: 严格按照已有规划文档生成（图生视频）**
```json
{
  "task_type": "image_to_video",
  "reference_image": "output/火锅店开业筹备/Z2-空间设计AIGC助手/results/view-01-entrance.png",
  "prompt": "摄像机从入口缓慢推进,展示接待台、等候区、品牌logo墙。温暖灯光,人物自然走动,平滑运镜。",
  "camera_movement": "push_in",
  "duration": 5,
  "resolution": "1920x1080"
}
```

**场景2: 多视角创作中基于图生视频保持一致性**
```json
{
  "task_type": "image_to_video",
  "reference_image": "output/火锅店开业筹备/Z2-空间设计AIGC助手/results/view-02-dining.png",
  "prompt": "摄像机从就餐区左侧开始,向右侧平移,展示整个开放就餐区。保持工业风格、灰色墙面、木质家具一致。顾客用餐场景,烟雾缭绕,氛围温馨。",
  "camera_movement": "pan_right",
  "keep_consistent": [
    "工业风格",
    "整体色调",
    "家具风格",
    "灯光氛围"
  ],
  "duration": 8,
  "resolution": "1920x1080"
}
```

**场景3: 用户单独指定使用skills时的智能分析**
- Agent需要智能分析用户意图（展示什么空间、什么镜头运动）
- 自动检测是否有参考图（空间设计图、3D可视化HTML）
- 根据用户描述选择合适的camera_movement（push_in/pull_out/pan/orbit/dolly）
- 提供多个镜头方案供用户选择

#### 4.4.4 镜头运动类型

**基础镜头运动**:
- `push_in`: 推进镜头（从远到近，吸引观众进入空间）
- `pull_out`: 拉出镜头（从近到远，展示整体布局）
- `pan_left/pan_right`: 左右平移（展示横向空间关系）
- `tilt_up/tilt_down`: 上下倾斜（展示垂直空间关系）

**高级镜头运动**:
- `orbit`: 环绕镜头（围绕中心点旋转，展示360度视角）
- `dolly`: 轨道推拉（沿直线移动，展示空间深度）
- `crane`: 升降镜头（垂直升降，展示空间层次）

#### 4.4.5 Agent改造清单

**文件**: `plugins/筹建组/agents/Z4-建筑动画AIGC助手.md`

**改造内容**:
1. 更新文件名和YAML frontmatter
   ```yaml
   ---
   name: Z4-建筑动画AIGC助手
   description: AIGC建筑动画专家,根据高质量建筑/室内动画设计标准构建专业提示词,调用Wan(通义万相)生成空间动画、动线展示动画、场景分析动画。支持图生视频、多视角一致性、智能镜头运动。
   model: sonnet
   color: blue
   tools: [Read, Write, Edit, Bash, Skill, Grep, Glob]
   ---
   ```

2. 重写核心身份定位
   - 从传统建筑动画师 → AIGC视频提示词工程师
   - 移除Lumion/3ds Max相关内容
   - 新增Wan API调用专业能力

3. 新增三大场景处理章节
   - 场景1: 严格按规划生成（图生视频模式）
   - 场景2: 多视角一致性（图生视频，保持风格）
   - 场景3: 智能分析用户意图（镜头运动选择）

4. 新增镜头运动设计章节
   - 7种镜头运动类型说明
   - 镜头运动与空间叙事的匹配原则
   - 常见空间类型的镜头运动模板

5. 新增Wan提示词工程规范
   - 核心提示词构建原则（空间描述、镜头运动、氛围营造）
   - camera_movement参数选择标准
   - duration和resolution的建议值

6. 更新工作流程
   ```
   Step 1: 需求分析（接收Z2的空间设计图或Z3的3D可视化）
   Step 2: 场景类型判断（图生视频 或 智能分析模式）
   Step 3: 镜头运动设计（选择合适的camera_movement）
   Step 4: 构建提示词JSON（生成Wan API配置）
   Step 5: 调用Wan（执行视频生成）
   Step 6: 质量验证（检查镜头流畅度、一致性、专业性）
   Step 7: 迭代优化（如不满意，调整镜头或提示词）
   Step 8: 交付成果（保存MP4到results/，通知ZZ）
   ```

---

## 5. Skills改造方案

### 5.1 canvas-design改造（平面图生成）

#### 5.1.1 克隆位置

```bash
# 从全局example-skills插件克隆到筹建组
plugins/筹建组/skills/canvas-design-floor-plan/
```

#### 5.1.2 改造内容

**SKILL.md改造**:
```yaml
---
name: canvas-design-floor-plan
description: 专为筹建组Z1-平面图计划师定制的平面图生成技能包。基于自然语言描述生成建筑平面图PNG/PDF,支持功能分区、动线设计、家具布置的可视化表达。
---
```

**核心改造点**:
1. 新增"建筑平面图"设计模板
   - 预设线条粗细（墙体3px、门窗1.5px、家具0.8px）
   - 预设配色方案（建筑制图标准色）
   - 预设图例和比例尺模板

2. 新增平面图专用prompt处理逻辑
   - 解析"平面图配置.md"中的结构化描述
   - 提取空间尺寸、功能分区、家具布置信息
   - 转化为canvas-design可理解的绘图指令

3. 输出优化
   - PNG: 4K分辨率，适合屏幕展示
   - PDF: 矢量格式，适合A3打印
   - 自动添加比例尺、指北针、图例

**scripts/改造**:
新增 `floor_plan_generator.py`:
```python
def generate_floor_plan(config_md_path: str, output_dir: str):
    """
    从平面图配置.md生成平面图PNG/PDF

    Args:
        config_md_path: 平面图配置.md文件路径
        output_dir: 输出目录

    Returns:
        生成的PNG和PDF文件路径
    """
    # 1. 解析配置文档
    config = parse_floor_plan_config(config_md_path)

    # 2. 生成canvas-design提示词
    prompt = build_canvas_design_prompt(config)

    # 3. 调用canvas-design核心引擎
    result = canvas_design_engine.generate(
        prompt=prompt,
        style="architectural_floor_plan",
        output_formats=["png", "pdf"],
        resolution="4K"
    )

    # 4. 保存文件
    save_outputs(result, output_dir)

    return result
```

#### 5.1.3 测试验证

**测试用例1: 基础平面图**
- 输入: 简单的300㎡火锅店配置.md
- 预期输出: 清晰的功能分区、家具布置、尺寸标注

**测试用例2: 复杂平面图**
- 输入: 包含多个包间、复杂动线的配置.md
- 预期输出: 准确的空间关系、动线箭头、完整图例

---

### 5.2 Nano-banana改造（空间设计图生成）

#### 5.2.1 当前位置

```bash
plugins/筹建组/skills/Nano-banana/
```

#### 5.2.2 改造内容

**SKILL.md改造**:
```yaml
---
name: Nano-banana-space-design
description: 专为筹建组Z2-空间设计AIGC助手定制的空间设计图生成技能包。基于高质量建筑/室内设计提示词生成概念图、场景渲染图,支持多种模式：文生图、图生图保持一致性、局部修改。
---
```

**核心改造点**:
1. 新增"建筑/室内设计"专用提示词模板
   - 空间类型模板（餐饮/办公/零售/住宅）
   - 风格模板（现代简约/工业风/新中式/日式侘寂/北欧风/复古怀旧）
   - 视角模板（入口视角/就餐区俯视/包间内视/细节特写）

2. 强化keep_consistent和change_elements逻辑
   - 预设常见保持元素（风格、色调、材质、家具）
   - 预设常见变化元素（视角、焦点、局部装饰、光影）
   - 智能推荐strength值（根据变化程度）

3. 新增多场景支持
   - `generate_from_plan()`: 严格按规划生成（文生图模式）
   - `generate_multi_view()`: 多视角一致性（图生图模式）
   - `modify_local()`: 局部修改（图生图低strength模式）
   - `analyze_user_intent()`: 智能分析用户意图

**scripts/改造**:
更新 `api_client.py`:
```python
class NanoBananaSpaceDesign:
    """筹建组专用Nano-banana空间设计API客户端"""

    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1"

    def generate_from_plan(self, plan_md_path: str, output_dir: str):
        """场景1: 严格按规划生成（文生图）"""
        # 1. 解析规划文档
        plan = self.parse_plan_document(plan_md_path)

        # 2. 构建建筑设计提示词
        prompt = self.build_architectural_prompt(plan)

        # 3. 调用API
        result = self.call_text_to_image_api(prompt)

        # 4. 保存结果
        self.save_result(result, output_dir)

    def generate_multi_view(self, reference_image: str, new_view: str, output_dir: str):
        """场景2: 多视角一致性（图生图高一致性）"""
        # 自动提取参考图的风格特征
        keep_elements = self.extract_style_features(reference_image)

        # 构建新视角变化描述
        change_elements = [f"视角: 变为{new_view}"]

        # 调用图生图API（高strength保持一致性）
        result = self.call_image_to_image_api(
            reference_image=reference_image,
            keep_consistent=keep_elements,
            change_elements=change_elements,
            strength=0.65
        )

        self.save_result(result, output_dir)

    def modify_local(self, reference_image: str, modification: str, output_dir: str):
        """场景3: 局部修改（图生图低strength）"""
        # 保持所有主要元素
        keep_elements = ["整体布局", "主要家具", "墙面装饰", "地面材质"]

        # 只改变指定部分
        change_elements = [modification]

        # 调用图生图API（低strength只改局部）
        result = self.call_image_to_image_api(
            reference_image=reference_image,
            keep_consistent=keep_elements,
            change_elements=change_elements,
            strength=0.50
        )

        self.save_result(result, output_dir)

    def analyze_user_intent(self, user_input: str, context: dict):
        """场景4: 智能分析用户意图"""
        # 检测是否有参考图
        has_reference = self.detect_reference_image(context)

        # 分析用户描述的详细程度
        detail_level = self.analyze_detail_level(user_input)

        # 智能推荐模式和参数
        if not has_reference:
            return {
                "mode": "text_to_image",
                "prompt": self.build_architectural_prompt(user_input),
                "strength": None
            }
        elif "视角" in user_input or "角度" in user_input:
            return {
                "mode": "image_to_image",
                "keep_consistent": ["风格", "色调", "家具"],
                "change_elements": [user_input],
                "strength": 0.65
            }
        elif "修改" in user_input or "更换" in user_input:
            return {
                "mode": "image_to_image",
                "keep_consistent": ["整体布局", "主要元素"],
                "change_elements": [user_input],
                "strength": 0.50
            }
        else:
            # 默认中等变化
            return {
                "mode": "image_to_image",
                "strength": 0.60
            }
```

#### 5.2.3 测试验证

**测试用例1: 严格按规划生成**
- 输入: Z1的平面图配置.md
- 预期输出: 符合平面布局的空间设计图

**测试用例2: 多视角一致性**
- 输入: 已有的入口视角图 + "生成就餐区俯视视角"
- 预期输出: 保持风格一致的新视角图

**测试用例3: 局部修改**
- 输入: 已有的就餐区图 + "将吊灯更换为球形吊灯"
- 预期输出: 只有吊灯改变，其他元素不变

**测试用例4: 智能分析**
- 输入: 用户模糊描述"生成一个温馨的火锅店空间"
- 预期输出: Agent智能分析并推荐text_to_image模式

---

### 5.3 algorithmic-art改造（3D可视化）

#### 5.3.1 克隆位置

```bash
# 从全局example-skills插件克隆到筹建组
plugins/筹建组/skills/algorithmic-art-3d-viz/
```

#### 5.3.2 改造内容

**SKILL.md改造**:
```yaml
---
name: algorithmic-art-3d-viz
description: 专为筹建组Z3-3D可视化师定制的3D可视化技能包。使用p5.js生成等轴测图、线框图、体块分析图,输出HTML交互演示。适用于建筑空间的3D模拟表现。
---
```

**核心改造点**:
1. 新增"建筑3D可视化"专用模板
   - 等轴测图模板（45度俯视投影）
   - 线框图模板（强调结构）
   - 体块分析图模板（强调体量）

2. 强化建筑元素绘制
   - 墙体绘制（不同厚度、材质模拟）
   - 门窗绘制（开启方向、玻璃效果）
   - 家具绘制（桌椅、隔断、装饰）
   - 楼板绘制（地面、吊顶、设备层）

3. 新增交互功能
   - 鼠标滚轮缩放
   - 鼠标拖拽平移
   - 图层控制（显示/隐藏不同楼层）

**scripts/改造**:
新增 `isometric_generator.py`:
```python
def generate_isometric_view(config_md_path: str, output_dir: str):
    """
    从3D建模配置.md生成等轴测图HTML

    Args:
        config_md_path: 3D建模和细节表现.md文件路径
        output_dir: 输出目录

    Returns:
        生成的HTML文件路径
    """
    # 1. 解析配置文档
    config = parse_3d_config(config_md_path)

    # 2. 生成p5.js代码
    p5_code = generate_p5js_code(config, mode="isometric")

    # 3. 生成HTML文件
    html = build_html_template(p5_code)

    # 4. 保存文件
    output_path = os.path.join(output_dir, "isometric_view.html")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    return output_path

def generate_p5js_code(config: dict, mode: str):
    """生成p5.js绘图代码"""

    if mode == "isometric":
        return f"""
        // 等轴测图绘制
        function setup() {{
            createCanvas(1200, 900);
            angleMode(DEGREES);
        }}

        function draw() {{
            background(245);

            // 设置等轴测投影
            translate(width/2, height/2);
            rotate(-45);
            scale(1, 0.5);

            // 绘制地面层
            drawFloor({config['floor']});

            // 绘制墙体
            drawWalls({config['walls']});

            // 绘制家具
            drawFurniture({config['furniture']});
        }}

        function drawFloor(floorData) {{
            // 根据配置绘制地面
            fill(200);
            rect(0, 0, floorData.width, floorData.length);
        }}

        function drawWalls(wallsData) {{
            // 根据配置绘制墙体
            stroke(51);
            strokeWeight(3);
            noFill();

            wallsData.forEach(wall => {{
                line(wall.x1, wall.y1, wall.x2, wall.y2);
            }});
        }}

        function drawFurniture(furnitureData) {{
            // 根据配置绘制家具
            stroke(102);
            strokeWeight(2);
            fill(139, 111, 71, 100);

            furnitureData.forEach(item => {{
                rect(item.x, item.y, item.width, item.length);
            }});
        }}
        """

    elif mode == "wireframe":
        # 线框图模式代码
        pass

    elif mode == "massing":
        # 体块分析图模式代码
        pass
```

#### 5.3.3 测试验证

**测试用例1: 等轴测图**
- 输入: Z1的平面图配置.md
- 预期输出: 清晰的等轴测投影HTML，可交互缩放平移

**测试用例2: 线框图**
- 输入: 强调结构的配置
- 预期输出: 技术感强的线框图HTML

---

### 5.4 three.js技能包新建（高级3D）

#### 5.4.1 创建位置

```bash
plugins/筹建组/skills/three-js-advanced-3d/
```

#### 5.4.2 技能包结构

```
three-js-advanced-3d/
├── SKILL.md
├── scripts/
│   ├── __init__.py
│   ├── threejs_generator.py
│   └── templates/
│       ├── threejs_template.html
│       └── orbit_controls.js
├── reference.md
└── examples/
    └── example_3d_model.html
```

#### 5.4.3 核心内容

**SKILL.md**:
```yaml
---
name: three-js-advanced-3d
description: 专为筹建组Z3-3D可视化师定制的高级3D建模技能包。使用three.js生成交互式3D模型,支持体块分析、多视角切换、图层控制。适用于复杂建筑空间的沉浸式3D表现。
---
```

**threejs_generator.py**:
```python
def generate_interactive_3d(config_md_path: str, output_dir: str):
    """
    从3D建模配置.md生成three.js交互3D模型

    Args:
        config_md_path: 3D建模和细节表现.md文件路径
        output_dir: 输出目录

    Returns:
        生成的HTML文件路径
    """
    # 1. 解析配置文档
    config = parse_3d_config(config_md_path)

    # 2. 生成three.js几何体代码
    geometries_code = generate_geometries_code(config)

    # 3. 生成materials和lights代码
    materials_code = generate_materials_code(config)
    lights_code = generate_lights_code(config)

    # 4. 加载HTML模板
    with open('scripts/templates/threejs_template.html', 'r') as f:
        template = f.read()

    # 5. 填充模板
    html = template.format(
        geometries=geometries_code,
        materials=materials_code,
        lights=lights_code,
        controls="OrbitControls"  # 添加轨道控制
    )

    # 6. 保存文件
    output_path = os.path.join(output_dir, "interactive_3d_model.html")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    return output_path

def generate_geometries_code(config: dict):
    """生成three.js几何体代码"""
    code = ""

    # 地面层
    code += f"""
    // 地面
    const floorGeometry = new THREE.BoxGeometry({config['floor']['width']}, 0.1, {config['floor']['length']});
    const floorMaterial = new THREE.MeshStandardMaterial({{ color: 0x999999 }});
    const floor = new THREE.Mesh(floorGeometry, floorMaterial);
    floor.position.y = 0;
    scene.add(floor);
    """

    # 墙体
    for wall in config['walls']:
        code += f"""
        // 墙体
        const wallGeometry = new THREE.BoxGeometry({wall['width']}, {wall['height']}, {wall['thickness']});
        const wallMaterial = new THREE.MeshStandardMaterial({{ color: 0xCCCCCC }});
        const wall = new THREE.Mesh(wallGeometry, wallMaterial);
        wall.position.set({wall['x']}, {wall['y']}, {wall['z']});
        scene.add(wall);
        """

    # 家具
    for furniture in config['furniture']:
        code += f"""
        // 家具: {furniture['type']}
        const furnitureGeometry = new THREE.BoxGeometry({furniture['width']}, {furniture['height']}, {furniture['length']});
        const furnitureMaterial = new THREE.MeshStandardMaterial({{ color: 0x8B6F47 }});
        const furnitureItem = new THREE.Mesh(furnitureGeometry, furnitureMaterial);
        furnitureItem.position.set({furniture['x']}, {furniture['y']}, {furniture['z']});
        scene.add(furnitureItem);
        """

    return code
```

#### 5.4.4 测试验证

**测试用例1: 体块分析图**
- 输入: Z1的平面图配置.md
- 预期输出: 可旋转缩放的3D体块模型HTML

**测试用例2: 多图层控制**
- 输入: 包含地面层、吊顶层、设备层的配置
- 预期输出: 可切换显示/隐藏各层的3D模型

---

### 5.5 Wan改造（建筑动画生成）

#### 5.5.1 当前位置

```bash
plugins/筹建组/skills/Wan/
```

#### 5.5.2 改造内容

**SKILL.md改造**:
```yaml
---
name: Wan-architectural-animation
description: 专为筹建组Z4-建筑动画AIGC助手定制的建筑动画生成技能包。基于通义万相图生视频能力,支持空间动画、动线展示动画、场景分析动画。支持多种镜头运动：推拉摇移、环绕升降。
---
```

**核心改造点**:
1. 新增"建筑动画"专用提示词模板
   - 镜头运动模板（push_in/pull_out/pan/orbit/dolly/crane）
   - 空间类型模板（入口区/就餐区/包间/厨房/动线）
   - 叙事模板（品牌展示/空间体验/功能演示/氛围营造）

2. 强化图生视频模式
   - 从Z2的空间设计图生成动画
   - 从Z3的3D可视化生成动画
   - 保持视觉风格一致性

3. 新增镜头运动控制
   - camera_movement参数映射
   - 镜头速度控制（slow/medium/fast）
   - 镜头路径优化（避免突兀运动）

**scripts/改造**:
更新 `wan-execute.py`:
```python
class WanArchitecturalAnimation:
    """筹建组专用Wan建筑动画API客户端"""

    def __init__(self):
        self.api_key = os.getenv("ALIYUN_API_KEY")
        self.base_url = "https://dashscope.aliyuncs.com/api/v1"

    def generate_from_image(self, reference_image: str, camera_movement: str, prompt: str, output_dir: str):
        """场景1: 严格按规划生成（图生视频）"""

        # 1. 构建建筑动画提示词
        full_prompt = self.build_architectural_animation_prompt(
            base_prompt=prompt,
            camera_movement=camera_movement
        )

        # 2. 调用Wan图生视频API
        result = self.call_image_to_video_api(
            reference_image=reference_image,
            prompt=full_prompt,
            duration=5,
            resolution="1920x1080"
        )

        # 3. 保存视频
        self.save_video(result, output_dir)

        return result

    def generate_multi_view_animation(self, reference_image: str, new_view: str, keep_style: list, output_dir: str):
        """场景2: 多视角一致性（图生视频保持风格）"""

        # 构建保持一致性的提示词
        prompt = self.build_consistent_prompt(
            new_view=new_view,
            keep_elements=keep_style
        )

        # 调用图生视频API
        result = self.call_image_to_video_api(
            reference_image=reference_image,
            prompt=prompt,
            duration=8,
            resolution="1920x1080"
        )

        self.save_video(result, output_dir)
        return result

    def analyze_user_intent(self, user_input: str, context: dict):
        """场景3: 智能分析用户意图（镜头运动选择）"""

        # 关键词检测
        if "推进" in user_input or "进入" in user_input:
            camera_movement = "push_in"
        elif "拉出" in user_input or "退出" in user_input:
            camera_movement = "pull_out"
        elif "左右" in user_input or "平移" in user_input:
            camera_movement = "pan_left" if "左" in user_input else "pan_right"
        elif "环绕" in user_input or "旋转" in user_input:
            camera_movement = "orbit"
        elif "升降" in user_input:
            camera_movement = "crane"
        else:
            # 默认推进镜头
            camera_movement = "push_in"

        # 检测参考图
        has_reference = self.detect_reference_image(context)

        return {
            "mode": "image_to_video" if has_reference else "text_to_video",
            "camera_movement": camera_movement,
            "reference_image": context.get("reference_image") if has_reference else None
        }

    def build_architectural_animation_prompt(self, base_prompt: str, camera_movement: str):
        """构建建筑动画专用提示词"""

        # 镜头运动描述映射
        camera_descriptions = {
            "push_in": "摄像机缓慢推进,从远到近,吸引观众进入空间",
            "pull_out": "摄像机缓慢拉出,从近到远,展示整体空间布局",
            "pan_left": "摄像机向左平移,展示横向空间关系",
            "pan_right": "摄像机向右平移,展示横向空间关系",
            "orbit": "摄像机围绕中心点旋转,展示360度全景视角",
            "dolly": "摄像机沿轨道移动,展示空间深度和层次",
            "crane": "摄像机垂直升降,展示空间高度和垂直关系"
        }

        camera_desc = camera_descriptions.get(camera_movement, "摄像机平稳运镜")

        # 组合完整提示词
        full_prompt = f"{base_prompt}。{camera_desc}。平滑运镜,专业建筑摄影,温暖灯光,氛围感强。"

        return full_prompt
```

#### 5.5.3 测试验证

**测试用例1: 图生视频（推进镜头）**
- 输入: Z2的入口视角图 + "推进镜头展示入口区域"
- 预期输出: 5秒推进镜头视频MP4

**测试用例2: 多视角一致性**
- 输入: 已有的入口视角图 + "生成就餐区平移镜头动画"
- 预期输出: 保持风格一致的新视角动画MP4

**测试用例3: 智能镜头选择**
- 输入: 用户模糊描述"展示整个火锅店空间"
- 预期输出: Agent智能推荐orbit环绕镜头

---

## 6. 实施计划

### 6.1 实施阶段划分

**阶段1: Z1平面图计划师重构（3天）**
- Day 1: Agent改造（更新Z1-平面图计划师.md）
- Day 2: Skills克隆和改造（canvas-design-floor-plan）
- Day 3: 集成测试（Z1 → canvas-design完整工作流）

**阶段2: Z2空间设计AIGC助手重构（4天）**
- Day 1: Agent改造（更新Z2-空间设计AIGC助手.md）
- Day 2-3: Skills改造（Nano-banana多场景支持）
- Day 4: 集成测试（Z2 → Nano-banana四大场景）

**阶段3: Z3-3D可视化师重构（5天）**
- Day 1: Agent改造（更新Z3-3D可视化师.md）
- Day 2: Skills克隆（algorithmic-art-3d-viz）
- Day 3-4: Skills新建（three-js-advanced-3d）
- Day 5: 集成测试（Z3 → p5.js/three.js双模式）

**阶段4: Z4建筑动画AIGC助手重构（4天）**
- Day 1: Agent改造（更新Z4-建筑动画AIGC助手.md）
- Day 2-3: Skills改造（Wan建筑动画专用）
- Day 4: 集成测试（Z4 → Wan图生视频工作流）

**阶段5: 整体联调和文档更新（3天）**
- Day 1: 全流程测试（Z0 → Z1 → Z2 → Z3 → Z4 → ZZ完整链路）
- Day 2: 更新筹建组README.md和plugin.json
- Day 3: 创建培训文档和最佳实践案例

**总计**: 19个工作日（约3周）

### 6.2 实施顺序建议

**推荐顺序**: Z1 → Z2 → Z3 → Z4
- Z1的平面图配置.md是Z2的输入基础
- Z2的空间设计图是Z3和Z4的参考基础
- 按依赖关系串行实施，避免并行带来的接口不稳定

### 6.3 关键里程碑

**里程碑1**: Z1完成（第3天）
- 标志: 成功生成第一张平面图PNG/PDF

**里程碑2**: Z2完成（第7天）
- 标志: 成功生成四大场景的空间设计图

**里程碑3**: Z3完成（第12天）
- 标志: 成功生成等轴测图和交互3D模型HTML

**里程碑4**: Z4完成（第16天）
- 标志: 成功生成建筑动画视频MP4

**里程碑5**: 全流程打通（第19天）
- 标志: 从Z0需求输入到ZZ成果交付的完整链路验证

---

## 7. 验证测试

### 7.1 单元测试

**Z1-平面图计划师测试**:
```bash
# 测试1: 基础平面图生成
输入: 简单的300㎡火锅店配置.md
预期: 清晰的PNG/PDF平面图

# 测试2: 复杂平面图生成
输入: 包含多个包间、复杂动线的配置.md
预期: 准确的空间关系、动线箭头、完整图例

# 测试3: 错误处理
输入: 缺少必填字段的配置.md
预期: 友好的错误提示，指出缺失字段
```

**Z2-空间设计AIGC助手测试**:
```bash
# 测试1: 严格按规划生成（文生图）
输入: Z1的平面图配置.md
预期: 符合平面布局的空间设计图PNG

# 测试2: 多视角一致性（图生图）
输入: 已有的入口视角图 + "生成就餐区俯视视角"
预期: 保持风格一致的新视角图PNG

# 测试3: 局部修改（图生图低strength）
输入: 已有的就餐区图 + "将吊灯更换为球形吊灯"
预期: 只有吊灯改变，其他元素不变

# 测试4: 智能分析用户意图
输入: 模糊描述"生成一个温馨的火锅店空间"
预期: Agent推荐text_to_image模式并生成图像
```

**Z3-3D可视化师测试**:
```bash
# 测试1: 等轴测图（p5.js）
输入: Z1的平面图配置.md
预期: 清晰的等轴测投影HTML，可交互缩放平移

# 测试2: 交互3D模型（three.js）
输入: 包含地面层、吊顶层、设备层的配置
预期: 可旋转缩放的3D体块模型HTML，可切换图层

# 测试3: 线框图（p5.js）
输入: 强调结构的配置
预期: 技术感强的线框图HTML
```

**Z4-建筑动画AIGC助手测试**:
```bash
# 测试1: 图生视频（推进镜头）
输入: Z2的入口视角图 + "推进镜头展示入口区域"
预期: 5秒推进镜头视频MP4

# 测试2: 多视角一致性
输入: 已有的入口视角图 + "生成就餐区平移镜头动画"
预期: 保持风格一致的新视角动画MP4

# 测试3: 智能镜头选择
输入: 用户模糊描述"展示整个火锅店空间"
预期: Agent推荐orbit环绕镜头并生成视频
```

### 7.2 集成测试

**完整链路测试**:
```
Step 1: Z0需求输入
  输入: "我需要为新开的火锅店做开业筹备的完整设计方案"
  预期: Z0分析需求，分配任务给Z1-Z4

Step 2: Z1生成平面图
  输出: output/火锅店开业筹备/Z1-平面图计划师/
        ├── plans/平面图配置.md
        └── results/floor_plan.png

Step 3: Z2生成空间设计图（4个视角）
  输出: output/火锅店开业筹备/Z2-空间设计AIGC助手/
        └── results/
            ├── view-01-entrance.png
            ├── view-02-dining.png
            ├── view-03-booth.png
            └── view-04-private-room.png

Step 4: Z3生成3D可视化（2种模式）
  输出: output/火锅店开业筹备/Z3-3D可视化师/
        └── results/
            ├── isometric_view.html (p5.js等轴测图)
            └── interactive_3d_model.html (three.js交互3D)

Step 5: Z4生成建筑动画（3个镜头）
  输出: output/火锅店开业筹备/Z4-建筑动画AIGC助手/
        └── results/
            ├── animation-01-push-in.mp4 (入口推进镜头)
            ├── animation-02-pan.mp4 (就餐区平移镜头)
            └── animation-03-orbit.mp4 (整体环绕镜头)

Step 6: ZZ汇总交付
  输出: output/火锅店开业筹备/ZZ-筹建组组长/
        └── 完整设计方案交付包.zip
            ├── 平面图/
            ├── 空间设计图/
            ├── 3D可视化/
            └── 建筑动画/
```

### 7.3 性能测试

**生成速度基准**:
- Z1平面图生成: ≤2分钟
- Z2空间设计图生成（单张）: ≤3分钟
- Z3等轴测图生成: ≤1分钟
- Z3交互3D模型生成: ≤2分钟
- Z4建筑动画生成（5秒）: ≤5分钟

**质量标准**:
- 平面图: 尺寸准确（±5%误差）、功能分区清晰、符合建筑制图规范
- 空间设计图: 视觉风格统一、构图专业、符合建筑设计美学
- 3D可视化: 空间关系准确、交互流畅（≥30fps）、视觉清晰
- 建筑动画: 镜头平稳、运动流畅、风格一致、时长准确

---

## 8. 风险与对策

### 8.1 技术风险

**风险1: AIGC生成质量不稳定**
- 症状: 同样的提示词，不同批次生成的图像质量差异大
- 影响: 无法保证交付质量，用户体验差
- 对策:
  - 建立提示词最佳实践库，沉淀高质量提示词模板
  - 实施多轮生成机制（生成3张，选择最佳）
  - 引入质量评分机制（基于美学评估API）

**风险2: API调用失败或超时**
- 症状: Nano-banana/Wan API返回错误或超时
- 影响: 工作流中断，无法完成交付
- 对策:
  - 实施重试机制（3次重试，指数退避）
  - 添加降级策略（API失败时使用备用方案）
  - 提供详细的错误日志和用户反馈

**风险3: Skills执行引擎bug**
- 症状: Python脚本报错、HTML无法渲染等
- 影响: 无法生成最终成果
- 对策:
  - 充分的单元测试和集成测试
  - 建立快速回滚机制（保留改造前的原始版本）
  - 提供详细的错误堆栈信息和调试工具

### 8.2 业务风险

**风险4: Agent提示词工程能力不足**
- 症状: Agent生成的配置文档/提示词质量差，无法指导Skills执行
- 影响: 生成的图像/视频不符合要求
- 对策:
  - 在Agent.md中提供详尽的提示词工程规范和示例
  - 建立提示词评审机制（Agent生成后由ZZ或专家审核）
  - 提供提示词优化工具（基于历史成功案例的推荐系统）

**风险5: 输出成果不符合建筑行业标准**
- 症状: 生成的平面图/空间设计图/3D模型不符合专业规范
- 影响: 无法用于实际施工或营销
- 对策:
  - 在Agent.md中嵌入建筑行业标准和规范知识
  - 建立质量检查清单（功能分区合理性、动线合理性、尺寸准确性等）
  - 引入人工审核环节（由ZZ或专业设计师把关）

**风险6: 用户期望与实际能力不匹配**
- 症状: 用户期望CAD/BIM级别的专业成果，但AIGC只能提供概念级别
- 影响: 用户满意度低，重构失败
- 对策:
  - 明确沟通重构后的能力边界（概念设计 vs 施工图设计）
  - 调整用户期望（AIGC适合早期概念阶段，不适合施工阶段）
  - 提供清晰的使用场景说明（新店规划、方案展示、营销宣传）

### 8.3 项目风险

**风险7: 实施周期延误**
- 症状: 19天实施计划无法按时完成
- 影响: 影响整体项目进度
- 对策:
  - 预留缓冲时间（实际排期22天，留3天缓冲）
  - 识别关键路径（Z1 → Z2 → Z3 → Z4串行依赖）
  - 并行推进文档工作（Agent改造和Skills改造可并行）

**风险8: Skills改造破坏原有功能**
- 症状: 改造后的Nano-banana/Wan无法用于其他业务组
- 影响: 影响创意组等其他团队的工作
- 对策:
  - 创建筹建组专用版本（Nano-banana-space-design, Wan-architectural-animation）
  - 保留原始版本不动
  - 明确两个版本的使用场景和边界

---

## 9. 附录

### 9.1 环境变量检查

**必需的环境变量**:
```bash
# 从.env文件检查
OPENROUTER_API_KEY=sk-or-v1-xxx  # Nano-banana
ALIYUN_API_KEY=sk-xxx             # Wan (通义万相)
DASHSCOPE_API_KEY=sk-xxx          # Wan (同上)

# 可选的环境变量
KLING_JWT_TOKEN=xxx               # 可灵AI（Z4备用方案）
MINIMAX_API_KEY=xxx               # MiniMax海螺AI（Z4备用方案）
VOLCENGINE_ACCESS_KEY_ID=xxx      # 即梦AI（Z4备用方案）
```

**环境变量验证**:
```python
# scripts/check_env.py
import os
from dotenv import load_dotenv

def check_env():
    load_dotenv()

    required_vars = [
        "OPENROUTER_API_KEY",
        "ALIYUN_API_KEY",
        "DASHSCOPE_API_KEY"
    ]

    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)

    if missing:
        print(f"❌ 缺少必需环境变量: {', '.join(missing)}")
        print("请在.env文件中配置这些变量")
        return False
    else:
        print("✅ 所有必需环境变量已配置")
        return True

if __name__ == "__main__":
    check_env()
```

### 9.2 Skills改造清单汇总

| Skills | 改造类型 | 源位置 | 目标位置 | 预计工时 |
|--------|---------|--------|---------|---------|
| canvas-design-floor-plan | 克隆+改造 | example-skills:canvas-design | plugins/筹建组/skills/ | 2天 |
| Nano-banana-space-design | 原地改造 | plugins/筹建组/skills/Nano-banana/ | 同位置 | 3天 |
| algorithmic-art-3d-viz | 克隆+改造 | example-skills:algorithmic-art | plugins/筹建组/skills/ | 2天 |
| three-js-advanced-3d | 新建 | 无 | plugins/筹建组/skills/ | 3天 |
| Wan-architectural-animation | 原地改造 | plugins/筹建组/skills/Wan/ | 同位置 | 3天 |

**总计**: 13天（Skills改造）+ 6天（Agent改造+测试）= 19天

### 9.3 输出路径示例

**完整的火锅店开业筹备项目输出**:
```
output/
└── 火锅店开业筹备/
    ├── Z1-平面图计划师/
    │   ├── plans/
    │   │   └── 平面图配置-20251028.md
    │   ├── results/
    │   │   ├── floor_plan-20251028-4K.png
    │   │   └── floor_plan-20251028-A3.pdf
    │   ├── logs/
    │   │   └── execution-20251028-103000.log
    │   └── metadata/
    │       └── task-20251028-103000-meta.json
    │
    ├── Z2-空间设计AIGC助手/
    │   ├── plans/
    │   │   ├── view-01-entrance-prompt.json
    │   │   ├── view-02-dining-prompt.json
    │   │   ├── view-03-booth-prompt.json
    │   │   └── view-04-private-room-prompt.json
    │   ├── results/
    │   │   ├── view-01-entrance-1024x1024.png
    │   │   ├── view-02-dining-1024x1024.png
    │   │   ├── view-03-booth-1024x1024.png
    │   │   └── view-04-private-room-1024x1024.png
    │   ├── logs/
    │   │   └── execution-20251028-110000.log
    │   └── metadata/
    │       └── batch-20251028-110000-meta.json
    │
    ├── Z3-3D可视化师/
    │   ├── plans/
    │   │   └── 3D建模和细节表现-20251028.md
    │   ├── results/
    │   │   ├── isometric_view-20251028.html
    │   │   └── interactive_3d_model-20251028.html
    │   ├── logs/
    │   │   └── execution-20251028-120000.log
    │   └── metadata/
    │       └── task-20251028-120000-meta.json
    │
    └── Z4-建筑动画AIGC助手/
        ├── plans/
        │   ├── animation-01-push-in-prompt.json
        │   ├── animation-02-pan-prompt.json
        │   └── animation-03-orbit-prompt.json
        ├── results/
        │   ├── animation-01-push-in-5s-1080p.mp4
        │   ├── animation-02-pan-8s-1080p.mp4
        │   └── animation-03-orbit-10s-1080p.mp4
        ├── logs/
        │   └── execution-20251028-130000.log
        └── metadata/
            └── batch-20251028-130000-meta.json
```

---

## 📝 总结

本重构方案将筹建组agents从不切实际的CAD/BIM工具属性，转向实际可行的AIGC创作工具体系。核心思路是：

1. **Agent定位调整**: 从工具操作者 → 提示词工程师 + 执行引擎调度者
2. **三层架构强化**: 规范层（专业知识） → 计划层（结构化配置） → 执行层（AIGC API）
3. **Skills深度改造**: 将通用AIGC工具改造为筹建组专用的建筑/室内设计工具
4. **输出路径规范**: 统一的output/[项目名]/[agent-name]/结构
5. **质量标准明确**: 从概念设计出发，而非施工图级别

**预期成果**:
- ✅ 每个agent能够实际执行（不再是"空壳"）
- ✅ 生成的成果符合建筑/室内设计的基本标准
- ✅ 完整的工作流程可追溯、可复现
- ✅ 为后续迭代优化奠定基础

**实施周期**: 19个工作日（约3周）

**关键成功因素**:
- 充分的提示词工程规范和模板
- 稳定的AIGC API调用机制
- 全面的测试验证
- 清晰的用户期望管理

---

**文档状态**: ✅ 设计完成，待实施验证
**下一步**: 开始阶段1实施（Z1-平面图计划师重构）
