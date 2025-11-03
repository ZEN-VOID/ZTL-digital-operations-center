---
name: excel-automation
description: Excel文件智能处理和自动化，支持数据读取、分析、清洗、报表生成和批量处理
---

# Excel自动化处理技能包

## 概述

提供完整的Excel文件处理能力，支持数据读取、写入、分析、清洗和报表自动化生成。

## 核心能力

### 1. 数据读取和解析
- 读取.xlsx/.xls格式文件
- 支持多工作表读取
- 智能类型推断
- 大文件分块读取

### 2. 数据清洗和转换
- 空值处理和填充
- 数据类型转换
- 重复数据检测和去重
- 异常值识别和处理

### 3. 数据分析
- 统计分析（求和、平均、最大/最小值）
- 分组聚合
- 数据透视
- 趋势分析

### 4. 报表生成
- 基于模板生成报表
- 自动样式设置（字体、颜色、边框）
- 图表生成（柱状图、折线图、饼图）
- 多工作表报表

### 5. 批量处理
- 批量读取多个Excel文件
- 数据合并和拆分
- 批量格式转换

## 快速开始

### 基础用法

```python
from scripts.excel_processor import ExcelProcessor

# 创建处理器
processor = ExcelProcessor()

# 读取Excel
data = processor.read('sales_data.xlsx')

# 数据清洗
cleaned_data = processor.clean_data(data, {
    'fill_na': True,
    'remove_duplicates': True,
    'convert_types': {'日期': 'datetime', '金额': 'float'}
})

# 保存结果到项目output目录
processor.write(cleaned_data, 'output/行政组/excel/cleaned_sales.xlsx')
```

### 数据分析示例

```python
# 读取并分析
data = processor.read('sales.xlsx')

# 分组统计
summary = processor.group_by(data,
    group_cols=['门店', '月份'],
    agg_cols={'销售额': 'sum', '订单数': 'count'}
)

# 生成报表到项目output目录
processor.generate_report(
    data=summary,
    output='output/战略组/reports/monthly_report.xlsx',
    charts=[
        {'type': 'bar', 'x': '门店', 'y': '销售额'},
        {'type': 'line', 'x': '月份', 'y': '销售额'}
    ]
)
```

### 批量处理示例

```python
# 批量合并Excel文件
merged = processor.merge_files(
    pattern='input/data/*.xlsx',
    output='output/中台组/reports/merged_report.xlsx'
)

# 批量应用同一处理逻辑
processor.batch_process(
    input_dir='input/raw_data/',
    output_dir='output/行政组/excel/processed/',
    process_func=lambda df: df[df['销售额'] > 1000]
)
```

## API参考

### ExcelProcessor

#### read(file_path, sheet_name=None, **kwargs)
读取Excel文件

**参数**:
- `file_path` (str): 文件路径
- `sheet_name` (str|int|None): 工作表名称或索引，None读取第一个
- `**kwargs`: pandas.read_excel的其他参数

**返回**: pandas.DataFrame

#### write(data, file_path, sheet_name='Sheet1', **kwargs)
写入Excel文件

**参数**:
- `data` (DataFrame|dict): 数据
- `file_path` (str): 输出路径
- `sheet_name` (str): 工作表名称
- `**kwargs`: pandas.to_excel的其他参数

#### clean_data(data, options)
数据清洗

**参数**:
- `data` (DataFrame): 原始数据
- `options` (dict): 清洗选项
  - `fill_na` (bool|value): 填充空值
  - `remove_duplicates` (bool): 去除重复
  - `convert_types` (dict): 类型转换映射

**返回**: pandas.DataFrame

#### group_by(data, group_cols, agg_cols)
分组聚合

**参数**:
- `data` (DataFrame): 数据
- `group_cols` (list): 分组列
- `agg_cols` (dict): 聚合列和函数映射

**返回**: pandas.DataFrame

#### generate_report(data, output, template=None, charts=None)
生成报表

**参数**:
- `data` (DataFrame): 数据
- `output` (str): 输出路径
- `template` (str|None): 模板路径
- `charts` (list|None): 图表配置列表

