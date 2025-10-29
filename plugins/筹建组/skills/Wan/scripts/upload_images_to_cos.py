#!/usr/bin/env python3
"""
将Midjourney主图上传到腾讯云COS，获取公网URL
为通义万相API提供URL模式的图片输入
"""

import os
import json
from pathlib import Path
from qcloud_cos import CosConfig, CosS3Client
from dotenv import load_dotenv

# 加载环境变量
project_root = Path(__file__).parent.parent.parent.parent
load_dotenv(project_root / ".env")

def upload_images():
    """上传所有图片到COS并返回URL映射"""

    # 从环境变量获取COS配置
    secret_id = os.getenv("CLOUD_STORAGE_TENCENT_SECRET_ID")
    secret_key = os.getenv("CLOUD_STORAGE_TENCENT_SECRET_KEY")
    region = os.getenv("CLOUD_STORAGE_TENCENT_REGION", "ap-chengdu")
    bucket = os.getenv("CLOUD_STORAGE_TENCENT_BUCKET", "minghong-redbook-1353737511")

    if not secret_id or not secret_key:
        print("❌ 错误: 未配置腾讯云密钥 (TENCENT_SECRET_ID, TENCENT_SECRET_KEY)")
        return {}

    # 初始化COS客户端
    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
    client = CosS3Client(config)

    # 图片目录
    image_dir = project_root / "output/花间集美妆店双11活动/4-Midjourney主图"

    # 获取所有PNG文件
    png_files = sorted([f for f in os.listdir(image_dir) if f.endswith('.png')])

    print(f"找到 {len(png_files)} 张图片")
    print("=" * 80)

    # URL映射表（本地路径 -> COS URL）
    url_mapping = {}

    for filename in png_files:
        local_path = image_dir / filename
        # COS对象键：huajian-i2v/主图文件名
        object_key = f"huajian-i2v/{filename}"

        print(f"\n上传: {filename}")

        try:
            # 上传文件
            with open(local_path, 'rb') as f:
                client.put_object(
                    Bucket=bucket,
                    Key=object_key,
                    Body=f,
                    ContentType='image/png'
                )

            # 生成带签名的临时URL（7天有效期）
            cos_url = client.get_presigned_url(
                Method='GET',
                Bucket=bucket,
                Key=object_key,
                Expired=7 * 24 * 3600  # 7天
            )

            url_mapping[str(local_path)] = cos_url
            print(f"  ✅ 上传成功")
            print(f"  📍 URL: {cos_url[:100]}...")

        except Exception as e:
            print(f"  ❌ 异常: {e}")

    print("\n" + "=" * 80)
    print(f"上传完成: {len(url_mapping)}/{len(png_files)} 张图片成功")

    # 保存URL映射表
    mapping_file = project_root / "output/tongyi-wanxiang/metadata/image_url_mapping.json"
    with open(mapping_file, 'w', encoding='utf-8') as f:
        json.dump(url_mapping, f, ensure_ascii=False, indent=2)

    print(f"\n✅ URL映射表已保存: {mapping_file}")
    return url_mapping

if __name__ == "__main__":
    upload_images()
