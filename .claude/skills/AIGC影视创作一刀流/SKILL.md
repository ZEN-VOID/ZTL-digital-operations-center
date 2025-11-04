---
name: one-blade-flow
description: 端到端影视制作自动化工作流,一键完成从剧本到完整分镜脚本CSV的全流程处理。整合30个专业智能体,覆盖8个制作组,支持自由创作模式和批量生产模式。
---
# 一刀流影视制作工作流 (One-Blade-Flow Production Workflow)

> **定位**: 端到端影视制作自动化系统的统一入口
> **核心理念**: "一刀切入,全链路打通" - 用户只需提供剧本或创意需求,系统自动完成所有制作流程
> **技术架构**: 基于Claude Code的多智能体协同系统,集成30个专业智能体,覆盖8个制作组

---

## 快速开始 (Quick Start)

### 用法1: 从剧本到完整分镜脚本 (最常用)

```
用户输入: 我有一个赛博朋克侦探的剧本,需要生成完整的分镜脚本CSV

一刀流执行:
1. 剧本分析 (screenplay-writer)
2. 分镜设计 (storyboard-director)
3. 美学指导 (film-aesthetic-advisor)
4. 8部门批量处理:
   - 表演组 (3个智能体)
   - 场景组 (3个智能体)
   - 摄影组 (5个智能体)
   - 制作组 (3个智能体)
5. Super-Director整合生成15字段CSV
6. 输出production-ready分镜脚本

输出文件:
- output/{项目名}/全组分镜脚本.csv (15字段完整CSV)
- output/{项目名}/批量整合报告.md (8章节质量报告)
```

### 用法2: 从创意概念到成片素材

```
用户输入: 生成一个30秒的赛博朋克城市夜景视频,要有侦探追逐的场景

一刀流执行:
1-5. (同用法1)
6. AIGC工具选择 (EE队长智能体)
7. 视觉素材生成:
   - Midjourney: 角色参考图
   - SORA-2: 30秒视频生成
   - Nano-banana: 角色衍生图(一致性≥95%)
8. 输出production-ready素材包

输出文件:
- output/{项目名}/全组分镜脚本.csv
- output/{项目名}/批量整合报告.md
- output/{项目名}/images/ (参考图)
- output/{项目名}/videos/ (成片素材)
```

---

## 核心能力 (Core Capabilities)

### 能力1: 端到端自动化

**传统流程** (需要15-20天):

```
剧本创作(3天) → 分镜设计(5天) → 美学指导(2天) →
表演设计(2天) → 场景设计(2天) → 摄影设计(3天) →
后期设计(2天) → 整合协调(3天) → 质量检查(2天)
```

**一刀流流程** (需要1-2小时):

```
用户输入剧本/需求
    ↓
一刀流自动执行(60-120分钟)
    ↓
输出production-ready分镜脚本CSV + 素材包
```

**时间节省**: 95%+ (15天 → 1-2小时)ß

### 能力2: 30个智能体协同

**8大制作组架构**:

```yaml
提词组 (11个智能体):
  - EE (队长): AIGC工具统一调度,决策矩阵11维度×10工具
  - SORA-2: OpenAI视频,最长20秒,原生音频
  - Runway: 专业视频,运动控制
  - Luma: 3D场景理解
  - Kling: 快手可灵,中文优化
  - Minimax: 海螺AI,多模态
  - Dreamina: 字节即梦,多镜头
  - VEO: Google视频,4K分辨率
  - Midjourney: 图像生成,v7
  - Wan: 阿里通义万相,Composer
  - Nano-banana: 衍生图,一致性≥95%

表演组 (3个智能体):
  - character-style-consultant: 角色个性与表演风格
  - micro-performance-designer: 微表演设计
  - action-choreographer: 动作编排

创作组 (2个智能体):
  - screenplay-writer: 剧本创作与改编
  - film-aesthetic-advisor: 美学设计与视觉风格

摄影组 (5个智能体):
  - cinematography-designer: 构图设计
  - cinematography-lighting-designer: 灯光设计
  - cinematography-equipment-master: 器材与参数
  - cinematography-movement-designer: 运镜设计
  - film-color-design-master: 色彩艺术

场景组 (3个智能体):
  - spatial-designer: 空间设计与布局
  - costume-designer: 服装设计
  - makeup-hair-designer: 化妆与发型

制作组 (3个智能体):
  - vfx-design-advisor: 视效设计
  - film-editor-advisor: 剪辑设计
  - film-composer: 配乐设计

导演组 (1个智能体):
  - storyboard-director: 分镜脚本创建

管理组 (2个智能体):
  - film-producer: 团队配置/需求文档
  - film-distributor: 宣传策略/推广
```

### 能力3: 双模式架构

**🎨 自由创作模式** (Free Creative Mode):

- 适用场景: 单场景探索,创意实验,风格测试
- 执行特点: 逐场景深度创作,允许风格多样性
- 输出格式: Markdown报告 (详细的设计思路和建议)

