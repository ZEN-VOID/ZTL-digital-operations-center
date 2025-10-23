---
name: chart-generator-mcp
description: Professional chart and data visualization generation with 15+ chart types (bar, line, pie, scatter, heatmap, radar, etc.). Supports multiple export formats (PNG, SVG, HTML) and advanced customization. Use for data analysis reports, business dashboards, statistical visualization, and trend analysis.
---

# Chart-Generator-MCP Skill

基于chart-generator-mcp的专业图表生成能力包，提供15+图表类型、多种导出格式和高级自定义选项，适用于数据分析报告、商业仪表盘、统计可视化等场景。

## Quick Start

### 基础柱状图

```python
# 创建简单柱状图
await chart_generator_create_chart({
    "type": "bar",
    "data": {
        "labels": ["Q1", "Q2", "Q3", "Q4"],
        "datasets": [{
            "label": "2025年销售额",
            "data": [120, 190, 150, 220]
        }]
    },
    "options": {
        "title": {"text": "季度销售趋势"},
        "format": "png",
        "filename": "quarterly_sales"
    }
})
```

### 折线图（趋势分析）

```python
# 创建多系列折线图
await chart_generator_create_chart({
    "type": "line",
    "data": {
        "labels": ["1月", "2月", "3月", "4月", "5月", "6月"],
        "datasets": [
            {
                "label": "本年",
                "data": [65, 78, 90, 81, 95, 105],
                "borderColor": "rgb(75, 192, 192)"
            },
            {
                "label": "去年",
                "data": [55, 69, 78, 75, 82, 88],
                "borderColor": "rgb(255, 99, 132)"
            }
        ]
    },
    "options": {
        "title": {"text": "营收同比趋势"},
        "format": "svg"
    }
})
```

### 饼图（占比分析）

```python
# 创建饼图
await chart_generator_create_chart({
    "type": "pie",
    "data": {
        "labels": ["华北", "华东", "华南", "西部"],
        "datasets": [{
            "data": [35, 40, 15, 10],
            "backgroundColor": [
                "rgb(255, 99, 132)",
                "rgb(54, 162, 235)",
                "rgb(255, 205, 86)",
                "rgb(75, 192, 192)"
            ]
        }]
    },
    "options": {
        "title": {"text": "区域销售占比"},
        "format": "png"
    }
})
```

## Core Capabilities

### 1. 图表类型矩阵

#### 基础图表类型

| 图表类型 | 英文名 | 适用场景 | 关键特性 |
|---------|--------|---------|---------|
| 柱状图 | bar | 分类对比、时间序列 | 垂直/水平、堆叠/分组 |
| 折线图 | line | 趋势分析、连续数据 | 多系列、曲线平滑 |
| 饼图 | pie | 占比分析、部分与整体 | 百分比标签、环形变体 |
| 散点图 | scatter | 相关性分析、分布研究 | 气泡大小、颜色编码 |
| 雷达图 | radar | 多维评估、性能对比 | 多边形填充、多系列 |
| 热力图 | heatmap | 矩阵数据、密度分析 | 颜色渐变、数值标注 |

#### 高级图表类型

| 图表类型 | 英文名 | 适用场景 | 关键特性 |
|---------|--------|---------|---------|
| 箱线图 | boxplot | 统计分析、离群值检测 | 四分位数、异常值 |
| 漏斗图 | funnel | 转化分析、流程监控 | 阶段转化率、颜色分段 |
| 瀑布图 | waterfall | 累计变化、增减分析 | 正负值、累计总和 |
| 甘特图 | gantt | 项目管理、时间规划 | 时间线、任务依赖 |
| 桑基图 | sankey | 流量分析、能量流转 | 节点连接、流量粗细 |
| 树状图 | treemap | 层级数据、占比可视化 | 嵌套矩形、颜色映射 |

### 2. 导出格式支持

