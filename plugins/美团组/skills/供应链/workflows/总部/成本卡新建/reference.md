# 成本卡创建技能包 - 扩展文档

## 架构设计

### 三层架构详解

```
┌─────────────────────────────────────────────────────────┐
│ Layer 1: 规范层 (Specification Layer)                    │
│ - SKILL.md: 业务逻辑、领域知识、工作流程、质量标准       │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 2: 计划层 (Plan Layer)                             │
│ - JSON配置文件: 参数化配置、批次定义、版本控制           │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 3: 执行层 (Execution Layer)                        │
│ ├─ cost_card_generator.py (主执行引擎)                   │
│ ├─ parsers/ (信息解析)                                   │
│ │   └─ text_parser.py                                   │
│ ├─ matchers/ (编码匹配)                                  │
│ │   ├─ dish_matcher.py                                  │
│ │   └─ item_matcher.py                                  │
│ └─ generators/ (Excel生成)                               │
│     └─ excel_generator.py                               │
└─────────────────────────────────────────────────────────┘
```

### 设计原则

#### 1. 职责分离 (Separation of Concerns)

**规范层职责**:
- 定义"做什么": 成本卡创建的业务目标
- 定义"为什么": 吼巷总部的成本管理规范
- 定义"质量标准": 必填字段验证、匹配准确率要求

**计划层职责**:
- 定义"怎么配置": 匹配阈值、批次大小、重试策略
- 定义"执行什么": 具体的菜品和配料信息
- 定义"追溯信息": 版本号、时间戳、输出路径

**执行层职责**:
- 定义"如何执行": 实际的API调用、数据处理、文件生成
- 定义"错误处理": 异常捕获、重试逻辑、日志记录
- 定义"性能优化": 缓存机制、批量处理、资源管理

#### 2. 配置驱动 (Configuration-Driven)

**配置示例**:
```json
{
  "execution_config": {
    "match_threshold": 0.7,           // 匹配阈值
    "auto_confirm_above": 0.9,        // 自动确认阈值
    "require_manual_confirm": true,   // 是否需要人工确认
    "batch_size": 50,                 // 批次大小
    "enable_cache": true,             // 是否启用缓存
    "max_retry": 3                    // 最大重试次数
  }
}
```

**好处**:
- ✅ 业务逻辑与配置分离,易于调整
- ✅ 不同项目可以使用不同配置
- ✅ 配置文件可以版本控制和追溯

#### 3. 标准化 (Standardization)

**命名规范**:
- 文件名: `成本卡_菜品名_YYYYMMDD_HHMMSS.xlsx`
- 计划文件: `plan_成本卡生成_YYYYMMDD_HHMMSS.json`
- 日志文件: `log_execution_YYYYMMDD_HHMMSS.txt`
- 元数据: `metadata_YYYYMMDD_HHMMSS.json`

**输出路径规范**:
```
output/[项目名]/cost-card-creator/
├── 成本卡_麻辣牛肉_20250103_143000.xlsx
├── 成本卡_酸菜鱼_20250103_143001.xlsx
├── plan_成本卡生成_20250103_143000.json
├── log_execution_20250103_143000.txt
└── metadata_20250103_143000.json
```

#### 4. 可扩展性 (Scalability)

**扩展点**:
1. **解析器扩展**: 添加新的输入格式 (如Word、PDF)
2. **匹配器扩展**: 添加新的匹配策略 (如NLP语义匹配)
3. **生成器扩展**: 添加新的输出格式 (如JSON、CSV)
4. **验证器扩展**: 添加新的质量检查规则

**扩展示例**:
```python
# 添加新的解析器
class PDFParser(BaseParser):
    def parse(self, file_path: str) -> Dict[str, Any]:
        # 实现PDF解析逻辑
        pass

# 注册到主生成器
generator.register_parser("pdf", PDFParser())
```

#### 5. 可追溯性 (Traceability)

**追溯机制**:
1. **执行计划**: 记录输入参数和配置
2. **元数据**: 记录执行时间、版本号、输出路径
3. **日志**: 记录每个步骤的执行状态
4. **错误记录**: 记录匹配失败的物品和原因

