"""
Render Engine - SVG渲染引擎

生成符合建筑制图规范的SVG矢量图
"""

from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)


class FloorPlanRenderer:
    """建筑平面图渲染引擎"""

    def __init__(
        self,
        canvas_size: Tuple[int, int] = (1920, 1440),
        scale: str = "1:100",
        line_weight_factor: float = 1.0,
        color_mode: str = "standard"
    ):
        self.canvas_size = canvas_size
        self.scale = scale
        self.line_weight_factor = line_weight_factor
        self.color_mode = color_mode

        # 线条粗细基准
        self.line_weights = {
            'wall': 3 * line_weight_factor,
            'door': 1.5 * line_weight_factor,
            'furniture': 0.8 * line_weight_factor,
            'dimension': 0.5 * line_weight_factor,
            'axis': 0.5 * line_weight_factor
        }

        # 颜色方案
        self.colors = self._init_colors(color_mode)

        logger.info(f"渲染引擎已初始化: {canvas_size}, {scale}, {color_mode}")

    def _init_colors(self, mode: str) -> Dict:
        """初始化颜色方案"""

        if mode == "standard":
            return {
                'background': '#F5F5F5',
                'wall': '#000000',
                'door': '#000000',
                'furniture': '#666666',
                'dimension': '#0000FF',
                'axis': '#FF0000',
                'zone_dining': '#E3F2FD',
                'zone_kitchen': '#E8F5E9',
                'zone_restroom': '#FFF9C4'
            }
        elif mode == "grayscale":
            return {
                'background': '#FFFFFF',
                'wall': '#000000',
                'door': '#333333',
                'furniture': '#666666',
                'dimension': '#999999',
                'axis': '#CCCCCC',
                'zone_dining': '#F0F0F0',
                'zone_kitchen': '#E0E0E0',
                'zone_restroom': '#D0D0D0'
            }
        elif mode == "high_contrast":
            return {
                'background': '#FFFFFF',
                'wall': '#000000',
                'door': '#000000',
                'furniture': '#000000',
                'dimension': '#0000FF',
                'axis': '#FF0000',
                'zone_dining': '#FFEB3B',
                'zone_kitchen': '#4CAF50',
                'zone_restroom': '#2196F3'
            }

    def render_svg(
        self,
        config: Dict,
        show_dimensions: bool = True,
        show_furniture: bool = True
    ) -> str:
        """
        渲染SVG矢量图

        Args:
            config: 解析后的配置字典
            show_dimensions: 是否显示尺寸标注
            show_furniture: 是否显示家具

        Returns:
            SVG XML字符串
        """

        logger.info("开始渲染SVG...")

        # 创建SVG画布
        svg_content = []
        svg_content.append(f'<?xml version="1.0" encoding="UTF-8"?>')
        svg_content.append(f'<svg width="{self.canvas_size[0]}" height="{self.canvas_size[1]}" ')
        svg_content.append(f'     xmlns="http://www.w3.org/2000/svg" ')
        svg_content.append(f'     xmlns:xlink="http://www.w3.org/1999/xlink">')

        # 背景
        svg_content.append(self._render_background())

        # 标题和项目信息
        svg_content.append(self._render_title(config))

        # 功能分区
        svg_content.append(self._render_zones(config['zones']))

        # 墙体和结构
        svg_content.append(self._render_walls(config))

        # 门窗
        svg_content.append(self._render_doors_windows(config))

        # 家具（如果启用）
        if show_furniture:
            svg_content.append(self._render_furniture(config))

        # 尺寸标注（如果启用）
        if show_dimensions:
            svg_content.append(self._render_dimensions(config))

        # 图例
        svg_content.append(self._render_legend(config))

        svg_content.append('</svg>')

        logger.info("✅ SVG渲染完成")

        return '\n'.join(svg_content)

    def _render_background(self) -> str:
        """渲染背景"""

        return f'<rect width="{self.canvas_size[0]}" height="{self.canvas_size[1]}" fill="{self.colors["background"]}" />'

    def _render_title(self, config: Dict) -> str:
        """渲染标题"""

        project_name = config.get('basic_info', {}).get('project_name', 'Untitled')
        total_area = config.get('basic_info', {}).get('total_area', 'N/A')

        return f'''
        <text x="100" y="60" font-family="SimSun" font-size="32" font-weight="bold" fill="#000000">{project_name} 平面图</text>
        <text x="100" y="95" font-family="SimSun" font-size="18" fill="#666666">总面积: {total_area}</text>
        '''

    def _render_zones(self, zones: Dict) -> str:
        """渲染功能分区（色块）"""

        logger.info(f"渲染 {len(zones)} 个功能分区...")

        zone_svg = ['<!-- 功能分区色块 -->']

        # 定义功能分区的颜色映射
        zone_color_map = {
            '入口': self.colors.get('zone_dining', '#E3F2FD'),
            '就餐': self.colors.get('zone_dining', '#E3F2FD'),
            '包间': self.colors.get('zone_dining', '#E3F2FD'),
            '厨房': self.colors.get('zone_kitchen', '#E8F5E9'),
            '卫生间': self.colors.get('zone_restroom', '#FFF9C4'),
            '仓储': self.colors.get('zone_kitchen', '#E8F5E9')
        }

        # 根据zones数量动态布局
        # 简化布局：将区域从左到右、从上到下排列
        canvas_width = self.canvas_size[0] - 300  # 留出边距
        canvas_height = self.canvas_size[1] - 300
        start_x = 150
        start_y = 150

        zone_index = 0
        for zone_name, zone_data in zones.items():
            # 提取面积信息
            area_str = zone_data.get('area', '0㎡')
            area_value = int(area_str.replace('㎡', ''))

            # 根据面积计算矩形大小（简化算法）
            zone_width = min(area_value * 3, canvas_width * 0.3)
            zone_height = min(area_value * 2, canvas_height * 0.3)

            # 计算位置（简单的网格布局）
            col = zone_index % 3
            row = zone_index // 3
            x = start_x + col * (canvas_width / 3)
            y = start_y + row * (canvas_height / 2)

            # 确定颜色
            zone_color = self.colors.get('zone_dining', '#E3F2FD')
            for keyword, color in zone_color_map.items():
                if keyword in zone_name:
                    zone_color = color
                    break

            # 绘制区域矩形
            zone_svg.append(f'<rect x="{x}" y="{y}" width="{zone_width}" height="{zone_height}" ')
            zone_svg.append(f'      fill="{zone_color}" stroke="{self.colors["wall"]}" ')
            zone_svg.append(f'      stroke-width="{self.line_weights["wall"]}" opacity="0.3" />')

            # 绘制区域标签
            text_x = x + zone_width / 2
            text_y = y + zone_height / 2
            zone_svg.append(f'<text x="{text_x}" y="{text_y}" font-family="SimSun" font-size="20" ')
            zone_svg.append(f'      fill="#000000" text-anchor="middle">{zone_name}</text>')
            zone_svg.append(f'<text x="{text_x}" y="{text_y + 25}" font-family="SimSun" font-size="14" ')
            zone_svg.append(f'      fill="#666666" text-anchor="middle">{area_str}</text>')

            zone_index += 1

        return '\n'.join(zone_svg)

    def _render_walls(self, config: Dict) -> str:
        """渲染墙体"""

        logger.info("渲染墙体...")

        wall_svg = ['<!-- 墙体 -->']

        # 提取基础信息
        basic_info = config.get('basic_info', {})
        length_str = basic_info.get('length', '20m')
        width_str = basic_info.get('width', '15m')

        # 解析尺寸（去除单位）
        try:
            length = float(length_str.replace('m', ''))
            width = float(width_str.replace('m', ''))
        except:
            length = 20
            width = 15

        # 计算绘制比例（适应画布）
        canvas_width = self.canvas_size[0] - 300
        canvas_height = self.canvas_size[1] - 300
        scale_x = canvas_width / length
        scale_y = canvas_height / width
        scale = min(scale_x, scale_y)

        # 计算实际绘制尺寸
        wall_width = length * scale
        wall_height = width * scale
        wall_x = (self.canvas_size[0] - wall_width) / 2
        wall_y = (self.canvas_size[1] - wall_height) / 2

        # 绘制外墙（双线表示墙体厚度）
        wall_thickness = 10  # 墙体厚度（像素）

        # 外墙外轮廓
        wall_svg.append(f'<rect x="{wall_x}" y="{wall_y}" ')
        wall_svg.append(f'      width="{wall_width}" height="{wall_height}" ')
        wall_svg.append(f'      fill="none" stroke="{self.colors["wall"]}" ')
        wall_svg.append(f'      stroke-width="{self.line_weights["wall"]}" />')

        # 外墙内轮廓
        wall_svg.append(f'<rect x="{wall_x + wall_thickness}" y="{wall_y + wall_thickness}" ')
        wall_svg.append(f'      width="{wall_width - wall_thickness * 2}" height="{wall_height - wall_thickness * 2}" ')
        wall_svg.append(f'      fill="none" stroke="{self.colors["wall"]}" ')
        wall_svg.append(f'      stroke-width="{self.line_weights["wall"]}" />')

        # 绘制内墙（根据功能分区）
        zones = config.get('zones', {})
        if len(zones) > 1:
            # 简单的垂直/水平内墙分隔
            # 厨房通常在后方，用垂直墙分隔
            kitchen_wall_x = wall_x + wall_width * 0.7
            wall_svg.append(f'<line x1="{kitchen_wall_x}" y1="{wall_y + wall_thickness}" ')
            wall_svg.append(f'      x2="{kitchen_wall_x}" y2="{wall_y + wall_height - wall_thickness}" ')
            wall_svg.append(f'      stroke="{self.colors["wall"]}" ')
            wall_svg.append(f'      stroke-width="{self.line_weights["wall"]}" />')

            # 包间区域用水平墙分隔
            private_wall_y = wall_y + wall_height * 0.6
            wall_svg.append(f'<line x1="{wall_x + wall_thickness}" y1="{private_wall_y}" ')
            wall_svg.append(f'      x2="{kitchen_wall_x}" y2="{private_wall_y}" ')
            wall_svg.append(f'      stroke="{self.colors["wall"]}" ')
            wall_svg.append(f'      stroke-width="{self.line_weights["wall"]}" />')

        return '\n'.join(wall_svg)

    def _render_doors_windows(self, config: Dict) -> str:
        """渲染门窗"""

        logger.info("渲染门窗...")

        door_svg = ['<!-- 门窗 -->']

        # 提取基础信息
        basic_info = config.get('basic_info', {})
        length_str = basic_info.get('length', '20m')
        width_str = basic_info.get('width', '15m')

        try:
            length = float(length_str.replace('m', ''))
            width = float(width_str.replace('m', ''))
        except:
            length = 20
            width = 15

        # 计算墙体位置（与_render_walls保持一致）
        canvas_width = self.canvas_size[0] - 300
        canvas_height = self.canvas_size[1] - 300
        scale = min(canvas_width / length, canvas_height / width)
        wall_width = length * scale
        wall_height = width * scale
        wall_x = (self.canvas_size[0] - wall_width) / 2
        wall_y = (self.canvas_size[1] - wall_height) / 2

        # 门的标准宽度
        door_width = 1.5 * scale  # 1.5m标准门宽

        # 绘制主入口门（前墙中央）
        main_door_x = wall_x + wall_width / 2 - door_width / 2
        main_door_y = wall_y

        # 门的缺口（清除墙体）
        door_svg.append(f'<line x1="{main_door_x}" y1="{main_door_y}" ')
        door_svg.append(f'      x2="{main_door_x + door_width}" y2="{main_door_y}" ')
        door_svg.append(f'      stroke="{self.colors["background"]}" ')
        door_svg.append(f'      stroke-width="{self.line_weights["wall"] + 2}" />')

        # 门的开启弧线
        door_svg.append(f'<path d="M {main_door_x} {main_door_y} ')
        door_svg.append(f'         Q {main_door_x} {main_door_y + door_width}, {main_door_x + door_width} {main_door_y + door_width}" ')
        door_svg.append(f'      stroke="{self.colors["door"]}" ')
        door_svg.append(f'      stroke-width="{self.line_weights["door"]}" ')
        door_svg.append(f'      fill="none" />')

        # 门扇线
        door_svg.append(f'<line x1="{main_door_x}" y1="{main_door_y}" ')
        door_svg.append(f'      x2="{main_door_x + door_width}" y2="{main_door_y + door_width}" ')
        door_svg.append(f'      stroke="{self.colors["door"]}" ')
        door_svg.append(f'      stroke-width="{self.line_weights["door"]}" />')

        # 绘制厨房门（侧墙）
        kitchen_door_x = wall_x + wall_width * 0.7
        kitchen_door_y = wall_y + wall_height / 2

        door_svg.append(f'<line x1="{kitchen_door_x}" y1="{kitchen_door_y - door_width/2}" ')
        door_svg.append(f'      x2="{kitchen_door_x}" y2="{kitchen_door_y + door_width/2}" ')
        door_svg.append(f'      stroke="{self.colors["background"]}" ')
        door_svg.append(f'      stroke-width="{self.line_weights["wall"] + 2}" />')

        # 绘制窗（双线表示）
        window_width = 2 * scale  # 2m标准窗宽
        window_x = wall_x + wall_width * 0.2
        window_y = wall_y

        # 窗的外框
        door_svg.append(f'<line x1="{window_x}" y1="{window_y}" ')
        door_svg.append(f'      x2="{window_x + window_width}" y2="{window_y}" ')
        door_svg.append(f'      stroke="{self.colors["door"]}" ')
        door_svg.append(f'      stroke-width="{self.line_weights["door"]}" />')

        # 窗的内框（双线效果）
        door_svg.append(f'<line x1="{window_x}" y1="{window_y + 5}" ')
        door_svg.append(f'      x2="{window_x + window_width}" y2="{window_y + 5}" ')
        door_svg.append(f'      stroke="{self.colors["door"]}" ')
        door_svg.append(f'      stroke-width="{self.line_weights["door"]}" />')

        return '\n'.join(door_svg)

    def _render_furniture(self, config: Dict) -> str:
        """渲染家具"""

        logger.info("渲染家具...")

        furniture_svg = ['<!-- 家具 -->']

        # 提取基础信息
        basic_info = config.get('basic_info', {})
        zones = config.get('zones', {})

        try:
            length = float(basic_info.get('length', '20m').replace('m', ''))
            width = float(basic_info.get('width', '15m').replace('m', ''))
        except:
            length = 20
            width = 15

        # 计算墙体位置
        canvas_width = self.canvas_size[0] - 300
        canvas_height = self.canvas_size[1] - 300
        scale = min(canvas_width / length, canvas_height / width)
        wall_width = length * scale
        wall_height = width * scale
        wall_x = (self.canvas_size[0] - wall_width) / 2
        wall_y = (self.canvas_size[1] - wall_height) / 2

        # 遍历zones，为就餐区绘制桌椅
        for zone_name, zone_data in zones.items():
            if '就餐' in zone_name or '包间' in zone_name:
                # 解析座位数（从raw_content中提取）
                raw_content = zone_data.get('raw_content', '')

                # 简化处理：在就餐区绘制网格布局的桌子
                if '就餐' in zone_name:
                    # 主就餐区：绘制4人桌（正方形）
                    table_size = 0.8 * scale  # 0.8m桌子
                    table_spacing = 2 * scale  # 2m间距

                    # 计算就餐区域（中央区域）
                    dining_x = wall_x + wall_width * 0.15
                    dining_y = wall_y + wall_height * 0.2
                    dining_width = wall_width * 0.5
                    dining_height = wall_height * 0.5

                    # 绘制6×3网格的桌子
                    for row in range(3):
                        for col in range(6):
                            table_x = dining_x + col * table_spacing
                            table_y = dining_y + row * table_spacing

                            # 桌子矩形
                            furniture_svg.append(f'<rect x="{table_x}" y="{table_y}" ')
                            furniture_svg.append(f'      width="{table_size}" height="{table_size}" ')
                            furniture_svg.append(f'      fill="none" stroke="{self.colors["furniture"]}" ')
                            furniture_svg.append(f'      stroke-width="{self.line_weights["furniture"]}" />')

                            # 椅子（4个小矩形）
                            chair_size = 0.15 * scale
                            # 上方椅子
                            furniture_svg.append(f'<rect x="{table_x + table_size/2 - chair_size/2}" y="{table_y - chair_size - 0.05*scale}" ')
                            furniture_svg.append(f'      width="{chair_size}" height="{chair_size}" ')
                            furniture_svg.append(f'      fill="{self.colors["furniture"]}" />')
                            # 下方椅子
                            furniture_svg.append(f'<rect x="{table_x + table_size/2 - chair_size/2}" y="{table_y + table_size + 0.05*scale}" ')
                            furniture_svg.append(f'      width="{chair_size}" height="{chair_size}" ')
                            furniture_svg.append(f'      fill="{self.colors["furniture"]}" />')
                            # 左方椅子
                            furniture_svg.append(f'<rect x="{table_x - chair_size - 0.05*scale}" y="{table_y + table_size/2 - chair_size/2}" ')
                            furniture_svg.append(f'      width="{chair_size}" height="{chair_size}" ')
                            furniture_svg.append(f'      fill="{self.colors["furniture"]}" />')
                            # 右方椅子
                            furniture_svg.append(f'<rect x="{table_x + table_size + 0.05*scale}" y="{table_y + table_size/2 - chair_size/2}" ')
                            furniture_svg.append(f'      width="{chair_size}" height="{chair_size}" ')
                            furniture_svg.append(f'      fill="{self.colors["furniture"]}" />')

                elif '包间' in zone_name:
                    # 包间：绘制大圆桌
                    private_x = wall_x + wall_width * 0.15
                    private_y = wall_y + wall_height * 0.65
                    table_radius = 1.2 * scale  # 1.2m半径圆桌

                    # 绘制3个包间的圆桌
                    for i in range(3):
                        circle_x = private_x + i * (table_radius * 2.5)
                        circle_y = private_y

                        furniture_svg.append(f'<circle cx="{circle_x}" cy="{circle_y}" r="{table_radius}" ')
                        furniture_svg.append(f'      fill="none" stroke="{self.colors["furniture"]}" ')
                        furniture_svg.append(f'      stroke-width="{self.line_weights["furniture"]}" />')

        return '\n'.join(furniture_svg)

    def _render_dimensions(self, config: Dict) -> str:
        """渲染尺寸标注"""

        logger.info("渲染尺寸标注...")

        dim_svg = ['<!-- 尺寸标注 -->']

        # 提取基础信息
        basic_info = config.get('basic_info', {})

        try:
            length = float(basic_info.get('length', '20m').replace('m', ''))
            width = float(basic_info.get('width', '15m').replace('m', ''))
        except:
            length = 20
            width = 15

        # 计算墙体位置
        canvas_width = self.canvas_size[0] - 300
        canvas_height = self.canvas_size[1] - 300
        scale = min(canvas_width / length, canvas_height / width)
        wall_width = length * scale
        wall_height = width * scale
        wall_x = (self.canvas_size[0] - wall_width) / 2
        wall_y = (self.canvas_size[1] - wall_height) / 2

        # 尺寸标注线的偏移距离
        dim_offset = 30

        # 绘制水平总尺寸（下方）
        dim_y = wall_y + wall_height + dim_offset

        # 尺寸线
        dim_svg.append(f'<line x1="{wall_x}" y1="{dim_y}" x2="{wall_x + wall_width}" y2="{dim_y}" ')
        dim_svg.append(f'      stroke="{self.colors["dimension"]}" ')
        dim_svg.append(f'      stroke-width="{self.line_weights["dimension"]}" />')

        # 左侧箭头
        dim_svg.append(f'<line x1="{wall_x}" y1="{dim_y - 5}" x2="{wall_x}" y2="{dim_y + 5}" ')
        dim_svg.append(f'      stroke="{self.colors["dimension"]}" ')
        dim_svg.append(f'      stroke-width="{self.line_weights["dimension"]}" />')

        # 右侧箭头
        dim_svg.append(f'<line x1="{wall_x + wall_width}" y1="{dim_y - 5}" x2="{wall_x + wall_width}" y2="{dim_y + 5}" ')
        dim_svg.append(f'      stroke="{self.colors["dimension"]}" ')
        dim_svg.append(f'      stroke-width="{self.line_weights["dimension"]}" />')

        # 尺寸文字
        dim_text_x = wall_x + wall_width / 2
        dim_svg.append(f'<text x="{dim_text_x}" y="{dim_y + 20}" ')
        dim_svg.append(f'      font-family="SimSun" font-size="14" ')
        dim_svg.append(f'      fill="{self.colors["dimension"]}" text-anchor="middle">{length}m</text>')

        # 绘制垂直总尺寸（右侧）
        dim_x = wall_x + wall_width + dim_offset

        # 尺寸线
        dim_svg.append(f'<line x1="{dim_x}" y1="{wall_y}" x2="{dim_x}" y2="{wall_y + wall_height}" ')
        dim_svg.append(f'      stroke="{self.colors["dimension"]}" ')
        dim_svg.append(f'      stroke-width="{self.line_weights["dimension"]}" />')

        # 上侧箭头
        dim_svg.append(f'<line x1="{dim_x - 5}" y1="{wall_y}" x2="{dim_x + 5}" y2="{wall_y}" ')
        dim_svg.append(f'      stroke="{self.colors["dimension"]}" ')
        dim_svg.append(f'      stroke-width="{self.line_weights["dimension"]}" />')

        # 下侧箭头
        dim_svg.append(f'<line x1="{dim_x - 5}" y1="{wall_y + wall_height}" x2="{dim_x + 5}" y2="{wall_y + wall_height}" ')
        dim_svg.append(f'      stroke="{self.colors["dimension"]}" ')
        dim_svg.append(f'      stroke-width="{self.line_weights["dimension"]}" />')

        # 尺寸文字（垂直文字使用transform旋转）
        dim_text_y = wall_y + wall_height / 2
        dim_svg.append(f'<text x="{dim_x + 20}" y="{dim_text_y}" ')
        dim_svg.append(f'      font-family="SimSun" font-size="14" ')
        dim_svg.append(f'      fill="{self.colors["dimension"]}" text-anchor="middle" ')
        dim_svg.append(f'      transform="rotate(90 {dim_x + 20} {dim_text_y})">{width}m</text>')

        # 绘制局部尺寸（示例：厨房分隔墙）
        kitchen_wall_x = wall_x + wall_width * 0.7
        partial_dim_y = wall_y + wall_height + dim_offset * 0.5

        # 到厨房墙的尺寸
        dim_svg.append(f'<line x1="{wall_x}" y1="{partial_dim_y}" x2="{kitchen_wall_x}" y2="{partial_dim_y}" ')
        dim_svg.append(f'      stroke="{self.colors["dimension"]}" stroke-dasharray="2,2" ')
        dim_svg.append(f'      stroke-width="{self.line_weights["dimension"]}" />')

        partial_length = length * 0.7
        dim_svg.append(f'<text x="{(wall_x + kitchen_wall_x) / 2}" y="{partial_dim_y - 5}" ')
        dim_svg.append(f'      font-family="SimSun" font-size="12" ')
        dim_svg.append(f'      fill="{self.colors["dimension"]}" text-anchor="middle">{partial_length:.1f}m</text>')

        return '\n'.join(dim_svg)

    def _render_legend(self, config: Dict) -> str:
        """渲染图例"""

        legend_svg = ['<!-- 图例 -->']

        # 比例尺
        scale_text = config.get('visual_style', {}).get('legend', {}).get('scale', self.scale)
        legend_svg.append(f'<text x="100" y="{self.canvas_size[1] - 100}" font-family="SimSun" font-size="18" fill="#000000">比例尺: {scale_text}</text>')

        # 指北针
        legend_svg.append(f'<text x="{self.canvas_size[0] - 150}" y="150" font-family="SimSun" font-size="18" fill="#000000">↑N</text>')

        # 图例符号
        legend_svg.append(f'<text x="100" y="{self.canvas_size[1] - 50}" font-family="SimSun" font-size="14" fill="#666666">图例: █ 墙体  ▭ 门  ▢ 窗  ◻ 家具</text>')

        return '\n'.join(legend_svg)
