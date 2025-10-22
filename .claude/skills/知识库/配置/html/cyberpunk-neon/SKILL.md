---
name: Cyberpunk Neon Design
description: Create cyberpunk-inspired UI with neon colors (pink/purple/cyan), dark backgrounds, glowing effects, retro-futuristic animations, and metallic accents. Use when designing sci-fi games, tech websites, or when user mentions cyberpunk, neon, synthwave, or retro-futuristic design. High-impact visual style.
---

# Cyberpunk Neon Design

## Quick Start

### Basic Neon Card

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cyberpunk Neon</title>
    <style>
        body {
            margin: 0;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #0a0a0f;
            font-family: 'Orbitron', 'Courier New', monospace;
            overflow: hidden;
        }

        /* Animated background grid */
        body::before {
            content: '';
            position: absolute;
            width: 100%;
            height: 100%;
            background:
                linear-gradient(0deg, transparent 24%, rgba(255, 0, 255, 0.05) 25%, rgba(255, 0, 255, 0.05) 26%, transparent 27%, transparent 74%, rgba(255, 0, 255, 0.05) 75%, rgba(255, 0, 255, 0.05) 76%, transparent 77%, transparent),
                linear-gradient(90deg, transparent 24%, rgba(255, 0, 255, 0.05) 25%, rgba(255, 0, 255, 0.05) 26%, transparent 27%, transparent 74%, rgba(255, 0, 255, 0.05) 75%, rgba(255, 0, 255, 0.05) 76%, transparent 77%, transparent);
            background-size: 50px 50px;
            animation: grid-move 20s linear infinite;
            z-index: 0;
        }

        @keyframes grid-move {
            0% { transform: translateY(0); }
            100% { transform: translateY(50px); }
        }

        .cyber-card {
            /* Dark background with gradient */
            background: linear-gradient(135deg, #0f0f23 0%, #1a0a2e 100%);

            /* Neon border */
            border: 2px solid #ff00ff;
            border-radius: 8px;

            /* Neon glow effect */
            box-shadow:
                0 0 10px #ff00ff,
                0 0 20px rgba(255, 0, 255, 0.5),
                0 0 40px rgba(255, 0, 255, 0.3),
                inset 0 0 20px rgba(255, 0, 255, 0.1);

            /* Layout */
            padding: 48px;
            max-width: 500px;
            position: relative;
            z-index: 1;
        }

        .cyber-card h2 {
            margin: 0 0 16px 0;
            font-size: 36px;
            font-weight: 700;
            color: #00ffff;
            text-shadow:
                0 0 10px #00ffff,
                0 0 20px rgba(0, 255, 255, 0.5);
            text-transform: uppercase;
            letter-spacing: 3px;
        }

        .cyber-card p {
            margin: 0;
            line-height: 1.6;
            color: #a8a8ff;
        }

        .neon-button {
            background: transparent;
            color: #ff00ff;
            border: 2px solid #ff00ff;
            border-radius: 4px;
            padding: 14px 32px;
            margin-top: 24px;
            font-size: 16px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
            cursor: pointer;
            position: relative;
            overflow: hidden;
            transition: all 0.3s;
        }

        .neon-button::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            background: rgba(255, 0, 255, 0.3);
            border-radius: 50%;
            transform: translate(-50%, -50%);
            transition: width 0.5s, height 0.5s;
        }

        .neon-button:hover {
            color: #fff;
            box-shadow:
                0 0 10px #ff00ff,
                0 0 20px rgba(255, 0, 255, 0.5);
        }

        .neon-button:hover::before {
            width: 300px;
            height: 300px;
        }
    </style>
</head>
<body>
    <div class="cyber-card">
        <h2>Cyberpunk</h2>
        <p>Neon colors, dark backgrounds, and retro-futuristic glowing effects.</p>
        <button class="neon-button">Enter</button>
    </div>
