import { NextResponse } from 'next/server';
import { promises as fs } from 'fs';
import path from 'path';
import type { FileNode } from '@/types/resources';

// 项目根目录的 output 文件夹路径
const OUTPUT_DIR = path.join(process.cwd(), '../../output');

/**
 * 递归扫描目录，构建文件树
 */
async function scanDirectory(
  dirPath: string,
  basePath: string = '',
  idPrefix: string = ''
): Promise<FileNode[]> {
  const entries = await fs.readdir(dirPath, { withFileTypes: true });
  const nodes: FileNode[] = [];

  for (let i = 0; i < entries.length; i++) {
    const entry = entries[i];
    const fullPath = path.join(dirPath, entry.name);
    const relativePath = path.join(basePath, entry.name);
    const id = idPrefix ? `${idPrefix}-${i}` : `${i}`;

    // 跳过隐藏文件和系统文件
    if (entry.name.startsWith('.') || entry.name === 'node_modules') {
      continue;
    }

    try {
      const stats = await fs.stat(fullPath);

      if (entry.isDirectory()) {
        // 递归扫描子目录
        const children = await scanDirectory(fullPath, relativePath, id);

        nodes.push({
          id,
          name: entry.name,
          type: 'folder',
          path: `/${relativePath}`,
          modifiedAt: stats.mtime,
          children: children.length > 0 ? children : undefined,
        });
      } else if (entry.isFile()) {
        const extension = path.extname(entry.name).slice(1);

        nodes.push({
          id,
          name: entry.name,
          type: 'file',
          path: `/${relativePath}`,
          extension,
          size: stats.size,
          modifiedAt: stats.mtime,
        });
      }
    } catch (error) {
      console.error(`Error scanning ${fullPath}:`, error);
      // 继续处理其他文件
      continue;
    }
  }

  return nodes;
}

/**
 * 计算统计信息
 */
function calculateStats(nodes: FileNode[]): {
  totalFiles: number;
  totalFolders: number;
  totalSize: number;
} {
  let totalFiles = 0;
  let totalFolders = 0;
  let totalSize = 0;

  function traverse(node: FileNode) {
    if (node.type === 'folder') {
      totalFolders++;
      if (node.children) {
        node.children.forEach(traverse);
      }
    } else {
      totalFiles++;
      totalSize += node.size || 0;
    }
  }

  nodes.forEach(traverse);

  return { totalFiles, totalFolders, totalSize };
}

/**
 * GET /api/resources
 * 返回 output 目录的文件树
 */
export async function GET() {
  try {
    // 检查 output 目录是否存在
    try {
      await fs.access(OUTPUT_DIR);
    } catch {
      return NextResponse.json(
        {
          data: [],
          stats: {
            totalFiles: 0,
            totalFolders: 0,
            totalSize: 0,
          },
          message: 'output 目录不存在',
        },
        { status: 200 }
      );
    }

    // 扫描目录
    const fileTree = await scanDirectory(OUTPUT_DIR);
    const stats = calculateStats(fileTree);

    return NextResponse.json({
      data: fileTree,
      stats,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    console.error('Error scanning output directory:', error);
    return NextResponse.json(
      {
        error: '扫描文件系统失败',
        message: error instanceof Error ? error.message : '未知错误',
      },
      { status: 500 }
    );
  }
}
