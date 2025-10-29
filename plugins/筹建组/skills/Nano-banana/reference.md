# Nano Banana API 详细参考

> 本文档提供Nano Banana衍生图生成的完整API参数说明、配置选项和技术细节。

## 📡 API概述

### 基础信息

- **模型**: Nano Banana v1
- **提供商**: OpenRouter (google/gemini-2.5-flash-image-preview)
- **端点**: `https://openrouter.ai/api/v1/chat/completions`
- **认证方式**: Bearer Token (API Key)
- **输入格式**: Multimodal (Text + Image)
- **输出格式**: Base64编码的PNG图像

### 技术特性

| 特性 | 规格 |
|------|------|
| 输入分辨率 | 任意（建议≥512x512） |
| 输出分辨率 | 1024x1024 |
| 输出格式 | PNG（无损）|
| 平均生成时间 | 16.5秒 |
| 最大并发数 | 8个请求 |
| 超时设置 | 60秒 |

## ⚙️ 核心参数详解

### 1. variation_instruction（变化指令）

完整的变化指令对象包含以下字段：

```json
{
  "description": "string",           // 变化的简短描述
  "keep_consistent": ["string"],     // 保持一致的元素列表
  "change_elements": ["string"],     // 需要改变的元素列表
  "nano_banana_parameters": {        // Nano Banana特定参数
    "strength": 0.65,                // 变化强度 (0.4-0.8)
    "prompt_weight": "string"        // 提示词权重增强
  }
}
```

#### 1.1 description（必需）

**类型**: `string`
**说明**: 对本次变化的简短描述，用于文件命名和日志记录

**示例**:
```json
"description": "角色转身动作"
"description": "表情变化-微笑"
"description": "场景光线调整"
```

#### 1.2 keep_consistent（必需）

**类型**: `array<string>`
**说明**: 必须保持一致的元素列表，至少包含1个元素

**常见元素类别**:

1. **角色特征**:
   ```json
   ["角色服装", "发型特征", "面部特征", "体型特征"]
   ```

2. **风格特征**:
   ```json
   ["赛博朋克风格", "画风", "色调", "质感", "光影效果"]
   ```

3. **场景特征**:
   ```json
   ["背景场景", "环境氛围", "天气状态", "时间设定"]
   ```

**最佳实践**:
- ✅ 描述具体: "角色的黑色皮夹克" 而非 "衣服"
- ✅ 分层描述: 角色→服装→细节
- ❌ 避免模糊: "整体感觉" ❌

#### 1.3 change_elements（必需）

**类型**: `array<string>`
**说明**: 需要改变的元素列表，每个元素应清晰描述变化方向

**格式建议**:
```
"[元素类别]: [变化方向]"
```

**示例**:

1. **姿态动作**:
   ```json
   [
     "身体姿态: 从正面转为侧面",
     "头部角度: 微微转向右侧",
     "手臂位置: 自然摆动"
   ]
   ```

2. **表情变化**:
   ```json
   [
     "面部表情: 从平静变为微笑",
     "眼神: 更加温和",
     "嘴角: 微微上扬"
   ]
   ```

3. **场景变化**:
   ```json
   [
     "光线方向: 从正面改为侧面",
     "环境亮度: 稍微调暗",
     "背景虚化: 增强景深效果"
   ]
   ```

**最佳实践**:
- ✅ 描述具体: "身体角度从正面转为右侧45度"
- ✅ 包含方向: "从...到..." 或 "增强/减弱"
- ✅ 一次专注: 不要同时变化太多维度
- ❌ 避免冲突: 变化不要与keep_consistent重叠

#### 1.4 strength（变化强度）

**类型**: `float`
**范围**: `0.4 - 0.8`
**默认值**: `0.6`

**强度分级表**:

| 强度范围 | 变化程度 | 适用场景 | 示例 |
|---------|---------|---------|------|
| 0.4-0.5 | 轻微 | 表情微调、视角微调 | 微笑→浅笑 |
| 0.5-0.6 | 中轻 | 小幅姿态变化 | 正面→轻微侧面 |
| 0.6-0.7 | 中等 | 明显姿态、动作变化 | 站立→行走 |
| 0.7-0.8 | 较大 | 场景元素、光影变化 | 白天→黄昏 |

