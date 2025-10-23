---
name: Deep Research MCP
description: AI驱动的深度研究助手,支持多步骤迭代研究、智能信源聚合、综合报告生成。适用于行业调研、竞品分析、学术研究、市场洞察等需要深度信息挖掘的场景。
---

# Deep Research MCP - AI驱动的深度研究助手

AI-powered comprehensive research assistant for multi-step iterative exploration, intelligent source aggregation, and professional report generation.

---

## Quick Start

### 基础研究流程

```python
# 1. 启动研究任务
research_id = await mcp__deep_research__start_research(
    topic="餐饮行业2024年市场趋势分析",
    depth="comprehensive",  # quick/standard/comprehensive
    sources=["academic", "news", "industry_reports"]
)

# 2. 监控研究进度
status = await mcp__deep_research__get_research_status(
    research_id=research_id
)

# 3. 获取研究报告
report = await mcp__deep_research__get_research_report(
    research_id=research_id,
    format="markdown"  # markdown/pdf/html
)
```

### 迭代深化研究

```python
# 1. 基础研究
base_research = await mcp__deep_research__start_research(
    topic="火锅品类市场分析"
)

# 2. 深化特定子主题
detailed_research = await mcp__deep_research__expand_research(
    parent_research_id=base_research,
    subtopic="海底捞竞争策略分析",
    focus_areas=["定价策略", "服务模式", "扩张路径"]
)

# 3. 对比研究
comparison = await mcp__deep_research__compare_research(
    research_ids=[base_research, detailed_research],
    comparison_dimensions=["市场规模", "增长趋势", "竞争格局"]
)
```

---

## Core Capabilities

### 1. 研究启动与配置

**主要工具**:
- `start_research`: 启动新研究任务
- `configure_research`: 配置研究参数
- `set_research_constraints`: 设置研究约束

**核心参数**:
```python
{
    "topic": "研究主题",
    "depth": "quick|standard|comprehensive|expert",
    "sources": ["academic", "news", "industry_reports", "patents", "social_media"],
    "languages": ["zh", "en", "ja"],
    "time_range": {
        "start": "2023-01-01",
        "end": "2024-12-31"
    },
    "geo_focus": ["China", "Asia", "Global"],
    "output_format": "markdown|pdf|html|json"
}
```

### 2. 智能信源管理

**信源类型**:
- Academic: 学术论文、研究报告
- News: 新闻报道、媒体文章
- Industry Reports: 行业报告、市场分析
- Patents: 专利文献
- Social Media: 社交媒体洞察
- Government Data: 政府公开数据

**信源验证**:
- 自动可信度评分
- 交叉引用验证
- 时效性检查
- 偏见识别

### 3. 多步骤迭代研究

**研究流程**:
```
Step 1: 主题理解与范围界定
  ↓
Step 2: 信源发现与初步筛选
  ↓
Step 3: 深度内容提取与分析
  ↓
Step 4: 跨信源综合与对比
  ↓
Step 5: 洞察提炼与报告生成
  ↓
Step 6: 质量验证与优化
```

### 4. 综合报告生成

**报告结构**:
- Executive Summary (执行摘要)
- Research Methodology (研究方法)
- Key Findings (核心发现)
- Data Analysis (数据分析)
- Trend Insights (趋势洞察)
- Recommendations (建议)
- Source References (信源引用)

**输出格式**:
- Markdown: 易编辑的文本格式
- PDF: 专业排版的文档
- HTML: 可交互的网页报告
- JSON: 结构化数据导出

### 5. 协作研究功能

**工具**:
- `share_research`: 共享研究结果
- `merge_research`: 合并多个研究
- `annotate_research`: 添加注释和评论
- `export_research`: 导出研究数据

---

## Usage Patterns

### Pattern 1: 竞品深度调研

```python
# 场景: 分析竞争对手的全面情况
async def competitor_deep_dive(competitor_name: str):
    # 1. 启动多维度研究
    research_id = await mcp__deep_research__start_research(
        topic=f"{competitor_name}全面分析",
        depth="comprehensive",
        sources=["news", "industry_reports", "social_media", "patents"]
    )

    # 2. 并行深化子主题
    subtopics = [
        "产品策略与创新",
        "市场定位与品牌",
        "财务表现与融资",
        "组织架构与人才",
        "技术专利与研发"
    ]

    subtopic_research = []
    for subtopic in subtopics:
        sub_id = await mcp__deep_research__expand_research(
            parent_research_id=research_id,
            subtopic=f"{competitor_name} - {subtopic}"
        )
        subtopic_research.append(sub_id)

    # 3. 生成综合报告
    final_report = await mcp__deep_research__generate_comprehensive_report(
        research_ids=[research_id] + subtopic_research,
        report_type="competitor_intelligence",
        output_format="pdf"
    )

    return final_report
```