**追溯示例**:
```json
{
  "metadata": {
    "project_name": "火锅店成本管理",
    "dish_name": "麻辣牛肉",
    "created_at": "20250103_143000",
    "plan_path": "output/.../plan_xxx.json",
    "output_path": "output/.../成本卡_xxx.xlsx",
    "dish_spu_code": "SPU001",
    "ingredient_count": 5,
    "match_results": {
      "dish_similarity": 0.95,
      "item_exact_matches": 5,
      "item_failed_matches": 0
    }
  }
}
```

## 核心算法

### 模糊匹配算法

#### Levenshtein距离算法

**原理**: 计算两个字符串之间的编辑距离 (插入、删除、替换操作的次数)

**相似度计算**:
```python
similarity = 1 - (levenshtein_distance / max(len(a), len(b)))
```

**示例**:
```
输入: "麻辣牛肉"
菜品库: "麻辣牛肉片"
编辑距离: 1 (插入"片")
相似度: 1 - 1/5 = 0.8 (80%)
```

**阈值设计**:
- ≥ 0.9 (90%): 高置信度,自动采用
- 0.7 ~ 0.9 (70%-90%): 中等置信度,自动采用但记录
- < 0.7 (< 70%): 低置信度,暂停执行,请求人工确认

#### 综合匹配策略

**场景**: 同时匹配菜品名称和规格

**公式**:
```
total_similarity = name_similarity * 0.7 + spec_similarity * 0.3
```

**权重设计**:
- 菜品名称权重: 70% (主要匹配依据)
- 菜品规格权重: 30% (辅助匹配依据)

**示例**:
```
输入: dish_name="麻辣牛肉", dish_spec="标准"
候选: dish_name="麻辣牛肉片", dish_spec="标准"

name_similarity = 0.8
spec_similarity = 1.0
total_similarity = 0.8 * 0.7 + 1.0 * 0.3 = 0.86 (86%)
```

### 数据重构算法

#### 一对多关系扩展

**问题**: 一个菜品对应多个物品时,如何组织数据?

**策略**: 菜品信息在多行重复填写,物品信息每行填写一个

**输入数据**:
```json
{
  "dish_name": "麻辣牛肉",
  "ingredients": [
    {"item_name": "牛肉", "quantity": 500},
    {"item_name": "辣椒油", "quantity": 50},
    {"item_name": "花椒", "quantity": 10}
  ]
}
```

**输出数据** (Excel表格):

| 菜品SPU编码 | 菜品名称 | 物品编码 | 物品名称 | 净料量 |
|------------|---------|---------|---------|-------|
| SPU001     | 麻辣牛肉 | ITM001  | 牛肉    | 500   |
| SPU001     | 麻辣牛肉 | ITM002  | 辣椒油  | 50    |
| SPU001     | 麻辣牛肉 | ITM003  | 花椒    | 10    |

**实现代码**:
```python
def _restructure_data(dish_data, ingredients):
    rows = []
    for ingredient in ingredients:
        row = {
            "菜品SPU编码": dish_data["dish_code"],  # 重复填写
            "菜品名称": dish_data["dish_name"],      # 重复填写
            "物品编码": ingredient["item_code"],     # 每行一个
            "物品名称": ingredient["item_name"],     # 每行一个
            "净料量": ingredient["quantity"]         # 每行一个
        }
        rows.append(row)
    return rows
```

## 错误处理策略

### 错误分类

#### 1. 数据源错误

**错误**: 菜品库或物品清单文件不存在

**处理**:
```python
if not self.dish_db_path.exists():
    raise FileNotFoundError("菜品库文件不存在,请检查路径")
```

**提示用户**:
```
错误: 无法找到菜品库文件
路径: plugins/美团组/templates/吼巷_菜品库_总部.xlsx
建议: 请确认数据源文件存在
```

#### 2. 匹配失败错误

**错误**: 菜品或物品无法匹配

**处理**:
```python
if best_match["similarity"] < threshold:
    return {
        "status": "pending_confirm",
        "candidates": fuzzy_matches[:5]
    }
```

**提示用户**:
```
警告: 菜品匹配度低于70%,需要人工确认
输入: 麻辣牛肉
候选:
  1. 麻辣牛肉片 (80%)
  2. 麻辣牛肉丝 (75%)
  3. 香辣牛肉 (65%)
```

#### 3. 验证错误