**调参建议**:
```python
# 保守策略：从低值开始尝试
strength = 0.55  # 先测试低强度
# 如果变化不够明显，再逐步提高
strength = 0.65
strength = 0.75

# 激进策略：快速迭代（不推荐）
strength = 0.75  # 可能丢失一致性
```

#### 1.5 prompt_weight（提示词权重增强）

**类型**: `string`（可选）
**说明**: 用于增强某些变化方向的提示词，辅助AI理解

**使用场景**:
- 强调特定动作: `"turning around, dynamic twist"`
- 强调情绪表现: `"happy smile, warm expression"`
- 强调物理特性: `"natural motion, realistic movement"`

**示例**:
```json
{
  "change_elements": ["身体转身动作"],
  "prompt_weight": "turning around, smooth rotation, natural body mechanics"
}
```

**注意**: 该字段为辅助性质，主要依赖change_elements的描述。

### 2. execution_config（执行配置）

批量生成的执行配置：

```json
{
  "batch_size": 2,                // 每批处理数量
  "max_concurrent_requests": 2,   // 最大并发请求数
  "retry_attempts": 3,            // 失败重试次数
  "retry_delay_seconds": 5        // 重试间隔（秒）
}
```

#### 2.1 batch_size

**类型**: `int`
**范围**: `1-10`
**默认值**: `2`
**说明**: 每批处理的任务数量

**建议值**:
- 快速测试: `1-2`
- 正常生产: `2-4`
- 大批量: `5-8`

#### 2.2 max_concurrent_requests

**类型**: `int`
**范围**: `1-8`
**默认值**: `2`
**说明**: 同时执行的API请求数

**性能影响**:
```
并发数 = 2: 2张图 × 16.5秒 = ~33秒
并发数 = 4: 4张图 × 16.5秒 = ~33秒（并行）
并发数 = 8: 8张图 × 16.5秒 = ~33秒（并行）
```

**限制因素**:
- API配额限制
- 网络带宽
- 本地内存

#### 2.3 retry_attempts

**类型**: `int`
**范围**: `0-5`
**默认值**: `3`
**说明**: 任务失败时的最大重试次数

**重试触发条件**:
- API请求超时
- 网络连接错误
- 服务器临时错误 (5xx)
- 限流错误 (429)

**不重试的错误**:
- 参数验证失败 (400)
- 认证失败 (401)
- 配额耗尽 (402)

### 3. api_config（API配置）

```json
{
  "endpoint": "https://openrouter.ai/api/v1/chat/completions",
  "model": "google/gemini-2.5-flash-image-preview",
  "timeout_seconds": 60,
  "api_key": "sk-or-v1-xxx"  // 从环境变量读取
}
```

#### 3.1 endpoint

**类型**: `string`
**默认值**: `"https://openrouter.ai/api/v1/chat/completions"`
**说明**: OpenRouter API端点

#### 3.2 model

**类型**: `string`
**默认值**: `"google/gemini-2.5-flash-image-preview"`
**说明**: 使用的模型标识符

**替代模型**:
- `google/gemini-2.5-flash`: 更快但图像质量略低
- `google/gemini-2.0-flash-exp`: 实验性版本

#### 3.3 timeout_seconds

**类型**: `int`
**范围**: `30-120`
**默认值**: `60`
**说明**: API请求超时时间

**建议值**:
- 快速测试: `30秒`
- 正常使用: `60秒`
- 复杂任务: `90-120秒`

## 📋 完整配置示例

### 单任务配置

