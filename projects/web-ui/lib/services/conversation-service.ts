/**
 * Conversation Service - 对话服务层
 * 负责对话、记忆、快照的数据库操作
 */

import { createClient } from '@/lib/supabase/client';
import type { Message } from '@/components/chat/message-list';
import type { ExtractedMemory, MemoryType } from './memory-extractor';
import type { CompressionResult } from './conversation-compressor';
import type { ContinuationContext } from './continuation-generator';

// ============================================================
// Type Definitions
// ============================================================

export type ContextStatus = 'normal' | 'approaching_limit' | 'compacted' | 'continued';
export type TriggerReason = 'manual' | 'auto_compact' | 'context_limit' | 'session_end';

export interface Conversation {
  id: string;
  user_id: string;
  title: string;
  agent_name: string;
  context_status: ContextStatus;
  parent_conversation_id: string | null;
  continuation_index: number;
  is_root_conversation: boolean;
  last_compacted_at: string | null;
  message_count: number;
  metadata: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface ConversationMemory {
  id: string;
  conversation_id: string;
  memory_type: MemoryType;
  content: string;
  importance_score: number;
  metadata: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface ConversationSnapshot {
  id: string;
  conversation_id: string;
  trigger_reason: TriggerReason;
  snapshot_data: {
    compressedMessages: Message[];
    summary: string;
    memories: ExtractedMemory[];
    compressionRatio: number;
  };
  summary: string;
  extracted_memories: ExtractedMemory[];
  message_count: number;
  compressed_count: number;
  removed_count: number;
  total_tokens: number | null;
  compression_ratio: number;
  created_at: string;
}

// ============================================================
// Conversation Service Class
// ============================================================

export class ConversationService {
  private supabase;

  constructor() {
    this.supabase = createClient();
  }

  // ========================================
  // Conversation Operations
  // ========================================

  /**
   * 创建新对话
   */
  async createConversation(data: {
    title: string;
    agent_name: string;
    parent_conversation_id?: string;
  }): Promise<Conversation | null> {
    const { data: conversation, error } = await this.supabase
      .from('conversations')
      .insert({
        title: data.title,
        agent_name: data.agent_name,
        parent_conversation_id: data.parent_conversation_id || null,
        continuation_index: data.parent_conversation_id ? 1 : 0,
        is_root_conversation: !data.parent_conversation_id,
        context_status: 'normal',
        message_count: 0,
      })
      .select()
      .single();

    if (error) {
      console.error('创建对话失败:', error);
      return null;
    }

    return conversation;
  }

  /**
   * 获取对话详情
   */
  async getConversation(conversationId: string): Promise<Conversation | null> {
    const { data, error } = await this.supabase
      .from('conversations')
      .select('*')
      .eq('id', conversationId)
      .single();

    if (error) {
      console.error('获取对话失败:', error);
      return null;
    }

    return data;
  }

  /**
   * 更新对话状态
   */
  async updateConversationStatus(
    conversationId: string,
    status: ContextStatus,
    messageCount?: number
  ): Promise<boolean> {
    const updateData: any = { context_status: status };

    if (messageCount !== undefined) {
      updateData.message_count = messageCount;
    }

    if (status === 'compacted') {
      updateData.last_compacted_at = new Date().toISOString();
    }

    const { error } = await this.supabase
      .from('conversations')
      .update(updateData)
      .eq('id', conversationId);

    if (error) {
      console.error('更新对话状态失败:', error);
      return false;
    }

    return true;
  }

  /**
   * 获取对话延续链
   */
  async getConversationChain(conversationId: string): Promise<Conversation[]> {
    // 1. 获取当前对话
    const current = await this.getConversation(conversationId);
    if (!current) return [];

    // 2. 如果是根对话,查找所有子对话
    if (current.is_root_conversation) {
      const { data, error } = await this.supabase
        .from('conversations')
        .select('*')
        .or(`id.eq.${conversationId},parent_conversation_id.eq.${conversationId}`)
        .order('continuation_index', { ascending: true });

      if (error) {
        console.error('获取对话链失败:', error);
        return [current];
      }

      return data || [current];
    }

    // 3. 如果是延续对话,找到根对话并获取整条链
    const rootId = current.parent_conversation_id;
    if (!rootId) return [current];

    const { data, error } = await this.supabase
      .from('conversations')
      .select('*')
      .or(`id.eq.${rootId},parent_conversation_id.eq.${rootId}`)
      .order('continuation_index', { ascending: true });

    if (error) {
      console.error('获取对话链失败:', error);
      return [current];
    }

    return data || [current];
  }

  /**
   * 创建延续对话
   */
  async createContinuationConversation(
    parentId: string,
    title: string,
    agentName: string
  ): Promise<Conversation | null> {
    // 1. 获取父对话信息
    const parent = await this.getConversation(parentId);
    if (!parent) {
      console.error('父对话不存在');
      return null;
    }

    // 2. 计算延续序号
    const continuationIndex = parent.continuation_index + 1;

    // 3. 确定根对话ID
    const rootId = parent.is_root_conversation ? parentId : parent.parent_conversation_id;

    // 4. 创建新对话
    const { data, error } = await this.supabase
      .from('conversations')
      .insert({
        title,
        agent_name: agentName,
        parent_conversation_id: rootId,
        continuation_index: continuationIndex,
        is_root_conversation: false,
        context_status: 'continued',
        message_count: 0,
      })
      .select()
      .single();

    if (error) {
      console.error('创建延续对话失败:', error);
      return null;
    }

    return data;
  }

  // ========================================
  // Memory Operations
  // ========================================

  /**
   * 保存单条记忆
   */
  async saveMemory(
    conversationId: string,
    memory: ExtractedMemory
  ): Promise<ConversationMemory | null> {
    const { data, error } = await this.supabase
      .from('conversation_memories')
      .insert({
        conversation_id: conversationId,
        memory_type: memory.type,
        content: memory.content,
        importance_score: memory.importance,
        metadata: memory.metadata || {},
      })
      .select()
      .single();

    if (error) {
      console.error('保存记忆失败:', error);
      return null;
    }

    return data;
  }

  /**
   * 批量保存记忆
   */
  async saveMemories(
    conversationId: string,
    memories: ExtractedMemory[]
  ): Promise<ConversationMemory[]> {
    const insertData = memories.map(memory => ({
      conversation_id: conversationId,
      memory_type: memory.type,
      content: memory.content,
      importance_score: memory.importance,
      metadata: memory.metadata || {},
    }));

    const { data, error } = await this.supabase
      .from('conversation_memories')
      .insert(insertData)
      .select();

    if (error) {
      console.error('批量保存记忆失败:', error);
      return [];
    }

    return data || [];
  }

  /**
   * 获取对话的所有记忆
   */
  async getMemories(
    conversationId: string,
    options?: {
      memoryType?: MemoryType;
      minImportance?: number;
      limit?: number;
    }
  ): Promise<ConversationMemory[]> {
    let query = this.supabase
      .from('conversation_memories')
      .select('*')
      .eq('conversation_id', conversationId);

    if (options?.memoryType) {
      query = query.eq('memory_type', options.memoryType);
    }

    if (options?.minImportance !== undefined) {
      query = query.gte('importance_score', options.minImportance);
    }

    query = query.order('importance_score', { ascending: false });

    if (options?.limit) {
      query = query.limit(options.limit);
    }

    const { data, error } = await query;

    if (error) {
      console.error('获取记忆失败:', error);
      return [];
    }

    return data || [];
  }

  /**
   * 删除对话的所有记忆
   */
  async deleteMemories(conversationId: string): Promise<boolean> {
    const { error } = await this.supabase
      .from('conversation_memories')
      .delete()
      .eq('conversation_id', conversationId);

    if (error) {
      console.error('删除记忆失败:', error);
      return false;
    }

    return true;
  }

  // ========================================
  // Snapshot Operations
  // ========================================

  /**
   * 创建对话快照
   */
  async createSnapshot(
    conversationId: string,
    compressionResult: CompressionResult,
    triggerReason: TriggerReason,
    originalMessageCount: number
  ): Promise<ConversationSnapshot | null> {
    const snapshotData = {
      compressedMessages: compressionResult.compressedMessages,
      summary: compressionResult.summary,
      memories: compressionResult.memories,
      compressionRatio: compressionResult.compressionRatio,
    };

    const { data, error } = await this.supabase
      .from('conversation_snapshots')
      .insert({
        conversation_id: conversationId,
        trigger_reason: triggerReason,
        snapshot_data: snapshotData,
        summary: compressionResult.summary,
        extracted_memories: compressionResult.memories,
        message_count: originalMessageCount,
        compressed_count: compressionResult.compressedMessages.length,
        removed_count: compressionResult.removedCount,
        compression_ratio: compressionResult.compressionRatio,
      })
      .select()
      .single();

    if (error) {
      console.error('创建快照失败:', error);
      return null;
    }

    return data;
  }

  /**
   * 获取对话的最新快照
   */
  async getLatestSnapshot(conversationId: string): Promise<ConversationSnapshot | null> {
    const { data, error } = await this.supabase
      .from('conversation_snapshots')
      .select('*')
      .eq('conversation_id', conversationId)
      .order('created_at', { ascending: false })
      .limit(1)
      .single();

    if (error) {
      console.error('获取最新快照失败:', error);
      return null;
    }

    return data;
  }

  /**
   * 获取对话的所有快照
   */
  async getSnapshots(conversationId: string): Promise<ConversationSnapshot[]> {
    const { data, error } = await this.supabase
      .from('conversation_snapshots')
      .select('*')
      .eq('conversation_id', conversationId)
      .order('created_at', { ascending: false });

    if (error) {
      console.error('获取快照列表失败:', error);
      return [];
    }

    return data || [];
  }

  /**
   * 删除对话的所有快照
   */
  async deleteSnapshots(conversationId: string): Promise<boolean> {
    const { error } = await this.supabase
      .from('conversation_snapshots')
      .delete()
      .eq('conversation_id', conversationId);

    if (error) {
      console.error('删除快照失败:', error);
      return false;
    }

    return true;
  }

  // ========================================
  // Continuation Operations
  // ========================================

  /**
   * 从快照恢复对话上下文
   */
  async restoreFromSnapshot(snapshotId: string): Promise<{
    messages: Message[];
    memories: ExtractedMemory[];
    summary: string;
  } | null> {
    const { data, error } = await this.supabase
      .from('conversation_snapshots')
      .select('*')
      .eq('id', snapshotId)
      .single();

    if (error || !data) {
      console.error('恢复快照失败:', error);
      return null;
    }

    return {
      messages: data.snapshot_data.compressedMessages,
      memories: data.snapshot_data.memories,
      summary: data.summary,
    };
  }

  /**
   * 准备延续上下文
   * 从最新快照和记忆构建ContinuationContext
   */
  async prepareContinuationContext(
    conversationId: string,
    agentName: string
  ): Promise<ContinuationContext | null> {
    // 1. 获取最新快照
    const snapshot = await this.getLatestSnapshot(conversationId);
    if (!snapshot) {
      console.error('未找到快照,无法延续对话');
      return null;
    }

    // 2. 获取高重要性记忆
    const memories = await this.getMemories(conversationId, {
      minImportance: 5,
      limit: 20,
    });

    // 3. 转换为ContinuationContext格式
    const extractedMemories: ExtractedMemory[] = memories.map(m => ({
      type: m.memory_type,
      content: m.content,
      importance: m.importance_score,
      metadata: m.metadata,
      timestamp: new Date(m.created_at),
    }));

    // 4. 获取对话信息用于计算延续序号
    const conversation = await this.getConversation(conversationId);
    const continuationIndex = conversation
      ? conversation.continuation_index + 1
      : 1;

    // 5. 构建上下文
    const context: ContinuationContext = {
      conversationId,
      agentName,
      summary: snapshot.summary,
      memories: extractedMemories,
      lastMessages: snapshot.snapshot_data.compressedMessages.slice(-5),
      metadata: {
        originalMessageCount: snapshot.message_count,
        compressionRatio: snapshot.compression_ratio,
        continuationIndex,
      },
    };

    return context;
  }

  // ========================================
  // Statistics & Analytics
  // ========================================

  /**
   * 获取对话统计信息
   */
  async getConversationStats(conversationId: string): Promise<{
    totalMemories: number;
    totalSnapshots: number;
    memoryByType: Record<MemoryType, number>;
    avgImportance: number;
  } | null> {
    const [memories, snapshots] = await Promise.all([
      this.getMemories(conversationId),
      this.getSnapshots(conversationId),
    ]);

    // 按类型统计记忆
    const memoryByType: Record<string, number> = {};
    let totalImportance = 0;

    memories.forEach(memory => {
      memoryByType[memory.memory_type] = (memoryByType[memory.memory_type] || 0) + 1;
      totalImportance += memory.importance_score;
    });

    const avgImportance = memories.length > 0
      ? totalImportance / memories.length
      : 0;

    return {
      totalMemories: memories.length,
      totalSnapshots: snapshots.length,
      memoryByType: memoryByType as Record<MemoryType, number>,
      avgImportance,
    };
  }

  /**
   * 清理旧快照(保留最近N个)
   */
  async cleanupOldSnapshots(
    conversationId: string,
    keepCount: number = 5
  ): Promise<boolean> {
    const snapshots = await this.getSnapshots(conversationId);

    if (snapshots.length <= keepCount) {
      return true; // 无需清理
    }

    // 保留最新的N个,删除其余
    const toDelete = snapshots.slice(keepCount);
    const deleteIds = toDelete.map(s => s.id);

    const { error } = await this.supabase
      .from('conversation_snapshots')
      .delete()
      .in('id', deleteIds);

    if (error) {
      console.error('清理旧快照失败:', error);
      return false;
    }

    return true;
  }
}

// 导出默认实例
export const conversationService = new ConversationService();
