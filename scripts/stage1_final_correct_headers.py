#!/usr/bin/env python3
"""
Stage 1: Final correct header reading
Fix: 3.0 files have headers in row 2 (use header=2)
2.0 baseline: Pivot table format requiring custom parsing
"""

import pandas as pd
import json
from pathlib import Path
from datetime import datetime

print("=" * 80)
print("Stage 1: Final Data Structure Analysis with Correct Headers")
print("=" * 80)

# Define file paths
INPUT_DIR = Path("/Users/vincentlee/Desktop/ZTL数智化作战中心/input/情报组/【2.0 VS 3.0】产品销售对比")
OUTPUT_DIR = Path("/Users/vincentlee/Desktop/ZTL数智化作战中心/output/stage1-data-structure-analysis")

file_2_0_baseline = INPUT_DIR / "客单价.xlsx"
file_3_0_order_details = INPUT_DIR / "吼巷_全渠道订单明细_20251027_0208_1761556082620.xlsx"
file_3_0_product_stats = INPUT_DIR / "吼巷_销售品项统计_2025-10-27_02_11_52_a899380r_1761556312749.xlsx"
file_3_0_business_overview = INPUT_DIR / "吼巷_营业概览_20251027_0143_a899380r_1761554593716.xlsx"

# ============================================================================
# Part 1: Read 3.0 files with CORRECTED header=2
# ============================================================================
print("\n" + "=" * 80)
print("PART 1: Reading 3.0 Files (header=2)")
print("=" * 80)

print("\n[1/3] Reading 3.0 Order Details (header=2)...")
df_order_details = pd.read_excel(file_3_0_order_details, header=2)
print(f"✓ Shape: {df_order_details.shape}")
print(f"✓ Columns ({len(df_order_details.columns)} total):")
print(f"  First 10: {list(df_order_details.columns[:10])}")
print(f"  Last 5: {list(df_order_details.columns[-5:])}")

print("\n[2/3] Reading 3.0 Product Stats (header=2)...")
df_product_stats = pd.read_excel(file_3_0_product_stats, header=2)
print(f"✓ Shape: {df_product_stats.shape}")
print(f"✓ Columns: {list(df_product_stats.columns)}")

print("\n[3/3] Reading 3.0 Business Overview (header=2)...")
df_business_overview = pd.read_excel(file_3_0_business_overview, header=2)
print(f"✓ Shape: {df_business_overview.shape}")
print(f"✓ Columns: {list(df_business_overview.columns)}")

# ============================================================================
# Part 2: Read and Parse 2.0 Baseline Pivot Table
# ============================================================================
print("\n" + "=" * 80)
print("PART 2: Reading 2.0 Baseline Pivot Table")
print("=" * 80)

print("\n[1/1] Reading 2.0 baseline (pivot table format)...")
df_2_0_raw = pd.read_excel(file_2_0_baseline, header=0)
print(f"✓ Raw shape: {df_2_0_raw.shape}")
print(f"✓ Raw columns: {list(df_2_0_raw.columns)}")
print(f"\nFirst 5 rows of raw data:")
print(df_2_0_raw.head())

# Analyze pivot table structure
print("\n--- Pivot Table Structure Analysis ---")
print(f"Column 'Unnamed: 1' values (metrics):")
print(df_2_0_raw['Unnamed: 1'].dropna().unique())

# Extract date columns (columns that are not "Unnamed")
date_columns = [col for col in df_2_0_raw.columns if not col.startswith('Unnamed')]
print(f"\nDate columns identified: {date_columns}")

# ============================================================================
# Part 3: Generate Structure Documentation
# ============================================================================
print("\n" + "=" * 80)
print("PART 3: Generating Structure Documentation")
print("=" * 80)