### Pattern 2: 行业趋势追踪

```python
# 场景: 持续追踪行业动态
async def industry_trend_monitoring(industry: str, months: int = 6):
    # 1. 设置时间范围
    time_range = {
        "start": f"-{months}M",  # 相对时间表示
        "end": "now"
    }

    # 2. 启动趋势研究
    trend_id = await mcp__deep_research__start_research(
        topic=f"{industry}行业发展趋势",
        depth="standard",
        sources=["news", "industry_reports"],
        time_range=time_range,
        track_changes=True  # 启用变化追踪
    )

    # 3. 设置关键词监控
    await mcp__deep_research__set_keyword_alerts(
        research_id=trend_id,
        keywords=["新技术", "政策变化", "市场份额", "并购", "融资"]
    )

    # 4. 生成趋势报告
    report = await mcp__deep_research__get_trend_report(
        research_id=trend_id,
        include_predictions=True,
        visualization=True
    )

    return report
```

### Pattern 3: 学术文献综述

```python
# 场景: 快速生成文献综述
async def literature_review(research_question: str):
    # 1. 启动学术研究
    review_id = await mcp__deep_research__start_research(
        topic=research_question,
        depth="expert",
        sources=["academic"],
        min_citation_count=10,  # 最低引用数过滤
        peer_reviewed_only=True
    )

    # 2. 自动分类文献
    categorized = await mcp__deep_research__categorize_sources(
        research_id=review_id,
        categories=["Methodology", "Findings", "Theories", "Applications"]
    )

    # 3. 提取关键洞察
    insights = await mcp__deep_research__extract_key_insights(
        research_id=review_id,
        min_confidence=0.8
    )

    # 4. 生成综述报告
    review = await mcp__deep_research__generate_literature_review(
        research_id=review_id,
        style="academic",
        citation_format="APA"
    )

    return review
```

### Pattern 4: 市场机会识别

```python
# 场景: 发现未开发的市场机会
async def market_opportunity_scanner(industry: str, region: str):
    # 1. 市场全景研究
    market_id = await mcp__deep_research__start_research(
        topic=f"{region}{industry}市场全景",
        depth="comprehensive",
        sources=["industry_reports", "government_data", "news"]
    )

    # 2. 识别市场空白
    gaps = await mcp__deep_research__identify_market_gaps(
        research_id=market_id,
        analysis_dimensions=[
            "未满足需求",
            "竞争强度低",
            "增长潜力高",
            "进入壁垒适中"
        ]
    )

    # 3. 评估机会优先级
    opportunities = await mcp__deep_research__rank_opportunities(
        gap_analysis=gaps,
        criteria={
            "市场规模": 0.3,
            "增长率": 0.25,
            "竞争强度": 0.25,
            "可行性": 0.2
        }
    )

    # 4. 生成机会报告
    report = await mcp__deep_research__generate_opportunity_report(
        opportunities=opportunities,
        include_action_plan=True
    )

    return report
```

---

## Best Practices

### 1. 研究主题设计

**✅ 推荐**:
- 使用清晰、具体的研究问题
- 定义明确的研究范围和边界
- 包含时间维度和地理维度

**示例**:
```python
# ✅ 良好的研究主题
topic = "2023-2024年中国一线城市火锅品类市场竞争格局分析"

# ❌ 过于宽泛
topic = "火锅市场分析"

# ❌ 过于狭窄
topic = "海底捞2024年3月某门店营收分析"
```

### 2. 信源选择策略

**按研究类型选择信源**:

```python
research_configs = {
    "市场调研": {
        "sources": ["industry_reports", "news", "government_data"],
        "depth": "comprehensive"
    },
    "竞品分析": {
        "sources": ["news", "social_media", "patents", "industry_reports"],
        "depth": "comprehensive"
    },
    "学术研究": {
        "sources": ["academic"],
        "depth": "expert",
        "peer_reviewed_only": True
    },
    "趋势预测": {
        "sources": ["news", "social_media", "industry_reports"],
        "depth": "standard",
        "track_changes": True
    }
}
```

### 3. 质量控制