**📊 批量生产模式** (Batch Production Mode):

- 适用场景: 完整项目,多场景统一,生产就绪
- 执行特点: 批量处理所有场景,强制风格一致性
- 输出格式: CSV文件 (15字段production-ready格式)

**模式自动切换**:

- 检测输入: 单场景 → 🎨自由模式
- 检测输入: 多场景/完整剧本 → 📊批量模式

### 能力4: 15字段Production-Ready CSV

**完整字段结构**:

```csv
场景ID,分镜序号,场景描述,镜头描述,
角色演绎(character-style-consultant),
动作(action-choreographer),
微表演(micro-performance-designer),
服装(costume-designer),
妆造(makeup-hair-designer),
空间(spatial-designer),
构图(cinematography-designer),
摄影器材及参数(cinematography-equipment-master),
光影(cinematography-lighting-designer),
色彩(film-color-design-master),
运镜(cinematography-movement-designer),
配乐(film-composer),
特效(vfx-design-advisor),
剪辑(film-editor-advisor)
```

**字段覆盖率**: 100% (所有制作环节无遗漏)
**行业标准**: 符合好莱坞制片标准和中国影视工业化标准

---

## 执行流程 (Execution Workflow)

### 阶段1: 需求分析与剧本准备 (5-10分钟)

**Step 1.1: 接收用户输入**

**输入类型识别**:

```yaml
类型A: 完整剧本文件
  - 格式: .md/.txt/.pdf/.docx
  - 处理: 直接读取剧本内容
  - 示例: "我有一个剧本文件script.md,请生成分镜"

类型B: 剧本大纲或故事概要
  - 格式: 用户文本描述
  - 处理: screenplay-writer智能体补全剧本
  - 示例: "赛博朋克侦探,主角追查真相,3幕结构"

类型C: 创意概念
  - 格式: 抽象需求
  - 处理: 从需求 → 剧本 → 分镜
  - 示例: "生成一个30秒的城市追逐场景"
```

**Step 1.2: 项目初始化**

```yaml
创建项目目录:
  - output/{项目名}/
  - output/{项目名}/images/
  - output/{项目名}/videos/
  - output/{项目名}/documents/

项目元数据:
  project_name: [从用户输入提取]
  project_type: [科幻惊悚/动作冒险/爱情文艺/...]
  aesthetic_baseline: [赛博朋克美学/新黑色电影/...]
  total_scenes: [待确认]
  total_shots: [待确认]
```

**Step 1.3: 剧本结构分析**

**调用智能体**: `screenplay-writer` (如果需要补全剧本)

**分析维度**:

```yaml
叙事结构:
  - 三幕结构: 第一幕/第二幕/第三幕 (页数分配25%/50%/25%)
  - 或四幕结构: Setup/Confrontation/Escalation/Resolution

角色系统:
  - 主角: [姓名/性格特质/角色弧光]
  - 配角: [姓名/关系网络/功能定位]
  - 对手: [姓名/对抗动机/戏剧张力]

场景清单:
  - 场景总数: XX个
  - 室内场景: XX个
  - 室外场景: XX个
  - 特殊场景: XX个(虚拟空间/梦境等)

时长估算:
  - 总时长: XX分钟
  - 每场景平均时长: XX秒
```

### 阶段2: 分镜脚本设计 (10-20分钟)

**Step 2.1: 初始分镜脚本生成**

**调用智能体**: `storyboard-director`

**输入**: 完整剧本 + 项目元数据
**输出**: 基础分镜脚本CSV (仅含4个基础字段)

```csv
场景ID,分镜序号,场景描述,镜头描述
S01,001,"清晨公寓,主角与搭档对话","中景:两人坐在桌边,低角度"
S01,002,"清晨公寓,主角起身","全景:主角缓慢站起,镜头跟随"
S02,003,"夜晚街道,主角独自行走","远景:主角背影,街道霓虹灯"
...
```

**Step 2.2: 美学基调统一**

**调用智能体**: `film-aesthetic-advisor`

**输入**: 项目类型 + 剧本主题
**输出**: 美学指导文档

```yaml
项目: 赛博朋克侦探
美学基调:
  视觉维度:
    - 色彩: 冷色调为主(蓝紫70%),暖色点缀(橙黄30%)
    - 光影: 高对比度,霓虹灯光混合,低照度
    - 构图: 对称构图+三分法,视觉重心偏向画面右侧
    - 空间: 狭窄压抑的城市空间,垂直感强烈

  听觉维度:
    - 配乐: 电子-管弦混合,Hans Zimmer式音墙
    - 音效: 环境音层次丰富,机械声+人声+城市背景

  叙事维度:
    - 节奏: 前30%慢节奏建立氛围,中40%快节奏推进,后30%情感爆发
    - 主题: 认知的碎裂,时间的流动性,人性的保留
```

