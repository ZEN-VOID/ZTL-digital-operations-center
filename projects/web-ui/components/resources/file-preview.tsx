'use client';

import { useState, useEffect } from 'react';
import type { FileNode } from '@/types/resources';
import ImagePreview from './preview/image-preview';
import VideoAudioPreview from './preview/video-audio-preview';
import CodePreview from './preview/code-preview';
import MarkdownPreview from './preview/markdown-preview';
import FileActions from './file-actions';

interface FilePreviewProps {
  file: FileNode | null;
}

// File type categories
const IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg', 'bmp', 'ico'];
const VIDEO_EXTENSIONS = ['mp4', 'webm', 'ogg', 'mov', 'avi', 'mkv'];
const AUDIO_EXTENSIONS = ['mp3', 'wav', 'ogg', 'm4a', 'aac', 'flac'];
const CODE_EXTENSIONS = [
  'js', 'jsx', 'ts', 'tsx', 'py', 'java', 'c', 'cpp', 'cs', 'go', 'rs',
  'rb', 'php', 'swift', 'kt', 'scala', 'html', 'htm', 'css', 'scss',
  'sass', 'less', 'json', 'yaml', 'yml', 'toml', 'ini', 'sql', 'sh',
  'bash', 'zsh', 'fish', 'ps1', 'dockerfile', 'xml',
];
const MARKDOWN_EXTENSIONS = ['md', 'markdown'];
const TEXT_EXTENSIONS = ['txt', 'log', 'csv', 'env', 'gitignore', 'conf', 'config'];

interface FileContent {
  type: 'text' | 'image' | 'video' | 'audio' | 'binary';
  content?: string;
  extension?: string;
  size?: number;
  modifiedAt?: string;
  message?: string;
}

