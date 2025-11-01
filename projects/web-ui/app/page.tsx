import Link from 'next/link';

export default function Home() {
  return (
    <main className="min-h-screen cyber-grid-bg relative overflow-hidden">
      {/* Scanline Effect */}
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-neon-cyan/5 to-transparent animate-[grid-move_3s_linear_infinite]" />
      </div>

      {/* Content */}
      <div className="relative z-10 flex min-h-screen flex-col items-center justify-center p-8">
        <div className="max-w-4xl w-full text-center space-y-8">
          {/* Logo */}
          <h1 className="text-6xl md:text-8xl font-bold neon-text-cyan font-orbitron">
            ZTL
          </h1>

          {/* Title */}
          <h2 className="text-2xl md:text-4xl neon-text-purple font-orbitron">
            数智化作战中心
          </h2>

          {/* Description */}
          <p className="text-lg md:text-xl text-text-primary max-w-2xl mx-auto">
            Digital Intelligence Operations Center
          </p>

          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mt-12">
            <div className="neon-glow-cyan p-6 rounded-lg bg-cyber-bg-secondary/50 backdrop-blur-sm">
              <div className="text-3xl font-bold neon-text-cyan font-orbitron">60+</div>
              <div className="text-sm text-text-secondary mt-2">智能体</div>
            </div>
            <div className="neon-glow-pink p-6 rounded-lg bg-cyber-bg-secondary/50 backdrop-blur-sm">
              <div className="text-3xl font-bold neon-text-pink font-orbitron">8</div>
              <div className="text-sm text-text-secondary mt-2">业务组</div>
            </div>
            <div className="neon-glow-cyan p-6 rounded-lg bg-cyber-bg-secondary/50 backdrop-blur-sm">
              <div className="text-3xl font-bold neon-text-cyan font-orbitron">24/7</div>
              <div className="text-sm text-text-secondary mt-2">在线运行</div>
            </div>
            <div className="neon-glow-pink p-6 rounded-lg bg-cyber-bg-secondary/50 backdrop-blur-sm">
              <div className="text-3xl font-bold neon-text-pink font-orbitron">∞</div>
              <div className="text-sm text-text-secondary mt-2">无限可能</div>
            </div>
          </div>

          {/* Navigation Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-16">
            {/* Home Page */}
            <Link href="/home" className="group h-full">
              <div className="h-full flex flex-col neon-glow-cyan p-8 rounded-lg bg-cyber-bg-secondary/50 backdrop-blur-sm hover:bg-cyber-bg-secondary/70 transition-all duration-300 transform hover:scale-105 cursor-pointer">
                <div className="text-5xl mb-4">🏠</div>
                <h3 className="text-2xl font-bold neon-text-cyan font-orbitron mb-3">智能体总目录</h3>
                <p className="text-text-secondary text-sm flex-grow">浏览全部60+智能体，按业务组分类查看</p>
                <div className="mt-6 flex items-center gap-2 text-neon-cyan group-hover:translate-x-2 transition-transform">
                  <span className="text-sm font-medium">进入</span>
                  <span>→</span>
                </div>
              </div>
            </Link>

            {/* Chat Page */}
            <Link href="/chat" className="group h-full">
              <div className="h-full flex flex-col neon-glow-pink p-8 rounded-lg bg-cyber-bg-secondary/50 backdrop-blur-sm hover:bg-cyber-bg-secondary/70 transition-all duration-300 transform hover:scale-105 cursor-pointer">
                <div className="text-5xl mb-4">💬</div>
                <h3 className="text-2xl font-bold neon-text-pink font-orbitron mb-3">对话系统</h3>
                <p className="text-text-secondary text-sm flex-grow">与智能体实时对话，执行业务任务</p>
                <div className="mt-6 flex items-center gap-2 text-neon-pink group-hover:translate-x-2 transition-transform">
                  <span className="text-sm font-medium">进入</span>
                  <span>→</span>
                </div>
              </div>
            </Link>

            {/* Resources Page */}
            <Link href="/resources" className="group h-full">
              <div className="h-full flex flex-col neon-glow-cyan p-8 rounded-lg bg-cyber-bg-secondary/50 backdrop-blur-sm hover:bg-cyber-bg-secondary/70 transition-all duration-300 transform hover:scale-105 cursor-pointer">
                <div className="text-5xl mb-4">📁</div>
                <h3 className="text-2xl font-bold neon-text-cyan font-orbitron mb-3">资源管理</h3>
                <p className="text-text-secondary text-sm flex-grow">管理文档、图片、数据等项目资源</p>
                <div className="mt-6 flex items-center gap-2 text-neon-cyan group-hover:translate-x-2 transition-transform">
                  <span className="text-sm font-medium">进入</span>
                  <span>→</span>
                </div>
              </div>
            </Link>
          </div>

          {/* Status */}
          <div className="mt-12 text-text-secondary text-sm">
            <div className="flex items-center justify-center gap-2">
              <div className="w-2 h-2 rounded-full bg-neon-green animate-neon-pulse" />
              <span>系统初始化完成 | Next.js 16 + React 19 + TypeScript</span>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
