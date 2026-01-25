import type { Metadata } from 'next';
import { Orbitron, Electrolize } from 'next/font/google';
import './globals.css';

const orbitron = Orbitron({
  subsets: ['latin'],
  variable: '--font-orbitron',
  display: 'swap',
});

const electrolize = Electrolize({
  weight: '400',
  subsets: ['latin'],
  variable: '--font-electrolize',
  display: 'swap',
});

export const metadata: Metadata = {
  title: 'ZTL数智化作战中心',
  description: 'ZTL Digital Intelligence Operations Center - Cyberpunk Multi-Agent Orchestration Platform',
  keywords: ['AI', 'Multi-Agent', 'Restaurant Industry', 'Digital Transformation', 'Claude'],
  authors: [{ name: 'ZTL Team' }],
};

export const viewport = {
  width: 'device-width',
  initialScale: 1,
  themeColor: '#0a0a0f',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN" className={`${orbitron.variable} ${electrolize.variable}`}>
      <head>
        <link rel="icon" href="/favicon.ico" />
      </head>
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
