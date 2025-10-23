---
name: Tencent Cloud Object Storage
description: 腾讯云COS对象存储管理，提供文件上传下载、图片处理(AI增强/抠图/质量评估)、媒体智能封面、文档转换等18+专业功能，支持云端资源管理和AI图像处理
---

# Tencent Cloud COS MCP Skill

基于cos-mcp的腾讯云对象存储能力包，提供云端文件管理、AI图像处理、媒体处理和文档转换等完整功能。

## Quick Start

### 示例1: 文件上传与管理

```python
# 1. 上传本地文件
await mcp__cos_mcp__putObject(
    filePath="/path/to/local/image.jpg",
    fileName="product_image.jpg",
    targetDir="images/products/"
)

# 2. 从URL下载并上传
await mcp__cos_mcp__putObjectSourceUrl(
    sourceUrl="https://example.com/photo.jpg",
    fileName="photo.jpg",
    targetDir="images/gallery/"
)

# 3. 获取文件签名URL(用于分享)
url_info = await mcp__cos_mcp__getObjectUrl(
    objectKey="images/products/product_image.jpg"
)
# 返回带时效的签名下载链接

# 4. 列出目录下的文件
files = await mcp__cos_mcp__getBucket(
    Prefix="images/products/"
)
```

### 示例2: AI图像处理

```python
# 1. 图片质量评估
quality = await mcp__cos_mcp__assessQuality(
    objectKey="images/photo.jpg"
)
# 返回图片质量分数和评估报告

# 2. AI超分辨率增强
enhanced = await mcp__cos_mcp__aiSuperResolution(
    objectKey="images/low_res.jpg"
)
# 自动提升图片分辨率和清晰度

# 3. AI智能抠图
matting = await mcp__cos_mcp__aiPicMatting(
    objectKey="images/person.jpg",
    width="1920",
    height="1080"
)
# 自动识别主体并去除背景

# 4. 添加文字水印
watermarked = await mcp__cos_mcp__waterMarkFont(
    objectKey="images/photo.jpg",
    text="版权所有 © 2024"
)
```

### 示例3: 二维码识别与图片搜索

```python
# 1. 识别图片中的二维码
qrcode_info = await mcp__cos_mcp__aiQrcode(
    objectKey="images/qrcode.jpg"
)
# 返回二维码内容

# 2. 以图搜图
similar_images = await mcp__cos_mcp__imageSearchPic(
    uri="https://example.com/reference.jpg"
)

# 3. 文本搜图
search_results = await mcp__cos_mcp__imageSearchText(
    text="蓝色的海洋"
)
```

### 示例4: 媒体与文档处理

```python
# 1. 创建视频智能封面任务
job = await mcp__cos_mcp__createMediaSmartCoverJob(
    objectKey="videos/demo.mp4"
)

# 2. 查询处理任务状态
result = await mcp__cos_mcp__describeMediaJob(
    jobId=job['jobId']
)

# 3. 文档转PDF
doc_job = await mcp__cos_mcp__createDocToPdfJob(
    objectKey="documents/report.docx"
)

# 4. 查询文档转换结果
pdf_result = await mcp__cos_mcp__describeDocProcessJob(
    jobId=doc_job['jobId']
)
```

## Core Capabilities

### 1. 基础存储操作 (Basic Storage Operations)

#### 1.1 获取COS配置
```python
config = await mcp__cos_mcp__getCosConfig()
# 返回当前COS配置信息
```

#### 1.2 上传本地文件
```python
await mcp__cos_mcp__putObject(
    filePath="/Users/username/photo.jpg",  # 本地文件路径(含文件名)
    fileName="avatar.jpg",  # 存储在COS中的文件名(可选)
    targetDir="users/avatars/"  # 目标目录(可选)
)
```

**参数说明**:
- `filePath` (必需): 本地文件完整路径
- `fileName` (可选): COS中的文件名，默认使用原文件名
- `targetDir` (可选): COS中的目标目录，默认为根目录

#### 1.3 从URL上传文件
```python
await mcp__cos_mcp__putObjectSourceUrl(
    sourceUrl="https://cdn.example.com/image.png",  # 可下载的文件URL
    fileName="downloaded_image.png",  # 存储文件名(可选)
    targetDir="downloads/"  # 目标目录(可选)
)
```

