# Word技能包输出路径配置说明

## 概述

Word技能包遵循统一的输出路径规范，与Word和PDF技能包保持一致，便于文件管理和跨智能体协作。

---

## 输出路径规范

### 标准路径格式

所有Word文件统一输出到：

```
output/行政组/[项目名]/
```

**[项目名]** 根据实际业务场景灵活命名，可以是：
- 具体项目名称（如：`ZTL品牌升级2025`、`秋季新品发布`）
- 业务主题（如：`Q3经营分析`、`员工培训计划`）
- 客户名称（如：`海底捞合作方案`、`万达广场提案`）
- 活动名称（如：`双十一营销活动`、`年会策划`）

### 路径示例

```yaml
# 项目型
output/行政组/ZTL品牌升级2025/brand-presentation.docx
output/行政组/秋季新品发布/product-launch.docx
output/行政组/总部办公室装修/renovation-plan.docx

# 业务型
output/行政组/Q3经营分析/quarterly-report.docx
output/行政组/员工培训计划/training-course.docx
output/行政组/年度战略规划/strategy-2026.docx

# 客户型
output/行政组/海底捞合作方案/partnership-proposal.docx
output/行政组/万达广场提案/mall-restaurant-pitch.docx

# 活动型
output/行政组/双十一营销活动/campaign-deck.docx
output/行政组/2025年会策划/annual-meeting-plan.docx
```

---

## 使用示例

### 方法1：直接生成

```python
from word_generator import WordGenerator

generator = WordGenerator()

# 项目名称：品牌升级项目
generator.add_title_slide("品牌宣传", "ZTL数智化平台")
generator.save("output/行政组/品牌升级项目/brand-presentation.docx")

# 项目名称：Q3分析报告
generator.add_content_slide("业绩总结", ["营收增长25%", "新店3家"])
generator.save("output/行政组/Q3分析报告/quarterly-analysis.docx")

# 项目名称：新员工培训
generator.add_title_slide("欢迎加入ZTL", "新员工入职培训")
generator.save("output/行政组/新员工培训/onboarding-training.docx")
```

### 方法2：HTML转换

```python
from html_to_word_converter import convert_html_to_word

# 项目名称：技术架构文档
convert_html_to_word(
    html_content=tech_html,
    output_path="output/行政组/技术架构文档/architecture-guide.docx"
)

# 项目名称：新品发布会
convert_html_to_word(
    html_content=product_html,
    output_path="output/行政组/新品发布会/product-launch-deck.docx"
)
```

### 方法3：模板生成

```python
from word_generator import create_from_template

# 业务报告模板 - 项目名称：2025Q3业绩汇报
result = create_from_template(
    template_type="business-report",
    data=report_data,
    output_path="output/行政组/2025Q3业绩汇报/quarterly-report.docx"
)

# 产品发布模板 - 项目名称：秋季菜单更新
result = create_from_template(
    template_type="product-launch",
    data=launch_data,
    output_path="output/行政组/秋季菜单更新/menu-launch.docx"
)

# 培训模板 - 项目名称：服务技能提升培训
result = create_from_template(
    template_type="training",
    data=training_data,
    output_path="output/行政组/服务技能提升培训/service-training.docx"
)

# 路演模板 - 项目名称：B轮融资路演
result = create_from_template(
    template_type="pitch",
    data=pitch_data,
    output_path="output/行政组/B轮融资路演/series-b-pitch.docx"
)
```

---

## 跨智能体使用指南

### R1-财务管理员

```python
from word_generator import create_from_template

# 项目名称：2025财务规划
result = create_from_template(
    template_type="business-report",
    data=financial_data,
    output_path="output/行政组/2025财务规划/financial-plan.docx"
)

# 项目名称：成本控制方案
generator = WordGenerator()
generator.add_title_slide("成本优化策略", "2025年度计划")
generator.save("output/行政组/成本控制方案/cost-control-strategy.docx")
```

### R2-人事管理员

