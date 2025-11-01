'use client';

import { useState } from 'react';
import Image from 'next/image';

interface ImagePreviewProps {
  src: string;
  alt: string;
}

export default function ImagePreview({ src, alt }: ImagePreviewProps) {
  const [isZoomed, setIsZoomed] = useState(false);
  const [scale, setScale] = useState(1);

  const handleZoom = () => {
    setIsZoomed(!isZoomed);
    setScale(1);
  };

  const handleWheel = (e: React.WheelEvent) => {
    if (isZoomed) {
      e.preventDefault();
      const delta = e.deltaY > 0 ? -0.1 : 0.1;
      setScale(prev => Math.max(0.5, Math.min(3, prev + delta)));
    }
  };

  return (
    <div className="relative h-full flex items-center justify-center p-8">
      {/* Image Container */}
      <div
        className={`relative max-w-full max-h-full transition-all duration-300 ${
          isZoomed ? 'cursor-zoom-out' : 'cursor-zoom-in'
        }`}
        onClick={handleZoom}
        onWheel={handleWheel}
      >
        <div
          className="neon-glow-cyan rounded-lg overflow-hidden"
          style={{
            transform: isZoomed ? `scale(${scale})` : 'scale(1)',
            transition: 'transform 0.2s ease-out',
          }}
        >
          <img
            src={src}
            alt={alt}
            className="max-w-full max-h-[70vh] object-contain"
            loading="lazy"
          />
        </div>
      </div>

      {/* Zoom Controls */}
      {isZoomed && (
        <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 glass-panel neon-glow-cyan rounded-full px-6 py-3 flex items-center gap-4 z-10">
          <button
            onClick={(e) => {
              e.stopPropagation();
              setScale(prev => Math.max(0.5, prev - 0.1));
            }}
            className="text-neon-cyan hover:text-neon-pink transition-colors text-xl"
            title="缩小"
          >
            −
          </button>
          <span className="text-text-secondary font-electrolize text-sm min-w-[60px] text-center">
            {Math.round(scale * 100)}%
          </span>
          <button
            onClick={(e) => {
              e.stopPropagation();
              setScale(prev => Math.min(3, prev + 0.1));
            }}
            className="text-neon-cyan hover:text-neon-pink transition-colors text-xl"
            title="放大"
          >
            +
          </button>
          <button
            onClick={(e) => {
              e.stopPropagation();
              setScale(1);
            }}
            className="text-text-secondary hover:text-neon-cyan transition-colors text-sm ml-2"
            title="重置"
          >
            🔄
          </button>
        </div>
      )}

      {/* Hint */}
      {!isZoomed && (
        <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 text-text-secondary text-sm font-electrolize">
          点击查看大图
        </div>
      )}
    </div>
  );
}