### 阶段3: 8部门批量处理 (30-60分钟)

**执行策略**: Sequential Department Calling (顺序调用,依赖链)

```
表演组 (3个智能体,并行)
    ↓
场景组 (3个智能体,并行)
    ↓
摄影组 (5个智能体,并行)
    ↓
制作组 (3个智能体,并行)
```

**Step 3.1: 表演组批量处理**

**调用智能体** (并行):

- `character-style-consultant` → 填充"角色演绎"字段
- `action-choreographer` → 填充"动作"字段
- `micro-performance-designer` → 填充"微表演"字段

**输入**: 基础分镜脚本CSV + 美学指导文档
**输出**: CSV增加3个表演组字段

**批量处理原则**:

- ✅ 所有场景一次性处理,保证角色性格一致性
- ✅ 角色演绎贯穿整个项目的性格弧光
- ✅ 动作设计符合角色的身体条件和技能水平

**Step 3.2: 场景组批量处理**

**调用智能体** (并行):

- `costume-designer` → 填充"服装"字段
- `makeup-hair-designer` → 填充"妆造"字段
- `spatial-designer` → 填充"空间"字段

**输入**: 表演组输出CSV + 美学指导文档
**输出**: CSV增加3个场景组字段

**批量处理原则**:

- ✅ 服装/妆造在整个项目中保持角色造型一致性
- ✅ 空间设计符合叙事需求和摄影要求

**跨部门协调**:

- 角色演绎 ↔ 服装/妆造: 性格特质 → 造型设计
- 动作 ↔ 空间: 动作可行性 → 空间尺度匹配

**Step 3.3: 摄影组批量处理**

**调用智能体** (并行):

- `cinematography-designer` → 填充"构图"字段
- `cinematography-equipment-master` → 填充"摄影器材及参数"字段
- `cinematography-lighting-designer` → 填充"光影"字段
- `film-color-design-master` → 填充"色彩"字段
- `cinematography-movement-designer` → 填充"运镜"字段

**输入**: 场景组输出CSV + 美学指导文档
**输出**: CSV增加5个摄影组字段

**批量处理原则**:

- ✅ 所有摄影参数批量处理,保证视觉风格统一
- ✅ 构图/光影/色彩/运镜形成完整的视觉语言系统

**跨部门协调** (摄影组内部):

- 构图 ↔ 运镜: 构图设计 → 运镜路径规划
- 光影 ↔ 色彩: 光源色温 → 调色方向协调
- 摄影器材及参数 ↔ 光影: ISO感光度 → 光强度匹配

**Step 3.4: 制作组批量处理**

**调用智能体** (并行):

- `film-composer` → 填充"配乐"字段
- `vfx-design-advisor` → 填充"特效"字段
- `film-editor-advisor` → 填充"剪辑"字段

**输入**: 摄影组输出CSV + 美学指导文档
**输出**: CSV增加3个制作组字段 (完整15字段)

**批量处理原则**:

- ✅ 配乐在整个项目中形成完整的主题系统和Leitmotif网络
- ✅ 剪辑设计符合叙事节奏和情感曲线

**跨部门协调**:

- 构图+运镜 ↔ 配乐: 视觉节奏 → 音乐节奏
- 运镜 ↔ 剪辑: 运镜速度 → 剪辑时长
- 光影+色彩 ↔ 配乐: 视觉情绪 → 音乐情绪

### 阶段4: Super-Director整合与质量检查 (10-20分钟)

**Step 4.1: 跨部门协调检查**

**调用智能体**: `super-director` (批量模式)

**输入**: 完整15字段CSV + 所有部门输出
**执行**: 6-Step批量工作流

```yaml
Step 1: CSV识别与读取
  - 验证15字段完整性
  - 统计场景数/分镜数

Step 2: 批量场景理解与部门任务分配
  - 项目类型识别
  - 叙事结构分析
  - 部门任务分配矩阵验证

Step 3: 逐行填充15字段
  - 验证所有字段已填充
  - 检查字段格式规范性

Step 4: 跨部门字段协调
  - 表演组 ↔ 场景组协调检查
  - 摄影组内部协调检查
  - 摄影组 ↔ 制作组协调检查

Step 5: 批量质量检查 (5维度)
  - 场景内一致性
  - 跨场景主题一致性
  - 部门输出完整性
  - 技术可行性验证
  - 叙事流畅度

Step 6: CSV更新与综合批量报告生成
  - 更新CSV文件 (修复协调冲突)
  - 生成8章节批量整合报告
```

**Step 4.2: 质量分级**

**A级 (Production-Ready)**:

- 所有字段完整,无冲突
- 跨部门协调完美
- 技术可行性100%
- 可直接用于制片准备

**B级 (Minor Issues)**:

- 1-3个轻微冲突
- 需要微调但不影响整体
- 升级路径: 针对性修复冲突点