```python
# 项目名称：校招宣讲2025
result = create_from_template(
    template_type="training",
    data=recruitment_data,
    output_path="output/行政组/校招宣讲2025/campus-recruitment.docx"
)

# 项目名称：员工手册更新
generator = WordGenerator()
generator.add_title_slide("员工手册", "2025版")
generator.save("output/行政组/员工手册更新/employee-handbook.docx")
```

### R4-秘书

```python
# 项目名称：董事会会议20251021
generator = WordGenerator()
generator.add_title_slide("董事会会议", "2025年Q4战略讨论")
generator.save("output/行政组/董事会会议20251021/board-meeting.docx")

# 项目名称：月度工作汇报202510
result = create_from_template(
    template_type="business-report",
    data=work_summary,
    output_path="output/行政组/月度工作汇报202510/monthly-summary.docx"
)
```

### G1-经营分析优化师

```python
# 项目名称：10月经营数据分析
generator = WordGenerator()
generator.add_chart_slide(
    title="月度营业额趋势",
    chart_type="line",
    data=revenue_data
)
generator.save("output/行政组/10月经营数据分析/monthly-analysis.docx")
```

### X1-广告策划师

```python
# 项目名称：双十一营销策划
result = create_from_template(
    template_type="product-launch",
    data=campaign_data,
    output_path="output/行政组/双十一营销策划/double-11-campaign.docx"
)

# 项目名称：品牌故事2025
generator = WordGenerator()
generator.add_title_slide("ZTL品牌故事", "用心服务每一位顾客")
generator.save("output/行政组/品牌故事2025/brand-story.docx")
```

### GG-战略规划总监

```python
# 项目名称：三年战略规划2025-2027
result = create_from_template(
    template_type="business-report",
    data=strategy_data,
    output_path="output/行政组/三年战略规划2025-2027/strategy-plan.docx"
)

# 项目名称：B轮融资准备
result = create_from_template(
    template_type="pitch",
    data=pitch_data,
    output_path="output/行政组/B轮融资准备/series-b-pitch.docx"
)
```

---

## 路径命名最佳实践

### 1. 项目名称命名建议

```python
# ✅ 推荐：清晰、具体、易识别
output_path = "output/行政组/2025品牌升级项目/brand-upgrade.docx"
output_path = "output/行政组/Q3经营分析/quarterly-report.docx"
output_path = "output/行政组/新员工入职培训/onboarding.docx"

# ✅ 包含时间标识
output_path = "output/行政组/2025秋季新品发布/autumn-menu.docx"
output_path = "output/行政组/月度会议202510/monthly-meeting.docx"

# ❌ 不推荐：过于笼统
output_path = "output/行政组/项目1/file.docx"
output_path = "output/行政组/文档/presentation.docx"
```

### 2. 文件命名规范

```python
from datetime import datetime

# 包含日期的文件名
timestamp = datetime.now().strftime("%Y%m%d")
output_path = f"output/行政组/Q3经营分析/monthly-report-{timestamp}.docx"
# 结果: output/行政组/Q3经营分析/monthly-report-20251021.docx

# 包含版本号
output_path = "output/行政组/品牌升级项目/brand-presentation-v2.docx"

# 描述性命名
output_path = "output/行政组/新员工培训/sales-training-basic.docx"
```

### 3. 自动化路径生成

```python
from datetime import datetime
from pathlib import Path

def generate_word_path(
    project_name: str,
    filename: str,
    add_timestamp: bool = False
) -> str:
    """生成标准化的Word文档输出路径

    Args:
        project_name: 项目名称（根据业务场景命名）
        filename: 文件名
        add_timestamp: 是否添加时间戳

    Returns:
        标准化的输出路径
    """
    # 安全化文件名
    safe_filename = "".join(
        c for c in filename
        if c.isalnum() or c in (' ', '-', '_', '.')
    )
    safe_filename = safe_filename.replace(' ', '-').strip()

    # 确保.docx扩展名
    if not safe_filename.endswith('.docx'):
        if '.' in safe_filename:
            safe_filename = safe_filename.rsplit('.', 1)[0] + '.docx'
        else:
            safe_filename += '.docx'

    # 可选添加时间戳
    if add_timestamp:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = safe_filename.rsplit('.', 1)[0]
        safe_filename = f"{base_name}_{timestamp}.docx"

    return f"output/行政组/{project_name}/{safe_filename}"

# 使用示例
path = generate_word_path("品牌升级项目", "品牌介绍", add_timestamp=True)
# 结果: output/行政组/品牌升级项目/品牌介绍_20251021_143000.docx
```

