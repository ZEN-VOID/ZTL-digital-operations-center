'use client';

import * as React from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { SearchBar } from '@/components/home/search-bar';
import { GroupSelector } from '@/components/home/group-selector';
import { AgentGrid } from '@/components/home/agent-grid';
import { AgentDetailModal } from '@/components/home/agent-detail-modal';
import { Button } from '@/components/ui/button';
import { getAllAgents, filterAgentsByGroup, searchAgents, getAgentById } from '@/lib/services/agent-service';
import type { Agent } from '@/lib/types/agent';
import { Grid3x3, LayoutGrid, Square, MessageSquare, FolderOpen } from 'lucide-react';
import { cn } from '@/lib/utils/cn';

type ViewSize = 'small' | 'medium' | 'large';

export default function HomePage() {
  const router = useRouter();

  // State
  const [agents, setAgents] = React.useState<Agent[]>([]);
  const [groups, setGroups] = React.useState<string[]>([]);
  const [selectedGroup, setSelectedGroup] = React.useState<string | null>(null);
  const [searchQuery, setSearchQuery] = React.useState('');
  const [selectedAgent, setSelectedAgent] = React.useState<Agent | null>(null);
  const [isModalOpen, setIsModalOpen] = React.useState(false);
  const [isLoading, setIsLoading] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);
  const [viewSize, setViewSize] = React.useState<ViewSize>('medium');

  // Load agents on mount
  React.useEffect(() => {
    const loadData = async () => {
      try {
        setIsLoading(true);
        setError(null);
        const allAgents = await getAllAgents();
        setAgents(allAgents);

        // Extract unique groups
        const uniqueGroups = Array.from(new Set(allAgents.map((agent) => agent.group))).sort();
        setGroups(uniqueGroups);
      } catch (err) {
        console.error('Failed to load agents:', err);
        setError('加载智能体数据失败，请刷新页面重试');
      } finally {
        setIsLoading(false);
      }
    };

    loadData();
  }, []);

  // Filtered agents
  const filteredAgents = React.useMemo(() => {
    let result = agents;

    // Filter by group
    result = filterAgentsByGroup(result, selectedGroup);

    // Search
    result = searchAgents(result, searchQuery);

    return result;
  }, [agents, selectedGroup, searchQuery]);

  // Agent counts per group
  const agentCounts = React.useMemo(() => {
    const counts: Record<string, number> = {};
    const searchedAgents = searchAgents(agents, searchQuery);

    searchedAgents.forEach((agent) => {
      counts[agent.group] = (counts[agent.group] || 0) + 1;
    });

    return counts;
  }, [agents, searchQuery]);

  // Handlers
  const handleAgentSelect = (id: string) => {
    router.push(`/chat?agent=${encodeURIComponent(id)}`);
  };

  const handleAgentViewDetails = (id: string) => {
    const agent = getAgentById(agents, id);
    if (agent) {
      setSelectedAgent(agent);
      setIsModalOpen(true);
    }
  };

  const handleGroupChange = (group: string | null) => {
    setSelectedGroup(group);
  };

  // Loading state
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-cyber-bg-primary">
        <div className="flex flex-col items-center gap-4">
          <div className="w-16 h-16 border-4 border-neon-cyan border-t-transparent rounded-full animate-spin" />
          <p className="text-text-secondary animate-neon-pulse">加载智能体数据...</p>
        </div>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-cyber-bg-primary px-4">
        <div className="max-w-md w-full glass-panel rounded-lg p-8 text-center space-y-4">
          <div className="w-20 h-20 rounded-full bg-neon-pink/20 border-2 border-neon-pink mx-auto flex items-center justify-center">
            <svg className="w-10 h-10 text-neon-pink" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
              />
            </svg>
          </div>
          <h2 className="text-xl font-bold neon-text-pink">加载失败</h2>
          <p className="text-text-secondary">{error}</p>
          <Button variant="neon-cyan" onClick={() => window.location.reload()}>
            重新加载
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-cyber-bg-primary">
      {/* Background */}
      <div className="fixed inset-0 cyber-grid-bg opacity-20 pointer-events-none" />
      <div className="fixed inset-0 bg-gradient-to-b from-transparent via-cyber-bg-primary/50 to-cyber-bg-primary pointer-events-none" />

      {/* Content */}
      <div className="relative z-10">
        {/* Header */}
        <header className="sticky top-0 z-20 glass-panel border-b border-text-secondary/20 backdrop-blur-xl">
          <div className="container mx-auto px-4 py-6">
            <div className="flex flex-col gap-6">
              {/* Title and View Toggle */}
              <div className="flex items-start justify-between">
                <div>
                  <h1 className="text-2xl sm:text-3xl font-bold neon-text-cyan">
                    ZTL数智化情报中心·智能体总目录
                  </h1>
                  <p className="text-text-secondary text-sm mt-1">
                    共 {agents.length} 个智能体，{groups.length} 个业务组
                  </p>
                </div>

                {/* View Size Toggle */}
                <div className="flex items-center gap-1 glass-panel px-2 py-1 rounded-lg">
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => setViewSize('small')}
                    className={cn(
                      'h-8 w-8 transition-colors',
                      viewSize === 'small' ? 'text-neon-cyan bg-neon-cyan/10' : 'text-text-secondary hover:text-neon-cyan'
                    )}
                    title="小尺寸"
                  >
                    <Grid3x3 className="w-4 h-4" />
                  </Button>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => setViewSize('medium')}
                    className={cn(
                      'h-8 w-8 transition-colors',
                      viewSize === 'medium' ? 'text-neon-cyan bg-neon-cyan/10' : 'text-text-secondary hover:text-neon-cyan'
                    )}
                    title="中尺寸"
                  >
                    <LayoutGrid className="w-4 h-4" />
                  </Button>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => setViewSize('large')}
                    className={cn(
                      'h-8 w-8 transition-colors',
                      viewSize === 'large' ? 'text-neon-cyan bg-neon-cyan/10' : 'text-text-secondary hover:text-neon-cyan'
                    )}
                    title="大尺寸"
                  >
                    <Square className="w-4 h-4" />
                  </Button>
                </div>
              </div>

              {/* Navigation */}
              <div className="flex items-center gap-3">
                <Link href="/chat">
                  <Button variant="neon-cyan" size="sm" className="gap-2">
                    <MessageSquare className="w-4 h-4" />
                    <span>智能对话</span>
                  </Button>
                </Link>
                <Link href="/resources">
                  <Button variant="neon-pink" size="sm" className="gap-2">
                    <FolderOpen className="w-4 h-4" />
                    <span>资源管理</span>
                  </Button>
                </Link>
              </div>

              {/* Search Bar */}
              <SearchBar value={searchQuery} onChange={setSearchQuery} />

              {/* Group Selector */}
              <GroupSelector
                groups={groups}
                selectedGroup={selectedGroup}
                onGroupChange={handleGroupChange}
                agentCounts={agentCounts}
              />
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="container mx-auto px-4 py-8">
          {/* Stats */}
          <div className="mb-6 flex items-center justify-between">
            <div className="text-text-secondary text-sm">
              找到 <span className="text-neon-cyan font-bold">{filteredAgents.length}</span> 个智能体
            </div>

            {searchQuery && (
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setSearchQuery('')}
                className="text-text-secondary hover:text-neon-pink"
              >
                清除搜索
              </Button>
            )}
          </div>

          {/* Agent Grid */}
          <AgentGrid
            agents={filteredAgents}
            onAgentSelect={handleAgentSelect}
            onAgentViewDetails={handleAgentViewDetails}
            viewSize={viewSize}
          />
        </main>

        {/* Footer */}
        <footer className="mt-20 border-t border-text-secondary/20 py-8">
          <div className="container mx-auto px-4 text-center text-text-secondary text-sm">
            <p>ZTL 数智化作战中心 • 智能体协作平台</p>
          </div>
        </footer>
      </div>

      {/* Agent Detail Modal */}
      <AgentDetailModal agent={selectedAgent} open={isModalOpen} onOpenChange={setIsModalOpen} />
    </div>
  );
}
