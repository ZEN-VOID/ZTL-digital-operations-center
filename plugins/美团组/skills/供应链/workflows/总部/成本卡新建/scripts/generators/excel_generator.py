"""
Excel生成器 - 成本卡Excel文件生成
ExcelGenerator - Cost Card Excel File Generation

功能:
1. 基于总部成本卡导入模板生成Excel文件
2. 处理一对多关系 (一个菜品对应多个物品)
3. 格式化百分比字段 (文本格式 + %)
4. 支持集成奥术光辉/excel技能包
"""

import openpyxl
from pathlib import Path
from typing import List, Dict, Any
import logging


class ExcelGenerator:
    """Excel文件生成器"""

    def __init__(self, use_excel_skill: bool = False):
        """
        初始化生成器

        Args:
            use_excel_skill: 是否集成奥术光辉/excel技能包
        """
        self.use_excel_skill = use_excel_skill
        # 使用绝对路径(从项目根目录计算)
        script_dir = Path(__file__).parent
        self.template_path = script_dir / "../../../../../../templates/总部成本卡导入模版.xlsx"
        self.template_path = self.template_path.resolve()
        self.logger = logging.getLogger(__name__)

        # 字段映射 (模板列索引)
        self.field_mapping = {
            "菜品SPU编码": 0,
            "菜品名称": 1,
            "加工份数": 2,
            "菜品规格": 3,
            "其他成本": 4,
            "目标毛利率": 5,
            "配方名称": 6,
            "物品编码": 7,
            "物品名称": 8,
            "成本单位": 9,
            "净料量": 10,
            "净料率": 11,
            "是否主料": 12,
            "替代关系编号": 13,
            "替代关系名称": 14,
            "是否半成品": 15,
            "是否辅助单位扣减料": 16,
            "是否同时适用堂食和外卖菜品": 17,
            "门店是否可修改": 18,
            "备注": 19,
            "适用门店商户号": 20,
            "适用门店分组": 21
        }

    def generate(
        self,
        data: List[Dict[str, Any]],
        output_path: str
    ):
        """
        生成成本卡Excel文件

        Args:
            data: 重构后的数据 (list of dicts)
            output_path: 输出路径
        """
        self.logger.info(f"开始生成Excel文件: {output_path}")

        if not self.template_path.exists():
            raise FileNotFoundError(f"模板文件不存在: {self.template_path}")

        # 加载模板
        wb = openpyxl.load_workbook(str(self.template_path))
        ws = wb.active

        # 从第3行开始填充数据 (前2行是说明)
        start_row = 3

        for idx, row_data in enumerate(data):
            current_row = start_row + idx

            # 填充每个字段
            for field_name, col_idx in self.field_mapping.items():
                value = row_data.get(field_name, "")

                # 格式化百分比字段 (使用文本格式)
                if field_name in ["目标毛利率", "净料率"] and value:
                    # 确保包含%符号
                    if not str(value).endswith("%"):
                        value = f"{value}%"
                    # 使用文本格式
                    cell = ws.cell(row=current_row, column=col_idx + 1, value=value)
                    cell.number_format = '@'  # 文本格式
                else:
                    ws.cell(row=current_row, column=col_idx + 1, value=value)

        # 保存文件
        wb.save(output_path)
        self.logger.info(f"Excel文件生成成功: {output_path}")

    def generate_with_excel_skill(
        self,
        data: List[Dict[str, Any]],
        output_path: str
    ):
        """
        使用奥术光辉/excel技能包生成Excel

        提供更高级的功能:
        - 数据验证
        - 样式设置
        - 图表生成
        """
        try:
            # 导入奥术光辉/excel技能包
            import sys
            sys.path.insert(0, ".claude/skills/奥术光辉/excel/scripts")
            from excel_processor import ExcelProcessor

            processor = ExcelProcessor()

            # 转换数据格式
            import pandas as pd
            df = pd.DataFrame(data)

            # 使用高级功能生成Excel
            processor.generate_report(
                data=df,
                output=output_path,
                template=str(self.template_path)
            )

            self.logger.info(f"使用奥术光辉/excel生成成功: {output_path}")

        except ImportError as e:
            self.logger.warning(f"无法导入奥术光辉/excel,回退到基础生成: {e}")
            self.generate(data, output_path)