**使用场景**: 从第三方URL直接下载并存储到COS，无需本地中转

#### 1.4 获取文件下载链接
```python
url_info = await mcp__cos_mcp__getObjectUrl(
    objectKey="images/photo.jpg"  # 文件的完整路径
)
# 返回带签名的临时下载链接(有时效性)
```

#### 1.5 下载文件
```python
file_data = await mcp__cos_mcp__getObject(
    objectKey="documents/report.pdf"
)
# 下载文件内容到本地
```

#### 1.6 列出存储桶文件
```python
files = await mcp__cos_mcp__getBucket(
    Prefix="images/"  # 路径前缀(可选)，默认列出根目录
)

# 遍历文件
for file in files['Contents']:
    print(f"文件: {file['Key']}, 大小: {file['Size']} bytes")
```

### 2. AI图像处理 (AI Image Processing)

#### 2.1 获取图片信息
```python
info = await mcp__cos_mcp__imageInfo(
    objectKey="images/photo.jpg"
)
# 返回: 宽度、高度、格式、大小等元数据
```

#### 2.2 图片质量评估
```python
quality_report = await mcp__cos_mcp__assessQuality(
    objectKey="images/photo.jpg"
)

# 返回质量评估结果:
# - 整体质量分数
# - 清晰度评分
# - 色彩评分
# - 构图评分
```

**应用场景**:
- 自动筛选高质量图片
- 用户上传图片质量检测
- 图片库质量分析

#### 2.3 AI超分辨率
```python
enhanced_image = await mcp__cos_mcp__aiSuperResolution(
    objectKey="images/low_resolution.jpg"
)

# 功能: 自动提升图片分辨率和清晰度
# 适用: 低分辨率图片增强、老照片修复
```

#### 2.4 AI智能抠图
```python
matting_result = await mcp__cos_mcp__aiPicMatting(
    objectKey="images/person.jpg",
    width="1920",  # 输出宽度(可选)
    height="1080"  # 输出高度(可选)
)

# 功能: 自动识别主体并去除背景
# 返回: 透明背景PNG图片
```

**应用场景**:
- 电商产品图片去背景
- 证件照背景更换
- 人像抠图

#### 2.5 二维码识别
```python
qrcode_data = await mcp__cos_mcp__aiQrcode(
    objectKey="images/qrcode_image.jpg"
)

# 返回二维码内容:
# - 解析的文本/URL
# - 二维码类型
# - 位置坐标
```

**使用场景**:
- 批量识别二维码
- 图片中二维码提取
- 二维码内容验证

#### 2.6 文字水印
```python
watermarked = await mcp__cos_mcp__waterMarkFont(
    objectKey="images/photo.jpg",
    text="版权所有 © 2024 公司名称"  # 水印文字，支持中文
)

# 功能: 添加文字水印到图片
# 返回: 带水印的图片URL
```

**特性**:
- 支持中文水印
- 自动调整水印位置
- 保持原图质量

### 3. 图片搜索 (Image Search)

#### 3.1 以图搜图
```python
similar_images = await mcp__cos_mcp__imageSearchPic(
    uri="https://example.com/reference_image.jpg"
)

# 返回相似图片列表:
# - 相似度评分
# - 图片URL
# - 元数据
```

**应用场景**:
- 相似图片查找
- 重复图片检测
- 商品图片匹配

#### 3.2 文本搜图
```python
results = await mcp__cos_mcp__imageSearchText(
    text="蓝色的海洋 日落 沙滩"
)

# 功能: 根据文字描述搜索图片
# 返回: 匹配的图片列表
```

**应用场景**:
- 语义化图片检索
- 图库智能搜索
- 内容推荐

### 4. 媒体处理 (Media Processing)

#### 4.1 创建智能封面任务
```python
job = await mcp__cos_mcp__createMediaSmartCoverJob(
    objectKey="videos/tutorial.mp4"
)

# 功能: 自动分析视频并生成封面图
# 返回: 任务ID
```