**C级 (Major Issues)**:

- 4+个重大冲突
- 技术可行性存疑
- 升级路径: 重新调用相关智能体

### 阶段5: AIGC素材生成 (可选,20-40分钟)

**Step 5.1: AIGC工具选择**

**调用智能体**: `EE` (队长)

**输入**: 完整分镜脚本CSV + 素材需求
**执行**: 决策矩阵分析 (11维度×10工具)

**决策矩阵** (部分示例):

```yaml
需求: 生成30秒赛博朋克城市追逐视频

维度评分 (0-10分):
  SORA-2:
    - 时长支持: 8分 (最长20秒,需拼接)
    - 运动控制: 9分 (原生运动理解优秀)
    - 音频同步: 10分 (原生音频)
    - 总分: 27分

  Runway:
    - 时长支持: 7分 (需拼接)
    - 运动控制: 10分 (Motion Brush精确控制)
    - 音频同步: 5分 (需后期配音)
    - 总分: 22分

  Luma:
    - 时长支持: 7分
    - 运动控制: 8分
    - 3D场景理解: 10分 (物理精确性最佳)
    - 总分: 25分

决策结果:
  首选: SORA-2 (27分,原生音频优势)
  混合策略:
    - Midjourney生成角色参考图
    - SORA-2生成视频素材
    - Nano-banana生成角色衍生图(一致性≥95%)
```

**Step 5.2: 素材生成执行**

**工具调用示例**:

```yaml
工具1: Midjourney
  - 任务: 生成侦探角色参考图
  - 提示词: "Cyberpunk detective, noir style, rain-soaked street, neon lights, --ar 2:3 --style raw --v 6.1"
  - 输出: output/{项目名}/images/character_ref_001.png

工具2: SORA-2
  - 任务: 生成30秒追逐视频
  - 提示词: (从分镜脚本S03场景提取,包含摄影组5字段的完整描述)
  - 输出: output/{项目名}/videos/chase_scene_s03.mp4

工具3: Nano-banana
  - 任务: 生成角色衍生图(不同角度/表情)
  - 输入: character_ref_001.png
  - 输出: output/{项目名}/images/character_variations_001-010.png
```

### 阶段6: 最终输出与交付 (5分钟)

**输出清单**:

```yaml
核心文件:
  - output/{项目名}/全组分镜脚本.csv
    ├─ 15字段完整CSV
    ├─ UTF-8 BOM编码 (Excel兼容)
    └─ Production-ready标准

  - output/{项目名}/批量整合报告.md
    ├─ 8章节质量报告
    ├─ 统计信息/部门质量/跨部门协调/质量检查
    ├─ 美学分析/叙事结构/生产就绪度/特别说明
    └─ Markdown格式,可转换为PDF/DOCX

素材文件 (如果生成):
  - output/{项目名}/images/
    ├─ 角色参考图
    ├─ 场景概念图
    └─ 道具设计图

  - output/{项目名}/videos/
    ├─ 场景视频素材
    └─ 运镜测试视频

文档文件:
  - output/{项目名}/documents/
    ├─ 剧本.md (如果从概念生成)
    ├─ 美学指导文档.md
    └─ 部门设计文档/ (各部门详细设计)
```

---

## 使用示例 (Examples)

### 示例1: 完整项目从剧本到分镜

**用户输入**:

```
我有一个赛博朋克侦探短片剧本,30分钟时长,3幕结构,需要生成完整的分镜脚本CSV和素材包。
剧本文件: project/赛博朋克侦探/剧本.md
```

**一刀流执行**:

```yaml
阶段1: 需求分析 (3分钟)
  - 读取剧本文件
  - 识别项目类型: 科幻惊悚
  - 叙事结构: 三幕结构
  - 场景总数: 15个
  - 分镜总数: 85个

阶段2: 分镜脚本设计 (12分钟)
  - storyboard-director生成基础分镜CSV
  - film-aesthetic-advisor提供美学指导
    美学基调: 赛博朋克美学 + 新黑色电影

阶段3: 8部门批量处理 (45分钟)
  - 表演组: 15分钟 (3智能体并行)
  - 场景组: 15分钟 (3智能体并行)
  - 摄影组: 20分钟 (5智能体并行)
  - 制作组: 15分钟 (3智能体并行)

阶段4: Super-Director整合 (15分钟)
  - 跨部门协调检查
  - 5维度质量检查
  - 质量分级: A级 (Production-Ready)
  - 生成8章节报告

阶段5: AIGC素材生成 (30分钟)
  - EE队长决策: Midjourney + SORA-2 + Nano-banana
  - 生成角色参考图×5
  - 生成场景视频×15
  - 生成角色衍生图×50

阶段6: 最终输出 (2分钟)
  - 全组分镜脚本.csv (15字段×85行)
  - 批量整合报告.md (12,000字)
  - images/ (55张图片)
  - videos/ (15个视频)

总耗时: 107分钟 (约1.8小时)
```

