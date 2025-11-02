-- Conversation Continuation System: Database Schema
-- 对话延续系统: 数据库架构
--
-- 此迁移创建对话延续所需的表和索引:
-- 1. conversation_memories: 存储提取的对话记忆
-- 2. conversation_snapshots: 存储压缩的对话快照
-- 3. 扩展 conversations 表: 添加上下文状态字段

-- ============================================================
-- 1. 创建 conversation_memories 表
-- ============================================================
CREATE TABLE IF NOT EXISTS conversation_memories (
  -- 主键
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  -- 关联关系
  conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,

  -- 记忆类型 (基于MANUS上下求索系统的10种类型)
  memory_type TEXT NOT NULL CHECK (memory_type IN (
    'focus',      -- 当前焦点
    'todo',       -- 待办事项
    'process',    -- 工作流程
    'error',      -- 错误学习
    'success',    -- 成功经验
    'insights',   -- 洞察发现
    'patterns',   -- 模式积累
    'context',    -- 项目背景
    'memory',     -- 长期记忆
    'snapshot'    -- 状态快照
  )),

  -- 记忆内容
  content TEXT NOT NULL,

  -- 重要性评分 (0-10)
  importance_score INTEGER DEFAULT 5 CHECK (importance_score BETWEEN 0 AND 10),

  -- 元数据 (JSON格式,存储额外信息)
  metadata JSONB DEFAULT '{}',

  -- 时间戳
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 索引优化
CREATE INDEX idx_conversation_memories_conversation_id
  ON conversation_memories(conversation_id);

CREATE INDEX idx_conversation_memories_type
  ON conversation_memories(memory_type);

CREATE INDEX idx_conversation_memories_importance
  ON conversation_memories(importance_score DESC);

CREATE INDEX idx_conversation_memories_created_at
  ON conversation_memories(created_at DESC);

-- 组合索引(常用查询模式)
CREATE INDEX idx_conversation_memories_conv_type
  ON conversation_memories(conversation_id, memory_type);

CREATE INDEX idx_conversation_memories_conv_importance
  ON conversation_memories(conversation_id, importance_score DESC);

-- ============================================================
-- 2. 创建 conversation_snapshots 表
-- ============================================================
CREATE TABLE IF NOT EXISTS conversation_snapshots (
  -- 主键
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  -- 关联关系
  conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,

  -- 触发原因
  trigger_reason TEXT NOT NULL CHECK (trigger_reason IN (
    'manual',         -- 手动触发
    'auto_compact',   -- 自动压缩
    'context_limit',  -- 上下文限制
    'session_end'     -- 会话结束
  )),

  -- 快照数据 (JSON格式)
  -- 包含: compressedMessages, summary, memories等
  snapshot_data JSONB NOT NULL,

  -- 压缩摘要(文本格式,便于搜索和显示)
  summary TEXT,

  -- 提取的记忆(JSON数组)
  extracted_memories JSONB DEFAULT '[]',

  -- 统计信息
  message_count INTEGER NOT NULL DEFAULT 0,      -- 原始消息数
  compressed_count INTEGER DEFAULT 0,            -- 压缩后消息数
  removed_count INTEGER DEFAULT 0,               -- 删除的消息数
  total_tokens INTEGER,                          -- 总token数(可选)
  compression_ratio REAL,                        -- 压缩比例 (0-1)

  -- 时间戳
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 索引优化
CREATE INDEX idx_conversation_snapshots_conversation_id
  ON conversation_snapshots(conversation_id);

CREATE INDEX idx_conversation_snapshots_trigger
  ON conversation_snapshots(trigger_reason);

CREATE INDEX idx_conversation_snapshots_created_at
  ON conversation_snapshots(created_at DESC);

-- 全文搜索索引(摘要)
CREATE INDEX idx_conversation_snapshots_summary_search
  ON conversation_snapshots USING gin(to_tsvector('chinese', summary));

-- ============================================================
-- 3. 扩展 conversations 表
-- ============================================================

-- 添加上下文状态字段
ALTER TABLE conversations
ADD COLUMN IF NOT EXISTS context_status TEXT DEFAULT 'normal'
CHECK (context_status IN (
  'normal',            -- 正常状态
  'approaching_limit', -- 接近限制
  'compacted',         -- 已压缩
  'continued'          -- 已延续
));

-- 添加延续关系字段
ALTER TABLE conversations
ADD COLUMN IF NOT EXISTS parent_conversation_id UUID REFERENCES conversations(id) ON DELETE SET NULL,
ADD COLUMN IF NOT EXISTS continuation_index INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS is_root_conversation BOOLEAN DEFAULT TRUE;

-- 添加压缩相关字段
ALTER TABLE conversations
ADD COLUMN IF NOT EXISTS last_compacted_at TIMESTAMP WITH TIME ZONE,
ADD COLUMN IF NOT EXISTS message_count INTEGER DEFAULT 0;

-- 添加元数据字段
ALTER TABLE conversations
ADD COLUMN IF NOT EXISTS metadata JSONB DEFAULT '{}';

-- 索引优化
CREATE INDEX IF NOT EXISTS idx_conversations_context_status
  ON conversations(context_status);

CREATE INDEX IF NOT EXISTS idx_conversations_parent_id
  ON conversations(parent_conversation_id);

CREATE INDEX IF NOT EXISTS idx_conversations_is_root
  ON conversations(is_root_conversation);

-- 组合索引(查询延续链)
CREATE INDEX IF NOT EXISTS idx_conversations_continuation_chain
  ON conversations(parent_conversation_id, continuation_index)
  WHERE parent_conversation_id IS NOT NULL;

-- ============================================================
-- 4. 创建触发器(自动更新时间戳)
-- ============================================================

-- conversation_memories 更新时间戳触发器
CREATE OR REPLACE FUNCTION update_conversation_memories_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_conversation_memories_updated_at
  BEFORE UPDATE ON conversation_memories
  FOR EACH ROW
  EXECUTE FUNCTION update_conversation_memories_updated_at();

-- ============================================================
-- 5. 创建视图(便捷查询)
-- ============================================================

-- 视图: 对话及其记忆统计
CREATE OR REPLACE VIEW conversation_memory_stats AS
SELECT
  c.id AS conversation_id,
  c.title,
  c.agent_name,
  c.context_status,
  c.message_count,
  c.continuation_index,
  c.is_root_conversation,
  COUNT(DISTINCT cm.id) AS total_memories,
  COUNT(DISTINCT cs.id) AS total_snapshots,
  MAX(cm.created_at) AS last_memory_at,
  MAX(cs.created_at) AS last_snapshot_at
FROM conversations c
LEFT JOIN conversation_memories cm ON c.id = cm.conversation_id
LEFT JOIN conversation_snapshots cs ON c.id = cs.conversation_id
GROUP BY c.id, c.title, c.agent_name, c.context_status, c.message_count,
         c.continuation_index, c.is_root_conversation;

-- 视图: 记忆按类型统计
CREATE OR REPLACE VIEW memory_type_distribution AS
SELECT
  conversation_id,
  memory_type,
  COUNT(*) AS count,
  AVG(importance_score) AS avg_importance,
  MAX(importance_score) AS max_importance
FROM conversation_memories
GROUP BY conversation_id, memory_type;

-- ============================================================
-- 6. RLS (Row Level Security) 策略
-- ============================================================

-- 启用 RLS
ALTER TABLE conversation_memories ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversation_snapshots ENABLE ROW LEVEL SECURITY;

-- conversation_memories 策略
CREATE POLICY "Users can view their own conversation memories"
  ON conversation_memories FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM conversations
      WHERE conversations.id = conversation_memories.conversation_id
        AND conversations.user_id = auth.uid()
    )
  );