#### 4.2 查询媒体任务结果
```python
result = await mcp__cos_mcp__describeMediaJob(
    jobId="job_xxxxxxxxxxxx"  # 任务ID
)

# 返回任务状态:
# - 处理状态 (处理中/成功/失败)
# - 封面图片URL
# - 处理时长
```

**使用场景**:
- 视频封面自动生成
- 视频关键帧提取
- 批量视频处理

### 5. 文档处理 (Document Processing)

#### 5.1 创建文档转PDF任务
```python
job = await mcp__cos_mcp__createDocToPdfJob(
    objectKey="documents/report.docx"
)

# 支持格式:
# - Word (.docx, .doc)
# - Excel (.xlsx, .xls)
# - PowerPoint (.pptx, .ppt)
# - 其他文档格式
```

#### 5.2 查询文档转换结果
```python
result = await mcp__cos_mcp__describeDocProcessJob(
    jobId="doc_job_xxxxxxxxxxxx"
)

# 返回:
# - 转换状态
# - PDF文件URL
# - 页数统计
# - 错误信息(如有)
```

**应用场景**:
- 文档格式统一转换
- 在线预览生成
- 归档文件转换

## Usage Patterns

### Pattern 1: 图片上传与优化流程

```python
async def upload_and_optimize_image(local_path: str, category: str):
    """上传图片并进行AI优化"""

    # 1. 上传原图
    file_name = f"{category}_{timestamp}.jpg"
    await mcp__cos_mcp__putObject(
        filePath=local_path,
        fileName=file_name,
        targetDir=f"images/{category}/original/"
    )

    # 2. 质量评估
    quality = await mcp__cos_mcp__assessQuality(
        objectKey=f"images/{category}/original/{file_name}"
    )

    # 3. 如果质量较低，进行超分辨率增强
    if quality['score'] < 70:
        enhanced = await mcp__cos_mcp__aiSuperResolution(
            objectKey=f"images/{category}/original/{file_name}"
        )
        final_key = enhanced['objectKey']
    else:
        final_key = f"images/{category}/original/{file_name}"

    # 4. 添加水印
    watermarked = await mcp__cos_mcp__waterMarkFont(
        objectKey=final_key,
        text="© 2024 Company"
    )

    # 5. 获取最终URL
    url = await mcp__cos_mcp__getObjectUrl(
        objectKey=watermarked['objectKey']
    )

    return url
```

### Pattern 2: 批量图片处理

```python
async def batch_process_images(image_folder: str):
    """批量处理图片目录"""

    # 1. 列出所有图片
    files = await mcp__cos_mcp__getBucket(
        Prefix=image_folder
    )

    results = []

    for file in files.get('Contents', []):
        object_key = file['Key']

        # 跳过非图片文件
        if not object_key.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        try:
            # 2. 质量评估
            quality = await mcp__cos_mcp__assessQuality(
                objectKey=object_key
            )

            # 3. 根据质量决定是否增强
            if quality['score'] < 60:
                enhanced = await mcp__cos_mcp__aiSuperResolution(
                    objectKey=object_key
                )
                status = "enhanced"
            else:
                status = "original"

            results.append({
                "file": object_key,
                "quality": quality['score'],
                "status": status
            })

        except Exception as e:
            results.append({
                "file": object_key,
                "error": str(e)
            })

    return results
```

### Pattern 3: 视频封面自动生成

```python
async def generate_video_cover(video_key: str, wait_for_result: bool = True):
    """生成视频封面"""

    # 1. 创建智能封面任务
    job = await mcp__cos_mcp__createMediaSmartCoverJob(
        objectKey=video_key
    )

    job_id = job['jobId']

    if not wait_for_result:
        return {"jobId": job_id, "status": "processing"}

    # 2. 轮询等待任务完成
    import asyncio
    max_retries = 30
    retry_delay = 10  # seconds

    for i in range(max_retries):
        result = await mcp__cos_mcp__describeMediaJob(
            jobId=job_id
        )

        status = result.get('state')

        if status == 'Success':
            return {
                "jobId": job_id,
                "status": "success",
                "coverUrl": result.get('coverUrl'),
                "covers": result.get('covers', [])
            }
        elif status == 'Failed':
            return {
                "jobId": job_id,
                "status": "failed",
                "error": result.get('message')
            }

        # 继续等待
        await asyncio.sleep(retry_delay)

    return {
        "jobId": job_id,
        "status": "timeout"
    }
```