**输出文件示例**:

`output/赛博朋克侦探/全组分镜脚本.csv` (前3行):

```csv
场景ID,分镜序号,场景描述,镜头描述,角色演绎(character-style-consultant),动作(action-choreographer),微表演(micro-performance-designer),服装(costume-designer),妆造(makeup-hair-designer),空间(spatial-designer),构图(cinematography-designer),摄影器材及参数(cinematography-equipment-master),光影(cinematography-lighting-designer),色彩(film-color-design-master),运镜(cinematography-movement-designer),配乐(film-composer),特效(vfx-design-advisor),剪辑(film-editor-advisor)
S01,001,"清晨公寓,主角与搭档对话","中景:两人坐在桌边,低角度","侦探李华+冷静理性型:[面部表情克制,眼神锐利,肢体语言紧绷,内心坚定外化为微微前倾的姿态]","缓慢起身,右手整理衣领,眼神扫视房间,展现警觉状态","眉头微蹙,眼神短暂闪躲,呼吸节奏加快,暗示内心不安","深灰色三件套西装,真丝领带暗红色,皮革手套黑色,展现冷峻专业形象","自然妆容凸显成熟魅力,短发梳理整齐,整体造型干练利落","现代公寓,落地窗前5m×3m区域,金属办公桌+皮质座椅,冷硬科技感氛围","中景,三分法构图,主角占画面右侧2/3,视觉焦点在眼神","Sony FX6,Sigma 35mm f/1.8 ART,ISO 800,f/2.8,快门1/50s,Log3拍摄","窗外自然光主光(5600K),内部补光柔光(3200K),光比3:1,营造戏剧性明暗对比","冷色调为主(蓝灰70%),暖色点缀(橙黄30%),营造疏离感,LUT: Cyberpunk Teal","慢推镜头,速度0.5m/s,从全景推至中景,强化角色决心的渐进感","音乐风格:温暖抒情(Thomas Newman式钢琴主导) | 乐器配置:钢琴主奏+弦乐垫底 | 节奏类型:Andante 72BPM+4/4拍 | 情感曲线:平静→微温暖→回归平静(20%→35%→25%) | 叙事功能:Hero Theme首次呈现+象征日常生活+哲学层:时间的流动性","无","硬切转场,镜头时长5秒,平稳节奏建立基调"
S03,015,"夜晚街道,主角追逐嫌疑人","全景:主角在屋顶奔跑,摇镜头跟随","侦探李华+冷静理性型:[身体前倾全速奔跑,眼神紧盯前方,面部肌肉紧绷,展现坚定追击意志]","全速奔跑,跨越障碍物,右手扶墙转弯,左手握持武器","眼神坚定不移,呼吸急促,额头汗珠滚落,展现极度专注","战术作战服黑色,反光条纹银色,防护头盔,凸显专业特工形象","战术妆容(面部防汗),短发紧贴头皮,整体造型实用主义","城市屋顶,20m×10m开阔区域,通风管道+水箱,夜晚霓虹灯光反射","全景,跟随构图,主角始终在画面中心,动态平衡","Sony FX6,Sigma 18-35mm f/1.8,ISO 3200,f/2.0,快门1/100s,高速快门防抖","霓虹灯混合光(多色温),无补光,高对比度,营造赛博朋克氛围","高饱和度霓虹色(蓝紫橙),暗部压低,强烈色彩冲击,LUT: Neon Noir","快速摇镜头,跟随主角移动,运镜速度2m/s,强化追逐的紧迫感","音乐风格:驱动性电子-管弦混合(Hans Zimmer式音墙) | 乐器配置:大型铜管组+电子低音合成器+打击乐组 | 节奏类型:Presto 140BPM+4/4拍+切分节奏 | 情感曲线:紧张→急速攀升→爆发(60%→85%→95%) | 叙事功能:无主题引用(纯氛围音乐)+象征追逐的机械性+哲学层:时间压缩感","全息地图投影特效,蓝色半透明,实时更新路径","快速剪辑,镜头时长1.5-2秒,硬切转场,强化动作节奏"
```

### 示例2: 从创意概念到成片

**用户输入**:

```
生成一个60秒的商业广告,主题是"未来科技改变生活",需要展示智能家居产品,风格要科幻但温馨。
```

**一刀流执行**:

```yaml
阶段1: 需求分析 (5分钟)
  - 输入类型: 创意概念
  - screenplay-writer生成广告剧本
    ├─ 时长: 60秒
    ├─ 场景: 5个 (早晨起床/智能厨房/工作场景/家庭团聚/夜晚入睡)
    └─ 叙事: 一天生活的智能化展示

阶段2-4: (同示例1流程)
  - 分镜设计
  - 8部门批量处理
  - Super-Director整合

阶段5: AIGC素材生成 (25分钟)
  - EE队长决策: VEO (Google,4K分辨率) + Midjourney
  - 策略: Midjourney生成产品概念图 → VEO生成4K视频
  - 输出: 5个场景×4K视频

阶段6: 最终输出
  - 全组分镜脚本.csv (15字段×15行)
  - 批量整合报告.md
  - images/ (产品概念图×10)
  - videos/ (4K场景视频×5)

总耗时: 85分钟 (约1.4小时)
```

