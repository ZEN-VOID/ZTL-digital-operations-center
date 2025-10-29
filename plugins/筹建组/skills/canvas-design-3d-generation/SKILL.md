---
name: 3D模型生成(Image-to-3D)
description: 基于TripoSR的图像到3D模型重建。输入2D空间设计效果图,输出高质量3D模型(GLB/OBJ/FBX)。支持单视角和多视角融合,10-30秒快速生成。适用于空间可视化、VR/AR体验、建筑漫游。
---

# 3D模型生成 (Image-to-3D)

> 基于TripoSR技术的专业Image-to-3D重建,将2D效果图快速转换为高质量3D模型。

## 🎯 核心能力

- **快速生成**: 10-30秒/模型,支持批量处理
- **高质量输出**: GLB/OBJ/FBX格式,1024分辨率网格
- **多格式支持**: Web(GLB), 通用(OBJ), 游戏引擎(FBX), iOS AR(USDZ)
- **成本低廉**: $0.01-0.05/模型 (via Replicate API)
- **开源保底**: TripoSR开源,可本地部署

## 🚀 快速开始

### 基础用法

```bash
# 1. 设置API密钥
export REPLICATE_API_TOKEN="your-api-token"

# 2. 单个3D模型生成
python scripts/api_client.py generate \
    --image "entrance-new-chinese.png" \
    --format "glb" \
    --resolution 1024 \
    --output "entrance-3d.glb"

# 3. 批量生成(6个场景)
python scripts/api_client.py batch \
    --config "config/hotpot-3d-generation.json"
```

### 核心参数

| 参数 | 说明 | 推荐值 |
|------|------|--------|
| `image` | 输入图像路径 | PNG/JPG, ≥512x512 |
| `format` | 输出格式 | glb, obj, fbx |
| `resolution` | 网格分辨率 | 1024 |
| `enable_texture` | 生成纹理 | true |

## 📁 常见场景

### 场景1: 单个空间3D重建

从Z2效果图生成3D模型:

```bash
python scripts/api_client.py generate \
    --image "output/Z2/entrance-new-chinese.png" \
    --format "glb" \
    --output "output/Z3/entrance-3d.glb"
```

输出:
- `entrance-3d.glb`: Web可查看的3D模型

### 场景2: 批量场景生成

生成整店6个场景3D模型:

```bash
python scripts/api_client.py batch \
    --config "examples/hotpot-300sqm-3d.json"
```

输出:
- 6个GLB格式3D模型
- generation-report.json (元数据)

### 场景3: 多格式导出

同时生成GLB, OBJ, FBX:

```bash
python scripts/api_client.py generate \
    --image "entrance.png" \
    --formats "glb,obj,fbx" \
    --output-dir "output/multi-format/"
```

## 🛠️ 使用脚本

### scripts/api_client.py

整合TripoSR API调用和批量处理的统一客户端(推荐使用)。

**功能**:
- 单张3D模型生成
- 批量场景处理
- 多格式导出
- 自动重试和错误处理
- 生成元数据

**调用方式**:

```bash
# 查看帮助
python scripts/api_client.py --help

# 单张生成
python scripts/api_client.py generate [参数]

# 批量生成
python scripts/api_client.py batch --config config.json
```

### scripts/triposr_base.py

TripoSR API客户端基础模板,提供底层API调用能力。

**功能**:
- Replicate API封装
- 图像上传和处理
- 3D模型下载
- 错误处理和重试

**适用场景**: 需要自定义API调用逻辑时使用

### scripts/config_template.json

标准配置文件模板,包含:
- 执行配置(batch_size, 并发数)
- API配置(endpoint, model, timeout)
- 场景列表(scenes_to_generate)

复制模板创建配置:
```bash
cp scripts/config_template.json config/my-project.json
```

## ⚙️ 配置说明

### 基础配置

```json
{
  "generation_config": {
    "model": "triposr",
    "api_endpoint": "replicate.com/stability-ai/triposr",
    "version": "latest"
  },
  "batch_config": {
    "max_concurrent": 2,
    "retry_attempts": 3
  }
}
```

### 场景配置

```json
{
  "scene_id": "scene-01",
  "scene_name": "入口迎宾区",
  "input_image": "output/Z2/entrance.png",
  "parameters": {
    "format": "glb",
    "resolution": 1024,
    "enable_texture": true
  },
  "output_path": "output/Z3/entrance-3d.glb"
}
```

## 🚨 注意事项

1. **输入图像质量**:
   - 分辨率至少512x512 (推荐1024x1024)
   - 清晰无模糊
   - 室内透视视角

2. **生成质量**:
   - 单视角可能有遮挡区域
   - 复杂场景细节可能丢失
   - 建议使用多视角融合

3. **成本控制**:
   - 每个模型约$0.01-0.05
   - 批量生成前预估成本
   - 设置API配额限制

4. **格式选择**:
   - Web展示: GLB (体积小)
   - 通用: OBJ (兼容性好)
   - 游戏引擎: FBX (支持材质)

## 📊 性能参考

- **生成速度**: 10-30秒/模型
- **成功率**: ≥95%
- **质量**: ⭐⭐⭐⭐ 4/5
- **文件大小**: 10-50MB (GLB)
- **并行能力**: 2-3倍并行

## 📖 延伸阅读

- [TripoSR GitHub](https://github.com/VAST-AI-Research/TripoSR)
- [Replicate API文档](https://replicate.com/stability-ai/triposr)
- [GLB格式规范](https://www.khronos.org/gltf/)

---

**版本**: 1.0.0
**更新日期**: 2025-10-28
**状态**: ✅ 初版完成
**兼容性**: TripoSR via Replicate API
