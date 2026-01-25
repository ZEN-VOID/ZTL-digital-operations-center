# 菜品创建技能包 - 扩展参考文档

## 美团管家菜品导入规范详解

### 字段完整说明

#### 1. 菜品基本信息 (6个字段)

**1.1 菜品名称** (必填)
- 字段类型: 文本
- 长度限制: 建议不超过30字
- 示例: "麻辣小龙虾"、"酸菜鱼"、"红烧肉"
- 注意事项:
  - 名称应清晰、易于理解
  - 避免使用特殊符号
  - 重复名称会导致导入失败

**1.2 所属品牌** (必填)
- 字段类型: 文本
- 说明: 必须是系统中已存在的品牌
- 示例: "吼巷"、"某某餐饮"
- 注意事项:
  - 品牌名称必须完全匹配
  - 区分大小写
  - 建议维护品牌白名单

**1.3 分类** (必填)
- 字段类型: 文本
- 格式: 一级分类/二级分类
- 示例: "招牌菜/海鲜"、"凉菜/川菜"、"主食"
- 注意事项:
  - 支持一级或二级分类
  - 两级分类用"/"分隔
  - 分类必须是系统中已存在的

**1.4 规格** (可选)
- 字段类型: 文本
- 示例: "大份"、"中份"、"小份"、"标准"、"1人份"
- 注意事项:
  - 用于区分同一菜品的不同规格
  - 规格不同时售价可以不同

**1.5 条形码** (可选)
- 字段类型: 文本
- 长度: 5-30位数字或字母
- 示例: "6901234567890"、"ABC123456"
- 注意事项:
  - 用于扫码点餐
  - 条形码不能重复

**1.6 助记码** (可选)
- 数字助记码: 点菜宝中使用,纯数字
- 拼音助记码: 点菜宝中使用,字母
- 示例:
  - 数字助记码: "001"、"123"
  - 拼音助记码: "MLXLX" (麻辣小龙虾)

#### 2. 价格信息 (3个字段)

**2.1 售卖价** (必填)
- 字段类型: 数值
- 单位: 元
- 示例: 88、99.9、128
- 注意事项:
  - 必须大于0
  - 支持小数点后2位

**2.2 会员价** (可选)
- 字段类型: 数值
- 单位: 元
- 示例: 78、89.9、115
- 注意事项:
  - 必须 ≤ 售卖价
  - 不填写则默认等于售卖价

**2.3 预估成本** (可选)
- 字段类型: 数值
- 单位: 元
- 示例: 30、45.5、60
- 注意事项:
  - 用于毛利率计算
  - 不影响售卖,仅作参考

#### 3. 销售设置 (8个字段)

**3.1 计价方式** (必填)
- 字段类型: 枚举
- 可选值: "按份销售"、"称重销售"
- 示例:
  - 按份销售: 大部分菜品
  - 称重销售: 水果、海鲜等

**3.2 单位** (可选)
- 字段类型: 文本
- 示例: "份"、"斤"、"两"、"杯"、"碗"
- 注意事项:
  - 按份销售: 通常是"份"
  - 称重销售: 通常是"斤"、"两"

**3.3 售卖状态** (可选)
- 字段类型: 枚举
- 可选值: "在售"、"停售"
- 默认值: "在售"
- 注意事项:
  - 停售的菜品不会在点餐端显示

**3.4 点餐端展示-统一设置** (可选)
- 字段类型: 枚举
- 可选值: "是"、"否"
- 默认值: "是"
- 说明: 是否在点餐端显示

**3.5 收银端临时改价** (可选)
- 字段类型: 枚举
- 可选值: "允许"、"不允许"
- 默认值: "不允许"
- 说明: 收银员能否临时修改价格

**3.6 收银端手动打折** (可选)
- 字段类型: 枚举
- 可选值: "允许"、"不允许"
- 默认值: "允许"
- 说明: 收银员能否手动打折

**3.7 起售份数** (可选)
- 字段类型: 数值
- 默认值: 1
- 示例: 2 (至少2份起卖)
- 注意事项:
  - 用于限制最小购买数量

**3.8 增量售卖数** (可选)
- 字段类型: 数值
- 默认值: 1
- 示例: 2 (每次增加2份)
- 注意事项:
  - 配合起售份数使用

#### 4. 保质期信息 (2个字段)

**4.1 保质期** (可选)
- 字段类型: 数值
- 范围: 1-999
- 示例: 30、90、365
- 注意事项:
  - 输入保质期后,保质期单位必填