### Pattern 4: 文档转换与归档

```python
async def convert_and_archive_documents(doc_folder: str):
    """批量转换文档为PDF并归档"""

    # 1. 列出所有文档
    files = await mcp__cos_mcp__getBucket(
        Prefix=doc_folder
    )

    supported_formats = ['.docx', '.doc', '.xlsx', '.xls', '.pptx', '.ppt']
    jobs = []

    for file in files.get('Contents', []):
        object_key = file['Key']

        # 检查是否为支持的文档格式
        if not any(object_key.lower().endswith(fmt) for fmt in supported_formats):
            continue

        # 2. 创建转换任务
        job = await mcp__cos_mcp__createDocToPdfJob(
            objectKey=object_key
        )

        jobs.append({
            "original": object_key,
            "jobId": job['jobId']
        })

    # 3. 等待所有任务完成
    results = []
    for job_info in jobs:
        result = await mcp__cos_mcp__describeDocProcessJob(
            jobId=job_info['jobId']
        )

        results.append({
            "original": job_info['original'],
            "pdf": result.get('pdfUrl'),
            "status": result.get('state')
        })

    return results
```

### Pattern 5: 智能图片库管理

```python
async def smart_image_library(action: str, **kwargs):
    """智能图片库管理"""

    if action == "upload":
        # 上传并自动分类
        local_path = kwargs['path']

        # 1. 上传原图
        await mcp__cos_mcp__putObject(
            filePath=local_path,
            targetDir="library/inbox/"
        )

        # 2. 质量评估
        quality = await mcp__cos_mcp__assessQuality(
            objectKey=f"library/inbox/{file_name}"
        )

        # 3. 根据质量分类
        if quality['score'] >= 80:
            target_dir = "library/high_quality/"
        elif quality['score'] >= 60:
            target_dir = "library/medium_quality/"
        else:
            target_dir = "library/low_quality/"

        # 4. 移动到分类目录(通过下载再上传实现)
        file_data = await mcp__cos_mcp__getObject(
            objectKey=f"library/inbox/{file_name}"
        )

        # ... 重新上传到分类目录

    elif action == "search":
        # 以图搜图或文本搜图
        if 'image_url' in kwargs:
            return await mcp__cos_mcp__imageSearchPic(
                uri=kwargs['image_url']
            )
        elif 'text' in kwargs:
            return await mcp__cos_mcp__imageSearchText(
                text=kwargs['text']
            )

    elif action == "enhance":
        # 批量增强低质量图片
        low_quality_files = await mcp__cos_mcp__getBucket(
            Prefix="library/low_quality/"
        )

        for file in low_quality_files.get('Contents', []):
            await mcp__cos_mcp__aiSuperResolution(
                objectKey=file['Key']
            )
```

## Best Practices

### 1. 文件命名规范
```python
# ✅ 推荐: 语义化命名
"products/category/product_id_view1.jpg"
"documents/reports/2024/Q1_financial_report.pdf"
"videos/tutorials/intro_video_v2.mp4"

# ❌ 避免: 随机或无意义命名
"abc123.jpg"
"untitled.pdf"
"video1.mp4"
```

### 2. 目录结构设计
```python
# 推荐的目录结构
"""
/images
  /products      # 产品图片
    /original    # 原图
    /optimized   # 优化后
    /watermarked # 带水印
  /users         # 用户上传
    /avatars     # 头像
    /photos      # 照片
/videos
  /tutorials     # 教程视频
  /covers        # 视频封面
/documents
  /contracts     # 合同
  /reports       # 报告
  /archives      # 归档
"""
```

### 3. 错误处理
```python
async def safe_upload(file_path: str, retry_count: int = 3):
    """带重试机制的安全上传"""

    for attempt in range(retry_count):
        try:
            await mcp__cos_mcp__putObject(
                filePath=file_path,
                targetDir="uploads/"
            )
            return {"status": "success"}

        except Exception as e:
            if attempt < retry_count - 1:
                # 等待后重试
                await asyncio.sleep(2 ** attempt)
                continue
            else:
                # 最后一次尝试失败
                return {
                    "status": "failed",
                    "error": str(e)
                }
```