CREATE POLICY "Users can insert their own conversation memories"
  ON conversation_memories FOR INSERT
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM conversations
      WHERE conversations.id = conversation_memories.conversation_id
        AND conversations.user_id = auth.uid()
    )
  );

CREATE POLICY "Users can update their own conversation memories"
  ON conversation_memories FOR UPDATE
  USING (
    EXISTS (
      SELECT 1 FROM conversations
      WHERE conversations.id = conversation_memories.conversation_id
        AND conversations.user_id = auth.uid()
    )
  );

CREATE POLICY "Users can delete their own conversation memories"
  ON conversation_memories FOR DELETE
  USING (
    EXISTS (
      SELECT 1 FROM conversations
      WHERE conversations.id = conversation_memories.conversation_id
        AND conversations.user_id = auth.uid()
    )
  );

-- conversation_snapshots 策略
CREATE POLICY "Users can view their own conversation snapshots"
  ON conversation_snapshots FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM conversations
      WHERE conversations.id = conversation_snapshots.conversation_id
        AND conversations.user_id = auth.uid()
    )
  );

CREATE POLICY "Users can insert their own conversation snapshots"
  ON conversation_snapshots FOR INSERT
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM conversations
      WHERE conversations.id = conversation_snapshots.conversation_id
        AND conversations.user_id = auth.uid()
    )
  );