---

## 配置与定制 (Configuration)

### 配置文件: `config.yaml`

```yaml
# 一刀流配置文件
project:
  default_output_path: "output/"
  auto_create_subdirs: true

workflow:
  # 执行模式
  mode: "auto"  # auto | manual | hybrid
    # auto: 全自动,无需用户干预
    # manual: 每个阶段需要用户确认
    # hybrid: 关键阶段需要确认

  # 质量门控
  quality_gates:
    enable: true
    min_grade: "B"  # A | B | C
    auto_retry: true
    max_retries: 2

agents:
  # 智能体超时设置
  timeout:
    screenplay_writer: 300  # 5分钟
    storyboard_director: 600  # 10分钟
    department_agents: 900  # 15分钟/组
    super_director: 1200  # 20分钟

  # 并行执行
  parallel_execution:
    enable: true
    max_concurrent: 5  # 最多5个智能体并行

aigc:
  # AIGC工具配置
  enable: true
  auto_select: true  # 使用EE队长自动选择

  # 手动指定工具 (覆盖EE决策)
  manual_tools: []
    # - SORA-2
    # - Midjourney

  # 素材生成配置
  image_generation:
    enable: true
    format: "png"
    resolution: "2048x2048"

  video_generation:
    enable: true
    format: "mp4"
    resolution: "4K"
    max_duration: 60  # 秒

output:
  # 输出格式
  csv:
    enable: true
    encoding: "utf-8-sig"  # UTF-8 BOM for Excel
    delimiter: ","

  report:
    enable: true
    format: "markdown"  # markdown | pdf | docx

  # 元数据
  metadata:
    enable: true
    include_timestamps: true
    include_agent_versions: true
```

### 自定义工作流

**场景1: 只需要分镜脚本,不需要AIGC素材**

```yaml
# config_storyboard_only.yaml
aigc:
  enable: false

workflow:
  skip_stages:
    - "阶段5: AIGC素材生成"
```

**场景2: 只需要特定部门的输出**

```yaml
# config_cinematography_only.yaml
departments:
  enable:
    - 摄影组
  disable:
    - 表演组
    - 场景组
    - 制作组

output:
  csv:
    fields:
      - 场景ID
      - 分镜序号
      - 场景描述
      - 镜头描述
      - 构图
      - 摄影器材及参数
      - 光影
      - 色彩
      - 运镜
```

---

## 最佳实践 (Best Practices)

### 实践1: 提供清晰的项目信息

**✅ 推荐**:

```
项目名称: 赛博朋克侦探
项目类型: 科幻惊悚短片
时长: 30分钟
叙事结构: 三幕结构
美学风格: 赛博朋克美学 + 新黑色电影
剧本文件: project/赛博朋克侦探/剧本.md
```

**❌ 不推荐**:

```
做一个视频
```

### 实践2: 分阶段验证质量

**流程**:

```
阶段1完成 → 检查剧本结构是否正确
阶段2完成 → 检查分镜数量和场景分布
阶段3完成 → 抽查几个字段的质量
阶段4完成 → 查看质量报告,确认分级
阶段5完成 → 验证素材与分镜脚本一致性
```

### 实践3: 利用混合策略

**AIGC工具组合建议**:

```yaml
角色一致性项目:
  - Midjourney: 生成角色参考图
  - Nano-banana: 生成角色衍生图(一致性≥95%)
  - SORA-2: 生成带角色的视频

高质量商业项目:
  - Midjourney: 概念设计
  - VEO: 4K视频生成
  - Runway: Motion Brush精修

快速原型项目:
  - Kling: 中文提示词优化
  - Dreamina: 单提示词多镜头
```

### 实践4: 定期备份和版本控制

**文件管理**:

```
output/
├── 赛博朋克侦探/
│   ├── v1.0_2024-01-15/  # 版本1
│   │   ├── 全组分镜脚本.csv
│   │   ├── 批量整合报告.md
│   │   └── ...
│   ├── v1.1_2024-01-16/  # 修订版本
│   │   └── ...
│   └── final_2024-01-20/ # 最终版本
│       └── ...
```

---

## 故障排除 (Troubleshooting)

### 问题1: CSV字段不完整

**症状**: 生成的CSV缺少某些字段或字段为空

**原因**:

- 某个智能体超时未响应
- 批量处理时部分场景未覆盖

**解决方案**:

```yaml
方法1: 重新调用缺失字段的智能体
  - 识别缺失字段对应的智能体
  - 单独调用该智能体补充字段

方法2: 增加超时时间
  - 编辑config.yaml
  - 增加agents.timeout.department_agents值

方法3: 启用自动重试
  - 设置workflow.quality_gates.auto_retry: true
```

### 问题2: 跨部门协调冲突

**症状**: Super-Director报告中出现多个协调冲突

**原因**:

- 部门智能体独立处理,未考虑跨部门约束
- 美学基调未正确传递

**解决方案**:

```yaml
方法1: 手动修复冲突
  - 查看批量整合报告的"跨部门协调"章节
  - 根据冲突描述,手动调整CSV字段

方法2: 重新生成美学指导
  - 调用film-aesthetic-advisor
  - 更明确地指定美学约束
  - 重新执行8部门批量处理

方法3: 降低质量标准
  - 设置workflow.quality_gates.min_grade: "C"
  - 允许轻微冲突存在
```

### 问题3: AIGC素材生成失败

**症状**: 阶段5 AIGC工具返回错误

**原因**:

- API密钥无效或超出配额
- 提示词不符合工具要求
- 网络连接问题

**解决方案**:

```yaml
方法1: 检查API配置
  - 验证.env文件中的API_KEY
  - 检查API配额和余额

方法2: 切换AIGC工具
  - 编辑config.yaml
  - 手动指定备用工具: aigc.manual_tools: ["Runway"]

方法3: 禁用AIGC生成
  - 设置aigc.enable: false
  - 只生成分镜脚本CSV,不生成素材
```

### 问题4: 执行时间过长

**症状**: 一刀流执行超过2小时

**原因**:

- 场景数量过多(>50个)
- 启用了所有AIGC工具
- 网络速度慢

**解决方案**:

```yaml
方法1: 分批处理
  - 将大项目拆分为多个小项目
  - 每个项目<30个场景

方法2: 禁用AIGC生成
  - 第一遍只生成分镜脚本
  - 第二遍单独生成AIGC素材

方法3: 减少并行数
  - 降低agents.parallel_execution.max_concurrent
  - 减少同时调用的智能体数量
```

---

## 技术架构 (Technical Architecture)

### 架构图

```
┌─────────────────────────────────────────────────────────────┐
│                     一刀流工作流引擎                           │
│                   (One-Blade-Flow Engine)                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      任务调度器                               │
│                   (Task Scheduler)                          │
│  - 阶段管理                                                   │
│  - 智能体调用                                                 │
│  - 依赖链解析                                                 │
│  - 并行执行控制                                               │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  创作阶段     │     │  执行阶段     │     │  生成阶段     │
│ (Creative)   │     │ (Execution)  │     │ (Generation) │
└──────────────┘     └──────────────┘     └──────────────┘
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│screenplay-   │     │8部门协同      │     │AIGC工具集成  │
│writer        │     │14个智能体     │     │10个工具       │
│storyboard-   │     │parallel       │     │EE队长调度     │
│director      │     │execution      │     │              │
│film-         │     │              │     │              │
│aesthetic-    │     │              │     │              │
│advisor       │     │              │     │              │
└──────────────┘     └──────────────┘     └──────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Super-Director整合层                        │
│                 (Integration & QC Layer)                     │
│  - 跨部门协调                                                 │
│  - 5维度质量检查                                              │
│  - A/B/C质量分级                                             │
│  - 8章节报告生成                                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      输出层                                   │
│                   (Output Layer)                             │
│  - CSV文件(15字段)                                            │
│  - 批量整合报告(Markdown)                                      │
│  - AIGC素材(images/videos)                                   │
│  - 元数据(timestamps/versions)                                │
└─────────────────────────────────────────────────────────────┘
```

### 数据流

```
用户输入 (剧本/需求)
    │
    ├─→ [阶段1] 需求分析
    │        ├─ 类型识别: A/B/C
    │        ├─ 项目初始化
    │        └─ 剧本结构分析
    │
    ├─→ [阶段2] 分镜脚本设计
    │        ├─ storyboard-director → 基础4字段CSV
    │        └─ film-aesthetic-advisor → 美学指导文档
    │
    ├─→ [阶段3] 8部门批量处理
    │        ├─ 表演组 (3智能体) → +3字段
    │        ├─ 场景组 (3智能体) → +3字段
    │        ├─ 摄影组 (5智能体) → +5字段
    │        └─ 制作组 (3智能体) → +3字段
    │             └→ 完整15字段CSV
    │
    ├─→ [阶段4] Super-Director整合
    │        ├─ 跨部门协调检查
    │        ├─ 5维度质量检查
    │        ├─ A/B/C质量分级
    │        └─ 8章节报告生成
    │
    ├─→ [阶段5] AIGC素材生成 (可选)
    │        ├─ EE队长决策矩阵
    │        └─ 10工具并行生成
    │
    └─→ [阶段6] 最终输出
             ├─ CSV文件
             ├─ 批量报告
             ├─ 素材包
             └─ 元数据
```

