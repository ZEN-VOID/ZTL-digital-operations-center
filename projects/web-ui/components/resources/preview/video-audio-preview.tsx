'use client';

import { useState, useRef, useEffect } from 'react';

interface VideoAudioPreviewProps {
  src: string;
  type: 'video' | 'audio';
  mimeType?: string;
}

export default function VideoAudioPreview({ src, type, mimeType }: VideoAudioPreviewProps) {
  const mediaRef = useRef<HTMLVideoElement | HTMLAudioElement>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [volume, setVolume] = useState(1);
  const [isMuted, setIsMuted] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);

  useEffect(() => {
    const media = mediaRef.current;
    if (!media) return;

    const handleTimeUpdate = () => setCurrentTime(media.currentTime);
    const handleDurationChange = () => setDuration(media.duration);
    const handleEnded = () => setIsPlaying(false);

    media.addEventListener('timeupdate', handleTimeUpdate);
    media.addEventListener('durationchange', handleDurationChange);
    media.addEventListener('ended', handleEnded);

    return () => {
      media.removeEventListener('timeupdate', handleTimeUpdate);
      media.removeEventListener('durationchange', handleDurationChange);
      media.removeEventListener('ended', handleEnded);
    };
  }, []);

  const togglePlayPause = () => {
    const media = mediaRef.current;
    if (!media) return;

    if (isPlaying) {
      media.pause();
    } else {
      media.play();
    }
    setIsPlaying(!isPlaying);
  };

  const handleSeek = (e: React.ChangeEvent<HTMLInputElement>) => {
    const media = mediaRef.current;
    if (!media) return;

    const time = parseFloat(e.target.value);
    media.currentTime = time;
    setCurrentTime(time);
  };

  const handleVolumeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const media = mediaRef.current;
    if (!media) return;

    const vol = parseFloat(e.target.value);
    media.volume = vol;
    setVolume(vol);
    setIsMuted(vol === 0);
  };

  const toggleMute = () => {
    const media = mediaRef.current;
    if (!media) return;

    media.muted = !isMuted;
    setIsMuted(!isMuted);
  };

  const toggleFullscreen = async () => {
    const media = mediaRef.current;
    if (!media || type !== 'video') return;

    try {
      if (!isFullscreen) {
        await media.requestFullscreen();
        setIsFullscreen(true);
      } else {
        await document.exitFullscreen();
        setIsFullscreen(false);
      }
    } catch (error) {
      console.error('Fullscreen error:', error);
    }
  };

  const formatTime = (seconds: number): string => {
    if (isNaN(seconds)) return '0:00';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="relative h-full flex flex-col items-center justify-center p-8">
      {/* Media Element */}
      <div className="relative w-full max-w-4xl">
        {type === 'video' ? (
          <video
            ref={mediaRef as React.RefObject<HTMLVideoElement>}
            src={src}
            className="w-full rounded-lg neon-glow-cyan"
            style={{ maxHeight: '60vh' }}
          />
        ) : (
          <div className="glass-panel neon-glow-cyan rounded-lg p-12">
            <audio ref={mediaRef as React.RefObject<HTMLAudioElement>} src={src} />
            <div className="text-center">
              <div className="text-6xl mb-4">🎵</div>
              <div className="text-text-secondary font-electrolize">音频播放中...</div>
            </div>
          </div>
        )}
      </div>

      {/* Custom Controls */}
      <div className="mt-6 w-full max-w-4xl glass-panel neon-glow-cyan rounded-lg p-4">
        {/* Progress Bar */}
        <div className="mb-4">
          <input
            type="range"
            min="0"
            max={duration || 0}
            value={currentTime}
            onChange={handleSeek}
            className="w-full h-1 bg-bg-secondary rounded-lg appearance-none cursor-pointer
                     [&::-webkit-slider-thumb]:appearance-none
                     [&::-webkit-slider-thumb]:w-4
                     [&::-webkit-slider-thumb]:h-4
                     [&::-webkit-slider-thumb]:rounded-full
                     [&::-webkit-slider-thumb]:bg-neon-cyan
                     [&::-webkit-slider-thumb]:shadow-[0_0_10px_rgba(0,255,255,0.8)]
                     [&::-moz-range-thumb]:w-4
                     [&::-moz-range-thumb]:h-4
                     [&::-moz-range-thumb]:rounded-full
                     [&::-moz-range-thumb]:bg-neon-cyan
                     [&::-moz-range-thumb]:shadow-[0_0_10px_rgba(0,255,255,0.8)]
                     [&::-moz-range-thumb]:border-0"
          />
          <div className="flex justify-between text-xs text-text-secondary mt-1 font-electrolize">
            <span>{formatTime(currentTime)}</span>
            <span>{formatTime(duration)}</span>
          </div>
        </div>

        {/* Control Buttons */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            {/* Play/Pause */}
            <button
              onClick={togglePlayPause}
              className="text-neon-cyan hover:text-neon-pink transition-colors text-2xl"
              title={isPlaying ? '暂停' : '播放'}
            >
              {isPlaying ? '⏸' : '▶'}
            </button>

            {/* Volume Controls */}
            <div className="flex items-center gap-2">
              <button
                onClick={toggleMute}
                className="text-neon-cyan hover:text-neon-pink transition-colors text-xl"
                title={isMuted ? '取消静音' : '静音'}
              >
                {isMuted || volume === 0 ? '🔇' : volume < 0.5 ? '🔉' : '🔊'}
              </button>
              <input
                type="range"
                min="0"
                max="1"
                step="0.1"
                value={isMuted ? 0 : volume}
                onChange={handleVolumeChange}
                className="w-24 h-1 bg-bg-secondary rounded-lg appearance-none cursor-pointer
                         [&::-webkit-slider-thumb]:appearance-none
                         [&::-webkit-slider-thumb]:w-3
                         [&::-webkit-slider-thumb]:h-3
                         [&::-webkit-slider-thumb]:rounded-full
                         [&::-webkit-slider-thumb]:bg-neon-cyan
                         [&::-moz-range-thumb]:w-3
                         [&::-moz-range-thumb]:h-3
                         [&::-moz-range-thumb]:rounded-full
                         [&::-moz-range-thumb]:bg-neon-cyan
                         [&::-moz-range-thumb]:border-0"
              />
            </div>
          </div>

          {/* Fullscreen (Video only) */}
          {type === 'video' && (
            <button
              onClick={toggleFullscreen}
              className="text-neon-cyan hover:text-neon-pink transition-colors text-xl"
              title="全屏"
            >
              ⛶
            </button>
          )}
        </div>
      </div>

      {/* Hint */}
      {!isPlaying && (
        <div className="absolute bottom-24 left-1/2 transform -translate-x-1/2 text-text-secondary text-sm font-electrolize">
          点击播放按钮开始播放
        </div>
      )}
    </div>
  );
}