**4.2 保质期单位** (条件必填)
- 字段类型: 枚举
- 可选值: "年"、"天"、"自然日"、"小时"、"分钟"
- 示例: "天"、"小时"
- 注意事项:
  - 若输入保质期,此字段必填

#### 5. 打印设置 (2个字段)

**5.1 是否打印** (可选)
- 字段类型: 枚举
- 可选值: "是"、"否"
- 默认值: "是"
- 说明: 是否在下单后自动打印小票

**5.2 仅套餐售卖** (可选)
- 字段类型: 枚举
- 可选值: "是"、"否"
- 默认值: "否"
- 说明: 是否只能作为套餐售卖

#### 6. 标签和描述 (6个字段)

**6.1 菜品角标** (可选)
- 字段类型: 文本
- 示例: "新菜"、"招牌菜"、"爆款"
- 注意事项:
  - 显示在菜品图片上方
  - 吸引顾客注意

**6.2 描述标签** (可选)
- 字段类型: 文本
- 格式: 多个标签用"//"分隔
- 示例: "含乳制品//可做热饮//低糖"
- 注意事项:
  - 用于展示菜品特性
  - 帮助顾客筛选

**6.3 点餐标签** (可选)
- 字段类型: 文本
- 格式: 多个标签用"//"分隔
- 示例: "团购//活动菜//店长推荐"
- 注意事项:
  - 用于营销推广
  - 突出显示特殊菜品

**6.4 菜品辣度** (可选)
- 字段类型: 枚举
- 可选值: "不辣"、"微微辣"、"微辣"、"中辣"、"重辣"、"爆辣"
- 示例: "重辣"
- 注意事项:
  - 帮助顾客选择合适口味

**6.5 菜品描述** (可选)
- 字段类型: 文本
- 长度限制: 最多50字
- 示例: "精选优质小龙虾,秘制麻辣调料,鲜香麻辣"
- 注意事项:
  - 简短描述,吸引顾客

**6.6 菜品详细描述** (可选)
- 字段类型: 文本
- 长度限制: 最多200字
- 示例: "精选优质小龙虾,采用秘制麻辣调料,经过多道工序精心烹制..."
- 注意事项:
  - 详细描述菜品特色、食材、制作工艺

#### 7. 自定义字段 (4个字段)

**7.1-7.4 自定义字段1-4** (可选)
- 字段类型: 文本
- 长度限制: 最多200字
- 说明: 用于存储额外的自定义信息
- 示例: "产地信息"、"推荐搭配"、"营养成分"

## 智能推断规则详解

### 1. 计价方式推断

**规则**:
```python
if "单位" in ["斤", "两", "公斤", "克"]:
    计价方式 = "称重销售"
else:
    计价方式 = "按份销售"
```

**示例**:
- "斤" → "称重销售"
- "份" → "按份销售"
- "杯" → "按份销售"

### 2. 单位推断

**规则**:
```python
if 计价方式 == "按份销售":
    单位 = "份"
elif 计价方式 == "称重销售":
    单位 = "斤"  # 或根据品类推断
```

**品类与单位映射**:
```python
CATEGORY_UNIT_MAP = {
    "饮料": "杯",
    "主食": "份",
    "水果": "斤",
    "海鲜": "斤",
    "汤品": "碗"
}
```

### 3. 辣度推断

**规则**:
```python
SPICY_KEYWORDS = {
    "不辣": ["清淡", "原味", "不辣"],
    "微微辣": ["微微辣"],
    "微辣": ["微辣", "微"],
    "中辣": ["中辣", "酸辣"],
    "重辣": ["重辣", "麻辣", "香辣"],
    "爆辣": ["爆辣", "超辣", "变态辣"]
}

def infer_spicy_level(dish_name):
    for level, keywords in SPICY_KEYWORDS.items():
        if any(kw in dish_name for kw in keywords):
            return level
    return "不辣"  # 默认值
```

**示例**:
- "麻辣小龙虾" → "重辣"
- "微辣口水鸡" → "微辣"
- "清蒸鲈鱼" → "不辣"

### 4. 拼音助记码生成

**规则**:
```python
from pypinyin import lazy_pinyin

def generate_pinyin_memo(dish_name):
    pinyin = lazy_pinyin(dish_name)
    return ''.join([py[0].upper() for py in pinyin])
```

**示例**:
- "麻辣小龙虾" → "MLXLX"
- "酸菜鱼" → "SCY"
- "红烧肉" → "HSR"

### 5. 菜品角标推断

