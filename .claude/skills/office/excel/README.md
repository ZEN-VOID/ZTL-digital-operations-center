# Excel自动化处理技能包

## 目录结构

```
.claude/skills/office/excel/
├── SKILL.md                    # 能力说明（Claude自动发现）
├── README.md                   # 本文件
├── scripts/                    # 执行引擎
│   ├── __init__.py
│   ├── excel_processor.py      # 核心处理器
│   └── excel_reporter.py       # 报表生成器
├── templates/                  # Excel模板（待添加）
│   ├── financial_report.xlsx
│   ├── sales_report.xlsx
│   └── hr_report.xlsx
└── examples/                   # 使用示例
    └── quick_start.py          # 快速开始示例

## 输出路径规范

**重要**: 所有输出文件必须保存到项目根目录的 `output/` 相关子目录中：

```
output/
├── 行政组/
│   ├── 财务报表/              # R1-财务管理员输出
│   ├── 人事数据/              # R2-人事管理员输出
│   └── excel/                 # 通用Excel处理输出
├── 战略组/
│   ├── 销售分析/              # G1-经营分析优化师输出
│   └── reports/               # 战略报表
└── 中台组/
    ├── 数据汇总/              # M4-美团管家报表管理员输出
    └── batch_test/            # 批量处理测试数据
```
```

## 快速开始

### 安装依赖

```bash
cd /Users/vincentlee/Desktop/ZTL数智化作战中心
pip install -r api/requirements-shared.txt
```

### 运行示例

```bash
cd .claude/skills/office/excel
python examples/quick_start.py
```

## 核心功能

### 1. ExcelProcessor (数据处理器)

```python
from scripts.excel_processor import ExcelProcessor

processor = ExcelProcessor()

# 读取
data = processor.read('file.xlsx')

# 清洗
cleaned = processor.clean_data(data, {
    'fill_na': 0,
    'remove_duplicates': True
})

# 分组
summary = processor.group_by(data,
    group_cols=['门店'],
    agg_cols={'销售额': 'sum'}
)

# 写入
processor.write(summary, 'output.xlsx')
```

### 2. ExcelReporter (报表生成器)

```python
from scripts.excel_reporter import ExcelReporter

reporter = ExcelReporter()

# 创建带图表的报表
reporter.create_report(
    data=sales_data,
    output='report.xlsx',
    config={
        'title': '月度销售报表',
        'charts': [
            {'type': 'bar', 'x': '门店', 'y': '销售额'}
        ]
    }
)
```

## 使用场景

### 财务报表自动化（R1-财务管理员）
```python
# 读取原始财务数据（从input目录）
data = processor.read('input/financial/financial_raw.xlsx')

# 计算利润率
data['利润率'] = (data['收入'] - data['成本']) / data['收入'] * 100

# 生成月度财务报表（输出到output/行政组/财务报表/）
processor.generate_report(data, 'output/行政组/财务报表/monthly_financial.xlsx')
```

### 销售数据分析（G1-经营分析优化师）
```python
# 按门店和产品分组
summary = processor.group_by(
    sales,
    group_cols=['门店', '产品类别'],
    agg_cols={'销售额': 'sum', '销量': 'sum'}
)

# 生成分析报表（输出到output/战略组/销售分析/）
reporter.create_report(summary, 'output/战略组/销售分析/sales_analysis.xlsx')
```

### 人事数据处理（R2-人事管理员）
```python
# 批量处理考勤数据
processor.batch_process(
    input_dir='input/hr/attendance/',
    output_dir='output/行政组/人事数据/processed/',
    process_func=lambda df: df[df['出勤天数'] >= 20]
)
```

## 依赖库说明

| 库 | 版本 | 用途 |
|---|------|------|
| pandas | >=2.0.0 | 数据处理核心 |
| openpyxl | >=3.1.0 | Excel读写 |
| xlrd | >=2.0.0 | 读取.xls格式 |
| xlsxwriter | >=3.0.0 | 高级报表 |

## 下一步计划

- [ ] 添加Excel模板文件
- [ ] 实现数据验证模块
- [ ] 支持复杂公式计算
- [ ] 添加更多图表类型
- [ ] 集成到各业务组智能体

## 相关智能体

- **R1-财务管理员**: 财务报表自动化
- **R2-人事管理员**: 人事数据处理
- **G1-经营分析优化师**: 经营数据分析
- **M4-美团管家报表管理员**: 美团数据报表

## 更新日志

### v1.0.0 (2025-01-21)
- ✅ 创建Excel自动化Skill
- ✅ 实现核心处理器和报表生成器
- ✅ 添加快速开始示例
- ✅ 更新项目依赖
