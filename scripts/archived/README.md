# Scripts 归档说明

本目录存放已归档的脚本文件,这些脚本在开发过程中使用过,但现已被核心脚本替代或完成历史使命。

## 归档时间
2025-10-06

## 目录结构

### 1. deprecated/ - 已废弃脚本
存放已被新版本替代的旧脚本,保留用于参考和回溯。

**主要脚本**:
- `batch_replace_*.py` - 旧版批量替换脚本(已被batch_replace_images.py替代)
- `fetch_figma_*.py` - 旧版Figma数据获取(已被API项目替代)
- `figma_to_next.py` - 旧版Figma转Next.js(已被完善版替代)
- `random_url_combination.py` - 旧版随机组合(已被batch版替代)

**废弃原因**: 功能重复、设计过时、已有更好的替代方案

### 2. process-scripts/ - 过程性脚本
存放特定任务或临时分析使用的一次性脚本。

**主要脚本**:
- `analyze_frame20_visual.py` - Frame20视觉元素分析
- `auto_batch_three_day_tour.py` - three-day-tour特定自动化
- `check_dimensions.py` - 临时尺寸检查工具
- `extract_*.py` - 各类临时信息提取工具
- `convert_random_json.py` - JSON格式转换(一次性任务)
- `remove_heic_from_json.py` - HEIC文件清理(一次性任务)
- `split_combined_json.py` - JSON拆分工具(一次性任务)

**归档原因**: 特定任务已完成、临时分析工具、一次性使用

### 3. test-scripts/ - 测试脚本
存放开发期间使用的测试和验证脚本。

**主要脚本**:
- `test_selector.py` - CSS选择器测试
- `verify_json_format.py` - JSON格式验证

**归档原因**: 开发验证已完成,功能已集成到核心脚本

## 核心脚本 (保留在scripts/)

以下脚本为当前项目的核心工具,保留在`scripts/`根目录:

1. **batch_replace_images.py** - 核心批量图片替换脚本
   - 支持精确映射和通用选择器两种模式
   - 完整的配置驱动流程
   - 自动截图和输出管理

2. **batch_extract_cos_urls.py** - 腾讯云COS URL批量提取
   - 从COS存储桶提取图片URL
   - 生成标准化JSON索引

3. **batch_random_url_combination.py** - 随机URL组合生成器
   - 从多个模板目录随机抽取URL
   - 生成批量组合配置

4. **random_image_combiner.py** - 图片组合工具
   - 单次随机组合生成
   - 支持自定义配置

5. **check-dependencies.sh** - 项目依赖检查
   - 验证Python环境和必需包
   - 系统环境检查

## 使用建议

### 归档脚本用途
- **学习参考**: 了解历史实现方案和设计思路
- **功能回溯**: 需要恢复某些历史功能时参考
- **问题排查**: 对比新旧实现定位问题

### 清理策略
建议每3个月评估一次归档脚本:
- 完全无用的脚本可以删除
- 有参考价值的继续保留
- 发现仍需使用的脚本可以恢复到scripts/

## 恢复方法

如需恢复某个归档脚本:

```bash
# 从归档目录移回scripts/
mv scripts/archived/deprecated/script_name.py scripts/

# 或复制一份
cp scripts/archived/deprecated/script_name.py scripts/
```

## 相关文档

- 核心脚本使用文档: [scripts/README.md](../README.md)
- 配置文件说明: [scripts/configs/README.md](../configs/README.md)
- 项目开发规范: [CLAUDE.md](../../.claude/CLAUDE.md)

---

**维护说明**: 本归档由AI辅助整理,归档决策基于脚本的使用频率、功能重复度和项目演进需求。