---

## API参考 (API Reference)

### 主函数: `execute_one_blade_flow()`

```python
def execute_one_blade_flow(
    input_data: Union[str, Path, Dict],
    config: Optional[Dict] = None,
    mode: str = "auto"
) -> OneBladeFlowResult:
    """
    执行一刀流完整工作流

    参数:
        input_data: 输入数据,可以是:
            - 剧本文件路径 (str/Path)
            - 剧本文本内容 (str)
            - 结构化需求 (Dict)

        config: 可选配置字典,覆盖默认config.yaml
            {
                "project": {...},
                "workflow": {...},
                "agents": {...},
                "aigc": {...},
                "output": {...}
            }

        mode: 执行模式
            - "auto": 全自动执行
            - "manual": 每阶段需确认
            - "hybrid": 关键阶段需确认

    返回:
        OneBladeFlowResult对象:
            .success: bool - 是否成功
            .project_name: str - 项目名称
            .output_paths: Dict - 输出文件路径
                {
                    "csv": Path,
                    "report": Path,
                    "images": List[Path],
                    "videos": List[Path]
                }
            .quality_grade: str - 质量分级 (A/B/C)
            .execution_time: float - 执行时长(秒)
            .metadata: Dict - 元数据

    异常:
        ValueError: 输入数据格式错误
        TimeoutError: 智能体超时
        QualityGateError: 质量门控失败

    示例:
        # 最简单用法
        result = execute_one_blade_flow("project/剧本.md")

        # 带配置
        config = {"aigc": {"enable": False}}
        result = execute_one_blade_flow(
            input_data="我要做一个30秒广告",
            config=config,
            mode="manual"
        )
    """
```

### 辅助函数

```python
def validate_csv(csv_path: Path) -> ValidationResult:
    """验证CSV文件的15字段完整性"""

def generate_report(csv_path: Path, output_path: Path) -> Path:
    """从CSV生成8章节批量整合报告"""

def select_aigc_tools(
    requirements: Dict,
    decision_matrix: Optional[Dict] = None
) -> List[str]:
    """使用EE决策矩阵选择AIGC工具"""

def coordinate_departments(
    csv_data: pd.DataFrame,
    aesthetic_doc: Dict
) -> CoordinationResult:
    """执行跨部门协调检查"""
```

---

## 性能优化 (Performance)

### 优化1: 智能体并行执行

**默认配置**: 最多5个智能体并行
**性能提升**: 3-5倍加速

```yaml
# 优化前: 顺序执行
表演组 (15分钟) → 场景组 (15分钟) → 摄影组 (25分钟) → 制作组 (15分钟)
总计: 70分钟

# 优化后: 组内并行
表演组 (3智能体并行,6分钟) →
场景组 (3智能体并行,6分钟) →
摄影组 (5智能体并行,8分钟) →
制作组 (3智能体并行,6分钟)
总计: 26分钟

加速比: 70 / 26 = 2.69倍
```

### 优化2: 增量更新

**场景**: 修改部分场景后重新生成

```yaml
智能检测:
  - 比较新旧剧本
  - 识别变更场景
  - 只更新变更部分

示例:
  原剧本: 15个场景
  修改: 第3场和第8场

  传统方式: 重新处理所有15个场景
  增量更新: 只处理第3场和第8场

  时间节省: (15-2)/15 = 86.7%
```

### 优化3: 缓存机制

**缓存内容**:

- 美学指导文档 (project_type → aesthetic_doc)
- AIGC决策结果 (requirements → tools_selection)
- 部门输出 (scene_id → department_outputs)

**性能提升**: 重复项目加速50%+

---

## 版本历史 (Changelog)

**v1.0.0** (2025-01-25)

- ✅ 初始版本发布
- ✅ 支持端到端工作流 (剧本 → 分镜脚本CSV)
- ✅ 整合30个智能体 (8个制作组)
- ✅ 双模式架构 (🎨自由模式 + 📊批量模式)
- ✅ 15字段Production-Ready CSV输出
- ✅ AIGC工具集成 (10个工具,EE队长调度)
- ✅ Super-Director整合层 (跨部门协调 + 5维度质量检查)
- ✅ 8章节批量整合报告

**待开发功能** (Roadmap):

- [ ] Web UI界面
- [ ] 实时进度监控
- [ ] 协同编辑支持
- [ ] 云端渲染集成
- [ ] 移动端App

---

## 许可证 (License)

MIT License - 详见项目根目录LICENSE文件

---

## 贡献指南 (Contributing)

欢迎贡献! 请参考项目根目录CONTRIBUTING.md

---

## 联系方式 (Contact)

- 项目主页: [GitHub仓库链接]
- 问题反馈: [Issue Tracker]
- 邮箱: [联系邮箱]

---

**一刀流** - 让影视制作回归创作本身
