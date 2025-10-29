# 3D模型生成 (Canvas Design - 3D Generation)

> 基于TripoSR的Image-to-3D重建技能包

## 概述

本技能包为Z3-3D生成AIGC助手提供专业的Image-to-3D重建能力,通过TripoSR技术将2D空间设计效果图快速转换为高质量3D模型。

## 核心特性

- **技术**: TripoSR (Stability AI + Tripo AI)
- **输入**: 2D效果图(PNG/JPG, ≥512x512)
- **输出**: 3D模型(GLB/OBJ/FBX)
- **速度**: 10-30秒/模型
- **成本**: $0.01-0.05/模型 (via Replicate API)
- **质量**: ⭐⭐⭐⭐ 4/5

## 快速开始

### 1. 环境准备

```bash
# 设置Replicate API Token
export REPLICATE_API_TOKEN="your-api-token"

# 安装依赖
pip install requests
```

### 2. 单个3D模型生成

```bash
cd plugins/筹建组/skills/canvas-design-3d-generation

python scripts/api_client.py generate \
    --image "entrance-new-chinese.png" \
    --format "glb" \
    --output "entrance-3d.glb"
```

### 3. 批量生成

```bash
# 使用配置文件
python scripts/api_client.py batch \
    --config "scripts/config_template.json" \
    --output-dir "output/3d-models/"
```

## 目录结构

```
canvas-design-3d-generation/
├── SKILL.md                    # 技能包元数据
├── README.md                   # 本文件
├── scripts/
│   ├── api_client.py           # TripoSR API客户端
│   ├── triposr_base.py         # 底层API封装
│   └── config_template.json    # 配置模板
└── examples/
    └── hotpot-300sqm-3d.json   # 完整项目示例
```

## 配置文件格式

### project_info
```json
{
  "project_name": "火锅店开业筹备",
  "z3_task_id": "Z3-3D-20251028-001"
}
```

### scenes_to_generate
```json
{
  "scene_name": "入口迎宾区",
  "input_image": "path/to/entrance.png",
  "parameters": {
    "format": "glb",
    "resolution": 1024
  },
  "output_path": "output/entrance-3d.glb"
}
```

## 支持的3D格式

| 格式 | 适用场景 | 特点 |
|------|---------|------|
| **GLB** | Web 3D查看器, AR | 紧凑,包含纹理 |
| **OBJ** | 通用3D软件 | 广泛支持 |
| **FBX** | Unity, Unreal Engine | 游戏引擎标准 |

## 成本估算

**典型300㎡火锅店**:
- 场景数量: 6个
- 单模型成本: $0.04
- 总成本: $0.24

## 性能参考

- 生成速度: 10-30秒/模型
- 成功率: ≥95%
- 质量评分: 4/5
- 文件大小: 10-50MB (GLB)

## 注意事项

1. **输入图像**: 需要清晰、完整的空间效果图
2. **单视角限制**: 遮挡区域质量可能较差
3. **API配额**: 注意Replicate API使用限制
4. **成本控制**: 批量生成前预估成本

## 相关文档

- [Z3智能体定义](../../agents/Z3-3D生成AIGC助手.md)
- [技术调研报告](../../../../reports/Phase3-3D生成技术调研报告.md)
- [TripoSR GitHub](https://github.com/VAST-AI-Research/TripoSR)

## 更新日志

### v1.0.0 (2025-10-28)
- ✅ 初版发布
- ✅ TripoSR API集成
- ✅ 单张和批量生成
- ✅ 配置文件驱动

## 许可证

本技能包为ZTL数智化作战中心内部使用。