</body>
</html>
```

## Color Palette

### Neon Colors

```css
:root {
    /* Primary neon colors */
    --neon-pink: #ff00ff;
    --neon-cyan: #00ffff;
    --neon-purple: #b000ff;
    --neon-yellow: #ffff00;
    --neon-green: #00ff00;

    /* Dark backgrounds */
    --cyber-bg-primary: #0a0a0f;
    --cyber-bg-secondary: #0f0f23;
    --cyber-bg-tertiary: #1a0a2e;

    /* Metallic accents */
    --cyber-metal-light: #8b9dc3;
    --cyber-metal-dark: #3d5a80;
}
```

### Gradient Combinations

```css
/* Pink-purple gradient */
.cyber-gradient-pink {
    background: linear-gradient(135deg, #ff00ff 0%, #b000ff 100%);
}

/* Cyan-blue gradient */
.cyber-gradient-cyan {
    background: linear-gradient(135deg, #00ffff 0%, #0080ff 100%);
}

/* Sunset gradient */
.cyber-gradient-sunset {
    background: linear-gradient(135deg, #ff00ff 0%, #ff8800 50%, #ffff00 100%);
}
```

## Neon Glow Effects

### Text Glow

```css
.neon-text {
    color: #00ffff;
    text-shadow:
        0 0 5px #00ffff,
        0 0 10px #00ffff,
        0 0 20px #00ffff,
        0 0 40px rgba(0, 255, 255, 0.5);
}

.neon-text-pink {
    color: #ff00ff;
    text-shadow:
        0 0 5px #ff00ff,
        0 0 10px #ff00ff,
        0 0 20px #ff00ff,
        0 0 40px rgba(255, 0, 255, 0.5);
}
```

### Box Glow

```css
.neon-glow {
    border: 2px solid #ff00ff;
    box-shadow:
        0 0 5px #ff00ff,
        0 0 10px #ff00ff,
        0 0 20px rgba(255, 0, 255, 0.5),
        0 0 40px rgba(255, 0, 255, 0.3),
        inset 0 0 10px rgba(255, 0, 255, 0.1);
}
```

### Pulsing Glow Animation

```css
@keyframes neon-pulse {
    0%, 100% {
        box-shadow:
            0 0 5px #ff00ff,
            0 0 10px #ff00ff,
            0 0 20px rgba(255, 0, 255, 0.5);
    }
    50% {
        box-shadow:
            0 0 10px #ff00ff,
            0 0 20px #ff00ff,
            0 0 40px rgba(255, 0, 255, 0.8);
    }
}

.neon-pulse {
    animation: neon-pulse 2s ease-in-out infinite;
}
```

## Background Effects

### Cyberpunk Grid

```css
.cyber-grid {
    background:
        linear-gradient(0deg, transparent 24%, rgba(255, 0, 255, 0.05) 25%, rgba(255, 0, 255, 0.05) 26%, transparent 27%, transparent 74%, rgba(255, 0, 255, 0.05) 75%, rgba(255, 0, 255, 0.05) 76%, transparent 77%, transparent),
        linear-gradient(90deg, transparent 24%, rgba(255, 0, 255, 0.05) 25%, rgba(255, 0, 255, 0.05) 26%, transparent 27%, transparent 74%, rgba(255, 0, 255, 0.05) 75%, rgba(255, 0, 255, 0.05) 76%, transparent 77%, transparent);
    background-size: 50px 50px;
    background-color: #0a0a0f;
}
```

### Scanline Effect

```css
.scanlines::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: repeating-linear-gradient(
        0deg,
        rgba(0, 0, 0, 0.15),
        rgba(0, 0, 0, 0.15) 1px,
        transparent 1px,
        transparent 2px
    );
    pointer-events: none;
    animation: scanline 8s linear infinite;
}

@keyframes scanline {
    0% { transform: translateY(0); }
    100% { transform: translateY(100%); }
}
```

### Glitch Effect

```css
@keyframes glitch {
    0% {
        clip-path: inset(40% 0 61% 0);
        transform: translate(0);
    }
    20% {
        clip-path: inset(92% 0 1% 0);
        transform: translate(-5px, 5px);
    }
    40% {
        clip-path: inset(43% 0 1% 0);
        transform: translate(5px, -5px);
    }
    60% {
        clip-path: inset(25% 0 58% 0);
        transform: translate(-5px, 0);
    }
    80% {
        clip-path: inset(54% 0 7% 0);
        transform: translate(5px, 5px);
    }
    100% {
        clip-path: inset(58% 0 43% 0);
        transform: translate(0);
    }
}

.glitch-effect::before,
.glitch-effect::after {
    content: attr(data-text);
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
}

.glitch-effect::before {
    color: #ff00ff;
    animation: glitch 0.3s infinite;
}

.glitch-effect::after {
    color: #00ffff;
    animation: glitch 0.3s infinite reverse;
}
```

## Interactive Components

### Neon Button

```css
.neon-button {
    background: transparent;
    color: #ff00ff;
    border: 2px solid #ff00ff;
    border-radius: 4px;
    padding: 14px 32px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: all 0.3s;
}

.neon-button::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    background: rgba(255, 0, 255, 0.3);
    border-radius: 50%;
    transform: translate(-50%, -50%);
    transition: width 0.5s, height 0.5s;
}

.neon-button:hover {
    color: #fff;
    box-shadow:
        0 0 10px #ff00ff,
        0 0 20px rgba(255, 0, 255, 0.5),
        0 0 40px rgba(255, 0, 255, 0.3);
}

.neon-button:hover::before {
    width: 300px;
    height: 300px;
}
```

### Holographic Card

```css
.holographic-card {
    background: linear-gradient(135deg, #0f0f23 0%, #1a0a2e 100%);
    border: 1px solid rgba(255, 0, 255, 0.3);
    border-radius: 8px;
    padding: 32px;
    position: relative;
    overflow: hidden;
}

.holographic-card::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(
        45deg,
        transparent,
        rgba(255, 0, 255, 0.1),
        transparent
    );
    transform: rotate(45deg);
    animation: holographic-shine 3s linear infinite;
}

@keyframes holographic-shine {
    0% { transform: translateX(-100%) rotate(45deg); }
    100% { transform: translateX(100%) rotate(45deg); }
}
```

## Typography

### Cyberpunk Fonts

```html
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Electrolize&display=swap" rel="stylesheet">
```

```css
.cyber-heading {
    font-family: 'Orbitron', sans-serif;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 3px;
    color: #00ffff;
    text-shadow: 0 0 10px #00ffff;
}

.cyber-body {
    font-family: 'Electrolize', sans-serif;
    font-weight: 400;
    color: #a8a8ff;
}

.cyber-code {
    font-family: 'Courier New', monospace;
    color: #00ff00;
    background: rgba(0, 255, 0, 0.1);
    padding: 2px 6px;
    border-radius: 3px;
}
```

## Templates

- [templates/complete.html](templates/complete.html) - Full cyberpunk landing page
- [templates/dashboard.html](templates/dashboard.html) - Neon dashboard interface
- [templates/game-ui.html](templates/game-ui.html) - Game-style UI elements

## Browser Support

| Feature | Support |
|---------|---------|
| Box-shadow glow | ✅ All browsers |
| Text-shadow glow | ✅ All browsers |
| CSS animations | ✅ All modern browsers |
| Clip-path (glitch) | ✅ Chrome 55+, Safari 9.1+ |

## Performance Considerations

1. **Limit animations**: Use `will-change` sparingly
2. **Reduce glow layers**: Max 3-4 shadow layers
3. **GPU acceleration**: Use `transform: translateZ(0)` for heavy effects
4. **Lazy load**: Consider loading effects on scroll
5. **Reduce motion**: Respect user preferences

```css
@media (prefers-reduced-motion: reduce) {
    * {
        animation: none !important;
        transition: none !important;
    }
}
```

## Accessibility

### Contrast Issues

Neon colors can have poor contrast. Ensure:

```css
/* Use darker neon for text on dark backgrounds */
.accessible-neon {
    color: #ff66ff; /* Lighter pink for better contrast */
}

/* Provide alternative high-contrast mode */
@media (prefers-contrast: high) {
    .neon-text {
        color: #ffffff;
        text-shadow: none;
    }
}
```

### Focus States

```css
.neon-button:focus-visible {
    outline: 2px solid #00ffff;
    outline-offset: 4px;
}
```

## Common Use Cases

- Sci-fi game interfaces
- Tech startup websites
- Music and entertainment platforms
- Virtual event pages
- Futuristic product launches
- Streaming overlays
- Cyber security platforms

## Related Skills

- For dark themes: See `../dark-mode-premium/SKILL.md`
- For glass effects: See `../ios-liquid-glass/SKILL.md`