**规则**:
```python
BADGE_KEYWORDS = {
    "新菜": ["新品", "新上", "最新"],
    "招牌菜": ["招牌", "爆款", "必点"],
    "特价": ["特价", "促销", "优惠"]
}

def infer_badge(dish_name, description):
    text = dish_name + " " + description
    for badge, keywords in BADGE_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            return badge
    return None  # 无角标
```

**示例**:
- "新品麻辣小龙虾" → "新菜"
- "招牌红烧肉" → "招牌菜"

### 6. 描述标签推断

**规则**:
```python
TAG_KEYWORDS = {
    "含乳制品": ["奶油", "芝士", "牛奶", "酸奶"],
    "可做热饮": ["可热", "热饮"],
    "含坚果": ["花生", "核桃", "杏仁"],
    "海鲜": ["虾", "蟹", "鱼", "贝"],
    "辣": ["辣", "麻"]
}

def infer_description_tags(dish_name, description):
    text = dish_name + " " + description
    tags = []
    for tag, keywords in TAG_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            tags.append(tag)
    return "//".join(tags) if tags else None
```

**示例**:
- "芝士奶盖奶茶" → "含乳制品"
- "麻辣小龙虾" → "海鲜//辣"

## 错误处理机制

### 1. 必填字段缺失

**错误类型**: `MissingRequiredFieldError`

**处理流程**:
1. 检测缺失字段
2. 生成错误报告
3. 提示用户补充
4. 暂停执行

**错误报告格式**:
```json
{
  "error_type": "MissingRequiredFieldError",
  "missing_fields": ["菜品名称", "售卖价"],
  "message": "缺少必填字段: 菜品名称, 售卖价"
}
```

### 2. 字段格式错误

**错误类型**: `FieldFormatError`

**常见错误**:
- 会员价 > 售卖价
- 保质期不在1-999范围内
- 条形码长度不在5-30位
- 计价方式不是"按份销售"或"称重销售"

**处理流程**:
1. 检测格式错误
2. 尝试自动修正
3. 若无法修正,生成错误报告
4. 提示用户修改

**错误报告格式**:
```json
{
  "error_type": "FieldFormatError",
  "field": "会员价",
  "value": 100,
  "message": "会员价(100)不能大于售卖价(88)"
}
```

### 3. 枚举值错误

**错误类型**: `InvalidEnumValueError`

**常见错误**:
- 计价方式: "按份" (正确: "按份销售")
- 辣度: "特辣" (正确: "重辣" 或 "爆辣")
- 售卖状态: "在卖" (正确: "在售")

**处理流程**:
1. 检测枚举值错误
2. 尝试自动修正 (模糊匹配)
3. 若无法修正,生成候选建议
4. 请求用户确认

**错误报告格式**:
```json
{
  "error_type": "InvalidEnumValueError",
  "field": "辣度",
  "value": "特辣",
  "candidates": ["重辣", "爆辣"],
  "message": "辣度值'特辣'不合法,建议使用: 重辣, 爆辣"
}
```

## 性能优化策略

### 1. 批量处理优化

**问题**: 处理100+菜品时,重复读取模板和数据源

**解决方案**:
- 缓存模板文件 (openpyxl Workbook对象)
- 缓存品牌库、分类数据
- 使用多进程并行处理

**代码示例**:
```python
from multiprocessing import Pool

def process_batch(batch_data, template_cache):
    results = []
    for data in batch_data:
        # 使用缓存的模板
        result = create_dish_from_cache(data, template_cache)
        results.append(result)
    return results

# 主流程
template_cache = load_template_cache()
batch_size = 50
batches = [batch_data[i:i+batch_size]
           for i in range(0, len(batch_data), batch_size)]

with Pool(4) as pool:
    results = pool.starmap(process_batch,
                          [(batch, template_cache) for batch in batches])
```

### 2. 字段验证优化

**问题**: 每个字段独立验证,重复执行

**解决方案**:
- 批量验证所有字段
- 缓存验证规则
- 跳过已验证的字段

**代码示例**:
```python
class FieldValidator:
    def __init__(self):
        self._validation_cache = {}

    def validate_batch(self, fields):
        errors = []
        for field_name, field_value in fields.items():
            if field_name in self._validation_cache:
                continue  # 跳过已验证字段

            error = self._validate_field(field_name, field_value)
            if error:
                errors.append(error)
            else:
                self._validation_cache[field_name] = True

        return errors
```

### 3. Excel生成优化

**问题**: 逐行写入Excel,性能较慢

