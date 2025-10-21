---
name: Glassmorphism Design
description: Create glassmorphism UI with frosted glass surfaces, transparency, layering, and background blur. Use when designing modern SaaS platforms, card layouts, or when user mentions glassmorphism, frosted glass, or translucent UI. Pure CSS, cross-browser compatible.
---

# Glassmorphism Design

## Quick Start

### Basic Glassmorphism Card

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Glassmorphism Card</title>
    <style>
        body {
            margin: 0;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #8EC5FC 0%, #E0C3FC 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        .glass {
            /* Glassmorphism effect */
            background: rgba(255, 255, 255, 0.25);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);

            /* Border highlight */
            border: 1px solid rgba(255, 255, 255, 0.18);
            border-radius: 16px;

            /* Shadow for depth */
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);

            /* Layout */
            padding: 48px;
            max-width: 400px;
            color: #333;
        }

        .glass h2 {
            margin: 0 0 16px 0;
            font-size: 32px;
            font-weight: 700;
            color: #1a1a1a;
        }

        .glass p {
            margin: 0;
            line-height: 1.6;
            color: #444;
        }
    </style>
</head>
<body>
    <div class="glass">
        <h2>Glassmorphism</h2>
        <p>Modern frosted glass UI with transparency and layered depth.</p>
    </div>
</body>
</html>
```

## Core CSS Formula

### Standard Glassmorphism

```css
.glassmorphism {
    /* Semi-transparent background */
    background: rgba(255, 255, 255, 0.25);

    /* Backdrop blur */
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);

    /* Subtle border */
    border: 1px solid rgba(255, 255, 255, 0.18);

    /* Rounded corners */
    border-radius: 16px;

    /* Layered shadow */
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
}
```

## Style Variants

### Light Glassmorphism (Default)

```css
.glass-light {
    background: rgba(255, 255, 255, 0.25);
    border: 1px solid rgba(255, 255, 255, 0.18);
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    color: #333;
}
```

### Dark Glassmorphism

```css
.glass-dark {
    background: rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
    color: white;
}
```

### Colored Glassmorphism

```css
.glass-blue {
    background: rgba(100, 200, 255, 0.2);
    border: 1px solid rgba(100, 200, 255, 0.3);
    box-shadow: 0 8px 32px 0 rgba(100, 200, 255, 0.4);
}

.glass-purple {
    background: rgba(150, 100, 255, 0.2);
    border: 1px solid rgba(150, 100, 255, 0.3);
    box-shadow: 0 8px 32px 0 rgba(150, 100, 255, 0.4);
}
```

## Transparency Levels

| Level | Alpha | Use Case |
|-------|-------|----------|
| **Subtle** | `0.1 - 0.15` | Lightweight overlays |
| **Standard** | `0.2 - 0.25` | Cards, panels |
| **Medium** | `0.3 - 0.35` | Modals, dialogs |
| **Strong** | `0.4 - 0.5` | Navigation bars |

## Blur Intensity Guide

```css
/* Minimal blur (4-6px) */
backdrop-filter: blur(5px);

/* Standard blur (8-12px) - Recommended */
backdrop-filter: blur(10px);

/* Heavy blur (16-24px) */
backdrop-filter: blur(20px);
```

## Layering Techniques

### Multiple Glass Layers

```css
/* Background layer */
.glass-layer-1 {
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(8px);
}

/* Middle layer */
.glass-layer-2 {
    background: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(10px);
}

/* Foreground layer */
.glass-layer-3 {
    background: rgba(255, 255, 255, 0.25);
    backdrop-filter: blur(12px);
}
```

## Templates

- [templates/complete.html](templates/complete.html) - Full SaaS dashboard with glassmorphism
- [templates/components.html](templates/components.html) - Reusable glass components
- [templates/minimal.html](templates/minimal.html) - Simple glass card

## Browser Support

| Browser | Version | Support |
|---------|---------|---------|
| Chrome | 76+ | ✅ Full |
| Safari | 14+ | ✅ Full |
| Firefox | 103+ | ✅ Full |
| Edge | 79+ | ✅ Full |
| iOS Safari | 14+ | ✅ Full |

**Fallback:**
```css
@supports not (backdrop-filter: blur(10px)) {
    .glass {
        background: rgba(255, 255, 255, 0.85);
    }
}
```

## Accessibility

### Contrast Requirements

Ensure text meets WCAG 2.1 AA standards:
- Normal text: 4.5:1 contrast ratio
- Large text (18pt+): 3:1 contrast ratio

```css
/* Good contrast on light glass */
.glass-light {
    color: #1a1a1a; /* High contrast */
}

/* Good contrast on dark glass */
.glass-dark {
    color: #ffffff; /* High contrast */
}
```

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
    .glass {
        backdrop-filter: none;
        background: rgba(255, 255, 255, 0.9);
    }
}
```

## Performance Tips

1. **Limit blur layers**: Max 3-4 overlapping elements
2. **Static positioning**: Avoid animating backdrop-filter
3. **Use will-change**: Only when necessary
4. **Test on mobile**: Android performance varies
5. **Optimize images**: Blur effect is GPU-intensive

## Common Use Cases

- SaaS platform dashboards
- Card-based layouts
- Pricing tables
- Profile cards
- Navigation menus
- Modals and overlays
- Form containers

## Design Principles

1. **Contrast**: Ensure readability with proper text colors
2. **Layering**: Stack elements from light to dark
3. **Spacing**: Use generous padding (32px+)
4. **Simplicity**: Limit to 2-3 glass layers
5. **Background**: Use colorful gradients for best effect

## Advanced Techniques

For advanced implementations:
- [reference.md](reference.md) - Design theory and best practices
- [examples/](examples/) - Industry-specific examples

## Related Skills

- For iOS variant: See `../ios-liquid-glass/SKILL.md`
- For dark themes: See `../dark-mode-premium/SKILL.md`
