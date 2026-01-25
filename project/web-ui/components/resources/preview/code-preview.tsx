'use client';

import { useState } from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

interface CodePreviewProps {
  content: string;
  language: string;
  filename: string;
}

// Map file extensions to syntax highlighter language names
const getLanguageFromExtension = (ext: string): string => {
  const languageMap: Record<string, string> = {
    js: 'javascript',
    jsx: 'jsx',
    ts: 'typescript',
    tsx: 'tsx',
    py: 'python',
    java: 'java',
    c: 'c',
    cpp: 'cpp',
    cs: 'csharp',
    go: 'go',
    rs: 'rust',
    rb: 'ruby',
    php: 'php',
    swift: 'swift',
    kt: 'kotlin',
    scala: 'scala',
    html: 'html',
    htm: 'html',
    xml: 'xml',
    css: 'css',
    scss: 'scss',
    sass: 'sass',
    less: 'less',
    json: 'json',
    yaml: 'yaml',
    yml: 'yaml',
    toml: 'toml',
    ini: 'ini',
    sql: 'sql',
    sh: 'bash',
    bash: 'bash',
    zsh: 'bash',
    fish: 'fish',
    ps1: 'powershell',
    dockerfile: 'dockerfile',
    md: 'markdown',
    txt: 'text',
  };

  return languageMap[ext.toLowerCase()] || 'text';
};

export default function CodePreview({ content, language, filename }: CodePreviewProps) {
  const lang = getLanguageFromExtension(language);
  const lineCount = content.split('\n').length;

  // Custom style with cyber theme colors
  const customStyle = {
    ...vscDarkPlus,
    'pre[class*="language-"]': {
      ...vscDarkPlus['pre[class*="language-"]'],
      background: 'rgba(10, 25, 47, 0.8)',
      border: '1px solid rgba(0, 255, 255, 0.2)',
      borderRadius: '0.5rem',
      padding: '1.5rem',
      margin: 0,
      fontSize: '0.875rem',
      lineHeight: '1.5',
      fontFamily: '"Fira Code", "Consolas", "Monaco", monospace',
    },
    'code[class*="language-"]': {
      ...vscDarkPlus['code[class*="language-"]'],
      background: 'transparent',
      fontFamily: '"Fira Code", "Consolas", "Monaco", monospace',
    },
  };

  return (
    <div className="relative h-full flex flex-col">
      {/* Code Editor */}
      <div className="flex-1 overflow-auto neon-glow-cyan rounded-lg">
        <SyntaxHighlighter
          language={lang}
          style={customStyle}
          showLineNumbers
          wrapLines
          lineNumberStyle={{
            minWidth: '3em',
            paddingRight: '1em',
            color: 'rgba(0, 255, 255, 0.4)',
            borderRight: '1px solid rgba(0, 255, 255, 0.2)',
            marginRight: '1em',
            userSelect: 'none',
          }}
          customStyle={{
            margin: 0,
            background: 'rgba(10, 25, 47, 0.8)',
            border: '1px solid rgba(0, 255, 255, 0.2)',
            borderRadius: '0.5rem',
            maxHeight: '70vh',
          }}
        >
          {content}
        </SyntaxHighlighter>
      </div>
    </div>
  );
}