### 4. 异步任务管理
```python
# 对于耗时任务，使用异步轮询
async def wait_for_job_completion(job_id: str, timeout: int = 300):
    """等待任务完成(带超时)"""

    start_time = time.time()
    check_interval = 5  # seconds

    while time.time() - start_time < timeout:
        result = await mcp__cos_mcp__describeMediaJob(
            jobId=job_id
        )

        if result.get('state') in ['Success', 'Failed']:
            return result

        await asyncio.sleep(check_interval)

    raise TimeoutError(f"Job {job_id} did not complete within {timeout}s")
```

### 5. 图片优化策略
```python
# 根据用途选择处理方式
async def optimize_for_purpose(image_key: str, purpose: str):
    """根据用途优化图片"""

    if purpose == "thumbnail":
        # 缩略图: 无需超高清
        return image_key

    elif purpose == "display":
        # 展示用: 评估质量
        quality = await mcp__cos_mcp__assessQuality(
            objectKey=image_key
        )

        if quality['score'] < 70:
            # 质量不佳，进行增强
            enhanced = await mcp__cos_mcp__aiSuperResolution(
                objectKey=image_key
            )
            return enhanced['objectKey']

    elif purpose == "print":
        # 打印用: 必须高清
        enhanced = await mcp__cos_mcp__aiSuperResolution(
            objectKey=image_key
        )
        return enhanced['objectKey']

    return image_key
```

### 6. 成本优化
```python
# 避免重复处理
processed_cache = {}

async def process_with_cache(object_key: str, operation: str):
    """带缓存的处理"""

    cache_key = f"{object_key}:{operation}"

    if cache_key in processed_cache:
        return processed_cache[cache_key]

    # 执行实际处理
    if operation == "enhance":
        result = await mcp__cos_mcp__aiSuperResolution(
            objectKey=object_key
        )
    elif operation == "matting":
        result = await mcp__cos_mcp__aiPicMatting(
            objectKey=object_key
        )

    # 缓存结果
    processed_cache[cache_key] = result
    return result
```

## Common Issues

### Issue 1: 文件路径错误
**问题**: 文件上传失败，提示路径不存在
**解决**:
```python
import os

# ✅ 使用绝对路径
file_path = os.path.abspath("/path/to/file.jpg")

# ✅ 检查文件是否存在
if not os.path.exists(file_path):
    raise FileNotFoundError(f"File not found: {file_path}")

await mcp__cos_mcp__putObject(
    filePath=file_path,
    targetDir="uploads/"
)
```

### Issue 2: objectKey格式错误
**问题**: 获取文件时提示objectKey无效
**解决**:
```python
# ❌ 错误: 包含开头斜杠
objectKey = "/images/photo.jpg"

# ✅ 正确: 不包含开头斜杠
objectKey = "images/photo.jpg"

await mcp__cos_mcp__getObject(objectKey=objectKey)
```

### Issue 3: 任务状态查询失败
**问题**: 查询媒体任务时提示任务不存在
**解决**:
```python
# 任务创建后需要等待一小段时间
job = await mcp__cos_mcp__createMediaSmartCoverJob(
    objectKey="videos/test.mp4"
)

# 等待几秒再查询
await asyncio.sleep(3)

result = await mcp__cos_mcp__describeMediaJob(
    jobId=job['jobId']
)
```

### Issue 4: 图片格式不支持
**问题**: AI处理时提示图片格式不支持
**解决**:
```python
supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.webp']

def check_image_format(object_key: str) -> bool:
    """检查图片格式是否支持"""
    ext = os.path.splitext(object_key)[1].lower()
    return ext in supported_formats

if not check_image_format(object_key):
    raise ValueError(f"Unsupported image format: {object_key}")
```

## Integration Examples

### 示例1: 电商图片管理系统