---

## 注意事项

### 1. 目录自动创建

所有路径中的目录会自动创建，无需手动操作：

```python
# 即使 output/行政组/新项目名称/ 不存在，也会自动创建
generator.save("output/行政组/新项目名称/presentation.docx")
```

### 2. 中文路径支持

完全支持中文路径和文件名：

```python
# ✅ 支持中文项目名和文件名
output_path = "output/行政组/2025年品牌升级/品牌宣传Word.docx"

# ✅ 也支持英文
output_path = "output/行政组/Brand-Upgrade-2025/brand-presentation.docx"

# ✅ 中英混合
output_path = "output/行政组/品牌升级Brand-2025/presentation-v1.docx"
```

### 3. 文件覆盖警告

如果文件已存在，将会覆盖：

```python
# 建议使用时间戳避免覆盖
from datetime import datetime
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_path = f"output/行政组/经营分析报告/report_{timestamp}.docx"
```

### 4. 项目名称建议

- **具体明确**: 避免使用"文档"、"资料"等过于笼统的名称
- **包含时间**: 对于周期性项目，建议包含年份或月份
- **易于识别**: 项目名称应能清晰表达内容主题
- **避免特殊字符**: 不要使用 `/`、`\`、`:`、`*`、`?`、`"`、`<`、`>`、`|` 等字符

---

## 与Word和PDF的统一

Word、Word、PDF技能包使用相同的输出路径规范：

```python
# 同一项目的不同格式文档
word_path = "output/行政组/Q3经营分析/quarterly-report.docx"   # Word演示
word_path = "output/行政组/Q3经营分析/quarterly-report.docx"  # Word详细报告
pdf_path = "output/行政组/Q3经营分析/quarterly-report.pdf"    # PDF分发版本

# 便于管理同一份内容的不同格式
```

---

## 常见场景示例

### 场景1：季度业务汇报

```python
project_name = "2025Q3业务汇报"

generator = WordGenerator()
generator.add_title_slide("Q3业务汇报", "2025年第三季度")
# ... 添加内容
generator.save(f"output/行政组/{project_name}/q3-report.docx")
```

### 场景2：客户提案

```python
project_name = "海底捞合作提案"

result = create_from_template(
    template_type="pitch",
    data=proposal_data,
    output_path=f"output/行政组/{project_name}/partnership-proposal.docx"
)
```

### 场景3：营销活动策划

```python
project_name = "双十一营销活动2025"

result = create_from_template(
    template_type="product-launch",
    data=campaign_data,
    output_path=f"output/行政组/{project_name}/campaign-plan.docx"
)
```

### 场景4：培训课程

```python
project_name = "新员工入职培训202510"

result = create_from_template(
    template_type="training",
    data=training_data,
    output_path=f"output/行政组/{project_name}/onboarding-course.docx"
)
```

---

## 总结

### 核心优势

- **灵活性**: 项目名称根据实际业务场景自由命名
- **易管理**: 同一项目的所有文档集中在一个目录
- **可扩展**: 支持任意项目名称，不受固定分类限制
- **跨智能体**: 多个智能体可共享统一的输出规范
- **格式统一**: Word、Word、PDF共用相同路径规范

### 适用智能体

- R1-财务管理员: 财务分析、预算规划项目
- R2-人事管理员: 培训课件、招聘项目
- R4-秘书: 会议材料、工作汇报项目
- G1-经营分析优化师: 经营分析、数据报告项目
- X1-广告策划师: 营销策划、品牌推广项目
- GG-战略规划总监: 战略规划、投资路演项目

---

**最后更新**: 2025-10-21
**文档版本**: v2.0.0