```python
# PNG格式（默认，高质量位图）
await chart_generator_create_chart({
    "type": "bar",
    "data": {...},
    "options": {
        "format": "png",
        "width": 1920,
        "height": 1080,
        "dpi": 300  # 高分辨率
    }
})

# SVG格式（矢量图，可缩放）
await chart_generator_create_chart({
    "type": "line",
    "data": {...},
    "options": {
        "format": "svg"
    }
})

# HTML格式（交互式）
await chart_generator_create_chart({
    "type": "scatter",
    "data": {...},
    "options": {
        "format": "html",
        "interactive": True  # 支持缩放、tooltip
    }
})
```

### 3. 高级样式定制

#### 颜色主题

```python
# 使用预设主题
"options": {
    "theme": "professional",  # professional | vibrant | pastel | dark
    "colorScheme": "blue"     # blue | red | green | purple
}

# 自定义颜色
"datasets": [{
    "backgroundColor": ["#FF6384", "#36A2EB", "#FFCE56"],
    "borderColor": "rgb(75, 192, 192)",
    "borderWidth": 2
}]
```

#### 标题与标签

```python
"options": {
    "title": {
        "text": "2025年度销售报表",
        "fontSize": 24,
        "fontWeight": "bold",
        "color": "#333"
    },
    "legend": {
        "position": "top",  # top | bottom | left | right
        "align": "center"
    },
    "axes": {
        "xAxis": {"title": "月份"},
        "yAxis": {"title": "销售额（万元）"}
    }
}
```

#### 数据标签

```python
"options": {
    "dataLabels": {
        "enabled": True,
        "position": "top",  # top | center | bottom
        "format": "{value}万",
        "fontSize": 12,
        "color": "#666"
    }
}
```

### 4. 响应式设计

```python
# 移动端优化
"options": {
    "responsive": True,
    "maintainAspectRatio": True,
    "aspectRatio": 16/9,
    "breakpoints": {
        "mobile": {"width": 375, "fontSize": 10},
        "tablet": {"width": 768, "fontSize": 12},
        "desktop": {"width": 1920, "fontSize": 14}
    }
}
```

## Usage Patterns

### Pattern 1: 数据分析报告生成

```python
async def generate_analysis_report(data: dict):
    """生成包含多个图表的分析报告"""

    charts = []

    # 1. 趋势分析（折线图）
    trend_chart = await chart_generator_create_chart({
        "type": "line",
        "data": {
            "labels": data['months'],
            "datasets": [{
                "label": "月度趋势",
                "data": data['monthly_values']
            }]
        },
        "options": {
            "title": {"text": "营收趋势分析"},
            "format": "png",
            "filename": "trend_analysis"
        }
    })
    charts.append(trend_chart)

    # 2. 分类对比（柱状图）
    comparison_chart = await chart_generator_create_chart({
        "type": "bar",
        "data": {
            "labels": data['categories'],
            "datasets": [{
                "label": "分类数据",
                "data": data['category_values']
            }]
        },
        "options": {
            "title": {"text": "分类对比"},
            "format": "png",
            "filename": "category_comparison"
        }
    })
    charts.append(comparison_chart)

    # 3. 占比分析（饼图）
    proportion_chart = await chart_generator_create_chart({
        "type": "pie",
        "data": {
            "labels": data['segments'],
            "datasets": [{
                "data": data['segment_values']
            }]
        },
        "options": {
            "title": {"text": "市场份额"},
            "format": "png",
            "filename": "market_share"
        }
    })
    charts.append(proportion_chart)

    return {
        "report_id": generate_id(),
        "charts": charts,
        "generated_at": datetime.now()
    }
```

### Pattern 2: 动态仪表盘

