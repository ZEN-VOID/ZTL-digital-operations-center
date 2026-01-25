'use client';

import { useState, useEffect } from 'react';
import FileExplorer from '@/components/resources/file-explorer';
import FilePreview from '@/components/resources/file-preview';
import UploadZone from '@/components/resources/upload-zone';
import { Navigation } from '@/components/layout/navigation';
import type { FileNode } from '@/types/resources';

interface ResourceStats {
  totalFiles: number;
  totalFolders: number;
  totalSize: number;
}

export default function ResourcesPage() {
  const [fileData, setFileData] = useState<FileNode[]>([]);
  const [stats, setStats] = useState<ResourceStats>({
    totalFiles: 0,
    totalFolders: 0,
    totalSize: 0,
  });
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<FileNode | null>(null);
  const [isLeftPanelOpen, setIsLeftPanelOpen] = useState(true);
  const [showUpload, setShowUpload] = useState(false);

  // 加载文件数据
  useEffect(() => {
    async function loadResources() {
      try {
        setIsLoading(true);
        setError(null);

        const response = await fetch('/api/resources');

        if (!response.ok) {
          throw new Error('Failed to fetch resources');
        }

        const result = await response.json();

        if (result.error) {
          throw new Error(result.message || result.error);
        }

        setFileData(result.data || []);
        setStats(result.stats || { totalFiles: 0, totalFolders: 0, totalSize: 0 });
      } catch (err) {
        console.error('Error loading resources:', err);
        setError(err instanceof Error ? err.message : '加载资源失败');
      } finally {
        setIsLoading(false);
      }
    }

    loadResources();
  }, []);

  const handleFileSelect = (file: FileNode) => {
    setSelectedFile(file);
  };

  const handleUpload = (files: File[]) => {
    console.log('Uploading files:', files);
    // TODO: 实现文件上传功能
  };

  const handleRefresh = async () => {
    setIsLoading(true);
    try {
      const response = await fetch('/api/resources');
      const result = await response.json();
      setFileData(result.data || []);
      setStats(result.stats || { totalFiles: 0, totalFolders: 0, totalSize: 0 });
    } catch (err) {
      console.error('Error refreshing resources:', err);
    } finally {
      setIsLoading(false);
    }
  };

  // 格式化文件大小
  const formatSize = (bytes: number): string => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return `${(bytes / Math.pow(k, i)).toFixed(2)} ${sizes[i]}`;
  };

  return (
    <div className="flex flex-col h-screen bg-cyber-bg-primary">
      {/* Background */}
      <div className="fixed inset-0 cyber-grid-bg opacity-20 pointer-events-none" />
      <div className="fixed inset-0 bg-gradient-to-b from-transparent via-neon-cyan/5 to-transparent animate-[grid-move_3s_linear_infinite] pointer-events-none" />

      {/* Header */}
      <header className="flex-shrink-0 border-b border-text-secondary/20 bg-cyber-bg-secondary/50 backdrop-blur-md relative z-10">
        <div className="px-4 py-4">
          {/* Navigation */}
          <div className="mb-4">
            <Navigation variant="header" />
          </div>

          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-2xl sm:text-3xl font-bold neon-text-cyan font-orbitron">
                资源管理
              </h1>
              <p className="text-text-secondary font-electrolize text-sm mt-1">
                Resource Management Center
              </p>
            </div>

            <div className="flex items-center gap-2">
              {/* Toggle Left Panel */}
              <button
                onClick={() => setIsLeftPanelOpen(!isLeftPanelOpen)}
                className="neon-glow-cyan px-3 py-1.5 rounded-lg text-neon-cyan hover:bg-neon-cyan/10 transition-all lg:hidden text-sm"
                title="切换侧边栏"
              >
                {isLeftPanelOpen ? '◀' : '▶'}
              </button>

              {/* Refresh Button */}
              <button
                onClick={handleRefresh}
                disabled={isLoading}
                className="neon-glow-cyan px-3 py-1.5 rounded-lg text-neon-cyan hover:bg-neon-cyan/10 transition-all disabled:opacity-50 text-sm"
                title="刷新文件列表"
              >
                🔄 刷新
              </button>

              {/* Upload Button */}
              <button
                onClick={() => setShowUpload(!showUpload)}
                className={`
                  neon-glow-pink px-3 py-1.5 rounded-lg font-orbitron text-sm
                  transition-all duration-200
                  ${showUpload
                    ? 'bg-neon-pink/10 text-neon-pink'
                    : 'text-neon-pink hover:bg-neon-pink/10'
                  }
                `}
              >
                📤 上传
              </button>
            </div>
          </div>

          {/* Stats Bar */}
          <div className="grid grid-cols-4 gap-3 glass-panel rounded-lg p-3">
            <div className="text-center">
              <div className="text-lg font-bold neon-text-cyan font-orbitron">
                {isLoading ? '...' : stats.totalFiles}
              </div>
              <div className="text-xs text-text-secondary">文件</div>
            </div>
            <div className="text-center">
              <div className="text-lg font-bold neon-text-pink font-orbitron">
                {isLoading ? '...' : stats.totalFolders}
              </div>
              <div className="text-xs text-text-secondary">文件夹</div>
            </div>
            <div className="text-center">
              <div className="text-lg font-bold neon-text-cyan font-orbitron">
                {isLoading ? '...' : formatSize(stats.totalSize)}
              </div>
              <div className="text-xs text-text-secondary">总大小</div>
            </div>
            <div className="text-center">
              <div className="text-lg font-bold neon-text-pink font-orbitron">
                {isLoading ? '...' : fileData.length}
              </div>
              <div className="text-xs text-text-secondary">顶层项目</div>
            </div>
          </div>
        </div>

        {/* Upload Zone (Collapsible) */}
        {showUpload && (
          <div className="px-4 pb-4 animate-[message-appear_0.3s_ease-out]">
            <UploadZone onUpload={handleUpload} />
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="px-4 pb-4">
            <div className="glass-panel neon-glow-pink rounded-lg p-3">
              <div className="flex items-center gap-3">
                <span className="text-xl">⚠️</span>
                <div>
                  <div className="font-orbitron text-neon-pink text-sm">加载错误</div>
                  <div className="text-xs text-text-secondary mt-1">{error}</div>
                </div>
              </div>
            </div>
          </div>
        )}
      </header>

      {/* Main Content */}
      <div className="flex-1 overflow-hidden">
        {/* Loading State */}
        {isLoading && !error ? (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-neon-cyan mb-4"></div>
              <div className="text-text-secondary font-electrolize">正在加载资源...</div>
            </div>
          </div>
        ) : !error ? (
          <div className="h-full grid grid-cols-1 lg:grid-cols-12 gap-4 p-4">
            {/* Left Panel - File Explorer */}
            <div
              className={`
                lg:col-span-4 h-full overflow-hidden
                ${isLeftPanelOpen ? 'block' : 'hidden lg:block'}
              `}
            >
              <FileExplorer
                data={fileData}
                onSelect={handleFileSelect}
                selectedId={selectedFile?.id}
              />
            </div>

            {/* Right Panel - File Preview */}
            <div className="lg:col-span-8 h-full overflow-hidden">
              <FilePreview file={selectedFile} />
            </div>
          </div>
        ) : null}
      </div>

      {/* Status Indicator */}
      <div className="fixed bottom-6 right-6 z-20">
        <div className="glass-panel neon-glow-cyan rounded-full px-3 py-1.5 flex items-center gap-2">
          <div className={`w-2 h-2 rounded-full ${isLoading ? 'bg-neon-pink animate-neon-pulse' : 'bg-neon-green animate-neon-pulse'}`} />
          <span className="text-xs text-text-secondary font-electrolize">
            {isLoading ? '加载中...' : '在线'}
          </span>
        </div>
      </div>
    </div>
  );
}