**设置质量门槛**:
```python
quality_config = {
    "min_source_count": 20,           # 最少信源数量
    "min_citation_count": 5,          # 最低引用数
    "max_source_age_days": 365,       # 最大信源年龄
    "require_cross_validation": True, # 要求交叉验证
    "min_confidence_score": 0.7,      # 最低置信度
    "exclude_low_credibility": True   # 排除低可信度信源
}

research_id = await mcp__deep_research__start_research(
    topic="研究主题",
    quality_settings=quality_config
)
```

### 4. 迭代优化

**渐进式深化**:
```python
# Step 1: 快速探索
quick_scan = await mcp__deep_research__start_research(
    topic="新兴餐饮品类机会",
    depth="quick"
)

# Step 2: 评估初步结果
preliminary = await mcp__deep_research__get_preliminary_insights(
    research_id=quick_scan
)

# Step 3: 针对性深化
if "预制菜" in preliminary["high_potential_areas"]:
    detailed = await mcp__deep_research__expand_research(
        parent_research_id=quick_scan,
        subtopic="预制菜市场深度分析",
        depth="comprehensive"
    )
```

### 5. 报告定制

**按受众定制报告**:
```python
# 高管版: 简洁、可视化
executive_report = await mcp__deep_research__get_research_report(
    research_id=research_id,
    format="pdf",
    style="executive",
    max_pages=10,
    visualization_heavy=True
)

# 分析师版: 详细、数据驱动
analyst_report = await mcp__deep_research__get_research_report(
    research_id=research_id,
    format="html",
    style="analytical",
    include_raw_data=True,
    include_methodology=True
)

# 学术版: 严谨、引用完整
academic_report = await mcp__deep_research__get_research_report(
    research_id=research_id,
    format="pdf",
    style="academic",
    citation_format="APA",
    include_appendix=True
)
```

---

## Integration Examples

### 与情报组智能体集成

```python
# E1-公开资料调研员 + Deep Research MCP
async def enhanced_public_research(topic: str):
    """结合E1智能体和Deep Research MCP的增强型调研"""

    # 1. E1提供调研框架
    e1_framework = await call_agent(
        agent="E1-公开资料调研员",
        task=f"为'{topic}'设计调研框架"
    )

    # 2. Deep Research执行深度研究
    research_id = await mcp__deep_research__start_research(
        topic=topic,
        depth="comprehensive",
        research_framework=e1_framework
    )

    # 3. E4深度分析结果
    raw_report = await mcp__deep_research__get_research_report(
        research_id=research_id,
        format="json"
    )

    final_insights = await call_agent(
        agent="E4-深度情报分析员",
        task=f"分析deep-research报告: {raw_report}"
    )

    return final_insights
```

### 与战略组智能体集成

```python
# G4-竞争情报分析师 + Deep Research MCP
async def competitor_intelligence_workflow(competitor: str):
    """竞品情报收集与分析全流程"""

    # 1. Deep Research收集公开情报
    research_id = await mcp__deep_research__start_research(
        topic=f"{competitor}竞争情报分析",
        sources=["news", "industry_reports", "social_media", "patents"]
    )

    # 2. G4分析竞争策略
    intelligence_report = await mcp__deep_research__get_research_report(
        research_id=research_id
    )

    strategic_analysis = await call_agent(
        agent="G4-竞争情报分析师",
        task=f"基于以下情报分析竞争策略: {intelligence_report}"
    )

    # 3. G1提供经营建议
    recommendations = await call_agent(
        agent="G1-经营分析优化师",
        task=f"基于竞品分析提供经营优化建议: {strategic_analysis}"
    )

    return recommendations
```

### 与创意组智能体集成

```python
# X1-广告策划师 + Deep Research MCP
async def data_driven_campaign_planning(campaign_theme: str):
    """数据驱动的广告策划"""

    # 1. Deep Research收集市场洞察
    market_research = await mcp__deep_research__start_research(
        topic=f"{campaign_theme}相关市场趋势与消费者洞察",
        sources=["social_media", "news", "industry_reports"]
    )

    insights = await mcp__deep_research__get_research_report(
        research_id=market_research,
        format="json"
    )

    # 2. X1基于洞察设计策划方案
    campaign_plan = await call_agent(
        agent="X1-广告策划师",
        task=f"基于以下市场洞察设计广告策划: {insights}"
    )

    return campaign_plan
```

---

## Common Issues

### Issue 1: 研究范围过大导致超时

