# Chat Components Documentation

## 📚 Components Overview

This directory contains all chat-related components for the ZTL Web-UI Chat Page.

---

## 🧩 Components

### 1. ChatMessage
**File**: `chat-message.tsx`

Displays individual messages in the chat with proper styling based on role (user/assistant/system).

**Props**:
```typescript
interface ChatMessageProps {
  content: string;
  role: 'user' | 'assistant' | 'system';
  agentName?: string;
  timestamp?: Date | string;
  showTimestamp?: boolean;
  status?: 'sending' | 'sent' | 'error';
  isStreaming?: boolean;
}
```

**Usage**:
```tsx
<ChatMessage
  content="Hello, how can I help you?"
  role="assistant"
  agentName="G1-经营分析优化师"
  timestamp={new Date()}
  isStreaming={false}
/>
```

---

### 2. ChatInput
**File**: `chat-input.tsx`

Smart input component with command autocomplete and auto-resizing textarea.

**Props**:
```typescript
interface ChatInputProps {
  value: string;
  onChange: (value: string) => void;
  onSubmit: (message: string) => void;
  isLoading?: boolean;
  placeholder?: string;
  showCommandSuggestions?: boolean;
  onCommandSelect?: (command: string) => void;
  disabled?: boolean;
}
```

**Features**:
- ✅ Auto-resizing textarea
- ✅ Command autocomplete (type `/`)
- ✅ Enter to send, Shift+Enter for newline
- ✅ Loading state with spinner
- ✅ Character count display

**Usage**:
```tsx
<ChatInput
  value={inputValue}
  onChange={setInputValue}
  onSubmit={handleSend}
  isLoading={isTyping}
  placeholder="输入消息..."
  showCommandSuggestions
/>
```

---

### 3. MessageList
**File**: `message-list.tsx`

Container for displaying message history with auto-scroll and typing indicator.

**Props**:
```typescript
interface MessageListProps {
  messages: Message[];
  isTyping?: boolean;
  typingAgentName?: string;
  autoScroll?: boolean;
  showTimestamps?: boolean;
  emptyMessage?: string;
}

interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant' | 'system';
  agentName?: string;
  timestamp: Date;
  status?: 'sending' | 'sent' | 'error';
  isStreaming?: boolean;
}
```

**Features**:
- ✅ Auto-scroll to bottom
- ✅ User scroll detection
- ✅ "Scroll to bottom" button
- ✅ Empty state display
- ✅ Typing indicator integration

**Usage**:
```tsx
<MessageList
  messages={messages}
  isTyping={isTyping}
  typingAgentName="G1-经营分析优化师"
  autoScroll
  showTimestamps
  emptyMessage="开始对话..."
/>
```

---

### 4. TypingIndicator
**File**: `typing-indicator.tsx`

Animated indicator shown when agent is typing.

**Props**:
```typescript
interface TypingIndicatorProps {
  agentName?: string;
  variant?: 'dots' | 'pulse' | 'wave';
}
```

**Variants**:
- **dots**: Bouncing dots (default)
- **pulse**: Pulsing bars
- **wave**: Wave animation

**Usage**:
```tsx
<TypingIndicator
  agentName="G1-经营分析优化师"
  variant="dots"
/>
```

---

### 5. AgentSwitcher
**File**: `agent-switcher.tsx`

Dropdown selector for switching between different AI agents.

**Props**:
```typescript
interface AgentSwitcherProps {
  agents: Agent[];
  currentAgentId: string;
  onAgentChange: (agentId: string) => void;
  showGroups?: boolean;
  position?: 'top' | 'bottom' | 'left' | 'right';
}

interface Agent {
  id: string;
  name: string;
  description: string;
  avatar?: string;
  group?: string;
  color?: 'cyan' | 'purple' | 'pink';
}
```

**Features**:
- ✅ Grouped by business units
- ✅ Color-coded agents
- ✅ Search/filter support
- ✅ Current agent highlight
- ✅ Avatar display

**Usage**:
```tsx
<AgentSwitcher
  agents={AGENTS}
  currentAgentId={currentId}
  onAgentChange={setCurrentId}
  showGroups
/>
```

---

### 6. CommandPalette
**File**: `command-palette.tsx`

Keyboard-driven command palette for quick actions.

**Props**:
```typescript
interface CommandPaletteProps {
  isOpen: boolean;
  onClose: () => void;
  commands: Command[];
  searchPlaceholder?: string;
}

interface Command {
  id: string;
  name: string;
  description: string;
  icon?: React.ReactNode;
  shortcut?: string;
  group?: string;
  onExecute: () => void;
}
```

**Features**:
- ✅ Fuzzy search
- ✅ Grouped commands
- ✅ Arrow key navigation
- ✅ Shortcut display
- ✅ Cmd/Ctrl+K to open