def get_dataframe_info(df, name, description=""):
    """Extract comprehensive structure information from DataFrame"""
    info = {
        "file_name": name,
        "description": description,
        "shape": {
            "rows": int(df.shape[0]),
            "columns": int(df.shape[1])
        },
        "columns": list(df.columns),
        "column_types": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "sample_data": df.head(5).to_dict(orient='records'),
        "null_counts": df.isnull().sum().to_dict(),
        "memory_usage_mb": round(df.memory_usage(deep=True).sum() / 1024 / 1024, 2)
    }
    return info

structure_report = {
    "report_metadata": {
        "generated_at": datetime.now().isoformat(),
        "stage": "Stage 1 - Data Structure Analysis",
        "description": "Final corrected data structure analysis - 3.0 files use header=2",
        "correction_history": [
            "Attempt 1: header=0 - Failed (row 0 is metadata)",
            "Attempt 2: header=1 - Failed (row 1 is filter criteria)",
            "Attempt 3: header=2 - SUCCESS (row 2 contains actual column headers)"
        ],
        "data_format_notes": {
            "3.0_files": "Standard tabular format with proper column headers in row 2",
            "2.0_baseline": "Pivot table format - metrics as rows, dates as columns"
        }
    },
    "files": {
        "3.0_order_details": get_dataframe_info(
            df_order_details,
            "吼巷_全渠道订单明细_20251027_0208_1761556082620.xlsx",
            "Transaction-level order details from 3.0 system"
        ),
        "3.0_product_stats": get_dataframe_info(
            df_product_stats,
            "吼巷_销售品项统计_2025-10-27_02_11_52_a899380r_1761556312749.xlsx",
            "Product-level sales statistics from 3.0 system"
        ),
        "3.0_business_overview": get_dataframe_info(
            df_business_overview,
            "吼巷_营业概览_20251027_0143_a899380r_1761554593716.xlsx",
            "Business overview metrics from 3.0 system"
        ),
        "2.0_baseline": get_dataframe_info(
            df_2_0_raw,
            "客单价.xlsx",
            "2.0 baseline data in pivot table format (requires custom parsing)"
        )
    },
    "pivot_table_analysis": {
        "2.0_baseline_structure": {
            "format": "pivot_table",
            "metrics_column": "Unnamed: 1",
            "date_columns": date_columns,
            "total_dates": len(date_columns),
            "identified_metrics": list(df_2_0_raw['Unnamed: 1'].dropna().unique()),
            "parsing_required": True,
            "parsing_note": "Need to extract metrics from 'Unnamed: 1' and map to date columns"
        }
    }
}

# Save structure report
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = OUTPUT_DIR / f"data-structure-final-{timestamp}.json"

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(structure_report, f, ensure_ascii=False, indent=2)

print(f"\n✓ Structure report saved: {output_file}")

# ============================================================================
# Part 4: Validation Summary
# ============================================================================
print("\n" + "=" * 80)
print("VALIDATION SUMMARY")
print("=" * 80)

print("\n[3.0 Order Details]")
print(f"  ✓ Columns properly extracted: {len(df_order_details.columns)} columns")
print(f"  ✓ Key columns present:")
for col in ['省份', '城市', '门店名称', '营业日期', '订单金额', '顾客实付']:
    status = "✓" if col in df_order_details.columns else "✗"
    print(f"    {status} {col}")

print("\n[3.0 Product Stats]")
print(f"  ✓ Columns properly extracted: {len(df_product_stats.columns)} columns")
print(f"  ✓ All columns: {list(df_product_stats.columns)}")

print("\n[3.0 Business Overview]")
print(f"  ✓ Columns properly extracted: {len(df_business_overview.columns)} columns")
print(f"  ✓ All columns: {list(df_business_overview.columns)}")

print("\n[2.0 Baseline]")
print(f"  ✓ Pivot table structure identified")
print(f"  ✓ Date columns: {len(date_columns)} dates")
print(f"  ⚠ Custom parsing required for metrics extraction")

print("\n" + "=" * 80)
print("✓ Stage 1 Data Structure Analysis - Phase 1 Complete")
print("✓ Next: Implement 2.0 pivot table parsing logic")
print(f"✓ Output: {output_file}")
print("=" * 80)