```python
async def create_dashboard(metrics: dict):
    """创建实时更新的仪表盘"""

    dashboard_charts = []

    # KPI指标卡（数字）
    kpi_chart = await chart_generator_create_chart({
        "type": "metric",
        "data": {
            "value": metrics['revenue'],
            "label": "当月营收",
            "unit": "万元",
            "change": "+12.5%",
            "trend": "up"
        },
        "options": {
            "format": "html",
            "interactive": True
        }
    })

    # 实时趋势（折线图）
    realtime_chart = await chart_generator_create_chart({
        "type": "line",
        "data": {
            "labels": metrics['hourly_labels'],
            "datasets": [{
                "label": "实时流量",
                "data": metrics['hourly_traffic']
            }]
        },
        "options": {
            "format": "html",
            "realtime": True,
            "updateInterval": 60000  # 每分钟更新
        }
    })

    return {
        "dashboard_id": generate_id(),
        "charts": dashboard_charts,
        "refresh_rate": 60
    }
```

### Pattern 3: 对比分析

```python
async def create_comparison_analysis(current_data, previous_data):
    """创建同比/环比对比分析"""

    # 多系列对比
    comparison = await chart_generator_create_chart({
        "type": "bar",
        "data": {
            "labels": ["Q1", "Q2", "Q3", "Q4"],
            "datasets": [
                {
                    "label": "本年",
                    "data": current_data,
                    "backgroundColor": "rgba(54, 162, 235, 0.8)"
                },
                {
                    "label": "去年",
                    "data": previous_data,
                    "backgroundColor": "rgba(255, 99, 132, 0.8)"
                }
            ]
        },
        "options": {
            "title": {"text": "年度对比分析"},
            "grouped": True,  # 分组显示
            "format": "png"
        }
    })

    # 计算增长率
    growth_rates = [
        ((c - p) / p * 100) for c, p in zip(current_data, previous_data)
    ]

    # 增长率折线图
    growth_chart = await chart_generator_create_chart({
        "type": "line",
        "data": {
            "labels": ["Q1", "Q2", "Q3", "Q4"],
            "datasets": [{
                "label": "增长率(%)",
                "data": growth_rates
            }]
        },
        "options": {
            "title": {"text": "增长率趋势"},
            "format": "png"
        }
    })

    return {
        "comparison_chart": comparison,
        "growth_chart": growth_chart,
        "average_growth": sum(growth_rates) / len(growth_rates)
    }
```

### Pattern 4: 统计分析可视化

```python
async def create_statistical_visualization(data: list):
    """创建统计分析图表集"""

    # 1. 分布直方图
    histogram = await chart_generator_create_chart({
        "type": "histogram",
        "data": {
            "values": data,
            "bins": 10
        },
        "options": {
            "title": {"text": "数据分布"},
            "format": "png"
        }
    })

    # 2. 箱线图（显示离群值）
    boxplot = await chart_generator_create_chart({
        "type": "boxplot",
        "data": {
            "values": data
        },
        "options": {
            "title": {"text": "统计特征"},
            "showOutliers": True,
            "format": "png"
        }
    })

    # 3. 小提琴图（密度+箱线）
    violin = await chart_generator_create_chart({
        "type": "violin",
        "data": {
            "values": data
        },
        "options": {
            "title": {"text": "密度分布"},
            "format": "png"
        }
    })

    return {
        "histogram": histogram,
        "boxplot": boxplot,
        "violin": violin,
        "statistics": {
            "mean": sum(data) / len(data),
            "median": sorted(data)[len(data) // 2],
            "std": calculate_std(data)
        }
    }
```

### Pattern 5: 地理数据可视化

```python
async def create_geographic_visualization(location_data: dict):
    """创建地理热力图"""

    # 地理热力图
    heatmap = await chart_generator_create_chart({
        "type": "heatmap",
        "data": {
            "locations": location_data['coordinates'],
            "values": location_data['metrics']
        },
        "options": {
            "title": {"text": "区域销售热力图"},
            "map": {
                "center": {"lat": 39.9, "lng": 116.4},
                "zoom": 5
            },
            "colorScale": "hot",
            "format": "html",
            "interactive": True
        }
    })

    return heatmap
```

## Best Practices

