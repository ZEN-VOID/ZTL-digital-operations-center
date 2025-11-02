import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'neon-pink': '#ff00ff',
        'neon-cyan': '#00ffff',
        'neon-purple': '#b000ff',
        'neon-green': '#00ff00',
        'cyber-bg-primary': '#0a0a0f',
        'cyber-bg-secondary': '#0f0f23',
        'cyber-bg-tertiary': '#1a0a2e',
        'text-primary': '#a8a8ff',
        'text-secondary': '#6868a0',
      },
      fontFamily: {
        orbitron: ['var(--font-orbitron)'],
        electrolize: ['var(--font-electrolize)'],
      },
      animation: {
        'grid-move': 'grid-move 20s linear infinite',
        'holographic-shine': 'holographic-shine 3s linear infinite',
        'neon-pulse': 'neon-pulse 2s ease-in-out infinite',
        'message-appear': 'message-appear 0.3s ease-out',
        'streaming-pulse': 'streaming-pulse 1.4s ease-in-out infinite',
        'float': 'float 10s ease-in-out infinite',
        'toast-progress': 'toast-progress linear forwards',
        'typing-dot': 'typing-dot 1.4s ease-in-out infinite',
        'typing-pulse': 'typing-pulse 1s ease-in-out infinite',
        'typing-wave': 'typing-wave 1.2s ease-in-out infinite',
        'slide-down': 'slide-down 0.3s ease-out',
        'slide-up': 'slide-up 0.2s ease-out',
        'fade-in': 'fade-in 0.3s ease-out',
      },
      keyframes: {
        'grid-move': {
          '0%': { transform: 'translateY(0)' },
          '100%': { transform: 'translateY(50px)' },
        },
        'holographic-shine': {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(100%)' },
        },
        'neon-pulse': {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.5' },
        },
        'message-appear': {
          '0%': {
            opacity: '0',
            transform: 'translateY(20px)',
          },
          '100%': {
            opacity: '1',
            transform: 'translateY(0)',
          },
        },
        'streaming-pulse': {
          '0%, 80%, 100%': {
            opacity: '0.3',
            transform: 'scale(0.8)',
          },
          '40%': {
            opacity: '1',
            transform: 'scale(1.2)',
          },
        },
        'float': {
          '0%, 100%': {
            transform: 'translateY(0px) translateX(0px)',
          },
          '25%': {
            transform: 'translateY(-20px) translateX(10px)',
          },
          '50%': {
            transform: 'translateY(-10px) translateX(-10px)',
          },
          '75%': {
            transform: 'translateY(-15px) translateX(5px)',
          },
        },
        'toast-progress': {
          from: {
            transform: 'translateX(0)',
          },
          to: {
            transform: 'translateX(-100%)',
          },
        },
        'typing-dot': {
          '0%, 60%, 100%': {
            opacity: '0.3',
            transform: 'translateY(0)',
          },
          '30%': {
            opacity: '1',
            transform: 'translateY(-10px)',
          },
        },
        'typing-pulse': {
          '0%, 100%': {
            height: '1rem',
            opacity: '0.3',
          },
          '50%': {
            height: '1.5rem',
            opacity: '1',
          },
        },
        'typing-wave': {
          '0%, 100%': {
            height: '0.5rem',
          },
          '50%': {
            height: '1rem',
          },
        },
        'slide-down': {
          '0%': {
            opacity: '0',
            transform: 'translateY(-10px)',
          },
          '100%': {
            opacity: '1',
            transform: 'translateY(0)',
          },
        },
        'slide-up': {
          '0%': {
            opacity: '0',
            transform: 'translateY(10px)',
          },
          '100%': {
            opacity: '1',
            transform: 'translateY(0)',
          },
        },
        'fade-in': {
          '0%': {
            opacity: '0',
          },
          '100%': {
            opacity: '1',
          },
        },
      },
    },
  },
  plugins: [],
};

export default config;
