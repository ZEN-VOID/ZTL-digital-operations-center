# 菜品创建技能包 (Dish Creator)

## 快速开始

### 安装依赖

```bash
pip install pandas openpyxl pypinyin
```

### 基础用法

```python
from scripts.dish_creator import DishCreator

# 初始化
creator = DishCreator()

# 方式1: 自然语言创建
result = creator.create_from_text(
    text="创建新菜品'麻辣小龙虾',售价88元,会员价78元",
    project_name="新菜品上架"
)

# 方式2: 结构化数据创建
result = creator.create_from_dict(
    data={
        "dish_name": "麻辣小龙虾",
        "brand": "吼巷",
        "category": "招牌菜/海鲜",
        "selling_price": 88,
        "member_price": 78
    },
    project_name="新菜品上架"
)

# 方式3: 批量创建
batch_data = [
    {"dish_name": "麻辣小龙虾", "selling_price": 88},
    {"dish_name": "蒜蓉小龙虾", "selling_price": 88}
]
results = creator.create_batch(
    batch_data=batch_data,
    project_name="批量上架"
)
```

## 目录结构

```
菜品新建/
├── SKILL.md                    # 技能包主文档
├── reference.md                # 扩展参考文档
├── README.md                   # 本文件
├── scripts/                    # 执行脚本
│   ├── dish_creator.py        # 主引擎
│   ├── parsers/               # 解析器
│   │   └── text_parser.py     # 文本解析
│   ├── validators/            # 验证器
│   │   └── field_validator.py # 字段验证
│   └── generators/            # 生成器
│       └── excel_generator.py # Excel生成
├── examples/                   # 示例代码
│   ├── example_basic.py       # 基础示例
│   └── example_batch.py       # 批量示例
└── templates/                  # 模板文件
```

## 核心功能

### 1. 智能字段推断

- ✅ 计价方式: 根据单位自动推断
- ✅ 单位: 根据品类自动推断
- ✅ 拼音助记码: 自动生成
- ✅ 辣度: 根据菜品名称推断
- ✅ 默认值: 自动填充常用默认值

### 2. 字段验证

- ✅ 必填字段验证
- ✅ 字段格式验证
- ✅ 枚举值验证
- ✅ 业务规则验证

### 3. 批量处理

- ✅ 支持批量创建
- ✅ 进度追踪
- ✅ 错误处理
- ✅ 结果统计

## 运行示例

### 示例1: 基础创建

```bash
cd plugins/美团组/skills/运营中心/workflows/菜品新建
python examples/example_basic.py
```

### 示例2: 批量创建

```bash
python examples/example_batch.py
```

### 示例3: 命令行

```bash
python scripts/dish_creator.py "新菜品上架" "麻辣小龙虾" 88
```

## 输出路径

所有输出文件统一保存到:

```
output/[项目名]/dish-creator/
├── 菜品导入_麻辣小龙虾_20250103_143000.xlsx
├── plan_菜品创建_20250103_143000.json
├── log_execution_20250103_143000.txt
└── metadata_20250103_143000.json
```

## 注意事项

1. **必填字段**: 菜品名称、品牌、分类、售卖价、计价方式
2. **会员价**: 必须 ≤ 售卖价
3. **保质期**: 输入保质期后,保质期单位必填
4. **分类格式**: 两级分类用"/"分隔,如"招牌菜/海鲜"
5. **标签格式**: 多个标签用"//"分隔,如"团购//活动菜"

## 依赖资源

- **模板文件**: `plugins/美团组/templates/菜品导入模板.xlsx`
- **奥术光辉/excel**: `.claude/skills/奥术光辉/excel/` (可选)

## 相关文档

- [SKILL.md](./SKILL.md) - 完整技能包文档
- [reference.md](./reference.md) - 扩展参考文档
- [三层架构规范](~/.claude/CLAUDE.md#5-复杂系统三层架构规范)
- [输出路径规范](~/.claude/CLAUDE.md#45-输出路径规范)

## 版本历史

- **v1.0.0** (2025-01-03): 初始版本