export default function FilePreview({ file }: FilePreviewProps) {
  const [fileContent, setFileContent] = useState<FileContent | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!file || file.type === 'folder') {
      setFileContent(null);
      setError(null);
      return;
    }

    async function loadFileContent() {
      try {
        setIsLoading(true);
        setError(null);

        // Build API URL from file path
        const apiPath = file.path.startsWith('/') ? file.path.slice(1) : file.path;
        const response = await fetch(`/api/resources/${apiPath}`);

        if (!response.ok) {
          throw new Error('Failed to fetch file content');
        }

        // Check if response is JSON (for text files and errors)
        const contentType = response.headers.get('Content-Type');
        if (contentType?.includes('application/json')) {
          const data = await response.json();
          if (data.error) {
            throw new Error(data.message || data.error);
          }
          setFileContent(data);
        } else {
          // For images, videos, audio - create blob URL
          const blob = await response.blob();
          const blobUrl = URL.createObjectURL(blob);
          setFileContent({
            type: getFileType(file.extension || ''),
            content: blobUrl,
            extension: file.extension,
            size: file.size,
            modifiedAt: file.modifiedAt?.toString(),
          });
        }
      } catch (err) {
        console.error('Error loading file content:', err);
        setError(err instanceof Error ? err.message : '加载文件失败');
      } finally {
        setIsLoading(false);
      }
    }

    loadFileContent();

    // Cleanup blob URLs
    return () => {
      if (fileContent?.content?.startsWith('blob:')) {
        URL.revokeObjectURL(fileContent.content);
      }
    };
  }, [file]);

  // Determine file type from extension
  const getFileType = (ext: string): 'text' | 'image' | 'video' | 'audio' | 'binary' => {
    const extension = ext.toLowerCase();
    if (IMAGE_EXTENSIONS.includes(extension)) return 'image';
    if (VIDEO_EXTENSIONS.includes(extension)) return 'video';
    if (AUDIO_EXTENSIONS.includes(extension)) return 'audio';
    if (CODE_EXTENSIONS.includes(extension) || MARKDOWN_EXTENSIONS.includes(extension) || TEXT_EXTENSIONS.includes(extension)) {
      return 'text';
    }
    return 'binary';
  };

  // Determine preview type
  const getPreviewType = (ext: string): 'image' | 'video' | 'audio' | 'code' | 'markdown' | 'text' | 'binary' => {
    const extension = ext.toLowerCase();
    if (IMAGE_EXTENSIONS.includes(extension)) return 'image';
    if (VIDEO_EXTENSIONS.includes(extension)) return 'video';
    if (AUDIO_EXTENSIONS.includes(extension)) return 'audio';
    if (MARKDOWN_EXTENSIONS.includes(extension)) return 'markdown';
    if (CODE_EXTENSIONS.includes(extension)) return 'code';
    if (TEXT_EXTENSIONS.includes(extension)) return 'text';
    return 'binary';
  };

  // Format file size
  const formatSize = (bytes: number): string => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return `${(bytes / Math.pow(k, i)).toFixed(2)} ${sizes[i]}`;
  };

  // No file selected
  if (!file) {
    return (
      <div className="glass-panel rounded-lg h-full flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl mb-4">📂</div>
          <div className="text-text-secondary font-electrolize">选择一个文件以预览</div>
        </div>
      </div>
    );
  }

  // Folder selected
  if (file.type === 'folder') {
    return (
      <div className="glass-panel rounded-lg h-full flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl mb-4">📁</div>
          <div className="text-xl font-orbitron text-neon-cyan mb-2">{file.name}</div>
          <div className="text-text-secondary font-electrolize">文件夹</div>
        </div>
      </div>
    );
  }

  // Loading state
  if (isLoading) {
    return (
      <div className="glass-panel rounded-lg h-full flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-neon-cyan mb-4"></div>
          <div className="text-text-secondary font-electrolize">正在加载文件...</div>
        </div>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="glass-panel neon-glow-pink rounded-lg h-full flex items-center justify-center p-8">
        <div className="text-center max-w-md">
          <div className="text-6xl mb-4">⚠️</div>
          <div className="text-xl font-orbitron text-neon-pink mb-2">加载失败</div>
          <div className="text-text-secondary font-electrolize">{error}</div>
        </div>
      </div>
    );
  }

  // No content loaded yet
  if (!fileContent) {
    return (
      <div className="glass-panel rounded-lg h-full flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl mb-4">📄</div>
          <div className="text-text-secondary font-electrolize">等待加载...</div>
        </div>
      </div>
    );
  }

  // Render appropriate preview component
  const previewType = getPreviewType(file.extension || '');

  switch (previewType) {
    case 'image':
      return (
        <div className="glass-panel rounded-lg h-full overflow-hidden flex flex-col">
          <FileActions file={file} />
          <div className="flex-1 overflow-hidden mt-4">
            <ImagePreview src={fileContent.content || ''} alt={file.name} />
          </div>
        </div>
      );

    case 'video':
      return (
        <div className="glass-panel rounded-lg h-full overflow-hidden flex flex-col">
          <FileActions file={file} />
          <div className="flex-1 overflow-hidden mt-4">
            <VideoAudioPreview
              src={fileContent.content || ''}
              type="video"
              mimeType={`video/${file.extension}`}
            />
          </div>
        </div>
      );

    case 'audio':
      return (
        <div className="glass-panel rounded-lg h-full overflow-hidden flex flex-col">
          <FileActions file={file} />
          <div className="flex-1 overflow-hidden mt-4">
            <VideoAudioPreview
              src={fileContent.content || ''}
              type="audio"
              mimeType={`audio/${file.extension}`}
            />
          </div>
        </div>
      );

    case 'markdown':
      return (
        <div className="glass-panel rounded-lg h-full overflow-hidden flex flex-col">
          <FileActions file={file} fileContent={fileContent.content} />
          <div className="flex-1 overflow-hidden mt-4">
            <MarkdownPreview content={fileContent.content || ''} filename={file.name} />
          </div>
        </div>
      );

    case 'code':
      return (
        <div className="glass-panel rounded-lg h-full overflow-hidden flex flex-col">
          <FileActions file={file} fileContent={fileContent.content} />
          <div className="flex-1 overflow-hidden mt-4">
            <CodePreview
              content={fileContent.content || ''}
              language={file.extension || 'text'}
              filename={file.name}
            />
          </div>
        </div>
      );

    case 'text':
      return (
        <div className="glass-panel rounded-lg h-full overflow-hidden flex flex-col">
          <FileActions file={file} fileContent={fileContent.content} />
          <div className="flex-1 overflow-auto p-6 mt-4">
            <pre className="text-text-primary font-mono text-sm whitespace-pre-wrap break-words glass-panel neon-glow-cyan rounded-lg p-6">
              {fileContent.content}
            </pre>
          </div>
        </div>
      );

    case 'binary':
    default:
      return (
        <div className="glass-panel rounded-lg h-full overflow-hidden flex flex-col">
          <FileActions file={file} />
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center max-w-md">
              <div className="text-6xl mb-4">📦</div>
              <div className="text-xl font-orbitron text-neon-cyan mb-2">{file.name}</div>
              <div className="text-text-secondary font-electrolize mb-4">
                {fileContent.message || '此文件类型不支持预览'}
              </div>
              <div className="text-xs text-text-secondary font-electrolize">
                大小: {file.size ? formatSize(file.size) : 'Unknown'}
              </div>
              {file.modifiedAt && (
                <div className="text-xs text-text-secondary font-electrolize mt-1">
                  修改时间: {new Date(file.modifiedAt).toLocaleString('zh-CN')}
                </div>
              )}
            </div>
          </div>
        </div>
      );
  }
}
