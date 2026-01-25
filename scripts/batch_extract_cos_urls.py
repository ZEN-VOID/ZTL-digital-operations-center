"""
批量从腾讯云COS提取图片URL - 使用qcloud_cos直接实现

执行/2指令的核心功能:从COS目录提取所有图片文件的URL,
按子目录结构保存为JSON索引文件。
"""

import os
import json
from pathlib import Path
from datetime import datetime, timedelta
from qcloud_cos import CosConfig, CosS3Client
from dotenv import load_dotenv


def create_cos_client():
    """创建COS客户端"""
    load_dotenv()

    secret_id = os.getenv('SecretId')
    secret_key = os.getenv('SecretKey')
    region = os.getenv('Region', 'ap-chengdu')

    if not secret_id or not secret_key:
        raise ValueError("缺少SecretId或SecretKey配置")

    config = CosConfig(
        Region=region,
        SecretId=secret_id,
        SecretKey=secret_key,
        Scheme='https'
    )

    return CosS3Client(config)


def list_all_files(client, bucket, prefix):
    """列出COS目录下的所有文件(带分页处理)"""
    print(f"\n📂 扫描COS目录: {prefix}")

    files = []
    marker = ""

    while True:
        response = client.list_objects(
            Bucket=bucket,
            Prefix=prefix,
            Marker=marker,
            MaxKeys=1000
        )

        if 'Contents' in response:
            for item in response['Contents']:
                # 跳过目录标记
                if item['Key'].endswith('/'):
                    continue
                if item['Key'] == prefix or item['Key'] == prefix.rstrip('/'):
                    continue
                files.append({
                    'key': item['Key'],
                    'size': item['Size'],
                    'last_modified': item['LastModified']
                })

        # 检查是否还有更多数据
        if response.get('IsTruncated') == 'false':
            break
        marker = response.get('NextMarker', '')

    print(f"✅ 找到 {len(files)} 个文件")
    return files


def generate_presigned_url(client, bucket, object_key, expires=86400):
    """生成预签名URL（默认24小时）"""
    try:
        url = client.get_presigned_url(
            Method='GET',
            Bucket=bucket,
            Key=object_key,
            Expired=expires
        )
        return url
    except Exception as e:
        print(f"  ❌ 生成URL失败: {object_key} - {str(e)}")
        return None


def extract_urls(client, bucket, cos_prefix, local_base_path, url_expires=86400):
    """提取URL并保存为JSON索引"""
    print(f"\n{'=' * 80}")
    print(f"📦 任务: {cos_prefix} → {local_base_path}")
    print(f"{'=' * 80}")

    # 列出所有文件
    all_files = list_all_files(client, bucket, cos_prefix)

    if not all_files:
        print(f"⚠️  目录为空或不存在")
        return {'success': False, 'message': '目录为空'}

    # 过滤图片文件（排除HEIC格式）
    # ⚠️ 重要：HEIC格式在浏览器中不被支持，必须排除
    image_extensions = {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.bmp', '.svg', '.PNG', '.JPG', '.JPEG'}
    heic_extensions = {'.heic', '.HEIC'}  # 明确排除的格式

    image_files = [
        f for f in all_files
        if Path(f['key']).suffix in image_extensions
        and Path(f['key']).suffix not in heic_extensions
    ]

    print(f"🔍 识别出 {len(image_files)} 个图片文件\n")

    if not image_files:
        print(f"⚠️  没有找到图片文件")
        return {'success': False, 'message': '没有图片文件'}

    # 按目录组织文件
    dir_files_map = {}

    print(f"🔗 生成预签名URL...")
    for idx, file_info in enumerate(image_files, 1):
        file_key = file_info['key']
        file_path = Path(file_key)

        # 计算相对于prefix的路径
        relative_path = file_key[len(cos_prefix):].lstrip('/')
        relative_dir = str(Path(relative_path).parent) if '/' in relative_path else ''

        # 生成URL
        url = generate_presigned_url(client, bucket, file_key, url_expires)
        if not url:
            continue

        # 计算URL过期时间
        expires_at = datetime.now() + timedelta(seconds=url_expires)

        file_data = {
            "id": idx,
            "filename": file_path.name,
            "object_key": file_key,
            "size": file_info['size'],
            "last_modified": file_info['last_modified'],
            "url": url,
            "url_valid_until": expires_at.isoformat()
        }

        # 按目录分组
        if relative_dir not in dir_files_map:
            dir_files_map[relative_dir] = []
        dir_files_map[relative_dir].append(file_data)

        print(f"  [{idx}/{len(image_files)}] {file_path.name}")

    print(f"\n✅ 成功生成 {sum(len(files) for files in dir_files_map.values())} 个URL\n")

    # 创建本地目录并保存JSON
    print(f"💾 保存索引文件...")
    local_base = Path(local_base_path)
    local_base.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    saved_files = []

    for dir_path, files_list in dir_files_map.items():
        # 创建对应的本地目录
        if dir_path:
            local_dir = local_base / dir_path
        else:
            local_dir = local_base

        local_dir.mkdir(parents=True, exist_ok=True)

        # 生成JSON索引
        json_data = {
            "metadata": {
                "source": "cos",
                "bucket": bucket,
                "prefix": cos_prefix,
                "directory": dir_path if dir_path else "(root)",
                "scan_time": timestamp,
                "total_images": len(files_list),
                "url_expires": url_expires,
                "version": "1.0"
            },
            "images": files_list
        }

        # 生成文件名(固定格式,不带时间戳)
        dir_safe = dir_path.replace('/', '-') if dir_path else 'root'
        json_filename = f"cos-index-{dir_safe}.json"
        json_path = local_dir / json_filename

        # 检查文件是否已存在
        if json_path.exists():
            print(f"  ⚠️  文件已存在,覆盖: {json_path}")

        # 保存JSON (覆盖模式)
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)

        saved_files.append(str(json_path))
        print(f"  ✅ {json_path}")

    # 统计信息
    total_images = sum(len(files) for files in dir_files_map.values())
    total_size = sum(int(file['size']) if isinstance(file['size'], str) else file['size']
                     for files in dir_files_map.values() for file in files)

    print(f"\n{'=' * 80}")
    print(f"🎉 索引生成完成！")
    print(f"{'=' * 80}\n")
    print(f"📊 统计信息:")
    print(f"  - 总文件数: {total_images} 个")
    print(f"  - 总大小: {total_size / 1024 / 1024:.2f} MB")
    print(f"  - 目录层级: {len(dir_files_map)} 个")
    print(f"  - 索引文件: {len(saved_files)} 个")
    print(f"  - URL有效期: {url_expires / 3600:.1f} 小时")
    print(f"  - 过期时间: {(datetime.now() + timedelta(seconds=url_expires)).strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    return {
        'success': True,
        'total_images': total_images,
        'total_size': total_size,
        'directories': len(dir_files_map),
        'index_files': saved_files
    }


