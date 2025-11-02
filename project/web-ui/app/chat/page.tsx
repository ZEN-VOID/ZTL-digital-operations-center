'use client';

import * as React from 'react';
import { useSearchParams } from 'next/navigation';
import { MessageList, type Message } from '@/components/chat/message-list';
import { ChatInput } from '@/components/chat/chat-input';
import { AgentSwitcher, type Agent as AgentSwitcherAgent } from '@/components/chat/agent-switcher';
import { AgentDetails } from '@/components/chat/agent-details';
import { SkillDetails } from '@/components/chat/skill-details';
import { Navigation } from '@/components/layout/navigation';
import { Button } from '@/components/ui/button';
import { getAllAgents } from '@/lib/services/agent-service';
import { getAllSkills } from '@/lib/services/skill-service';
import type { Agent } from '@/lib/types/agent';
import type { Skill } from '@/lib/types/skill';

export default function ChatPage() {
  const searchParams = useSearchParams();
  const agentIdFromUrl = searchParams.get('agent');

  const [messages, setMessages] = React.useState<Message[]>([]);
  const [inputValue, setInputValue] = React.useState('');
  const [isTyping, setIsTyping] = React.useState(false);
  const [currentAgentId, setCurrentAgentId] = React.useState<string>('');
  const [isSidebarCollapsed, setIsSidebarCollapsed] = React.useState(false);
  const [isSkillsSidebarCollapsed, setIsSkillsSidebarCollapsed] = React.useState(false);
  const [agents, setAgents] = React.useState<Agent[]>([]);
  const [isLoadingAgents, setIsLoadingAgents] = React.useState(true);
  const [skills, setSkills] = React.useState<Skill[]>([]);
  const [isLoadingSkills, setIsLoadingSkills] = React.useState(true);
  const [selectedSkillId, setSelectedSkillId] = React.useState<string | null>(null);

  // Load agents data
  React.useEffect(() => {
    const loadAgents = async () => {
      try {
        setIsLoadingAgents(true);
        const allAgents = await getAllAgents();
        setAgents(allAgents);

        // Set default agent if no URL parameter
        if (!agentIdFromUrl && allAgents.length > 0) {
          setCurrentAgentId(allAgents[0].id);
        }
      } catch (error) {
        console.error('Failed to load agents:', error);
      } finally {
        setIsLoadingAgents(false);
      }
    };

    loadAgents();
  }, [agentIdFromUrl]);

  // Load skills data
  React.useEffect(() => {
    const loadSkills = async () => {
      try {
        setIsLoadingSkills(true);
        const allSkills = await getAllSkills();
        setSkills(allSkills);

        // Set first skill as default selected
        if (allSkills.length > 0) {
          setSelectedSkillId(allSkills[0].id);
        }
      } catch (error) {
        console.error('Failed to load skills:', error);
      } finally {
        setIsLoadingSkills(false);
      }
    };

    loadSkills();
  }, []);

  // Initialize agent from URL parameter
  React.useEffect(() => {
    if (agentIdFromUrl && agents.length > 0) {
      const decodedAgentId = decodeURIComponent(agentIdFromUrl);
      const foundAgent = agents.find((agent) => agent.id === decodedAgentId);

      if (foundAgent) {
        setCurrentAgentId(decodedAgentId);
        // Add a welcome message from the selected agent
        setMessages([
          {
            id: `msg-welcome-${Date.now()}`,
            content: `您好!我是${foundAgent.name},${foundAgent.description}。有什么我可以帮助您的吗?`,
            role: 'assistant',
            agentName: foundAgent.name,
            timestamp: new Date(),
          },
        ]);
      }
    }
  }, [agentIdFromUrl, agents]);

  const currentAgent = agents.find((agent) => agent.id === currentAgentId);
  const selectedSkill = skills.find((skill) => skill.id === selectedSkillId);

  // Convert Agent to AgentSwitcherAgent format
  const agentSwitcherAgents: AgentSwitcherAgent[] = React.useMemo(
    () =>
      agents.map((agent) => ({
        id: agent.id,
        name: agent.name,
        description: agent.description,
        group: agent.group,
        color: 'purple' as const,
      })),
    [agents]
  );

  // Simulate streaming response
  const simulateStreamingResponse = React.useCallback(
    async (userMessage: string) => {
      if (!currentAgent) return;

      setIsTyping(true);

      // Add typing delay
      await new Promise((resolve) => setTimeout(resolve, 1000));

      const responseText = `作为${currentAgent.name},我收到您的消息:"${userMessage}"。我将为您提供专业的${currentAgent.description}服务...`;

      // Create assistant message with streaming
      const messageId = `msg-${Date.now()}-assistant`;
      const newMessage: Message = {
        id: messageId,
        content: '',
        role: 'assistant',
        agentName: currentAgent.name,
        timestamp: new Date(),
        isStreaming: true,
      };

      setMessages((prev) => [...prev, newMessage]);

      // Simulate character-by-character streaming
      for (let i = 0; i <= responseText.length; i++) {
        await new Promise((resolve) => setTimeout(resolve, 30));
        setMessages((prev) =>
          prev.map((msg) =>
            msg.id === messageId
              ? { ...msg, content: responseText.slice(0, i) }
              : msg
          )
        );
      }

      // Mark streaming as complete
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === messageId ? { ...msg, isStreaming: false } : msg
        )
      );

      setIsTyping(false);
    },
    [currentAgent]
  );

  // Handle message send
  const handleSendMessage = React.useCallback(
    async (message: string) => {
      if (!message.trim()) return;

      // Handle commands
      if (message.startsWith('/')) {
        handleCommand(message);
        setInputValue('');
        return;
      }

      // Add user message
      const userMessage: Message = {
        id: `msg-${Date.now()}-user`,
        content: message,
        role: 'user',
        timestamp: new Date(),
        status: 'sent',
      };

      setMessages((prev) => [...prev, userMessage]);
      setInputValue('');

      // Simulate assistant response
      await simulateStreamingResponse(message);
    },
    [simulateStreamingResponse]
  );

  // Handle commands
  const handleCommand = (command: string) => {
    const [cmd, ...args] = command.trim().split(' ');

    switch (cmd.toLowerCase()) {
      case '/help':
        setMessages((prev) => [
          ...prev,
          {
            id: `msg-${Date.now()}-system`,
            content: '可用命令: /help - 显示帮助, /clear - 清除历史, /switch - 切换智能体',
            role: 'system',
            timestamp: new Date(),
          },
        ]);
        break;

      case '/clear':
        setMessages([]);
        setMessages((prev) => [
          ...prev,
          {
            id: `msg-${Date.now()}-system`,
            content: '对话历史已清除',
            role: 'system',
            timestamp: new Date(),
          },
        ]);
        break;

      default:
        setMessages((prev) => [
          ...prev,
          {
            id: `msg-${Date.now()}-system`,
            content: `未知命令: ${cmd}。输入 /help 查看帮助。`,
            role: 'system',
            timestamp: new Date(),
          },
        ]);
    }
  };

  // Loading state
  if (isLoadingAgents || isLoadingSkills) {
    return (
      <div className="flex flex-col h-screen bg-cyber-bg-primary items-center justify-center">
        <div className="w-16 h-16 border-4 border-neon-cyan border-t-transparent rounded-full animate-spin" />
        <p className="text-text-secondary mt-4 animate-neon-pulse">
          {isLoadingAgents && isLoadingSkills && '加载智能体和技能包数据...'}
          {isLoadingAgents && !isLoadingSkills && '加载智能体数据...'}
          {!isLoadingAgents && isLoadingSkills && '加载技能包数据...'}
        </p>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-screen bg-cyber-bg-primary">
      {/* Header */}
      <header className="flex-shrink-0 border-b border-text-secondary/20 bg-cyber-bg-secondary/50 backdrop-blur-md">
        <div className="px-4 py-6">
          <div className="flex items-center justify-between mb-4">
            {/* Title - Left aligned */}
            <div>
              <h1 className="text-2xl sm:text-3xl font-bold neon-text-cyan">
                没有什么是对话解决不了的
              </h1>
            </div>

            {/* Navigation - Right aligned */}
            <Navigation variant="header" />
          </div>
        </div>
      </header>

      {/* Main content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Sidebar - Agent switcher */}
        <aside
          className={`
            border-r-2 border-neon-purple/20 bg-cyber-bg-secondary/30 backdrop-blur-sm
            transition-all duration-300 ease-in-out
            ${isSidebarCollapsed ? 'w-16' : 'w-80'}
            relative
          `}
        >
          {/* Collapse/Expand button */}
          <button
            onClick={() => setIsSidebarCollapsed(!isSidebarCollapsed)}
            className="absolute -right-3 top-4 z-50 w-6 h-6 rounded-full bg-neon-purple border-2 border-neon-purple hover:bg-neon-purple/70 active:scale-95 transition-all duration-200 flex items-center justify-center shadow-lg cursor-pointer"
            aria-label={isSidebarCollapsed ? '展开侧边栏' : '收起侧边栏'}
            style={{ pointerEvents: 'auto' }}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="12"
              height="12"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2.5"
              strokeLinecap="round"
              strokeLinejoin="round"
              className={`transition-transform duration-300 text-white ${isSidebarCollapsed ? 'rotate-180' : ''}`}
            >
              <path d="m15 18-6-6 6-6" />
            </svg>
          </button>

          <div className="p-4 pb-8 h-full overflow-y-auto">
            {!isSidebarCollapsed ? (
              // Expanded view
              <div className="space-y-4 pb-8">
                <div>
                  <h2 className="text-sm font-bold text-text-secondary uppercase tracking-wider mb-3">
                    作战小组
                  </h2>
                  <AgentSwitcher
                    agents={agentSwitcherAgents}
                    currentAgentId={currentAgentId}
                    onAgentChange={setCurrentAgentId}
                    showGroups
                  />
                </div>

                <div className="pt-4 border-t-2 border-text-secondary/10">
                  <h3 className="text-sm font-bold text-text-secondary uppercase tracking-wider mb-3">
                    快捷操作
                  </h3>
                  <div className="space-y-2">
                    <Button
                      variant="ghost"
                      size="sm"
                      className="w-full justify-start"
                      onClick={() => handleCommand('/help')}
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="16"
                        height="16"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      >
                        <circle cx="12" cy="12" r="10" />
                        <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3" />
                        <path d="M12 17h.01" />
                      </svg>
                      查看帮助
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      className="w-full justify-start"
                      onClick={() => handleCommand('/clear')}
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="16"
                        height="16"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      >
                        <path d="M3 6h18" />
                        <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6" />
                        <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2" />
                      </svg>
                      清除历史
                    </Button>
                  </div>
                </div>

                <div className="pt-4 border-t-2 border-text-secondary/10">
                  <h3 className="text-sm font-bold text-text-secondary uppercase tracking-wider mb-3">
                    AGENT详情
                  </h3>
                  <AgentDetails agent={currentAgent || null} />
                </div>
              </div>
            ) : (
              // Collapsed view - icon-only
              <div className="flex flex-col items-center gap-4 pt-12">
                {/* Current agent avatar */}
                <div
                  className={`
                    w-10 h-10 rounded-lg flex items-center justify-center font-bold text-sm
                    ${currentAgent?.color === 'cyan' && 'bg-neon-cyan/20 border-2 border-neon-cyan text-neon-cyan'}
                    ${currentAgent?.color === 'pink' && 'bg-neon-pink/20 border-2 border-neon-pink text-neon-pink'}
                    ${(!currentAgent?.color || currentAgent?.color === 'purple') &&
                      'bg-neon-purple/20 border-2 border-neon-purple text-neon-purple'}
                  `}
                  title={currentAgent?.name}
                >
                  {currentAgent?.id || 'A'}
                </div>

                {/* Quick actions icons */}
                <button
                  onClick={() => handleCommand('/help')}
                  className="p-2 rounded-lg hover:bg-cyber-bg-primary/50 transition-colors text-text-secondary hover:text-neon-cyan"
                  title="查看帮助"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="20"
                    height="20"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  >
                    <circle cx="12" cy="12" r="10" />
                    <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3" />
                    <path d="M12 17h.01" />
                  </svg>
                </button>

                <button
                  onClick={() => handleCommand('/clear')}
                  className="p-2 rounded-lg hover:bg-cyber-bg-primary/50 transition-colors text-text-secondary hover:text-neon-cyan"
                  title="清除历史"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="20"
                    height="20"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  >
                    <path d="M3 6h18" />
                    <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6" />
                    <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2" />
                  </svg>
                </button>

                {/* Message count badge */}
                <div className="mt-4 px-2 py-1 rounded bg-neon-cyan/20 text-neon-cyan text-xs font-bold" title={`${messages.length} 条消息`}>
                  {messages.length}
                </div>
              </div>
            )}
          </div>
        </aside>

        {/* Chat area */}
        <main className="flex-1 flex flex-col">
          {/* Messages */}
          <MessageList
            messages={messages}
            isTyping={isTyping}
            typingAgentName={currentAgent?.name}
            autoScroll
            showTimestamps
            emptyMessage="欢迎使用ZTL智能对话系统"
          />

          {/* Input */}
          <div className="flex-shrink-0 p-4 border-t-2 border-neon-cyan/20 bg-cyber-bg-secondary/30 backdrop-blur-sm">
            <div className="container mx-auto max-w-4xl">
              <ChatInput
                value={inputValue}
                onChange={setInputValue}
                onSubmit={handleSendMessage}
                isLoading={isTyping}
                placeholder={`与 ${currentAgent?.name} 对话... (/ 显示命令)`}
                showCommandSuggestions
              />
            </div>
          </div>
        </main>

        {/* Right Sidebar - Skills */}
        <aside
          className={`
            border-l-2 border-neon-pink/20 bg-cyber-bg-secondary/30 backdrop-blur-sm
            transition-all duration-300 ease-in-out
            ${isSkillsSidebarCollapsed ? 'w-16' : 'w-80'}
            relative
          `}
        >
          {/* Collapse/Expand button */}
          <button
            onClick={() => setIsSkillsSidebarCollapsed(!isSkillsSidebarCollapsed)}
            className="absolute -left-3 top-4 z-50 w-6 h-6 rounded-full bg-neon-pink border-2 border-neon-pink hover:bg-neon-pink/70 active:scale-95 transition-all duration-200 flex items-center justify-center shadow-lg cursor-pointer"
            aria-label={isSkillsSidebarCollapsed ? '展开技能包侧边栏' : '收起技能包侧边栏'}
            style={{ pointerEvents: 'auto' }}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="12"
              height="12"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2.5"
              strokeLinecap="round"
              strokeLinejoin="round"
              className={`transition-transform duration-300 text-white ${isSkillsSidebarCollapsed ? '' : 'rotate-180'}`}
            >
              <path d="m15 18-6-6 6-6" />
            </svg>
          </button>

          <div className="p-4 pb-8 h-full overflow-y-auto">
            {!isSkillsSidebarCollapsed ? (
              // Expanded view
              <div className="space-y-4 pb-8">
                <div>
                  <h2 className="text-sm font-bold text-text-secondary uppercase tracking-wider mb-3">
                    技能包
                  </h2>
                  {isLoadingSkills ? (
                    <div className="flex items-center justify-center py-8">
                      <div className="w-8 h-8 border-2 border-neon-pink border-t-transparent rounded-full animate-spin" />
                    </div>
                  ) : (
                    <div className="space-y-2">
                      {skills.map((skill) => (
                        <button
                          key={skill.id}
                          onClick={() => setSelectedSkillId(skill.id)}
                          className={`
                            w-full p-3 rounded-lg text-left transition-all
                            ${
                              selectedSkillId === skill.id
                                ? 'bg-neon-pink/20 border-2 border-neon-pink'
                                : 'bg-cyber-bg-tertiary/30 border border-text-secondary/20 hover:border-neon-pink/50'
                            }
                          `}
                        >
                          <div className="font-semibold text-sm line-clamp-1">{skill.name}</div>
                          <div className="text-xs text-text-secondary mt-1 line-clamp-1">{skill.category}</div>
                        </button>
                      ))}
                    </div>
                  )}
                </div>

                <div className="pt-4 border-t-2 border-text-secondary/10">
                  <h3 className="text-sm font-bold text-text-secondary uppercase tracking-wider mb-3">
                    技能包详情
                  </h3>
                  <SkillDetails skill={selectedSkill || null} />
                </div>
              </div>
            ) : (
              // Collapsed view - icon-only
              <div className="flex flex-col items-center gap-4 pt-12">
                {/* Current skill icon */}
                <div
                  className="w-10 h-10 rounded-lg flex items-center justify-center font-bold text-sm bg-neon-pink/20 border-2 border-neon-pink text-neon-pink"
                  title={selectedSkill?.name}
                >
                  {selectedSkill?.name.charAt(0) || 'S'}
                </div>

                {/* Skill count badge */}
                <div className="mt-4 px-2 py-1 rounded bg-neon-pink/20 text-neon-pink text-xs font-bold" title={`${skills.length} 个技能包`}>
                  {skills.length}
                </div>
              </div>
            )}
          </div>
        </aside>
      </div>

    </div>
  );
}