CREATE POLICY "Users can delete their own conversation snapshots"
  ON conversation_snapshots FOR DELETE
  USING (
    EXISTS (
      SELECT 1 FROM conversations
      WHERE conversations.id = conversation_snapshots.conversation_id
        AND conversations.user_id = auth.uid()
    )
  );

-- conversations 表的扩展列需要更新现有策略
-- (假设原有策略已存在,这里只是注释说明)
-- 确保 UPDATE 策略允许更新新增的列

-- ============================================================
-- 7. 数据完整性约束
-- ============================================================

-- 确保延续链的完整性(父对话必须是根对话或另一个延续对话)
ALTER TABLE conversations
ADD CONSTRAINT check_continuation_chain
CHECK (
  (parent_conversation_id IS NULL AND continuation_index = 0) OR
  (parent_conversation_id IS NOT NULL AND continuation_index > 0)
);

-- 确保压缩比例在有效范围
ALTER TABLE conversation_snapshots
ADD CONSTRAINT check_compression_ratio
CHECK (compression_ratio IS NULL OR (compression_ratio >= 0 AND compression_ratio <= 1));

-- 确保消息计数非负
ALTER TABLE conversation_snapshots
ADD CONSTRAINT check_message_counts
CHECK (
  message_count >= 0 AND
  compressed_count >= 0 AND
  removed_count >= 0 AND
  compressed_count + removed_count <= message_count
);

-- ============================================================
-- 8. 注释(文档化)
-- ============================================================

COMMENT ON TABLE conversation_memories IS '对话记忆表: 存储从对话中提取的关键记忆,基于MANUS上下求索系统的10种记忆类型';
COMMENT ON COLUMN conversation_memories.memory_type IS '记忆类型: focus(焦点), todo(待办), process(流程), error(错误), success(成功), insights(洞察), patterns(模式), context(背景), memory(长期记忆), snapshot(快照)';
COMMENT ON COLUMN conversation_memories.importance_score IS '重要性评分: 0-10, 数值越高越重要';

COMMENT ON TABLE conversation_snapshots IS '对话快照表: 存储压缩的对话历史快照,用于对话延续和恢复';
COMMENT ON COLUMN conversation_snapshots.trigger_reason IS '触发原因: manual(手动), auto_compact(自动压缩), context_limit(上下文限制), session_end(会话结束)';
COMMENT ON COLUMN conversation_snapshots.snapshot_data IS '快照数据: JSON格式,包含压缩后的消息、摘要、记忆等完整信息';

COMMENT ON COLUMN conversations.context_status IS '上下文状态: normal(正常), approaching_limit(接近限制), compacted(已压缩), continued(已延续)';
COMMENT ON COLUMN conversations.parent_conversation_id IS '父对话ID: 用于延续对话链,指向被延续的原对话';
COMMENT ON COLUMN conversations.continuation_index IS '延续序号: 从0开始,表示这是第几次延续';
COMMENT ON COLUMN conversations.is_root_conversation IS '是否根对话: true表示原始对话,false表示延续对话';

-- ============================================================
-- 9. 示例数据(可选,用于测试)
-- ============================================================

-- 注意: 在生产环境中应删除此部分或注释掉

-- INSERT INTO conversation_memories (conversation_id, memory_type, content, importance_score) VALUES
-- ('example-conv-uuid', 'focus', '当前正在讨论对话延续系统的实现', 9),
-- ('example-conv-uuid', 'todo', '需要实现UI组件和Supabase集成', 8),
-- ('example-conv-uuid', 'insights', '压缩算法应该保留最近消息和重要历史消息', 7);

-- ============================================================
-- 完成
-- ============================================================