def main():
    """主函数"""
    print("=" * 80)
    print("🚀 COS批量URL提取任务 - /2指令")
    print("=" * 80)

    # 创建COS客户端
    print("\n📋 初始化COS客户端...")
    try:
        client = create_cos_client()
        bucket = os.getenv('Bucket', 'minghong-redbook-1353737511')
        print(f"✅ 客户端创建成功")
        print(f"   Bucket: {bucket}")
    except Exception as e:
        print(f"❌ 客户端创建失败: {str(e)}")
        return

    # 项目根目录
    project_root = Path(__file__).parent.parent

    # 定义任务
    tasks = [
        {
            'cos_prefix': '输入/旅游/模板5/',
            'local_path': project_root / 'input' / '明红' / '图片URL' / '模板5'
        },
        {
            'cos_prefix': '输入/旅游/模板6/',
            'local_path': project_root / 'input' / '明红' / '图片URL' / '模板6'
        },
        {
            'cos_prefix': '输入/旅游/模板7/',
            'local_path': project_root / 'input' / '明红' / '图片URL' / '模板7'
        }
    ]

    # 执行任务
    all_results = []

    for idx, task in enumerate(tasks, 1):
        print(f"\n\n{'#' * 80}")
        print(f"任务 {idx}/{len(tasks)}: {task['cos_prefix']}")
        print(f"{'#' * 80}\n")

        result = extract_urls(
            client=client,
            bucket=bucket,
            cos_prefix=task['cos_prefix'],
            local_base_path=task['local_path'],
            url_expires=86400  # 24小时
        )

        all_results.append({
            'task': task,
            'result': result
        })

    # 打印总结
    print(f"\n{'=' * 80}")
    print("📊 全部任务总结")
    print(f"{'=' * 80}\n")

    total_images = 0
    total_index_files = 0

    for idx, item in enumerate(all_results, 1):
        task = item['task']
        result = item['result']

        print(f"任务 {idx}: {task['cos_prefix']}")
        if result.get('success'):
            print(f"  ✅ 成功")
            print(f"  - 图片总数: {result['total_images']} 个")
            print(f"  - 子目录数: {result['directories']} 个")
            print(f"  - 索引文件: {len(result['index_files'])} 个")
            total_images += result['total_images']
            total_index_files += len(result['index_files'])
        else:
            print(f"  ❌ 失败: {result.get('message', '未知错误')}")
        print()

    print(f"{'=' * 80}")
    print(f"✅ 全部完成!")
    print(f"   总图片数: {total_images} 个")
    print(f"   总索引文件: {total_index_files} 个")
    print(f"{'=' * 80}\n")


if __name__ == '__main__':
    main()