**Usage**:
```tsx
<CommandPalette
  isOpen={isOpen}
  onClose={() => setIsOpen(false)}
  commands={[
    {
      id: 'help',
      name: '显示帮助',
      description: '查看所有可用命令',
      group: '系统',
      shortcut: '/help',
      onExecute: () => showHelp(),
    },
  ]}
/>
```

---

## 🎨 Styling

All components use:
- **Tailwind v4** for styling
- **Cyberpunk theme** colors (cyan, purple, pink)
- **Orbitron** font for headers
- **Electrolize** font for body text
- **Neon glow** effects
- **Smooth animations**

### Color Palette
```css
--color-neon-cyan: #00ffff;
--color-neon-purple: #b000ff;
--color-neon-pink: #ff00ff;
--color-cyber-bg-primary: #0a0a0f;
--color-cyber-bg-secondary: #0f0f23;
--color-text-primary: #a8a8ff;
--color-text-secondary: #6868a0;
```

---

## 🔑 Key Patterns

### Message State Management
```typescript
const [messages, setMessages] = useState<Message[]>([]);

// Add message
setMessages(prev => [...prev, newMessage]);

// Update message (for streaming)
setMessages(prev =>
  prev.map(msg =>
    msg.id === messageId
      ? { ...msg, content: updatedContent }
      : msg
  )
);
```

### Streaming Implementation
```typescript
// Character-by-character streaming
for (let i = 0; i <= text.length; i++) {
  await new Promise(resolve => setTimeout(resolve, 30));
  updateMessage(text.slice(0, i));
}
```

### Command Handling
```typescript
const handleCommand = (command: string) => {
  const [cmd, ...args] = command.trim().split(' ');

  switch (cmd.toLowerCase()) {
    case '/help':
      showHelp();
      break;
    case '/clear':
      clearHistory();
      break;
    case '/switch':
      openAgentSwitcher();
      break;
  }
};
```

---

## 🚀 Quick Start

### 1. Import Components
```typescript
import {
  ChatInput,
  MessageList,
  TypingIndicator,
  AgentSwitcher,
  CommandPalette,
  type Message,
  type Agent,
  type Command,
} from '@/components/chat';
```

### 2. Set Up State
```typescript
const [messages, setMessages] = useState<Message[]>([]);
const [input, setInput] = useState('');
const [isTyping, setIsTyping] = useState(false);
const [currentAgentId, setCurrentAgentId] = useState('g1');
```

### 3. Build Layout
```tsx
<div className="flex flex-col h-screen">
  <MessageList
    messages={messages}
    isTyping={isTyping}
  />
  <ChatInput
    value={input}
    onChange={setInput}
    onSubmit={handleSend}
  />
</div>
```

---

## 📱 Responsive Design

All components are responsive and work on:
- ✅ Desktop (1920x1080+)
- ✅ Laptop (1366x768+)
- ✅ Tablet (768x1024+)
- ✅ Mobile (375x667+)

### Mobile Optimizations
- Touch-friendly tap targets (44x44px minimum)
- Collapsible sidebar
- Full-screen chat on small devices
- Optimized animations for lower-end devices

---

## ♿ Accessibility

- ✅ **Keyboard Navigation**: All interactive elements accessible via keyboard
- ✅ **Focus Indicators**: Clear visual focus states
- ✅ **ARIA Labels**: Proper labels for screen readers
- ✅ **Color Contrast**: WCAG AA compliant (4.5:1 minimum)
- ✅ **Semantic HTML**: Proper heading hierarchy

### Keyboard Shortcuts
- `Enter` - Send message
- `Shift+Enter` - New line
- `Cmd/Ctrl+K` - Open command palette
- `↑/↓` - Navigate commands
- `Esc` - Close modals

---

## 🧪 Testing

### Unit Tests (Coming Soon)
```typescript
// Example test structure
describe('ChatInput', () => {
  it('should submit message on Enter press', () => {
    // Test implementation
  });

  it('should show command suggestions on /', () => {
    // Test implementation
  });
});
```

### Integration Tests (Coming Soon)
```typescript
describe('Chat Flow', () => {
  it('should handle full message send/receive cycle', () => {
    // Test implementation
  });
});
```

---

## 📖 Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev)
- [Tailwind CSS](https://tailwindcss.com)
- [TypeScript Handbook](https://www.typescriptlang.org/docs)

---

## 🤝 Contributing

When adding new chat components:

1. Follow existing naming conventions
2. Use TypeScript with strict types
3. Add JSDoc comments for props
4. Include usage examples
5. Maintain cyberpunk theme consistency
6. Ensure responsive design
7. Add to this README

---

## 📄 License

Part of ZTL数智化作战中心 project.
