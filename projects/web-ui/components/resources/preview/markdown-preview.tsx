'use client';

import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeRaw from 'rehype-raw';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

interface MarkdownPreviewProps {
  content: string;
  filename: string;
}

export default function MarkdownPreview({ content, filename }: MarkdownPreviewProps) {

  return (
    <div className="relative h-full flex flex-col">
      {/* Markdown Content */}
      <div className="flex-1 overflow-auto p-6">
        <div className="glass-panel neon-glow-cyan rounded-lg p-8 markdown-body">
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            rehypePlugins={[rehypeRaw]}
            components={{
              // Custom code block rendering with syntax highlighting
              code({ node, inline, className, children, ...props }) {
                const match = /language-(\w+)/.exec(className || '');
                const lang = match ? match[1] : '';

                return !inline && lang ? (
                  <SyntaxHighlighter
                    style={vscDarkPlus}
                    language={lang}
                    PreTag="div"
                    customStyle={{
                      margin: '1rem 0',
                      borderRadius: '0.5rem',
                      border: '1px solid rgba(0, 255, 255, 0.2)',
                    }}
                    {...props}
                  >
                    {String(children).replace(/\n$/, '')}
                  </SyntaxHighlighter>
                ) : (
                  <code
                    className="bg-neon-cyan/10 text-neon-cyan px-1.5 py-0.5 rounded text-sm font-mono"
                    {...props}
                  >
                    {children}
                  </code>
                );
              },
              // Headings
              h1: ({ children }) => (
                <h1 className="text-3xl font-bold text-neon-cyan mb-4 mt-6 border-b border-neon-cyan/30 pb-2">
                  {children}
                </h1>
              ),
              h2: ({ children }) => (
                <h2 className="text-2xl font-bold text-neon-cyan mb-3 mt-5 border-b border-neon-cyan/20 pb-2">
                  {children}
                </h2>
              ),
              h3: ({ children }) => (
                <h3 className="text-xl font-bold text-neon-cyan mb-2 mt-4">{children}</h3>
              ),
              h4: ({ children }) => (
                <h4 className="text-lg font-bold text-text-primary mb-2 mt-3">{children}</h4>
              ),
              // Paragraphs
              p: ({ children }) => (
                <p className="text-text-primary mb-4 leading-relaxed">{children}</p>
              ),
              // Links
              a: ({ href, children }) => (
                <a
                  href={href}
                  className="text-neon-cyan hover:text-neon-pink underline transition-colors"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {children}
                </a>
              ),
              // Lists
              ul: ({ children }) => (
                <ul className="list-disc list-inside mb-4 space-y-1 text-text-primary">
                  {children}
                </ul>
              ),
              ol: ({ children }) => (
                <ol className="list-decimal list-inside mb-4 space-y-1 text-text-primary">
                  {children}
                </ol>
              ),
              li: ({ children }) => <li className="ml-4">{children}</li>,
              // Blockquotes
              blockquote: ({ children }) => (
                <blockquote className="border-l-4 border-neon-cyan pl-4 py-2 my-4 bg-neon-cyan/5 italic text-text-secondary">
                  {children}
                </blockquote>
              ),
              // Tables
              table: ({ children }) => (
                <div className="overflow-x-auto my-4">
                  <table className="min-w-full border border-neon-cyan/30 rounded-lg overflow-hidden">
                    {children}
                  </table>
                </div>
              ),
              thead: ({ children }) => (
                <thead className="bg-neon-cyan/10">{children}</thead>
              ),
              th: ({ children }) => (
                <th className="border border-neon-cyan/30 px-4 py-2 text-left text-neon-cyan font-semibold">
                  {children}
                </th>
              ),
              td: ({ children }) => (
                <td className="border border-neon-cyan/30 px-4 py-2 text-text-primary">
                  {children}
                </td>
              ),
              // Horizontal Rule
              hr: () => <hr className="my-6 border-neon-cyan/30" />,
              // Images
              img: ({ src, alt }) => (
                <img
                  src={src}
                  alt={alt}
                  className="max-w-full rounded-lg neon-glow-cyan my-4"
                />
              ),
            }}
          >
            {content}
          </ReactMarkdown>
        </div>
      </div>

      {/* Custom Markdown Styles */}
      <style jsx global>{`
        .markdown-body {
          color: var(--text-primary);
          line-height: 1.6;
        }

        .markdown-body img {
          max-width: 100%;
          height: auto;
        }

        .markdown-body pre {
          overflow-x: auto;
        }

        .markdown-body :first-child {
          margin-top: 0;
        }

        .markdown-body :last-child {
          margin-bottom: 0;
        }
      `}</style>
    </div>
  );
}
