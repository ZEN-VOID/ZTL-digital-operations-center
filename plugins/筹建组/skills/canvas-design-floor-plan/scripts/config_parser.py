"""
Config Parser - 配置文档解析器

解析Markdown格式的平面图配置文档
"""

import re
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)


def parse_config(config_md_path: str) -> Dict:
    """
    解析平面图配置.md文档

    Args:
        config_md_path: 配置文档路径

    Returns:
        Dict 结构化配置数据
    """

    logger.info(f"解析配置文档: {config_md_path}")

    with open(config_md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    config = {
        'basic_info': {},
        'zones': {},
        'flows': {},
        'visual_style': {},
        'canvas_params': {}
    }

    # 解析基础信息
    basic_info_section = _extract_section(content, "基础信息")
    if basic_info_section:
        config['basic_info'] = _parse_basic_info(basic_info_section)

    # 解析功能分区
    zones_section = _extract_section(content, "功能分区布局")
    if zones_section:
        config['zones'] = _parse_zones(zones_section)

    # 解析动线设计
    flows_section = _extract_section(content, "动线设计")
    if flows_section:
        config['flows'] = _parse_flows(flows_section)

    # 解析视觉风格
    visual_section = _extract_section(content, "视觉风格要求")
    if visual_section:
        config['visual_style'] = _parse_visual_style(visual_section)

    # 解析canvas-design参数
    canvas_section = _extract_section(content, "canvas-design调用参数")
    if canvas_section:
        config['canvas_params'] = _parse_canvas_params(canvas_section)

    return config


def validate_config(config: Dict) -> bool:
    """
    验证配置完整性

    Args:
        config: 配置字典

    Raises:
        ValueError: 如果缺少必需字段

    Returns:
        bool 验证通过返回True
    """

    required_fields = [
        ('basic_info', 'project_name'),
        ('basic_info', 'total_area'),
        ('zones',),
        ('visual_style',)
    ]

    for field_path in required_fields:
        current = config
        for key in field_path:
            if key not in current or not current[key]:
                raise ValueError(f"缺少必需字段: {' -> '.join(field_path)}")
            current = current[key]

    logger.info("✅ 配置验证通过")
    return True


def _extract_section(content: str, section_name: str) -> str:
    """提取Markdown章节内容"""

    pattern = rf"##\s+{re.escape(section_name)}\s*\n(.*?)(?=\n##|\Z)"
    match = re.search(pattern, content, re.DOTALL)

    return match.group(1).strip() if match else ""


def _parse_basic_info(section: str) -> Dict:
    """解析基础信息"""

    info = {}

    # 提取项目名称
    match = re.search(r'\*\*项目名称\*\*:\s*(.+)', section)
    if match:
        info['project_name'] = match.group(1).strip()

    # 提取空间尺寸
    match = re.search(r'\*\*空间尺寸\*\*:\s*(.+)', section)
    if match:
        size_str = match.group(1).strip()
        # 解析 "300㎡ (长20m × 宽15m)"
        total_match = re.search(r'(\d+)㎡', size_str)
        if total_match:
            info['total_area'] = f"{total_match.group(1)}㎡"

        dims_match = re.search(r'长(\d+)m\s*[×x]\s*宽(\d+)m', size_str)
        if dims_match:
            info['length'] = f"{dims_match.group(1)}m"
            info['width'] = f"{dims_match.group(2)}m"

    # 提取层高
    match = re.search(r'\*\*层高\*\*:\s*(.+)', section)
    if match:
        info['ceiling_height'] = match.group(1).strip()

    # 提取风格
    match = re.search(r'\*\*风格\*\*:\s*(.+)', section)
    if match:
        info['style'] = match.group(1).strip()

    return info


def _parse_zones(section: str) -> Dict:
    """解析功能分区"""

    zones = {}

    # 提取所有三级标题作为区域名称
    zone_pattern = r'###\s+(.+?)\s+\((\d+)㎡\)\s*\n(.*?)(?=\n###|\Z)'
    matches = re.finditer(zone_pattern, section, re.DOTALL)

    for match in matches:
        zone_name = match.group(1).strip()
        zone_area = match.group(2).strip()
        zone_content = match.group(3).strip()

        zones[zone_name] = {
            'area': f"{zone_area}㎡",
            'raw_content': zone_content
        }

        # TODO: 进一步解析zone_content中的位置、元素、设计要点

    return zones


def _parse_flows(section: str) -> Dict:
    """解析动线设计"""

    flows = {}

    # 提取所有三级标题作为动线类型
    flow_pattern = r'###\s+(.+?)\s*\n(.*?)(?=\n###|\Z)'
    matches = re.finditer(flow_pattern, section, re.DOTALL)

    for match in matches:
        flow_name = match.group(1).strip()
        flow_content = match.group(2).strip()

        flows[flow_name] = {
            'raw_content': flow_content
        }

        # TODO: 解析动线序列 (Entry → Waiting → Dining → Exit)

    return flows


def _parse_visual_style(section: str) -> Dict:
    """解析视觉风格"""

    style = {}

    # 提取线条风格
    line_section = _extract_subsection(section, "线条风格")
    if line_section:
        style['lines'] = _parse_line_styles(line_section)

    # 提取配色方案
    color_section = _extract_subsection(section, "配色方案")
    if color_section:
        style['colors'] = _parse_colors(color_section)

    # 提取图例要求
    legend_section = _extract_subsection(section, "图例要求")
    if legend_section:
        style['legend'] = _parse_legend(legend_section)

    return style


def _extract_subsection(section: str, subsection_name: str) -> str:
    """提取Markdown子章节"""

    pattern = rf"###\s+{re.escape(subsection_name)}\s*\n(.*?)(?=\n###|\Z)"
    match = re.search(pattern, section, re.DOTALL)

    return match.group(1).strip() if match else ""


def _parse_line_styles(section: str) -> Dict:
    """解析线条风格"""

    # TODO: 实现详细的线条风格解析
    # 提取: 墙体: 粗实线 (3px黑色) → {'walls': {'type': 'solid', 'width': '3px', 'color': '#000000'}}

    return {'raw': section}


def _parse_colors(section: str) -> Dict:
    """解析配色方案"""

    colors = {}

    # 提取颜色定义
    color_pattern = r'-\s+(.+?):\s+(.+?)\s+\(([#\w]+)\)'
    matches = re.finditer(color_pattern, section)

    for match in matches:
        element = match.group(1).strip()
        color_name = match.group(2).strip()
        color_hex = match.group(3).strip()

        colors[element] = {
            'name': color_name,
            'hex': color_hex
        }

    return colors


def _parse_legend(section: str) -> Dict:
    """解析图例要求"""

    legend = {}

    # 提取比例尺
    match = re.search(r'-\s+比例尺:\s*(.+)', section)
    if match:
        legend['scale'] = match.group(1).strip()

    # 提取指北针
    match = re.search(r'-\s+指北针:\s*(.+)', section)
    if match:
        legend['north_arrow'] = match.group(1).strip()

    # 提取图例位置
    match = re.search(r'-\s+图例:\s*(.+)', section)
    if match:
        legend['legend_position'] = match.group(1).strip()

    return legend


def _parse_canvas_params(section: str) -> Dict:
    """解析canvas-design参数"""

    params = {}

    # 提取创作风格
    match = re.search(r'\*\*创作风格\*\*:\s*(.+)', section)
    if match:
        params['style'] = match.group(1).strip()

    # 提取输出格式
    match = re.search(r'\*\*输出格式\*\*:\s*(.+)', section)
    if match:
        params['formats'] = match.group(1).strip()

    # 提取画布尺寸
    match = re.search(r'\*\*画布尺寸\*\*:\s*(.+)', section)
    if match:
        params['canvas_size'] = match.group(1).strip()

    return params