**解决方案**:
- 批量写入数据到内存
- 一次性保存到文件
- 使用 `openpyxl` 的优化模式

**代码示例**:
```python
from openpyxl import load_workbook

def generate_excel_optimized(data_list, output_path):
    wb = load_workbook(template_path)
    ws = wb.active

    # 批量准备数据
    rows = []
    for data in data_list:
        row = [data.get(field) for field in FIELD_ORDER]
        rows.append(row)

    # 一次性写入
    for i, row in enumerate(rows, start=2):
        for j, value in enumerate(row, start=1):
            ws.cell(row=i, column=j, value=value)

    # 保存
    wb.save(output_path)
```

## 测试用例

### 1. 基础功能测试

**测试用例1: 单个菜品创建**
```python
def test_single_dish_creation():
    creator = DishCreator()
    result = creator.create_from_dict(
        data={
            "dish_name": "麻辣小龙虾",
            "brand": "吼巷",
            "category": "招牌菜/海鲜",
            "selling_price": 88
        },
        project_name="测试项目"
    )

    assert result["status"] == "success"
    assert os.path.exists(result["output_path"])
```

**测试用例2: 批量菜品创建**
```python
def test_batch_dish_creation():
    creator = DishCreator()
    batch_data = [
        {"dish_name": "麻辣小龙虾", "selling_price": 88},
        {"dish_name": "蒜蓉小龙虾", "selling_price": 88},
        {"dish_name": "十三香小龙虾", "selling_price": 88}
    ]

    results = creator.create_batch(
        batch_data=batch_data,
        project_name="批量测试"
    )

    assert len(results) == 3
    assert all(r["status"] == "success" for r in results)
```

### 2. 字段验证测试

**测试用例3: 必填字段验证**
```python
def test_required_field_validation():
    creator = DishCreator()

    with pytest.raises(MissingRequiredFieldError):
        creator.create_from_dict(
            data={"dish_name": "测试菜品"},  # 缺少售卖价
            project_name="测试项目"
        )
```

**测试用例4: 字段格式验证**
```python
def test_field_format_validation():
    creator = DishCreator()

    with pytest.raises(FieldFormatError):
        creator.create_from_dict(
            data={
                "dish_name": "测试菜品",
                "selling_price": 88,
                "member_price": 100  # 会员价 > 售卖价
            },
            project_name="测试项目"
        )
```

### 3. 智能推断测试

**测试用例5: 辣度推断**
```python
def test_spicy_level_inference():
    validator = FieldValidator()

    assert validator.infer_spicy_level("麻辣小龙虾") == "重辣"
    assert validator.infer_spicy_level("微辣口水鸡") == "微辣"
    assert validator.infer_spicy_level("清蒸鲈鱼") == "不辣"
```

**测试用例6: 拼音助记码生成**
```python
def test_pinyin_memo_generation():
    parser = TextParser()

    assert parser.generate_pinyin_memo("麻辣小龙虾") == "MLXLX"
    assert parser.generate_pinyin_memo("酸菜鱼") == "SCY"
```

## API参考

### DishCreator类

#### 初始化
```python
creator = DishCreator(
    template_path="plugins/美团组/templates/菜品导入模板.xlsx",
    use_cache=True
)
```

#### 方法

**create_from_text(text, project_name)**
- 参数:
  - `text` (str): 自然语言描述
  - `project_name` (str): 项目名称
- 返回: `dict` - 执行结果

**create_from_dict(data, project_name)**
- 参数:
  - `data` (dict): 结构化数据
  - `project_name` (str): 项目名称
- 返回: `dict` - 执行结果

**create_batch(batch_data, project_name)**
- 参数:
  - `batch_data` (list): 批量数据列表
  - `project_name` (str): 项目名称
- 返回: `list` - 执行结果列表

### FieldValidator类

#### 方法

**validate_required_fields(data)**
- 参数: `data` (dict) - 菜品数据
- 返回: `list` - 错误列表

**validate_field_format(field_name, field_value)**
- 参数:
  - `field_name` (str): 字段名称
  - `field_value` (Any): 字段值
- 返回: `dict` or `None` - 错误信息

**infer_spicy_level(dish_name)**
- 参数: `dish_name` (str) - 菜品名称
- 返回: `str` - 辣度级别

### TextParser类

#### 方法

**parse(text)**
- 参数: `text` (str) - 自然语言文本
- 返回: `dict` - 解析后的结构化数据

**generate_pinyin_memo(dish_name)**
- 参数: `dish_name` (str) - 菜品名称
- 返回: `str` - 拼音助记码
