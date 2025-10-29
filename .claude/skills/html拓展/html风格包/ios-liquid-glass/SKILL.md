---
name: iOS Liquid Glass Design
description: Create iOS-style liquid glass UI components with frosted glass effects, backdrop blur, transparency, and depth layering. Use when designing modern modals, navigation bars, cards, or when user mentions iOS design, liquid glass, frosted glass, or glassmorphism effects. Pure CSS implementation, no dependencies.
---

# iOS Liquid Glass Design

## Quick Start

### Basic Liquid Glass Card

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>iOS Liquid Glass Card</title>
    <style>
        body {
            margin: 0;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }

        .glass-card {
            /* Liquid glass effect */
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px) saturate(180%);
            -webkit-backdrop-filter: blur(20px) saturate(180%);

            /* Border and shadow */
            border: 1px solid rgba(255, 255, 255, 0.18);
            border-radius: 20px;
            box-shadow:
                0 8px 32px 0 rgba(31, 38, 135, 0.37),
                inset 0 1px 0 0 rgba(255, 255, 255, 0.5);

            /* Layout */
            padding: 40px;
            max-width: 400px;
            color: white;
        }

        .glass-card h2 {
            margin: 0 0 16px 0;
            font-size: 28px;
            font-weight: 600;
        }

        .glass-card p {
            margin: 0;
            opacity: 0.9;
            line-height: 1.6;
        }
    </style>
</head>
<body>
    <div class="glass-card">
        <h2>Liquid Glass</h2>
        <p>iOS-inspired frosted glass effect with backdrop blur and transparency.</p>
    </div>
</body>
</html>
```

## Core CSS Properties

### Liquid Glass Effect

```css
.liquid-glass {
    /* Background with transparency */
    background: rgba(255, 255, 255, 0.1);

    /* Frosted glass blur effect */
    backdrop-filter: blur(20px) saturate(180%);
    -webkit-backdrop-filter: blur(20px) saturate(180%);

    /* Subtle border highlight */
    border: 1px solid rgba(255, 255, 255, 0.18);

    /* Rounded corners */
    border-radius: 20px;

    /* Depth shadow */
    box-shadow:
        0 8px 32px 0 rgba(31, 38, 135, 0.37),
        inset 0 1px 0 0 rgba(255, 255, 255, 0.5);
}
```

## Customization Options

### Transparency Levels

| Level | Use Case | Background Alpha |
|-------|----------|------------------|
| **Ultra Light** | Overlays | `rgba(255, 255, 255, 0.05)` |
| **Light** | Cards | `rgba(255, 255, 255, 0.1)` |
| **Medium** | Modals | `rgba(255, 255, 255, 0.15)` |
| **Strong** | Navigation | `rgba(255, 255, 255, 0.25)` |

### Blur Intensity

```css
/* Subtle blur (5-10px) - Lightweight effect */
backdrop-filter: blur(8px);

/* Standard blur (15-25px) - iOS default */
backdrop-filter: blur(20px) saturate(180%);

/* Heavy blur (30-40px) - Strong frosted glass */
backdrop-filter: blur(35px) saturate(200%);
```

### Color Variations

```css
/* Light mode glass */
.glass-light {
    background: rgba(255, 255, 255, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.3);
    color: #333;
}

/* Dark mode glass */
.glass-dark {
    background: rgba(0, 0, 0, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: white;
}

/* Tinted glass (colored) */
.glass-tinted {
    background: rgba(102, 126, 234, 0.15);
    border: 1px solid rgba(102, 126, 234, 0.3);
}
```

## Templates

### Complete Page
See [templates/complete.html](templates/complete.html) - Full landing page with multiple glass components

### Component Library
See [templates/components.html](templates/components.html) - Reusable glass UI components

### Minimal Example
See [templates/minimal.html](templates/minimal.html) - Simplest implementation

## Browser Compatibility

| Browser | Support | Notes |
|---------|---------|-------|
| Safari 14+ | ✅ Full | Best support, native `-webkit-backdrop-filter` |
| Chrome 76+ | ✅ Full | Requires both `backdrop-filter` and `-webkit-` prefix |
| Edge 79+ | ✅ Full | Chromium-based, full support |
| Firefox 103+ | ✅ Full | Added in July 2022 |
| iOS Safari | ✅ Full | Excellent performance |

**Fallback Strategy:**
```css
.glass-card {
    /* Fallback for unsupported browsers */
    background: rgba(255, 255, 255, 0.25);
}

@supports (backdrop-filter: blur(20px)) {
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px) saturate(180%);
    }
}
```

## Performance Best Practices

1. **Limit Blur Layers**: Use max 3-4 overlapping glass elements
2. **Static Backgrounds**: Avoid animating backdrop-filter
3. **GPU Acceleration**: Add `transform: translateZ(0)` if needed
4. **Reduce Repaints**: Use `will-change: backdrop-filter` sparingly
5. **Test on Mobile**: iOS handles blur better than Android

## Accessibility

- Ensure text contrast ratio ≥ 4.5:1 (WCAG AA)
- Provide alternative solid background for reduced motion:

```css
@media (prefers-reduced-motion: reduce) {
    .glass-card {
        backdrop-filter: none;
        background: rgba(255, 255, 255, 0.9);
    }
}
```

## Common Use Cases

- iOS-style navigation bars
- Modal dialogs and overlays
- Card components
- Sidebar panels
- Notification toasts
- Bottom sheets

## Advanced Features

For advanced customization and component generation, see:
- [reference.md](reference.md) - Design principles and advanced techniques
- [scripts/generate.py](scripts/generate.py) - Python generator for custom components

## Related Skills

- For glassmorphism variant: See `../glassmorphism/SKILL.md`
- For dark themes: See `../dark-mode-premium/SKILL.md`

## Examples Gallery

All examples include:
- ✅ Responsive design
- ✅ Light/dark mode support
- ✅ Accessibility compliant
- ✅ Browser fallbacks