**症状**: 研究任务长时间无响应

**原因**: 研究主题过于宽泛，信源数量过多

**解决方案**:
```python
# ❌ 问题配置
research_id = await mcp__deep_research__start_research(
    topic="全球餐饮行业分析",  # 过于宽泛
    depth="comprehensive",
    sources=["academic", "news", "industry_reports", "patents", "social_media"]
)

# ✅ 优化配置
research_id = await mcp__deep_research__start_research(
    topic="2023-2024年中国一线城市火锅品类市场分析",  # 具体化
    depth="standard",  # 降低深度
    sources=["industry_reports", "news"],  # 精选信源
    max_sources=50,  # 限制信源数量
    time_range={"start": "2023-01-01", "end": "2024-12-31"}
)
```

### Issue 2: 信源质量参差不齐

**症状**: 报告包含低质量或过时信息

**原因**: 未设置质量过滤

**解决方案**:
```python
research_id = await mcp__deep_research__start_research(
    topic="市场趋势分析",
    quality_settings={
        "min_source_credibility": 0.7,      # 最低可信度
        "max_source_age_days": 180,         # 最多6个月前
        "require_cross_validation": True,   # 要求交叉验证
        "exclude_duplicate_content": True   # 排除重复内容
    }
)
```

### Issue 3: 报告格式不符合预期

**症状**: 生成的报告结构混乱

**原因**: 未指定报告模板

**解决方案**:
```python
report = await mcp__deep_research__get_research_report(
    research_id=research_id,
    format="markdown",
    template={
        "sections": [
            "Executive Summary",
            "Methodology",
            "Key Findings",
            "Data Analysis",
            "Recommendations",
            "References"
        ],
        "max_section_length": 500,  # 每节最大字数
        "include_visualizations": True,
        "citation_style": "numbered"
    }
)
```

### Issue 4: 多语言研究混乱

**症状**: 中英文信源混杂，报告语言不统一

**解决方案**:
```python
# 方案1: 单一语言研究
research_id = await mcp__deep_research__start_research(
    topic="中国餐饮市场分析",
    languages=["zh"],  # 仅中文信源
    output_language="zh"  # 中文报告
)

# 方案2: 多语言分离研究
zh_research = await mcp__deep_research__start_research(
    topic="中国市场",
    languages=["zh"]
)

en_research = await mcp__deep_research__start_research(
    topic="Global market",
    languages=["en"]
)

# 合并时保持语言分离
merged = await mcp__deep_research__merge_research(
    research_ids=[zh_research, en_research],
    keep_languages_separate=True
)
```

---

## Tips & Tricks

### Tip 1: 使用研究模板加速流程

```python
# 创建可复用的研究模板
competitor_analysis_template = {
    "depth": "comprehensive",
    "sources": ["news", "industry_reports", "social_media", "patents"],
    "subtopics": [
        "产品策略",
        "市场定位",
        "财务表现",
        "技术创新",
        "组织架构"
    ],
    "quality_settings": {
        "min_source_count": 20,
        "require_cross_validation": True
    }
}

# 快速启动标准化研究
research_id = await mcp__deep_research__start_research(
    topic="竞品X分析",
    template=competitor_analysis_template
)
```

### Tip 2: 批量研究与对比

```python
# 批量研究多个竞品
competitors = ["海底捞", "呷哺呷哺", "小龙坎"]

research_tasks = []
for competitor in competitors:
    task = mcp__deep_research__start_research(
        topic=f"{competitor}竞品分析",
        template=competitor_analysis_template
    )
    research_tasks.append(task)

# 并行执行
research_ids = await asyncio.gather(*research_tasks)

# 生成对比报告
comparison = await mcp__deep_research__compare_research(
    research_ids=research_ids,
    comparison_dimensions=[
        "市场份额",
        "增长率",
        "创新能力",
        "品牌影响力",
        "盈利能力"
    ],
    output_format="html"
)
```

### Tip 3: 设置研究监控和告警

```python
# 启动长期研究监控
monitor_id = await mcp__deep_research__start_research(
    topic="餐饮行业监控",
    depth="standard",
    continuous_monitoring=True  # 持续监控模式
)

# 设置关键事件告警
await mcp__deep_research__set_alerts(
    research_id=monitor_id,
    alert_rules=[
        {
            "type": "keyword_mention",
            "keywords": ["并购", "融资", "政策变化"],
            "threshold": "high_impact"
        },
        {
            "type": "trend_change",
            "metrics": ["市场份额", "增长率"],
            "change_threshold": 0.1  # 10%变化
        },
        {
            "type": "new_competitor",
            "market_segment": "火锅品类"
        }
    ],
    notification_channels=["email", "webhook"]
)
```