**错误**: 必填字段缺失或格式不正确

**处理**:
```python
def validate_required_fields(data):
    required = ["菜品SPU编码", "菜品名称", "物品编码"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        raise ValueError(f"缺少必填字段: {missing}")
```

**提示用户**:
```
错误: 必填字段缺失
缺少字段: ['物品编码', '净料量']
建议: 请补充物品编码和净料量信息
```

### 重试机制

**场景**: API调用失败、文件读写失败

**策略**:
```python
def retry_with_backoff(func, max_retry=3):
    for attempt in range(max_retry):
        try:
            return func()
        except Exception as e:
            if attempt == max_retry - 1:
                raise
            time.sleep(2 ** attempt)  # 指数退避
```

**退避时间**:
- 第1次重试: 延迟1秒
- 第2次重试: 延迟2秒
- 第3次重试: 延迟4秒

## 性能优化

### 缓存机制

**问题**: 批量处理时,重复读取菜品库和物品清单

**解决方案**: 在类初始化时一次性加载,缓存到内存

```python
class DishMatcher:
    def __init__(self):
        self.dish_db = self._load_dish_database()  # 一次性加载
```

**性能提升**:
- 无缓存: 每次匹配都读取文件 (O(n) 文件IO)
- 有缓存: 只在初始化时读取一次 (O(1) 内存访问)
- 批量处理100个菜品: 从100次IO降低到1次IO

### 批量处理优化

**问题**: 逐个处理100个菜品,串行执行速度慢

**解决方案**: 分批并行处理

```python
def create_batch(batch_data, batch_size=50):
    # 分批处理
    for i in range(0, len(batch_data), batch_size):
        batch = batch_data[i:i + batch_size]

        # 并行处理每批
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(create_one, data) for data in batch]
            results = [f.result() for f in futures]
```

**性能提升**:
- 串行处理100个菜品: 100 * 2秒 = 200秒
- 并行处理(10线程): 100 / 10 * 2秒 = 20秒
- 提升: 10倍

### 内存优化

**问题**: 批量处理大文件时内存占用过高

**解决方案**: 分块读取 + 及时释放

```python
def process_large_file(file_path):
    # 分块读取
    for chunk in pd.read_excel(file_path, chunksize=1000):
        process_chunk(chunk)
        del chunk  # 及时释放内存
        gc.collect()
```

## 集成指南

### 集成奥术光辉/excel技能包

**目的**: 利用高级Excel处理能力

**集成方式**:
```python
from scripts.excel_generator import ExcelGenerator

generator = ExcelGenerator(use_excel_skill=True)
```

**调用示例**:
```python
# 自动调用奥术光辉/excel的高级特性
generator.generate_with_excel_skill(
    data=restructured_data,
    output_path="output/.../成本卡.xlsx"
)
```

**高级功能**:
1. **数据验证**: 自动验证必填字段、格式规范
2. **样式设置**: 自动设置字体、颜色、边框
3. **图表生成**: 自动生成成本分析图表
4. **公式计算**: 自动计算总成本、毛利率

### 集成CLI命令

**目的**: 提供命令行接口

**创建命令**:
```bash
# plugins/美团组/commands/cost-card.md
---
description: 创建成本卡
---

创建成本卡,支持单个和批量创建。

使用示例:
```bash
/cost-card "为麻辣牛肉创建成本卡"
/cost-card --batch "菜品配方清单.xlsx"
```
```

**调用技能包**:
```python
from scripts.cost_card_generator import CostCardGenerator

generator = CostCardGenerator()
result = generator.create_from_text(
    text="$ARGUMENTS",
    project_name="成本卡管理"
)
```

### 集成智能体

**目的**: 让智能体自动调用技能包

**智能体定义**:
```markdown
# plugins/美团组/agents/Y1-成本管理专员.md

你是成本管理专员,负责创建和维护成本卡。

## 核心能力

1. 调用 cost-card-creator 技能包创建成本卡
2. 分析成本数据,提供优化建议
3. 批量处理成本卡导入任务

## 工作流程

当用户请求创建成本卡时:
1. 理解用户需求,提取菜品和配料信息
2. 调用 cost-card-creator 技能包
3. 检查执行结果,处理人工确认请求
4. 返回成本卡文件路径

## 示例

用户: "为麻辣牛肉创建成本卡"
智能体: 调用技能包 → 返回成本卡文件
```