```python
async def ecommerce_image_pipeline(product_id: str, image_path: str):
    """电商产品图片处理流程"""

    # 1. 上传原图
    original_key = f"products/{product_id}/original.jpg"
    await mcp__cos_mcp__putObject(
        filePath=image_path,
        fileName="original.jpg",
        targetDir=f"products/{product_id}/"
    )

    # 2. AI抠图(去背景)
    matting = await mcp__cos_mcp__aiPicMatting(
        objectKey=original_key,
        width="1200",
        height="1200"
    )

    # 3. 超分辨率增强
    enhanced = await mcp__cos_mcp__aiSuperResolution(
        objectKey=matting['objectKey']
    )

    # 4. 添加品牌水印
    watermarked = await mcp__cos_mcp__waterMarkFont(
        objectKey=enhanced['objectKey'],
        text="© 品牌名称"
    )

    # 5. 生成多个尺寸版本(略)
    # ...

    # 6. 返回所有版本的URL
    return {
        "original": await mcp__cos_mcp__getObjectUrl(objectKey=original_key),
        "transparent": await mcp__cos_mcp__getObjectUrl(objectKey=matting['objectKey']),
        "enhanced": await mcp__cos_mcp__getObjectUrl(objectKey=enhanced['objectKey']),
        "final": await mcp__cos_mcp__getObjectUrl(objectKey=watermarked['objectKey'])
    }
```

### 示例2: 内容管理系统(CMS)

```python
async def cms_media_manager(action: str, **kwargs):
    """CMS媒体管理器"""

    if action == "upload_article_images":
        # 上传文章图片并优化
        images = kwargs['images']
        article_id = kwargs['article_id']

        optimized_urls = []

        for idx, image_path in enumerate(images):
            # 上传
            key = f"articles/{article_id}/image_{idx}.jpg"
            await mcp__cos_mcp__putObject(
                filePath=image_path,
                fileName=f"image_{idx}.jpg",
                targetDir=f"articles/{article_id}/"
            )

            # 质量检查
            quality = await mcp__cos_mcp__assessQuality(objectKey=key)

            if quality['score'] < 70:
                # 增强低质量图片
                enhanced = await mcp__cos_mcp__aiSuperResolution(objectKey=key)
                key = enhanced['objectKey']

            # 获取URL
            url = await mcp__cos_mcp__getObjectUrl(objectKey=key)
            optimized_urls.append(url)

        return optimized_urls

    elif action == "convert_documents":
        # 转换文章附件为PDF
        doc_key = kwargs['doc_key']

        job = await mcp__cos_mcp__createDocToPdfJob(
            objectKey=doc_key
        )

        # 等待转换完成
        result = await wait_for_job_completion(job['jobId'])

        return result.get('pdfUrl')
```

### 示例3: 视频平台自动化

```python
async def video_platform_automation(video_file: str):
    """视频平台自动化处理"""

    # 1. 上传视频
    video_id = generate_unique_id()
    video_key = f"videos/{video_id}/source.mp4"

    await mcp__cos_mcp__putObject(
        filePath=video_file,
        fileName="source.mp4",
        targetDir=f"videos/{video_id}/"
    )

    # 2. 生成智能封面
    cover_job = await mcp__cos_mcp__createMediaSmartCoverJob(
        objectKey=video_key
    )

    # 3. 异步等待封面生成
    cover_result = await wait_for_job_completion(cover_job['jobId'])

    # 4. 对封面添加标题水印
    if cover_result.get('coverUrl'):
        # 下载封面
        cover_key = extract_key_from_url(cover_result['coverUrl'])

        # 添加水印
        watermarked = await mcp__cos_mcp__waterMarkFont(
            objectKey=cover_key,
            text="精彩视频 点击观看"
        )

        final_cover_url = await mcp__cos_mcp__getObjectUrl(
            objectKey=watermarked['objectKey']
        )
    else:
        final_cover_url = None

    return {
        "video_id": video_id,
        "video_url": await mcp__cos_mcp__getObjectUrl(objectKey=video_key),
        "cover_url": final_cover_url
    }
```

## Tips & Tricks

### 1. 批量上传优化
```python
# 使用并发上传提高效率
import asyncio

async def batch_upload(file_list: list):
    """并发批量上传"""

    tasks = [
        mcp__cos_mcp__putObject(
            filePath=file_path,
            targetDir="batch_uploads/"
        )
        for file_path in file_list
    ]

    # 限制并发数
    semaphore = asyncio.Semaphore(5)

    async def upload_with_limit(task):
        async with semaphore:
            return await task

    results = await asyncio.gather(
        *[upload_with_limit(task) for task in tasks],
        return_exceptions=True
    )

    return results
```