```json
{
  "plan_id": "nano-character-turn-20251019",
  "agent_id": "Nano-banana",
  "execution_config": {
    "batch_size": 1,
    "max_concurrent_requests": 1,
    "retry_attempts": 3
  },
  "api_config": {
    "model": "google/gemini-2.5-flash-image-preview",
    "timeout_seconds": 60
  },
  "batches": [
    {
      "batch_id": 1,
      "tasks": [
        {
          "task_id": "turn-001",
          "reference_image": "output/project/character-base.png",
          "variation_instruction": {
            "description": "角色转身动作",
            "keep_consistent": [
              "赛博朋克风格",
              "角色服装",
              "发型特征"
            ],
            "change_elements": [
              "身体姿态: 从正面转为侧面"
            ],
            "nano_banana_parameters": {
              "strength": 0.65,
              "prompt_weight": "turning around, natural motion"
            }
          }
        }
      ]
    }
  ]
}
```

### 批量任务配置

```json
{
  "plan_id": "nano-expression-batch-20251019",
  "agent_id": "Nano-banana",
  "execution_config": {
    "batch_size": 2,
    "max_concurrent_requests": 2,
    "retry_attempts": 3
  },
  "batches": [
    {
      "batch_id": 1,
      "tasks": [
        {
          "task_id": "expr-smile",
          "reference_image": "base.png",
          "variation_instruction": {
            "description": "微笑表情",
            "keep_consistent": ["姿态", "背景"],
            "change_elements": ["表情: 微笑"],
            "nano_banana_parameters": {
              "strength": 0.50
            }
          }
        },
        {
          "task_id": "expr-surprise",
          "reference_image": "base.png",
          "variation_instruction": {
            "description": "惊讶表情",
            "keep_consistent": ["姿态", "背景"],
            "change_elements": ["表情: 惊讶"],
            "nano_banana_parameters": {
              "strength": 0.55
            }
          }
        }
      ]
    }
  ]
}
```

## 🚨 错误处理

### 常见错误码

| 错误码 | 说明 | 解决方案 |
|-------|------|---------|
| 400 | 参数验证失败 | 检查配置文件格式 |
| 401 | 认证失败 | 检查API Key |
| 402 | 配额不足 | 充值或等待配额恢复 |
| 429 | 请求过于频繁 | 降低并发数或增加延迟 |
| 500 | 服务器错误 | 稍后重试 |
| 504 | 请求超时 | 增加timeout或稍后重试 |

### 错误日志格式

```json
{
  "error_type": "API_ERROR",
  "error_code": 429,
  "error_message": "Rate limit exceeded",
  "task_id": "turn-001",
  "timestamp": "2025-10-19T10:30:00Z",
  "retry_count": 1,
  "max_retries": 3
}
```

## 📊 性能优化

### 1. 并发优化

```python
# 小批量高并发
execution_config = {
    "batch_size": 2,
    "max_concurrent_requests": 4  # 每批2个任务，同时处理2批
}

# 大批量中并发
execution_config = {
    "batch_size": 4,
    "max_concurrent_requests": 2
}
```

### 2. 网络优化

```python
# 使用本地参考图像（避免上传大文件）
reference_image = "/local/path/image.png"

# 结果保存到本地（避免网络传输）
output_path = "/local/output/"
```

### 3. 成本优化

```python
# 使用适当的strength值（避免多次重试）
strength = 0.60  # 从中等值开始

# 批量生成减少固定开销
batch_size = 4   # 而非每次1个
```

## 🔒 安全与限制

### 输入验证

```python
# 参考图像验证
- 文件存在性检查
- 文件大小限制: <10MB
- 格式检查: PNG/JPG/JPEG
- 分辨率检查: ≥512x512

# 参数验证
- strength范围: 0.4-0.8
- keep_consistent非空
- change_elements非空
```

### 配额管理

```python
# 预估成本
estimated_credits = num_tasks * 5  # 每张图约5积分

# 预算检查
if estimated_credits > budget_limit:
    request_user_confirmation()
```

### 数据隐私

- 参考图像仅用于生成，不会被保存到服务器
- 生成结果自动保存到本地output目录
- API Key从环境变量读取，不会被记录到日志

---

**版本**: 2.0.0
**更新日期**: 2025-10-19