## 测试指南

### 单元测试

**测试解析器**:
```python
def test_text_parser():
    parser = TextParser()
    text = """
    为"麻辣牛肉"创建成本卡:
    - 牛肉 500g
    - 辣椒油 50ml
    """
    result = parser.parse(text)
    assert result["dish_name"] == "麻辣牛肉"
    assert len(result["ingredients"]) == 2
```

**测试匹配器**:
```python
def test_dish_matcher():
    matcher = DishMatcher()
    result = matcher.match("麻辣牛肉")
    assert result["status"] == "success"
    assert result["similarity"] >= 0.7
```

### 集成测试

**测试完整流程**:
```python
def test_full_workflow():
    generator = CostCardGenerator()
    result = generator.create_from_text(
        text="为麻辣牛肉创建成本卡: - 牛肉 500g",
        project_name="测试项目"
    )
    assert result["status"] == "success"
    assert Path(result["output_path"]).exists()
```

### 数据质量测试

**测试匹配准确率**:
```python
def test_match_accuracy():
    matcher = DishMatcher()
    test_cases = [
        ("麻辣牛肉", "麻辣牛肉片", 0.8),
        ("酸菜鱼", "酸菜鱼", 1.0),
        ("水煮肉片", "水煮牛肉", 0.75)
    ]
    for input_name, expected_name, min_similarity in test_cases:
        result = matcher.match(input_name)
        assert result["similarity"] >= min_similarity
```

## 维护指南

### 数据源更新

**定期同步**:
1. 每月同步菜品库 (新菜品上架)
2. 每周同步物品清单 (新物品入库)
3. 检查数据源版本号

**更新流程**:
```bash
# 1. 备份旧数据
cp plugins/美团组/templates/吼巷_菜品库_总部.xlsx \
   plugins/美团组/templates/backup/吼巷_菜品库_总部_20250103.xlsx

# 2. 下载新数据
# (从美团总部系统导出)

# 3. 验证数据格式
python scripts/validate_data_source.py

# 4. 测试匹配功能
pytest tests/test_matchers.py
```

### 版本升级

**升级检查清单**:
- [ ] 测试用例全部通过
- [ ] 文档更新完成
- [ ] 数据源兼容性验证
- [ ] 性能测试通过
- [ ] 用户手册更新

**版本号规范**:
- v1.0.0 → v1.0.1: Bug修复
- v1.0.0 → v1.1.0: 新增功能
- v1.0.0 → v2.0.0: 重大重构

## 常见问题 (FAQ)

### Q1: 如何处理菜品匹配度低于70%的情况?

**A**: 系统会暂停执行,返回候选项列表,等待人工确认。

```python
if result["status"] == "pending_confirm":
    print("候选项:")
    for candidate in result["candidates"]:
        print(f"- {candidate['dish_name']} ({candidate['similarity']*100}%)")
```

### Q2: 如何批量导入100+菜品的成本卡?

**A**: 使用 `create_batch` 方法,支持分批并行处理。

```python
generator.create_batch(
    batch_data=batch_data,
    project_name="2025Q1成本卡批量导入"
)
```

### Q3: 成本卡生成后如何导入到美团系统?

**A**: 下载生成的Excel文件,在美团总部后台选择"成本卡导入",上传文件即可。

### Q4: 如何自定义匹配阈值?

**A**: 在执行计划中配置 `match_threshold` 参数。

```json
{
  "execution_config": {
    "match_threshold": 0.8  // 提高到80%
  }
}
```

### Q5: 如何查看执行日志?

**A**: 日志文件位于输出目录下。

```bash
cat output/[项目名]/cost-card-creator/log_execution_*.txt
```

## 相关资源

- [三层架构规范](~/.claude/CLAUDE.md#5-复杂系统三层架构规范)
- [输出路径规范](~/.claude/CLAUDE.md#45-输出路径规范)
- [奥术光辉/excel技能包](.claude/skills/奥术光辉/excel/SKILL.md)
- [吼巷总部成本管理手册](plugins/美团组/docs/成本管理手册.pdf)
- [美团成本卡导入指南](https://help.meituan.com/cost-card-import)
