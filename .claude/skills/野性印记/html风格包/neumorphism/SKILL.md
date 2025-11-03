---
name: Neumorphism Design
description: Create neumorphism (soft UI) with realistic 3D embossed elements, dual shadows, and tactile interfaces. Use when designing minimalist tools, health apps, buttons, or when user mentions neumorphism, soft UI, or skeuomorphic design. Improved accessibility with better contrast.
---

# Neumorphism Design

## Quick Start

### Basic Neumorphic Card

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Neumorphism Card</title>
    <style>
        body {
            margin: 0;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #e0e5ec;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        .neuro-card {
            /* Neumorphic effect - dual shadows */
            background: #e0e5ec;
            box-shadow:
                9px 9px 16px rgba(163, 177, 198, 0.6),
                -9px -9px 16px rgba(255, 255, 255, 0.5);

            /* Layout */
            border-radius: 20px;
            padding: 48px;
            max-width: 400px;
            color: #333;
        }

        .neuro-card h2 {
            margin: 0 0 16px 0;
            font-size: 32px;
            font-weight: 700;
            color: #2c3e50;
        }

        .neuro-card p {
            margin: 0;
            line-height: 1.6;
            color: #5a6c7d;
        }

        /* Neumorphic button */
        .neuro-button {
            background: #e0e5ec;
            box-shadow:
                6px 6px 12px rgba(163, 177, 198, 0.6),
                -6px -6px 12px rgba(255, 255, 255, 0.5);
            border: none;
            border-radius: 12px;
            padding: 14px 32px;
            margin-top: 24px;
            color: #2c3e50;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .neuro-button:active {
            /* Pressed state - inset shadows */
            box-shadow:
                inset 4px 4px 8px rgba(163, 177, 198, 0.6),
                inset -4px -4px 8px rgba(255, 255, 255, 0.5);
        }
    </style>
</head>
<body>
    <div class="neuro-card">
        <h2>Neumorphism</h2>
        <p>Soft UI with realistic 3D embossed elements and dual shadow technique.</p>
        <button class="neuro-button">Click Me</button>
    </div>
</body>
</html>
```

## Core CSS Formula

### Standard Neumorphism

```css
.neumorphic {
    /* Same background as container */
    background: #e0e5ec;

    /* Dual shadows: dark (bottom-right) + light (top-left) */
    box-shadow:
        9px 9px 16px rgba(163, 177, 198, 0.6),  /* Dark shadow */
        -9px -9px 16px rgba(255, 255, 255, 0.5); /* Light highlight */

    /* Soft rounded corners */
    border-radius: 20px;
}
```

## Element States

### Default (Raised)

```css
.neuro-raised {
    box-shadow:
        9px 9px 16px rgba(163, 177, 198, 0.6),
        -9px -9px 16px rgba(255, 255, 255, 0.5);
}
```

### Pressed (Inset)

```css
.neuro-pressed {
    box-shadow:
        inset 4px 4px 8px rgba(163, 177, 198, 0.6),
        inset -4px -4px 8px rgba(255, 255, 255, 0.5);
}
```

### Flat (Subtle)

```css
.neuro-flat {
    box-shadow:
        5px 5px 10px rgba(163, 177, 198, 0.4),
        -5px -5px 10px rgba(255, 255, 255, 0.4);
}
```

## Color Schemes

### Light Mode (Default)

```css
:root {
    --neuro-bg: #e0e5ec;
    --neuro-shadow-dark: rgba(163, 177, 198, 0.6);
    --neuro-shadow-light: rgba(255, 255, 255, 0.5);
    --neuro-text: #2c3e50;
}

.neuro-light {
    background: var(--neuro-bg);
    color: var(--neuro-text);
    box-shadow:
        9px 9px 16px var(--neuro-shadow-dark),
        -9px -9px 16px var(--neuro-shadow-light);
}
```

### Dark Mode

```css
:root {
    --neuro-dark-bg: #2c3e50;
    --neuro-dark-shadow: rgba(0, 0, 0, 0.5);
    --neuro-dark-highlight: rgba(255, 255, 255, 0.05);
    --neuro-dark-text: #ecf0f1;
}

.neuro-dark {
    background: var(--neuro-dark-bg);
    color: var(--neuro-dark-text);
    box-shadow:
        9px 9px 16px var(--neuro-dark-shadow),
        -9px -9px 16px var(--neuro-dark-highlight);
}
```

### Colored Variants

```css
/* Blue neumorphism */
.neuro-blue {
    background: #d1dbe8;
    box-shadow:
        9px 9px 16px rgba(130, 150, 175, 0.6),
        -9px -9px 16px rgba(255, 255, 255, 0.5);
}