### 1. 数据准备

```python
# ✓ 推荐：清洗和验证数据
def prepare_chart_data(raw_data):
    # 1. 移除空值
    clean_data = [x for x in raw_data if x is not None]

    # 2. 数据类型转换
    numeric_data = [float(x) for x in clean_data]

    # 3. 异常值处理
    filtered_data = filter_outliers(numeric_data)

    return filtered_data

# ✗ 避免：直接使用未处理的数据
await chart_generator_create_chart({
    "data": raw_data  # 可能包含空值、异常值
})
```

### 2. 颜色选择

```python
# ✓ 推荐：使用色盲友好的配色方案
color_schemes = {
    "colorblind_safe": [
        "#0173B2", "#DE8F05", "#029E73", "#CC78BC",
        "#CA9161", "#949494", "#ECE133", "#56B4E9"
    ]
}

# ✓ 推荐：保持品牌一致性
brand_colors = {
    "primary": "#1E88E5",
    "secondary": "#43A047",
    "accent": "#FFA726"
}

# ✗ 避免：使用过于鲜艳或对比度低的颜色
bad_colors = ["#FF00FF", "#00FFFF", "#FFFF00"]  # 过于刺眼
```

### 3. 图表类型选择

```python
# ✓ 正确的图表类型选择
visualization_guide = {
    "趋势分析": "line",        # 折线图显示趋势
    "分类对比": "bar",         # 柱状图对比数值
    "占比分析": "pie",         # 饼图显示占比
    "相关性": "scatter",       # 散点图显示相关性
    "分布": "histogram",       # 直方图显示分布
    "时间序列": "line",        # 折线图显示时序
    "层级关系": "treemap"      # 树状图显示层级
}

# ✗ 避免：使用不合适的图表类型
# 不要用饼图显示超过6个分类
# 不要用折线图显示离散分类数据
```

### 4. 性能优化

```python
# ✓ 推荐：数据采样（大数据集）
if len(data) > 10000:
    sampled_data = sample_data(data, target_size=5000)
else:
    sampled_data = data

# ✓ 推荐：异步批量生成
async def batch_generate_charts(chart_configs: list):
    tasks = [
        chart_generator_create_chart(config)
        for config in chart_configs
    ]
    return await asyncio.gather(*tasks)

# ✗ 避免：同步生成大量图表
for config in chart_configs:
    await chart_generator_create_chart(config)  # 串行，慢
```

### 5. 文件管理

```python
# ✓ 推荐：组织化的文件命名和路径
output_structure = {
    "reports": "output/情报组/reports/{date}/",
    "charts": "output/情报组/charts/{report_id}/",
    "naming": "{chart_type}_{metric}_{timestamp}.png"
}

# 示例
filename = f"line_revenue_trend_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
filepath = f"output/情报组/charts/{report_id}/{filename}"

# ✗ 避免：混乱的文件命名
filename = "chart1.png"  # 无法识别内容
```

## Common Issues

### Issue 1: 数据标签重叠

**原因**: 数据点过多或标签过长

**解决方案**:
```python
# 方案1：旋转标签
"options": {
    "axes": {
        "xAxis": {
            "labels": {
                "rotation": 45,
                "align": "right"
            }
        }
    }
}

# 方案2：隐藏部分标签
"options": {
    "axes": {
        "xAxis": {
            "labels": {
                "maxTicksLimit": 10,
                "autoSkip": True
            }
        }
    }
}
```

### Issue 2: 图表尺寸不合适

**原因**: 默认尺寸不适配输出场景

**解决方案**:
```python
# 报告场景（A4纸）
report_size = {
    "width": 2480,   # 210mm * 300dpi / 25.4
    "height": 3508,  # 297mm * 300dpi / 25.4
    "dpi": 300
}

# 演示场景（16:9）
presentation_size = {
    "width": 1920,
    "height": 1080,
    "dpi": 150
}

# 移动场景
mobile_size = {
    "width": 750,
    "height": 1334,
    "dpi": 72
}
```

