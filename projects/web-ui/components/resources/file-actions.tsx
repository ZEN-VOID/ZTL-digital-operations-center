'use client';

import { useState, useRef, useEffect } from 'react';
import { createPortal } from 'react-dom';
import type { FileNode } from '@/types/resources';

interface FileActionsProps {
  file: FileNode;
  fileContent?: string; // For text files
}

export default function FileActions({ file, fileContent }: FileActionsProps) {
  const [showSendMenu, setShowSendMenu] = useState(false);
  const [copied, setCopied] = useState(false);
  const [menuPosition, setMenuPosition] = useState({ top: 0, left: 0 });
  const sendButtonRef = useRef<HTMLButtonElement>(null);

  // 计算菜单位置
  useEffect(() => {
    if (showSendMenu && sendButtonRef.current) {
      const rect = sendButtonRef.current.getBoundingClientRect();
      setMenuPosition({
        top: rect.bottom + 8, // 按钮下方 8px
        left: rect.right - 120, // 右对齐，菜单宽度 120px
      });
    }
  }, [showSendMenu]);

  // 复制文件路径或内容
  const handleCopy = async () => {
    try {
      let textToCopy = '';

      if (fileContent) {
        // 文本文件：复制内容
        textToCopy = fileContent;
      } else {
        // 其他文件：复制路径
        textToCopy = file.path;
      }

      await navigator.clipboard.writeText(textToCopy);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      console.error('Failed to copy:', error);
    }
  };

  // 下载文件
  const handleDownload = async () => {
    try {
      const apiPath = file.path.startsWith('/') ? file.path.slice(1) : file.path;
      const response = await fetch(`/api/resources/${apiPath}`);

      if (!response.ok) {
        throw new Error('Failed to download file');
      }

      // 获取文件内容
      const blob = await response.blob();

      // 创建下载链接
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = file.name;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Failed to download:', error);
      alert('下载失败，请重试');
    }
  };

  // 发送到微信
  const handleSendToWechat = () => {
    alert('微信发送功能开发中...\n\n将会集成企业微信 API 实现文件发送');
    setShowSendMenu(false);
  };

  // 发送到飞书
  const handleSendToLark = () => {
    alert('飞书发送功能开发中...\n\n将会集成飞书 API 实现文件发送');
    setShowSendMenu(false);
  };

  return (
    <div className="flex items-center gap-2 p-3 glass-panel rounded-lg neon-glow-cyan">
      {/* 文件信息 */}
      <div className="flex items-center gap-2 flex-1 min-w-0">
        <span className="text-xl">
          {file.type === 'file' ? '📄' : '📁'}
        </span>
        <div className="min-w-0 flex-1">
          <div className="font-orbitron text-neon-cyan text-sm truncate">
            {file.name}
          </div>
          <div className="text-xs text-text-secondary font-electrolize">
            {file.size ? formatSize(file.size) : 'Unknown'}
          </div>
        </div>
      </div>

      {/* 操作按钮 */}
      <div className="flex items-center gap-2">
        {/* 复制按钮 */}
        <button
          onClick={handleCopy}
          className={`
            px-3 py-1.5 rounded-lg transition-all duration-200 text-sm font-electrolize
            ${copied
              ? 'bg-neon-green/10 text-neon-green'
              : 'text-neon-cyan hover:bg-neon-cyan/10'
            }
          `}
          title={fileContent ? '复制内容' : '复制路径'}
        >
          {copied ? '已复制' : '复制'}
        </button>

        {/* 下载按钮 */}
        <button
          onClick={handleDownload}
          className="px-3 py-1.5 rounded-lg text-neon-cyan hover:bg-neon-cyan/10 transition-all duration-200 text-sm font-electrolize"
          title="下载文件"
        >
          下载
        </button>

        {/* 发送按钮 */}
        <button
          ref={sendButtonRef}
          onClick={() => setShowSendMenu(!showSendMenu)}
          className="px-3 py-1.5 rounded-lg text-neon-pink hover:bg-neon-pink/10 transition-all duration-200 text-sm font-electrolize"
          title="发送文件"
        >
          发送
        </button>
      </div>

      {/* 发送菜单 - 使用 Portal 渲染到 body */}
      {showSendMenu && typeof window !== 'undefined' && createPortal(
        <>
          {/* 点击外部关闭菜单 - backdrop */}
          <div
            className="fixed inset-0 z-[9998]"
            onClick={() => setShowSendMenu(false)}
          />

          {/* 菜单本体 */}
          <div
            className="fixed glass-panel neon-glow-pink rounded-lg overflow-hidden z-[9999] min-w-[120px] animate-[message-appear_0.2s_ease-out]"
            style={{
              top: `${menuPosition.top}px`,
              left: `${menuPosition.left}px`,
            }}
          >
            <button
              onClick={handleSendToWechat}
              className="w-full px-4 py-2 text-left text-sm font-electrolize text-text-primary hover:bg-neon-pink/10 transition-colors"
            >
              微信
            </button>
            <button
              onClick={handleSendToLark}
              className="w-full px-4 py-2 text-left text-sm font-electrolize text-text-primary hover:bg-neon-pink/10 transition-colors"
            >
              飞书
            </button>
          </div>
        </>,
        document.body
      )}
    </div>
  );
}

// 格式化文件大小
function formatSize(bytes: number): string {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${(bytes / Math.pow(k, i)).toFixed(2)} ${sizes[i]}`;
}