/* Green neumorphism */
.neuro-green {
    background: #d8e5d0;
    box-shadow:
        9px 9px 16px rgba(160, 180, 150, 0.6),
        -9px -9px 16px rgba(255, 255, 255, 0.5);
}
```

## Interactive Components

### Button

```css
.neuro-button {
    background: #e0e5ec;
    box-shadow:
        6px 6px 12px rgba(163, 177, 198, 0.6),
        -6px -6px 12px rgba(255, 255, 255, 0.5);
    border: none;
    border-radius: 12px;
    padding: 14px 32px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.neuro-button:hover {
    box-shadow:
        8px 8px 14px rgba(163, 177, 198, 0.6),
        -8px -8px 14px rgba(255, 255, 255, 0.5);
}

.neuro-button:active {
    box-shadow:
        inset 4px 4px 8px rgba(163, 177, 198, 0.6),
        inset -4px -4px 8px rgba(255, 255, 255, 0.5);
}
```

### Input Field

```css
.neuro-input {
    background: #e0e5ec;
    box-shadow:
        inset 4px 4px 8px rgba(163, 177, 198, 0.6),
        inset -4px -4px 8px rgba(255, 255, 255, 0.5);
    border: none;
    border-radius: 12px;
    padding: 14px 20px;
    font-size: 16px;
    color: #2c3e50;
}

.neuro-input:focus {
    outline: none;
    box-shadow:
        inset 5px 5px 10px rgba(163, 177, 198, 0.7),
        inset -5px -5px 10px rgba(255, 255, 255, 0.6);
}
```

### Toggle Switch

```css
.neuro-toggle {
    width: 60px;
    height: 30px;
    background: #e0e5ec;
    box-shadow:
        inset 4px 4px 8px rgba(163, 177, 198, 0.6),
        inset -4px -4px 8px rgba(255, 255, 255, 0.5);
    border-radius: 15px;
    position: relative;
    cursor: pointer;
}

.neuro-toggle::after {
    content: '';
    width: 24px;
    height: 24px;
    background: #e0e5ec;
    box-shadow:
        3px 3px 6px rgba(163, 177, 198, 0.6),
        -3px -3px 6px rgba(255, 255, 255, 0.5);
    border-radius: 50%;
    position: absolute;
    top: 3px;
    left: 3px;
    transition: transform 0.3s;
}

.neuro-toggle.active::after {
    transform: translateX(30px);
}
```

## Templates

- [templates/complete.html](templates/complete.html) - Full app interface
- [templates/components.html](templates/components.html) - Component library
- [templates/minimal.html](templates/minimal.html) - Basic implementation

## Accessibility Improvements

### Enhanced Contrast

```css
/* Improved text contrast */
.neuro-accessible {
    background: #e0e5ec;
    color: #1a1a1a; /* WCAG AA compliant */
}

/* Interactive states with visible indicators */
.neuro-button:focus {
    outline: 2px solid #3498db;
    outline-offset: 2px;
}
```

### Dark Mode for Reduced Eye Strain

```css
@media (prefers-color-scheme: dark) {
    .neuro-card {
        background: #2c3e50;
        color: #ecf0f1;
        box-shadow:
            9px 9px 16px rgba(0, 0, 0, 0.5),
            -9px -9px 16px rgba(255, 255, 255, 0.05);
    }
}
```

## Browser Support

| Browser | Support | Notes |
|---------|---------|-------|
| All modern browsers | ✅ Full | Uses standard CSS box-shadow |
| IE11 | ✅ Partial | Works but no CSS variables support |

## Performance Tips

1. **Limit shadows**: Use max 2-3 shadow layers
2. **Static design**: Avoid animating box-shadow
3. **Use GPU**: Add `transform: translateZ(0)` if needed
4. **Optimize renders**: Minimize shadow blur radius

## Common Use Cases

- Minimalist productivity tools
- Health and wellness apps
- Music players
- Smart home controls
- Calculator interfaces
- Settings panels
- Form inputs

## Design Guidelines

1. **Background unity**: Element background must match container
2. **Consistent spacing**: Use 8px grid system
3. **Subtle depth**: Keep shadows soft and realistic
4. **Limit colors**: Use monochromatic or analogous colors
5. **Generous padding**: Minimum 24px for cards

## Related Skills

- For glass effects: See `../glassmorphism/SKILL.md`
- For dark themes: See `../dark-mode-premium/SKILL.md`
