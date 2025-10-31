# Adapter Development Guide - 适配器开发指南

> 如何为你的技能包创建适配器以使用通用并发执行引擎

## 📋 目录

1. [快速开始](#快速开始)
2. [适配器接口](#适配器接口)
3. [完整示例](#完整示例)
4. [最佳实践](#最佳实践)
5. [常见问题](#常见问题)

---

## 快速开始

### 步骤 1: 创建适配器文件

```bash
# 在你的技能包中创建适配器
touch .claude/skills/你的技能包/adapters/your_skill_adapter.py
```

### 步骤 2: 实现适配器类

```python
from .claude.skills.幻影之舞.universal_concurrent_executor.scripts.core import (
    SkillAdapter, TaskDefinition, TaskResult
)

class YourSkillAdapter(SkillAdapter):
    """你的技能包适配器"""

    def execute_task(self, task: TaskDefinition) -> TaskResult:
        """执行单个任务 (必须实现)"""
        # 1. 解析参数
        params = task.params

        # 2. 调用你的 API/工具
        result = your_api_call(**params)

        # 3. 包装为 TaskResult
        return TaskResult(
            task_id=task.task_id,
            status="success",
            start_time=0,  # 会被自动填充
            end_time=0,    # 会被自动填充
            duration=0,    # 会被自动填充
            output_files=[result.output_path]
        )
```

### 步骤 3: 使用适配器

```python
from .claude.skills.幻影之舞.universal_concurrent_executor.scripts.core import execute_plan
from .adapters.your_skill_adapter import YourSkillAdapter

adapter = YourSkillAdapter()
report = execute_plan(
    plan_path="output/项目名/your-skill/plans/execution_plan.json",
    adapter=adapter
)
```

---

## 适配器接口

### 必须实现的方法

#### `execute_task(task: TaskDefinition) -> TaskResult`

**职责**: 执行单个任务的核心逻辑

**参数**:
- `task`: TaskDefinition 对象,包含:
  - `task.task_id`: 任务唯一标识
  - `task.params`: 任务参数字典
  - `task.depends_on`: 依赖的任务ID列表
  - `task.metadata`: 额外元数据

**返回**: TaskResult 对象,必须包含:
- `task_id`: 任务ID
- `status`: "success" | "failed" | "skipped"
- `output_files`: 输出文件路径列表
- `error_message`: 错误信息 (如果失败)

**示例**:

```python
def execute_task(self, task: TaskDefinition) -> TaskResult:
    # 解析参数
    input_file = task.params["input_file"]
    output_file = task.params["output_file"]

    # 调用你的工具
    result = my_tool.process(input_file, output_file)

    # 包装结果
    return TaskResult(
        task_id=task.task_id,
        status="success" if result.ok else "failed",
        start_time=0,
        end_time=0,
        duration=0,
        output_files=[output_file],
        error_message=None if result.ok else result.error
    )
```

### 可选覆盖的方法

#### `validate_params(params: Dict[str, Any]) -> bool`

**职责**: 验证任务参数是否有效

**默认实现**: 总是返回 True

**何时覆盖**: 当需要严格的参数验证时

**示例**:

```python
def validate_params(self, params: Dict[str, Any]) -> bool:
    # 检查必需字段
    required = ["input_file", "output_file", "format"]
    if not all(key in params for key in required):
        return False

    # 检查文件存在
    if not Path(params["input_file"]).exists():
        return False

    # 检查格式有效
    valid_formats = ["png", "jpg", "pdf"]
    if params["format"] not in valid_formats:
        return False

    return True
```

#### `pre_execute_hook(task: TaskDefinition) -> None`

**职责**: 任务执行前的准备工作

**默认实现**: 空操作

**何时覆盖**: 需要预处理(如创建目录、检查环境、记录日志)

**示例**:

```python
def pre_execute_hook(self, task: TaskDefinition) -> None:
    # 创建输出目录
    output_dir = Path(task.params["output_file"]).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    # 记录日志
    logger.info(f"准备执行任务: {task.task_id}")
    logger.debug(f"参数: {task.params}")
```

#### `post_execute_hook(task: TaskDefinition, result: TaskResult) -> None`

**职责**: 任务执行后的清理/通知工作

**默认实现**: 空操作

**何时覆盖**: 需要后处理(如上传文件、发送通知、清理临时文件)

**示例**:

```python
def post_execute_hook(self, task: TaskDefinition, result: TaskResult) -> None:
    # 上传到云存储
    if result.status == "success":
        for file in result.output_files:
            cloud_storage.upload(file)

    # 清理临时文件
    if task.metadata and task.metadata.get("cleanup_temp"):
        temp_dir = Path("/tmp") / task.task_id
        shutil.rmtree(temp_dir, ignore_errors=True)

    # 记录成功/失败
    logger.info(f"任务完成: {task.task_id}, 状态: {result.status}")
```

---

## 完整示例

### 示例 1: 图片处理适配器

```python
from pathlib import Path
from PIL import Image
from .claude.skills.幻影之舞.universal_concurrent_executor.scripts.core import (
    SkillAdapter, TaskDefinition, TaskResult
)

class ImageProcessingAdapter(SkillAdapter):
    """图片处理适配器"""

    def __init__(self):
        self.supported_formats = ["png", "jpg", "jpeg", "webp"]

    def execute_task(self, task: TaskDefinition) -> TaskResult:
        """执行图片处理任务"""
        try:
            # 解析参数
            input_path = task.params["input_image"]
            output_path = task.params["output_image"]
            operation = task.params["operation"]  # resize, rotate, crop

            # 加载图片
            img = Image.open(input_path)

            # 执行操作
            if operation == "resize":
                width = task.params["width"]
                height = task.params["height"]
                img = img.resize((width, height))
            elif operation == "rotate":
                angle = task.params["angle"]
                img = img.rotate(angle)
            elif operation == "crop":
                box = task.params["crop_box"]  # (left, top, right, bottom)
                img = img.crop(box)

            # 保存结果
            img.save(output_path)

            return TaskResult(
                task_id=task.task_id,
                status="success",
                start_time=0,
                end_time=0,
                duration=0,
                output_files=[output_path]
            )

        except Exception as e:
            return TaskResult(
                task_id=task.task_id,
                status="failed",
                start_time=0,
                end_time=0,
                duration=0,
                error_message=str(e)
            )

    def validate_params(self, params: Dict[str, Any]) -> bool:
        """验证参数"""
        # 检查必需字段
        required = ["input_image", "output_image", "operation"]
        if not all(key in params for key in required):
            return False

        # 检查输入文件存在
        if not Path(params["input_image"]).exists():
            return False

        # 检查操作类型
        valid_operations = ["resize", "rotate", "crop"]
        if params["operation"] not in valid_operations:
            return False

        # 检查操作特定参数
        if params["operation"] == "resize":
            if "width" not in params or "height" not in params:
                return False

        return True

    def pre_execute_hook(self, task: TaskDefinition) -> None:
        """执行前创建输出目录"""
        output_dir = Path(task.params["output_image"]).parent
        output_dir.mkdir(parents=True, exist_ok=True)
```

### 示例 2: 网页爬虫适配器

```python
import requests
from bs4 import BeautifulSoup
from .claude.skills.幻影之舞.universal_concurrent_executor.scripts.core import (
    SkillAdapter, TaskDefinition, TaskResult
)

class WebScrapingAdapter(SkillAdapter):
    """网页爬虫适配器"""

    def __init__(self, rate_limit: float = 1.0):
        self.rate_limit = rate_limit
        self.last_request_time = 0

    def execute_task(self, task: TaskDefinition) -> TaskResult:
        """执行网页爬取任务"""
        try:
            # 解析参数
            url = task.params["url"]
            selector = task.params.get("selector")
            output_file = task.params["output_file"]

            # 限流
            import time
            current_time = time.time()
            if current_time - self.last_request_time < self.rate_limit:
                time.sleep(self.rate_limit - (current_time - self.last_request_time))
            self.last_request_time = time.time()

            # 爬取网页
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            # 解析HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # 提取数据
            if selector:
                elements = soup.select(selector)
                data = [el.text.strip() for el in elements]
            else:
                data = soup.get_text()

            # 保存结果
            with open(output_file, 'w', encoding='utf-8') as f:
                if isinstance(data, list):
                    f.write('\n'.join(data))
                else:
                    f.write(data)

            return TaskResult(
                task_id=task.task_id,
                status="success",
                start_time=0,
                end_time=0,
                duration=0,
                output_files=[output_file],
                api_response={"status_code": response.status_code}
            )

        except Exception as e:
            return TaskResult(
                task_id=task.task_id,
                status="failed",
                start_time=0,
                end_time=0,
                duration=0,
                error_message=str(e)
            )

    def validate_params(self, params: Dict[str, Any]) -> bool:
        """验证参数"""
        required = ["url", "output_file"]
        return all(key in params for key in required)

    def pre_execute_hook(self, task: TaskDefinition) -> None:
        """执行前准备"""
        output_dir = Path(task.params["output_file"]).parent
        output_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"准备爬取: {task.params['url']}")
```

### 示例 3: Excel 数据处理适配器

```python
import pandas as pd
from .claude.skills.幻影之舞.universal_concurrent_executor.scripts.core import (
    SkillAdapter, TaskDefinition, TaskResult
)

class ExcelProcessingAdapter(SkillAdapter):
    """Excel 数据处理适配器"""

    def execute_task(self, task: TaskDefinition) -> TaskResult:
        """执行Excel处理任务"""
        try:
            # 解析参数
            input_file = task.params["input_excel"]
            output_file = task.params["output_excel"]
            operation = task.params["operation"]  # filter, aggregate, merge

            # 读取Excel
            df = pd.read_excel(input_file)

            # 执行操作
            if operation == "filter":
                condition = task.params["condition"]
                df = df.query(condition)
            elif operation == "aggregate":
                group_by = task.params["group_by"]
                agg_func = task.params["agg_func"]
                df = df.groupby(group_by).agg(agg_func)
            elif operation == "merge":
                other_file = task.params["other_excel"]
                df_other = pd.read_excel(other_file)
                on_column = task.params["on"]
                df = pd.merge(df, df_other, on=on_column)

            # 保存结果
            df.to_excel(output_file, index=False)

            return TaskResult(
                task_id=task.task_id,
                status="success",
                start_time=0,
                end_time=0,
                duration=0,
                output_files=[output_file],
                api_response={"rows": len(df), "columns": len(df.columns)}
            )

        except Exception as e:
            return TaskResult(
                task_id=task.task_id,
                status="failed",
                start_time=0,
                end_time=0,
                duration=0,
                error_message=str(e)
            )
```

---

## 最佳实践

### 1. 错误处理

```python
def execute_task(self, task: TaskDefinition) -> TaskResult:
    try:
        # 你的逻辑
        result = do_work(task.params)

        return TaskResult(
            task_id=task.task_id,
            status="success",
            start_time=0,
            end_time=0,
            duration=0,
            output_files=[result.output]
        )

    except FileNotFoundError as e:
        # 文件不存在
        return TaskResult(
            task_id=task.task_id,
            status="failed",
            start_time=0,
            end_time=0,
            duration=0,
            error_message=f"文件不存在: {e}"
        )

    except requests.HTTPError as e:
        # HTTP错误
        return TaskResult(
            task_id=task.task_id,
            status="failed",
            start_time=0,
            end_time=0,
            duration=0,
            error_message=f"HTTP错误: {e.response.status_code}"
        )

    except Exception as e:
        # 通用错误
        return TaskResult(
            task_id=task.task_id,
            status="failed",
            start_time=0,
            end_time=0,
            duration=0,
            error_message=f"未知错误: {str(e)}"
        )
```

### 2. 日志记录

```python
import logging

logger = logging.getLogger(__name__)

def execute_task(self, task: TaskDefinition) -> TaskResult:
    logger.info(f"开始执行任务: {task.task_id}")
    logger.debug(f"参数: {task.params}")

    try:
        result = do_work(task.params)
        logger.info(f"任务成功: {task.task_id}")
        return TaskResult(...)

    except Exception as e:
        logger.error(f"任务失败: {task.task_id}, 错误: {e}")
        return TaskResult(...)
```

### 3. 资源管理

```python
def execute_task(self, task: TaskDefinition) -> TaskResult:
    # 使用上下文管理器确保资源释放
    with open(task.params["input_file"], 'r') as f:
        data = f.read()

    # 或者显式清理
    try:
        resource = acquire_resource()
        result = process(resource)
    finally:
        release_resource(resource)

    return TaskResult(...)
```

### 4. 参数验证

```python
def validate_params(self, params: Dict[str, Any]) -> bool:
    # 1. 检查必需字段
    required = ["input", "output"]
    if not all(key in params for key in required):
        logger.error(f"缺少必需参数: {required}")
        return False

    # 2. 检查类型
    if not isinstance(params["input"], str):
        logger.error("参数 'input' 必须是字符串")
        return False

    # 3. 检查值范围
    if params.get("threshold", 0) < 0 or params["threshold"] > 1:
        logger.error("参数 'threshold' 必须在 [0, 1] 范围内")
        return False

    return True
```

---

## 常见问题

### Q1: 如何处理依赖其他任务的任务?

**A**: 在执行计划中使用 `depends_on` 字段:

```json
{
  "task_id": "video-task",
  "depends_on": ["image-task"],
  "params": {
    "first_frame_image": "output/image-task/result.png"
  }
}
```

通用执行器会自动检测依赖并按顺序执行。

### Q2: 如何共享适配器状态(如API客户端)?

**A**: 在适配器的 `__init__` 中初始化共享资源:

```python
class MyAdapter(SkillAdapter):
    def __init__(self):
        self.api_client = create_api_client()
        self.cache = {}

    def execute_task(self, task: TaskDefinition) -> TaskResult:
        # 使用共享的 api_client 和 cache
        result = self.api_client.call(task.params)
        return TaskResult(...)
```

### Q3: 如何实现重试机制?

**A**: 在 `execute_task` 中添加重试逻辑:

```python
def execute_task(self, task: TaskDefinition) -> TaskResult:
    max_retries = task.params.get("max_retries", 3)

    for attempt in range(max_retries):
        try:
            result = do_work(task.params)
            return TaskResult(status="success", ...)

        except TransientError as e:
            if attempt == max_retries - 1:
                return TaskResult(status="failed", error_message=str(e), ...)
            time.sleep(2 ** attempt)  # 指数退避
```

### Q4: 如何支持进度追踪?

**A**: 使用 `metadata` 字段记录进度:

```python
def execute_task(self, task: TaskDefinition) -> TaskResult:
    total_steps = 100
    for i in range(total_steps):
        # 执行工作
        do_step(i)

        # 更新进度 (可选: 通过日志或回调)
        progress = (i + 1) / total_steps * 100
        logger.info(f"任务 {task.task_id} 进度: {progress:.1f}%")

    return TaskResult(...)
```

---

**更多帮助**: 参考 `plugins/创意组/skills/AIGC/nano-banana/` 和 `plugins/创意组/skills/AIGC/minimax/` 中的实际适配器实现。