### Issue 3: 颜色对比度不足

**原因**: 配色方案不当

**解决方案**:
```python
# 检查对比度
def check_contrast_ratio(foreground, background):
    # WCAG 2.0 标准：4.5:1（AA级）或 7:1（AAA级）
    ratio = calculate_contrast(foreground, background)
    return ratio >= 4.5

# 使用高对比度配色
high_contrast_theme = {
    "background": "#FFFFFF",
    "text": "#000000",
    "primary": "#0066CC",
    "secondary": "#FF6600"
}
```

## Integration Examples

### Example 1: 与Office Skills集成（报告生成）

```python
# 1. 生成图表
chart = await chart_generator_create_chart({
    "type": "bar",
    "data": analysis_data,
    "options": {"format": "png", "filename": "sales_chart"}
})

# 2. 插入Word报告
await word_insert_image(
    doc_path="analysis_report.docx",
    image_path=chart['filepath'],
    width=6.0,  # 英寸
    caption="图1：季度销售分析"
)

# 3. 插入Excel工作表
await excel_insert_chart(
    workbook="data.xlsx",
    sheet="Dashboard",
    chart_data=chart,
    position="B2"
)
```

### Example 2: 与Lark-MCP集成（自动推送）

```python
# 生成图表并推送到飞书
chart = await chart_generator_create_chart({
    "type": "line",
    "data": daily_metrics,
    "options": {"format": "png"}
})

# 上传到飞书
await lark_upload_image(
    image_path=chart['filepath'],
    chat_id="oc_xxx"
)

# 发送消息
await lark_send_message(
    chat_id="oc_xxx",
    message=f"📊 今日数据报表\n\n关键指标：...",
    image_key=uploaded_image_key
)
```

### Example 3: 与COS-MCP集成（云存储）

```python
# 生成图表
chart = await chart_generator_create_chart({
    "type": "heatmap",
    "data": geographic_data,
    "options": {"format": "svg"}
})

# 上传到COS
cos_url = await cos_upload_file(
    file_path=chart['filepath'],
    target_dir="charts/geographic/",
    public_read=True
)

# 生成CDN加速链接
cdn_url = await cos_get_cdn_url(cos_url)

return {
    "chart_url": cdn_url,
    "chart_type": "heatmap",
    "generated_at": datetime.now()
}
```

## Tips & Tricks

1. **数据精度**: 控制小数位数（0-2位），避免过度精确
2. **颜色数量**: 单个图表颜色不超过7种，避免视觉混乱
3. **标题简洁**: 标题不超过15个字，突出核心信息
4. **图例位置**: 数据系列≤3个时放顶部，>3个时放右侧
5. **网格线**: 使用浅灰色网格线（#E0E0E0），增强可读性
6. **数据标签**: 仅在数据点<10个时显示，避免拥挤
7. **响应式**: 移动端优先，确保小屏幕可读性
8. **导出格式**: 报告用PNG（300dpi），网页用SVG
9. **批量生成**: 使用异步并发，提升生成效率
10. **缓存策略**: 相同配置的图表使用缓存，避免重复生成

## Chart-Generator-MCP Tools Reference

### 核心工具列表

| 工具名称 | 功能描述 | 参数 |
|---------|---------|------|
| `create_chart` | 创建图表 | type, data, options |
| `update_chart` | 更新已有图表 | chart_id, data, options |
| `delete_chart` | 删除图表 | chart_id |
| `list_charts` | 列出所有图表 | filter, sort |
| `export_chart` | 导出图表 | chart_id, format, quality |

详见[Chart-Generator-MCP工具参考](reference.md)（待补充）

## Version History

- **v1.0.0** (2025-10-23): 初始版本
  - 15+图表类型支持
  - 多格式导出（PNG/SVG/HTML）
  - 高级样式定制
  - 响应式设计
  - 与其他Skills集成示例