### Tip 4: 导出可重用的研究数据

```python
# 导出结构化研究数据
research_data = await mcp__deep_research__export_research(
    research_id=research_id,
    export_format="json",
    include_raw_sources=True,
    include_metadata=True
)

# 保存到本地数据库
await supabase_mcp.insert(
    table="research_repository",
    data={
        "research_id": research_id,
        "topic": "市场分析",
        "data": research_data,
        "created_at": datetime.now()
    }
)

# 未来研究可引用历史数据
new_research = await mcp__deep_research__start_research(
    topic="2025市场预测",
    reference_research_ids=[research_id]  # 引用历史研究
)
```

### Tip 5: 自定义信源过滤器

```python
# 创建自定义信源过滤逻辑
custom_filters = {
    "source_filters": [
        {
            "type": "domain_whitelist",
            "domains": [
                "36kr.com",
                "chyxx.com",
                "iimedia.cn",
                "199it.com"
            ]
        },
        {
            "type": "exclude_keywords",
            "keywords": ["广告", "软文", "推广"]
        },
        {
            "type": "author_reputation",
            "min_score": 0.7
        }
    ]
}

research_id = await mcp__deep_research__start_research(
    topic="行业分析",
    custom_filters=custom_filters
)
```

---

## Advanced Features

### 1. AI驱动的研究路径规划

Deep Research MCP能够自主规划最优研究路径:

```python
research_id = await mcp__deep_research__start_research(
    topic="未来餐饮趋势",
    autonomous_planning=True,  # 启用自主规划
    planning_config={
        "exploration_breadth": 0.7,   # 探索广度
        "exploration_depth": 0.8,     # 探索深度
        "adaptivity": "high",         # 自适应级别
        "quality_vs_speed": 0.6       # 质量-速度平衡
    }
)

# 查看AI规划的研究路径
plan = await mcp__deep_research__get_research_plan(
    research_id=research_id
)
print(plan["planned_steps"])
```

### 2. 实时协作研究

```python
# 启动协作研究会话
session_id = await mcp__deep_research__start_collaborative_session(
    topic="新品类机会分析",
    participants=["analyst_1", "analyst_2", "strategist"]
)

# 实时添加研究线索
await mcp__deep_research__add_research_thread(
    session_id=session_id,
    thread_topic="预制菜市场潜力",
    assigned_to="analyst_1"
)

# 共享中间发现
await mcp__deep_research__share_finding(
    session_id=session_id,
    finding="市场规模预计达500亿",
    evidence_sources=[...]
)

# 生成协作报告
final_report = await mcp__deep_research__generate_collaborative_report(
    session_id=session_id
)
```

### 3. 预测性研究

```python
# 基于历史数据进行预测研究
prediction = await mcp__deep_research__predictive_research(
    topic="2025年餐饮行业趋势",
    historical_data_range="2020-2024",
    prediction_models=[
        "time_series_analysis",
        "trend_extrapolation",
        "pattern_recognition"
    ],
    confidence_level=0.8
)

# 获取预测报告
forecast_report = await mcp__deep_research__get_prediction_report(
    prediction_id=prediction,
    include_scenarios=True,      # 包含多种情景
    include_risk_analysis=True   # 包含风险分析
)
```

---

## Performance Optimization

### 缓存策略

```python
# 启用智能缓存
await mcp__deep_research__configure_cache(
    cache_strategy="intelligent",
    cache_duration_hours=24,
    cache_similar_queries=True,
    similarity_threshold=0.85
)

# 复用缓存研究
research_id = await mcp__deep_research__start_research(
    topic="火锅市场分析",
    use_cache=True,
    cache_freshness="1d"  # 1天内的缓存可用
)
```

### 并行处理

```python
# 配置并行处理
await mcp__deep_research__configure_parallelism(
    max_concurrent_sources=10,
    max_concurrent_subtopics=5,
    enable_distributed_processing=True
)
```

---

**适用场景**: 行业调研、竞品分析、学术研究、市场洞察、趋势预测、机会识别

**集成智能体**: E1(公开调研)、E4(深度分析)、G4(竞争情报)、X1(广告策划)

**输出目录**: `output/情报组/deep-research/`、`reports/research/`
