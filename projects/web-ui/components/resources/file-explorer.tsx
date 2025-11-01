'use client';

import { useState } from 'react';
import type { FileNode } from '@/types/resources';

interface FileExplorerProps {
  data: FileNode[];
  onSelect?: (file: FileNode) => void;
  selectedId?: string;
}

interface FileTreeItemProps {
  node: FileNode;
  level: number;
  onSelect?: (file: FileNode) => void;
  selectedId?: string;
}

function FileTreeItem({ node, level, onSelect, selectedId }: FileTreeItemProps) {
  const [isExpanded, setIsExpanded] = useState(true);
  const isSelected = selectedId === node.id;

  const handleClick = () => {
    if (node.type === 'folder') {
      setIsExpanded(!isExpanded);
    }
    onSelect?.(node);
  };

  return (
    <div>
      <div
        onClick={handleClick}
        className={`
          flex items-center gap-2 py-2 px-3 cursor-pointer
          transition-all duration-200
          hover:bg-cyber-bg-tertiary/50
          ${isSelected ? 'neon-glow-cyan bg-cyber-bg-tertiary/30' : ''}
        `}
        style={{ paddingLeft: `${level * 1.5}rem` }}
      >
        {node.type === 'folder' && (
          <span className="text-neon-cyan text-sm">
            {isExpanded ? '▼' : '▶'}
          </span>
        )}
        <span className={`
          text-lg
          ${node.type === 'folder' ? 'text-neon-cyan' : 'text-neon-pink'}
        `}>
          {node.type === 'folder' ? '📁' : getFileIcon(node.extension)}
        </span>
        <span className={`
          text-sm font-electrolize
          ${isSelected ? 'text-neon-cyan' : 'text-text-primary'}
        `}>
          {node.name}
        </span>
      </div>

      {node.type === 'folder' && isExpanded && node.children && (
        <div>
          {node.children.map((child) => (
            <FileTreeItem
              key={child.id}
              node={child}
              level={level + 1}
              onSelect={onSelect}
              selectedId={selectedId}
            />
          ))}
        </div>
      )}
    </div>
  );
}

function getFileIcon(extension?: string): string {
  if (!extension) return '📄';

  const iconMap: Record<string, string> = {
    'md': '📝',
    'txt': '📄',
    'pdf': '📕',
    'doc': '📘',
    'docx': '📘',
    'xls': '📊',
    'xlsx': '📊',
    'jpg': '🖼️',
    'jpeg': '🖼️',
    'png': '🖼️',
    'gif': '🖼️',
    'svg': '🎨',
    'mp4': '🎬',
    'mov': '🎬',
    'mp3': '🎵',
    'wav': '🎵',
    'zip': '📦',
    'rar': '📦',
    'json': '📋',
    'js': '📜',
    'ts': '📜',
    'tsx': '⚛️',
    'jsx': '⚛️',
  };

  return iconMap[extension.toLowerCase()] || '📄';
}

export default function FileExplorer({ data, onSelect, selectedId }: FileExplorerProps) {
  return (
    <div className="h-full overflow-auto glass-panel rounded-lg">
      <div className="sticky top-0 z-10 bg-cyber-bg-secondary/90 backdrop-blur-sm p-4 border-b border-neon-cyan/30">
        <h3 className="text-lg font-orbitron neon-text-cyan">文件资源</h3>
      </div>
      <div className="p-2">
        {data.map((node) => (
          <FileTreeItem
            key={node.id}
            node={node}
            level={0}
            onSelect={onSelect}
            selectedId={selectedId}
          />
        ))}
      </div>
    </div>
  );
}
