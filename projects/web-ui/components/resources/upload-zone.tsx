'use client';

import { useState, useRef, DragEvent, ChangeEvent } from 'react';
import { uploadFiles, validateFile, type UploadProgress } from '@/lib/services/file-service';

interface UploadZoneProps {
  onUpload?: (files: File[]) => void;
}

export default function UploadZone({ onUpload }: UploadZoneProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [uploadQueue, setUploadQueue] = useState<UploadProgress[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragEnter = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const files = Array.from(e.dataTransfer.files);
    handleFiles(files);
  };

  const handleFileInput = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const files = Array.from(e.target.files);
      handleFiles(files);
    }
  };

  const handleFiles = async (files: File[]) => {
    // Validate files first
    const validFiles: File[] = [];
    const invalidFiles: string[] = [];

    files.forEach((file) => {
      const validation = validateFile(file);
      if (validation.valid) {
        validFiles.push(file);
      } else {
        invalidFiles.push(`${file.name}: ${validation.error}`);
      }
    });

    // Show validation errors
    if (invalidFiles.length > 0) {
      alert(`以下文件无法上传:\n${invalidFiles.join('\n')}`);
    }

    if (validFiles.length === 0) return;

    // Initialize upload queue
    const initialQueue: UploadProgress[] = validFiles.map((file) => ({
      file,
      progress: 0,
      status: 'pending',
    }));
    setUploadQueue(initialQueue);
    setIsUploading(true);

    try {
      // Upload files with progress tracking
      const results = await uploadFiles(validFiles, 'uploads', (fileIndex, progress) => {
        setUploadQueue((prev) => {
          const updated = [...prev];
          updated[fileIndex].progress = progress;
          updated[fileIndex].status = progress === 100 ? 'completed' : 'uploading';
          return updated;
        });
      });

      // Update final status
      setUploadQueue(results);
      onUpload?.(validFiles);
    } catch (error) {
      console.error('Upload failed:', error);
      alert(`上传失败: ${error instanceof Error ? error.message : '未知错误'}`);
    } finally {
      setIsUploading(false);
    }
  };

  const handleClickUpload = () => {
    fileInputRef.current?.click();
  };

  const removeFile = (index: number) => {
    if (isUploading) return; // Don't allow removal during upload
    setUploadQueue((prev) => prev.filter((_, i) => i !== index));
  };

  const clearCompleted = () => {
    setUploadQueue((prev) => prev.filter((item) => item.status !== 'completed'));
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  };

  return (
    <div className="glass-panel rounded-lg p-6 space-y-4">
      {/* Upload Area */}
      <div
        onDragEnter={handleDragEnter}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={handleClickUpload}
        className={`
          border-2 border-dashed rounded-lg p-12 text-center cursor-pointer
          transition-all duration-300
          ${isDragging
            ? 'border-neon-cyan bg-neon-cyan/10 scale-105'
            : 'border-neon-cyan/30 hover:border-neon-cyan hover:bg-neon-cyan/5'
          }
        `}
      >
        <input
          ref={fileInputRef}
          type="file"
          multiple
          onChange={handleFileInput}
          className="hidden"
        />

        <div className="space-y-4">
          <div className="text-6xl">
            {isDragging ? '⬇️' : '📤'}
          </div>
          <div>
            <p className="text-lg font-orbitron neon-text-cyan mb-2">
              {isDragging ? '释放以上传文件' : '拖拽文件到此处'}
            </p>
            <p className="text-sm text-text-secondary font-electrolize">
              或点击选择文件上传
            </p>
          </div>
          <div className="flex items-center justify-center gap-2 text-xs text-text-secondary">
            <span>支持格式:</span>
            <span className="text-neon-pink">文档 • 图片 • 视频 • 音频</span>
          </div>
        </div>
      </div>

      {/* Upload Queue */}
      {uploadQueue.length > 0 && (
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <h4 className="text-sm font-orbitron neon-text-cyan">
              上传队列 ({uploadQueue.length})
            </h4>
            <button
              onClick={clearCompleted}
              disabled={isUploading}
              className="text-xs text-neon-pink hover:text-neon-pink/80 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              清除已完成
            </button>
          </div>

          <div className="space-y-2 max-h-64 overflow-auto">
            {uploadQueue.map((item, index) => (
              <div
                key={index}
                className="flex items-center justify-between p-3 glass-panel rounded-lg hover:bg-cyber-bg-tertiary/30 transition-colors"
              >
                <div className="flex items-center gap-3 flex-1 min-w-0">
                  {/* Status Icon */}
                  <span className="text-2xl">
                    {item.status === 'completed' ? '✅' : item.status === 'error' ? '❌' : item.status === 'uploading' ? '⏳' : '📄'}
                  </span>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm text-text-primary font-electrolize truncate">
                      {item.file.name}
                    </p>
                    <p className="text-xs text-text-secondary">
                      {formatFileSize(item.file.size)}
                      {item.status === 'error' && item.error && (
                        <span className="text-neon-pink ml-2">· {item.error}</span>
                      )}
                      {item.status === 'completed' && (
                        <span className="text-neon-cyan ml-2">· 上传成功</span>
                      )}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  {/* Upload Progress */}
                  <div className="w-32 h-1 bg-cyber-bg-tertiary rounded-full overflow-hidden">
                    <div
                      className={`h-full transition-all duration-300 ${
                        item.status === 'completed'
                          ? 'bg-neon-cyan'
                          : item.status === 'error'
                          ? 'bg-neon-pink'
                          : 'bg-gradient-to-r from-neon-cyan to-neon-pink'
                      }`}
                      style={{ width: `${item.progress}%` }}
                    />
                  </div>

                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      removeFile(index);
                    }}
                    disabled={isUploading && item.status === 'uploading'}
                    className="text-neon-pink hover:text-neon-pink/80 transition-colors p-1 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    ✕
                  </button>
                </div>
              </div>
            ))}
          </div>

          {/* Upload Summary */}
          <div className="flex items-center justify-between pt-3 border-t border-neon-cyan/30">
            <div className="text-xs text-text-secondary font-electrolize space-y-1">
              <div>
                总大小: {formatFileSize(uploadQueue.reduce((acc, item) => acc + item.file.size, 0))}
              </div>
              {isUploading && (
                <div className="text-neon-cyan">
                  上传中... {uploadQueue.filter(i => i.status === 'completed').length}/{uploadQueue.length}
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