### 2. 智能缓存策略
```python
# 缓存签名URL避免频繁请求
from datetime import datetime, timedelta

url_cache = {}

async def get_cached_url(object_key: str, cache_hours: int = 1):
    """获取带缓存的URL"""

    cache_key = object_key
    now = datetime.now()

    # 检查缓存
    if cache_key in url_cache:
        url, expire_time = url_cache[cache_key]
        if now < expire_time:
            return url

    # 获取新URL
    url_info = await mcp__cos_mcp__getObjectUrl(objectKey=object_key)
    url = url_info['url']

    # 缓存URL
    expire_time = now + timedelta(hours=cache_hours)
    url_cache[cache_key] = (url, expire_time)

    return url
```

### 3. 文件存在性检查
```python
async def check_file_exists(object_key: str) -> bool:
    """检查文件是否存在"""

    try:
        await mcp__cos_mcp__imageInfo(objectKey=object_key)
        return True
    except:
        return False
```

### 4. 条件处理
```python
async def conditional_enhance(object_key: str, min_quality: int = 70):
    """条件式图片增强"""

    # 先评估质量
    quality = await mcp__cos_mcp__assessQuality(objectKey=object_key)

    if quality['score'] < min_quality:
        # 质量不达标，进行增强
        enhanced = await mcp__cos_mcp__aiSuperResolution(
            objectKey=object_key
        )
        return enhanced['objectKey'], True
    else:
        # 质量合格，无需处理
        return object_key, False
```

### 5. 元数据管理
```python
# 使用文件名编码元数据
def encode_metadata_in_filename(
    base_name: str,
    quality: int,
    processed: bool,
    version: int
) -> str:
    """在文件名中编码元数据"""

    return f"{base_name}_q{quality}_{'proc' if processed else 'orig'}_v{version}.jpg"

# 示例
filename = encode_metadata_in_filename(
    base_name="product_001",
    quality=85,
    processed=True,
    version=2
)
# 结果: "product_001_q85_proc_v2.jpg"
```

### 6. 目录清理工具
```python
async def cleanup_old_files(folder: str, days_old: int = 30):
    """清理旧文件"""

    from datetime import datetime, timedelta

    cutoff_date = datetime.now() - timedelta(days=days_old)

    # 列出文件
    files = await mcp__cos_mcp__getBucket(Prefix=folder)

    for file in files.get('Contents', []):
        last_modified = file.get('LastModified')

        if last_modified and last_modified < cutoff_date:
            # 删除旧文件(需要使用COS SDK)
            print(f"Would delete: {file['Key']}")
```

### 7. 进度追踪
```python
async def process_with_progress(file_list: list, callback):
    """带进度回调的处理"""

    total = len(file_list)
    completed = 0

    for file_path in file_list:
        try:
            await mcp__cos_mcp__putObject(
                filePath=file_path,
                targetDir="uploads/"
            )
            completed += 1
            callback(completed, total, "success", file_path)

        except Exception as e:
            completed += 1
            callback(completed, total, "failed", file_path, str(e))

# 使用
def progress_callback(completed, total, status, file, error=None):
    print(f"Progress: {completed}/{total} - {file} - {status}")
    if error:
        print(f"Error: {error}")

await process_with_progress(files, progress_callback)
```

### 8. 智能重试机制
```python
async def upload_with_smart_retry(
    file_path: str,
    max_retries: int = 3,
    backoff_factor: float = 2.0
):
    """智能重试上传"""

    for attempt in range(max_retries):
        try:
            result = await mcp__cos_mcp__putObject(
                filePath=file_path,
                targetDir="uploads/"
            )
            return result

        except Exception as e:
            if attempt < max_retries - 1:
                # 指数退避
                delay = backoff_factor ** attempt
                print(f"Retry {attempt + 1}/{max_retries} after {delay}s")
                await asyncio.sleep(delay)
            else:
                # 所有尝试都失败
                raise Exception(f"Upload failed after {max_retries} attempts: {e}")
```
