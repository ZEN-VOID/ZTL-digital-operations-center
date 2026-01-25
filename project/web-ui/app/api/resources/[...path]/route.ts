import { NextRequest, NextResponse } from 'next/server';
import { promises as fs } from 'fs';
import path from 'path';

// 项目根目录的 output 文件夹路径
const OUTPUT_DIR = path.join(process.cwd(), '../../output');

// 支持的文本文件扩展名
const TEXT_EXTENSIONS = [
  'txt', 'md', 'json', 'yaml', 'yml', 'xml',
  'js', 'jsx', 'ts', 'tsx', 'css', 'scss', 'less',
  'html', 'htm', 'svg', 'py', 'java', 'c', 'cpp',
  'h', 'hpp', 'sh', 'bash', 'zsh', 'fish',
  'go', 'rs', 'rb', 'php', 'sql', 'gitignore',
  'env', 'conf', 'config', 'ini', 'toml',
];

// 支持的图片扩展名
const IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg', 'bmp', 'ico'];

// 支持的视频扩展名
const VIDEO_EXTENSIONS = ['mp4', 'webm', 'ogg', 'mov', 'avi', 'mkv'];

// 支持的音频扩展名
const AUDIO_EXTENSIONS = ['mp3', 'wav', 'ogg', 'm4a', 'aac', 'flac'];

/**
 * 获取文件的 MIME 类型
 */
function getMimeType(extension: string): string {
  const mimeTypes: Record<string, string> = {
    // 文本
    txt: 'text/plain',
    md: 'text/markdown',
    json: 'application/json',
    yaml: 'text/yaml',
    yml: 'text/yaml',
    xml: 'application/xml',

    // 代码
    js: 'text/javascript',
    jsx: 'text/javascript',
    ts: 'text/typescript',
    tsx: 'text/typescript',
    css: 'text/css',
    html: 'text/html',
    py: 'text/x-python',

    // 图片
    jpg: 'image/jpeg',
    jpeg: 'image/jpeg',
    png: 'image/png',
    gif: 'image/gif',
    webp: 'image/webp',
    svg: 'image/svg+xml',

    // 视频
    mp4: 'video/mp4',
    webm: 'video/webm',
    ogg: 'video/ogg',

    // 音频
    mp3: 'audio/mpeg',
    wav: 'audio/wav',
    m4a: 'audio/mp4',
  };

  return mimeTypes[extension.toLowerCase()] || 'application/octet-stream';
}

/**
 * GET /api/resources/[...path]
 * 获取文件内容或元数据
 */
export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ path: string[] }> }
) {
  try {
    // Next.js 16: params is now a Promise and must be awaited
    const { path: pathSegments } = await params;
    const filePath = pathSegments.join('/');
    const fullPath = path.join(OUTPUT_DIR, filePath);

    // 安全检查：确保路径在 OUTPUT_DIR 内
    const normalizedPath = path.normalize(fullPath);
    if (!normalizedPath.startsWith(OUTPUT_DIR)) {
      return NextResponse.json(
        { error: '无效的文件路径' },
        { status: 400 }
      );
    }

    // 检查文件是否存在
    try {
      await fs.access(fullPath);
    } catch {
      return NextResponse.json(
        { error: '文件不存在' },
        { status: 404 }
      );
    }

    // 获取文件统计信息
    const stats = await fs.stat(fullPath);

    // 如果是目录，返回错误
    if (stats.isDirectory()) {
      return NextResponse.json(
        { error: '无法读取目录内容' },
        { status: 400 }
      );
    }

    const extension = path.extname(fullPath).slice(1).toLowerCase();
    const searchParams = request.nextUrl.searchParams;
    const mode = searchParams.get('mode') || 'auto';

    // 文本文件：返回文本内容
    if (TEXT_EXTENSIONS.includes(extension) || mode === 'text') {
      const content = await fs.readFile(fullPath, 'utf-8');

      return NextResponse.json({
        type: 'text',
        extension,
        content,
        size: stats.size,
        modifiedAt: stats.mtime,
      });
    }

    // 图片文件：返回 base64 或直接提供文件流
    if (IMAGE_EXTENSIONS.includes(extension) || mode === 'image') {
      if (mode === 'base64') {
        const buffer = await fs.readFile(fullPath);
        const base64 = buffer.toString('base64');
        const mimeType = getMimeType(extension);

        return NextResponse.json({
          type: 'image',
          extension,
          data: `data:${mimeType};base64,${base64}`,
          size: stats.size,
          modifiedAt: stats.mtime,
        });
      }

      // 直接返回图片文件流
      const buffer = await fs.readFile(fullPath);
      return new NextResponse(buffer, {
        headers: {
          'Content-Type': getMimeType(extension),
          'Content-Length': stats.size.toString(),
          'Cache-Control': 'public, max-age=31536000',
        },
      });
    }

    // 视频/音频文件：返回文件流（支持 range 请求）
    if (VIDEO_EXTENSIONS.includes(extension) || AUDIO_EXTENSIONS.includes(extension)) {
      const buffer = await fs.readFile(fullPath);

      return new NextResponse(buffer, {
        headers: {
          'Content-Type': getMimeType(extension),
          'Content-Length': stats.size.toString(),
          'Accept-Ranges': 'bytes',
          'Cache-Control': 'public, max-age=31536000',
        },
      });
    }

    // 其他二进制文件：返回元数据
    return NextResponse.json({
      type: 'binary',
      extension,
      size: stats.size,
      modifiedAt: stats.mtime,
      message: '此文件类型不支持预览，请下载查看',
    });

  } catch (error) {
    console.error('Error reading file:', error);
    return NextResponse.json(
      {
        error: '读取文件失败',
        message: error instanceof Error ? error.message : '未知错误',
      },
      { status: 500 }
    );
  }
}
