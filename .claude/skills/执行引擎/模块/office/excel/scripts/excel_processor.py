"""
Excel文件处理核心模块

提供Excel文件的读取、写入、清洗、分析等核心功能
"""

import pandas as pd
from pathlib import Path
from typing import Union, List, Dict, Any, Optional, Callable
import logging

logger = logging.getLogger(__name__)


class ExcelProcessor:
    """Excel处理器核心类"""

    def __init__(self):
        """初始化处理器"""
        self.current_file = None
        self.current_data = None

    def read(
        self,
        file_path: Union[str, Path],
        sheet_name: Optional[Union[str, int]] = None,
        **kwargs
    ) -> pd.DataFrame:
        """读取Excel文件

        Args:
            file_path: 文件路径
            sheet_name: 工作表名称或索引，None读取第一个
            **kwargs: pandas.read_excel的其他参数

        Returns:
            pandas.DataFrame: 读取的数据

        Example:
            >>> processor = ExcelProcessor()
            >>> data = processor.read('sales.xlsx', sheet_name='2025年1月')
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"文件不存在: {file_path}")

            self.current_file = file_path
            self.current_data = pd.read_excel(
                file_path,
                sheet_name=sheet_name if sheet_name is not None else 0,
                **kwargs
            )

            logger.info(f"成功读取文件: {file_path}, 形状: {self.current_data.shape}")
            return self.current_data

        except Exception as e:
            logger.error(f"读取文件失败: {file_path}, 错误: {e}")
            raise

    def write(
        self,
        data: Union[pd.DataFrame, Dict[str, pd.DataFrame]],
        file_path: Union[str, Path],
        sheet_name: str = 'Sheet1',
        **kwargs
    ) -> None:
        """写入Excel文件

        Args:
            data: 数据，可以是DataFrame或{sheet_name: DataFrame}字典
            file_path: 输出路径（推荐使用项目根目录的output/子目录）
            sheet_name: 工作表名称（仅当data为DataFrame时有效）
            **kwargs: pandas.to_excel的其他参数

        Example:
            >>> processor.write(data, 'output/行政组/excel/report.xlsx')
            >>> processor.write({'销售': df1, '成本': df2}, 'output/战略组/reports/summary.xlsx')
        """
        try:
            file_path = Path(file_path)

            # 确保是绝对路径，如果是相对路径则相对于项目根目录
            if not file_path.is_absolute():
                # 假设当前工作目录是项目根目录
                file_path = Path.cwd() / file_path

            file_path.parent.mkdir(parents=True, exist_ok=True)

            if isinstance(data, dict):
                # 多工作表写入
                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                    for name, df in data.items():
                        df.to_excel(writer, sheet_name=name, index=False, **kwargs)
            else:
                # 单工作表写入
                data.to_excel(file_path, sheet_name=sheet_name, index=False, **kwargs)

            logger.info(f"成功写入文件: {file_path}")

        except Exception as e:
            logger.error(f"写入文件失败: {file_path}, 错误: {e}")
            raise

    def clean_data(
        self,
        data: pd.DataFrame,
        options: Dict[str, Any]
    ) -> pd.DataFrame:
        """数据清洗

        Args:
            data: 原始数据
            options: 清洗选项
                - fill_na: bool或值，填充空值
                - remove_duplicates: bool，去除重复
                - convert_types: dict，类型转换映射
                - drop_columns: list，删除列

        Returns:
            pandas.DataFrame: 清洗后的数据

        Example:
            >>> cleaned = processor.clean_data(data, {
            ...     'fill_na': 0,
            ...     'remove_duplicates': True,
            ...     'convert_types': {'日期': 'datetime', '金额': 'float'}
            ... })
        """
        df = data.copy()

        # 填充空值
        if 'fill_na' in options:
            fill_value = options['fill_na']
            if fill_value is True:
                df = df.fillna(method='ffill')  # 前向填充
            elif fill_value is not None:
                df = df.fillna(fill_value)

        # 去除重复
        if options.get('remove_duplicates', False):
            before_count = len(df)
            df = df.drop_duplicates()
            removed = before_count - len(df)
            if removed > 0:
                logger.info(f"删除了 {removed} 条重复数据")

        # 类型转换
        if 'convert_types' in options:
            for col, dtype in options['convert_types'].items():
                if col in df.columns:
                    if dtype == 'datetime':
                        df[col] = pd.to_datetime(df[col])
                    else:
                        df[col] = df[col].astype(dtype)

        # 删除列
        if 'drop_columns' in options:
            df = df.drop(columns=options['drop_columns'], errors='ignore')

        logger.info(f"数据清洗完成，最终形状: {df.shape}")
        return df

    def group_by(
        self,
        data: pd.DataFrame,
        group_cols: List[str],
        agg_cols: Dict[str, Union[str, List[str]]]
    ) -> pd.DataFrame:
        """分组聚合

        Args:
            data: 数据
            group_cols: 分组列
            agg_cols: 聚合列和函数映射
                例: {'销售额': 'sum', '订单数': ['count', 'mean']}

        Returns:
            pandas.DataFrame: 聚合后的数据

        Example:
            >>> summary = processor.group_by(
            ...     data,
            ...     group_cols=['门店', '月份'],
            ...     agg_cols={'销售额': 'sum', '订单数': 'count'}
            ... )
        """
        try:
            result = data.groupby(group_cols).agg(agg_cols).reset_index()

            # 扁平化多级列名
            if isinstance(result.columns, pd.MultiIndex):
                result.columns = ['_'.join(col).strip('_') for col in result.columns.values]

            logger.info(f"分组聚合完成，结果形状: {result.shape}")
            return result

        except Exception as e:
            logger.error(f"分组聚合失败: {e}")
            raise

    def merge_files(
        self,
        pattern: str,
        output: Optional[Union[str, Path]] = None,
        **kwargs
    ) -> pd.DataFrame:
        """合并多个Excel文件

        Args:
            pattern: 文件匹配模式（如 'data/*.xlsx'）
            output: 输出路径，None则不保存
            **kwargs: pandas.concat的其他参数

        Returns:
            pandas.DataFrame: 合并后的数据

        Example:
            >>> merged = processor.merge_files('stores/*/sales_*.xlsx', 'all_sales.xlsx')
        """
        from glob import glob

        files = glob(pattern)
        if not files:
            raise FileNotFoundError(f"没有找到匹配的文件: {pattern}")

        logger.info(f"找到 {len(files)} 个文件待合并")

        dfs = []
        for file in files:
            try:
                df = pd.read_excel(file)
                dfs.append(df)
            except Exception as e:
                logger.warning(f"读取文件失败: {file}, 错误: {e}")

        if not dfs:
            raise ValueError("没有成功读取任何文件")

        merged = pd.concat(dfs, ignore_index=True, **kwargs)
        logger.info(f"合并完成，最终形状: {merged.shape}")

        if output:
            self.write(merged, output)

        return merged

    def batch_process(
        self,
        input_dir: Union[str, Path],
        output_dir: Union[str, Path],
        process_func: Callable[[pd.DataFrame], pd.DataFrame],
        pattern: str = '*.xlsx'
    ) -> List[Path]:
        """批量处理Excel文件

        Args:
            input_dir: 输入目录
            output_dir: 输出目录
            process_func: 处理函数，接收DataFrame返回DataFrame
            pattern: 文件匹配模式

        Returns:
            List[Path]: 处理后的文件路径列表

        Example:
            >>> processor.batch_process(
            ...     'raw_data/',
            ...     'processed/',
            ...     lambda df: df[df['金额'] > 1000]
            ... )
        """
        input_dir = Path(input_dir)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        files = list(input_dir.glob(pattern))
        logger.info(f"找到 {len(files)} 个文件待处理")

        processed_files = []
        for file in files:
            try:
                # 读取
                df = self.read(file)

                # 处理
                processed_df = process_func(df)

                # 保存
                output_file = output_dir / file.name
                self.write(processed_df, output_file)
                processed_files.append(output_file)

                logger.info(f"处理完成: {file.name}")

            except Exception as e:
                logger.error(f"处理文件失败: {file}, 错误: {e}")

        logger.info(f"批量处理完成，成功处理 {len(processed_files)}/{len(files)} 个文件")
        return processed_files

    def generate_report(
        self,
        data: pd.DataFrame,
        output: Union[str, Path],
        template: Optional[Union[str, Path]] = None,
        charts: Optional[List[Dict[str, Any]]] = None
    ) -> None:
        """生成报表

        Args:
            data: 数据
            output: 输出路径
            template: 模板路径
            charts: 图表配置列表
                例: [{'type': 'bar', 'x': '门店', 'y': '销售额'}]

        Example:
            >>> processor.generate_report(
            ...     data,
            ...     'report.xlsx',
            ...     charts=[{'type': 'line', 'x': '月份', 'y': '销售额'}]
            ... )
        """
        # 基础报表生成
        self.write(data, output)

        # 如果需要图表，使用openpyxl添加
        if charts:
            from .excel_reporter import ExcelReporter
            reporter = ExcelReporter()
            reporter.add_charts(output, data, charts)

        logger.info(f"报表生成完成: {output}")
