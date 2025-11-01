'use client';

import { useState } from 'react';
import type { SortOrder } from '@/types/resources';

interface FileSearchProps {
  onSearch?: (query: string) => void;
  onSortChange?: (order: SortOrder) => void;
  onFilterChange?: (filter: string) => void;
}

export default function FileSearch({ onSearch, onSortChange, onFilterChange }: FileSearchProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [sortOrder, setSortOrder] = useState<SortOrder>('name');
  const [activeFilter, setActiveFilter] = useState<string>('all');

  const handleSearch = (value: string) => {
    setSearchQuery(value);
    onSearch?.(value);
  };

  const handleSortChange = (order: SortOrder) => {
    setSortOrder(order);
    onSortChange?.(order);
  };

  const handleFilterChange = (filter: string) => {
    setActiveFilter(filter);
    onFilterChange?.(filter);
  };

  const filters = [
    { id: 'all', label: '全部', icon: '📁' },
    { id: 'documents', label: '文档', icon: '📄' },
    { id: 'images', label: '图片', icon: '🖼️' },
    { id: 'videos', label: '视频', icon: '🎬' },
    { id: 'audio', label: '音频', icon: '🎵' },
  ];

  const sortOptions = [
    { id: 'name', label: '名称', icon: '🔤' },
    { id: 'date', label: '日期', icon: '📅' },
    { id: 'size', label: '大小', icon: '📊' },
    { id: 'type', label: '类型', icon: '🏷️' },
  ];

  return (
    <div className="glass-panel rounded-lg p-4 space-y-4">
      {/* Search Input */}
      <div className="relative">
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => handleSearch(e.target.value)}
          placeholder="搜索文件或文件夹..."
          className="
            w-full px-4 py-3 pl-12 rounded-lg
            bg-cyber-bg-secondary border border-neon-cyan/30
            text-text-primary placeholder-text-secondary
            font-electrolize text-sm
            focus:outline-none focus:border-neon-cyan focus:ring-1 focus:ring-neon-cyan
            transition-all duration-200
          "
        />
        <span className="absolute left-4 top-1/2 -translate-y-1/2 text-neon-cyan text-lg">
          🔍
        </span>
        {searchQuery && (
          <button
            onClick={() => handleSearch('')}
            className="absolute right-4 top-1/2 -translate-y-1/2 text-text-secondary hover:text-neon-pink transition-colors"
          >
            ✕
          </button>
        )}
      </div>

      {/* Filters */}
      <div className="space-y-2">
        <h4 className="text-xs font-orbitron text-text-secondary uppercase tracking-wide">
          文件类型
        </h4>
        <div className="flex flex-wrap gap-2">
          {filters.map((filter) => (
            <button
              key={filter.id}
              onClick={() => handleFilterChange(filter.id)}
              className={`
                flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-electrolize
                transition-all duration-200
                ${activeFilter === filter.id
                  ? 'neon-glow-cyan bg-neon-cyan/10 text-neon-cyan'
                  : 'bg-cyber-bg-secondary text-text-secondary hover:text-text-primary hover:bg-cyber-bg-tertiary/50'
                }
              `}
            >
              <span>{filter.icon}</span>
              <span>{filter.label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Sort Options */}
      <div className="space-y-2">
        <h4 className="text-xs font-orbitron text-text-secondary uppercase tracking-wide">
          排序方式
        </h4>
        <div className="grid grid-cols-2 gap-2">
          {sortOptions.map((option) => (
            <button
              key={option.id}
              onClick={() => handleSortChange(option.id as SortOrder)}
              className={`
                flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-electrolize
                transition-all duration-200
                ${sortOrder === option.id
                  ? 'neon-glow-pink bg-neon-pink/10 text-neon-pink'
                  : 'bg-cyber-bg-secondary text-text-secondary hover:text-text-primary hover:bg-cyber-bg-tertiary/50'
                }
              `}
            >
              <span>{option.icon}</span>
              <span>{option.label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Search Stats */}
      {searchQuery && (
        <div className="pt-3 border-t border-neon-cyan/30">
          <p className="text-xs text-text-secondary font-electrolize">
            搜索 "<span className="text-neon-cyan">{searchQuery}</span>" 的结果
          </p>
        </div>
      )}
    </div>
  );
}