#### merge_files(pattern, output, **kwargs)
合并多个Excel文件

**参数**:
- `pattern` (str): 文件匹配模式（如 'data/*.xlsx'）
- `output` (str): 输出路径
- `**kwargs`: 合并选项

**返回**: pandas.DataFrame

### ExcelReporter

#### create_report(data, output, config)
创建完整报表

**参数**:
- `data` (DataFrame|dict): 数据
- `output` (str): 输出路径
- `config` (dict): 报表配置
  - `title` (str): 报表标题
  - `sheets` (list): 工作表配置
  - `charts` (list): 图表配置
  - `styles` (dict): 样式配置

## 使用场景

### 场景1: 财务报表自动化
```python
# 读取原始财务数据
data = processor.read('financial_raw.xlsx')

# 清洗和计算
data = processor.clean_data(data, {'fill_na': 0})
data['利润率'] = (data['收入'] - data['成本']) / data['收入'] * 100

# 生成月度财务报表
processor.generate_report(
    data=data,
    output='output/行政组/财务报表/monthly_financial_report.xlsx',
    template='.claude/skills/office/excel/templates/financial_template.xlsx',
    charts=[
        {'type': 'line', 'x': '月份', 'y': '收入'},
        {'type': 'bar', 'x': '月份', 'y': '利润率'}
    ]
)
```

### 场景2: 销售数据分析
```python
# 读取销售数据
sales = processor.read('sales.xlsx')

# 按门店和产品分组统计
summary = processor.group_by(
    sales,
    group_cols=['门店', '产品类别'],
    agg_cols={'销售额': 'sum', '销量': 'sum', '订单数': 'count'}
)

# 生成分析报表
processor.generate_report(
    data=summary,
    output='output/战略组/销售分析/sales_analysis.xlsx',
    charts=[
        {'type': 'pie', 'values': '销售额', 'names': '产品类别'},
        {'type': 'bar', 'x': '门店', 'y': '销售额'}
    ]
)
```

### 场景3: 批量数据处理
```python
# 合并所有门店的销售数据
merged = processor.merge_files(
    pattern='input/stores/*/sales_*.xlsx',
    output='output/中台组/数据汇总/all_stores_sales.xlsx'
)

# 数据验证和清洗
cleaned = processor.clean_data(merged, {
    'fill_na': True,
    'remove_duplicates': True
})

# 生成汇总报表
processor.generate_report(
    data=cleaned,
    output='output/中台组/数据汇总/consolidated_report.xlsx'
)
```

## 高级功能

### 自定义数据验证
```python
from scripts.excel_validator import ExcelValidator

validator = ExcelValidator()

# 定义验证规则
rules = {
    '金额': {'type': 'numeric', 'min': 0},
    '日期': {'type': 'datetime', 'format': '%Y-%m-%d'},
    '门店': {'type': 'enum', 'values': ['门店A', '门店B', '门店C']}
}

# 验证数据
errors = validator.validate(data, rules)
if errors:
    print(f"发现{len(errors)}个错误")
```

### 动态模板填充
```python
from scripts.excel_template import TemplateEngine

engine = TemplateEngine()

# 加载模板
template = engine.load('templates/report_template.xlsx')

# 填充数据
filled = engine.fill(template, {
    'title': '2025年1月销售报表',
    'data': sales_data,
    'summary': summary_data
})

# 保存
filled.save('2025_01_sales_report.xlsx')
```

## 注意事项

1. **大文件处理**: 对于超过100MB的文件，使用分块读取
2. **内存管理**: 批量处理时注意及时释放DataFrame对象
3. **类型转换**: 日期和数值类型需要明确指定格式
4. **编码问题**: 中文文件名和内容确保使用UTF-8编码

## 依赖库

- pandas >= 2.0.0
- openpyxl >= 3.1.0
- xlrd >= 2.0.0 (可选，处理.xls格式)
- xlsxwriter >= 3.0.0 (可选，高级报表)

## 相关资源

- [pandas文档](https://pandas.pydata.org/docs/)
- [openpyxl文档](https://openpyxl.readthedocs.io/)
- [Excel最佳实践](../reference.md)
