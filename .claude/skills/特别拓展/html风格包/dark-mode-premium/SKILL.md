---
name: Premium Dark Mode Design
description: Create sophisticated dark mode interfaces with refined color palettes, subtle gradients, strategic accents, and reduced eye strain. Use when designing modern apps, dashboards, or when user mentions dark mode, dark theme, or night mode. Includes automatic system preference detection.
---

# Premium Dark Mode Design

## Quick Start

### Basic Dark Mode Page

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Premium Dark Mode</title>
    <style>
        :root {
            /* Dark mode color palette */
            --dark-bg-primary: #0f0f0f;
            --dark-bg-secondary: #1a1a1a;
            --dark-bg-tertiary: #242424;
            --dark-border: #333;
            --dark-text-primary: #e8e8e8;
            --dark-text-secondary: #a8a8a8;
            --dark-accent: #3b82f6;
        }

        body {
            margin: 0;
            min-height: 100vh;
            background: var(--dark-bg-primary);
            color: var(--dark-text-primary);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }

        .dark-card {
            /* Layered dark background */
            background: var(--dark-bg-secondary);

            /* Subtle border */
            border: 1px solid var(--dark-border);
            border-radius: 16px;

            /* Soft shadow */
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);

            /* Layout */
            padding: 48px;
            max-width: 600px;
            margin: 80px auto;
        }

        .dark-card h2 {
            margin: 0 0 16px 0;
            font-size: 32px;
            font-weight: 700;
            color: var(--dark-text-primary);
        }

        .dark-card p {
            margin: 0;
            line-height: 1.6;
            color: var(--dark-text-secondary);
        }

        .accent-button {
            background: var(--dark-accent);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 14px 28px;
            margin-top: 24px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }

        .accent-button:hover {
            background: #2563eb;
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(59, 130, 246, 0.3);
        }
    </style>
</head>
<body>
    <div class="dark-card">
        <h2>Premium Dark Mode</h2>
        <p>Sophisticated dark interface with refined colors, subtle gradients, and strategic accent colors.</p>
        <button class="accent-button">Get Started</button>
    </div>
</body>
</html>
```

## Color System

### Core Dark Palette

```css
:root {
    /* Backgrounds - progressively lighter */
    --dark-bg-primary: #0f0f0f;     /* Main background */
    --dark-bg-secondary: #1a1a1a;   /* Cards, panels */
    --dark-bg-tertiary: #242424;    /* Elevated elements */
    --dark-bg-hover: #2a2a2a;       /* Hover states */

    /* Borders and dividers */
    --dark-border: #333333;
    --dark-border-light: #404040;

    /* Text hierarchy */
    --dark-text-primary: #e8e8e8;   /* Headings */
    --dark-text-secondary: #a8a8a8; /* Body text */
    --dark-text-tertiary: #707070;  /* Muted text */

    /* Accent colors */
    --dark-accent-blue: #3b82f6;
    --dark-accent-purple: #8b5cf6;
    --dark-accent-green: #10b981;
    --dark-accent-red: #ef4444;
}
```

### Semantic Colors

```css
/* Success state */
--dark-success-bg: rgba(16, 185, 129, 0.1);
--dark-success-border: rgba(16, 185, 129, 0.3);
--dark-success-text: #34d399;

/* Warning state */
--dark-warning-bg: rgba(245, 158, 11, 0.1);
--dark-warning-border: rgba(245, 158, 11, 0.3);
--dark-warning-text: #fbbf24;

/* Error state */
--dark-error-bg: rgba(239, 68, 68, 0.1);
--dark-error-border: rgba(239, 68, 68, 0.3);
--dark-error-text: #f87171;

/* Info state */
--dark-info-bg: rgba(59, 130, 246, 0.1);
--dark-info-border: rgba(59, 130, 246, 0.3);
--dark-info-text: #60a5fa;
```

## Subtle Gradients

### Background Gradients

```css
/* Subtle radial gradient */
.dark-gradient-radial {
    background: radial-gradient(
        circle at top right,
        #1a1a1a 0%,
        #0f0f0f 100%
    );
}

/* Mesh gradient */
.dark-gradient-mesh {
    background:
        radial-gradient(at 0% 0%, rgba(59, 130, 246, 0.1) 0%, transparent 50%),
        radial-gradient(at 100% 100%, rgba(139, 92, 246, 0.1) 0%, transparent 50%),
        #0f0f0f;
}

/* Linear subtle */
.dark-gradient-linear {
    background: linear-gradient(
        180deg,
        #1a1a1a 0%,
        #0f0f0f 100%
    );
}
```

### Overlay Gradients

```css
/* Card overlay gradient */
.dark-card-gradient {
    background: linear-gradient(
        135deg,
        rgba(255, 255, 255, 0.05) 0%,
        rgba(255, 255, 255, 0.02) 100%
    );
}
```

## Component Styles

### Card

```css
.dark-card {
    background: var(--dark-bg-secondary);
    border: 1px solid var(--dark-border);
    border-radius: 16px;
    padding: 32px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
    transition: all 0.3s ease;
}

.dark-card:hover {
    border-color: var(--dark-border-light);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
    transform: translateY(-2px);
}
```

### Button

```css
/* Primary button */
.dark-button-primary {
    background: var(--dark-accent-blue);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s;
}

.dark-button-primary:hover {
    background: #2563eb;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

/* Secondary button */
.dark-button-secondary {
    background: var(--dark-bg-tertiary);
    color: var(--dark-text-primary);
    border: 1px solid var(--dark-border);
    border-radius: 8px;
    padding: 12px 24px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s;
}

.dark-button-secondary:hover {
    background: var(--dark-bg-hover);
    border-color: var(--dark-border-light);
}

/* Ghost button */
.dark-button-ghost {
    background: transparent;
    color: var(--dark-text-secondary);
    border: none;
    padding: 12px 24px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s;
}

.dark-button-ghost:hover {
    color: var(--dark-text-primary);
    background: rgba(255, 255, 255, 0.05);
}
```

### Input

```css
.dark-input {
    background: var(--dark-bg-primary);
    border: 1px solid var(--dark-border);
    border-radius: 8px;
    padding: 12px 16px;
    color: var(--dark-text-primary);
    font-size: 16px;
    transition: all 0.3s;
}

.dark-input:focus {
    outline: none;
    border-color: var(--dark-accent-blue);
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.dark-input::placeholder {
    color: var(--dark-text-tertiary);
}
```

### Navigation

```css
.dark-nav {
    background: rgba(26, 26, 26, 0.8);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-bottom: 1px solid var(--dark-border);
    padding: 16px 0;
}

.dark-nav-item {
    color: var(--dark-text-secondary);
    padding: 8px 16px;
    border-radius: 8px;
    transition: all 0.3s;
}

.dark-nav-item:hover {
    color: var(--dark-text-primary);
    background: rgba(255, 255, 255, 0.05);
}

.dark-nav-item.active {
    color: var(--dark-accent-blue);
    background: rgba(59, 130, 246, 0.1);
}
```

## Auto Dark Mode Detection

### System Preference

```css
/* Automatic dark mode based on system preference */
@media (prefers-color-scheme: dark) {
    :root {
        color-scheme: dark;
    }

    body {
        background: var(--dark-bg-primary);
        color: var(--dark-text-primary);
    }
}
```

### JavaScript Toggle

```html
<script>
// Toggle dark mode
function toggleDarkMode() {
    document.documentElement.classList.toggle('dark-mode');
    localStorage.setItem('darkMode',
        document.documentElement.classList.contains('dark-mode')
    );
}

// Load saved preference
if (localStorage.getItem('darkMode') === 'true') {
    document.documentElement.classList.add('dark-mode');
}
</script>
```

## Templates

- [templates/complete.html](templates/complete.html) - Full dashboard with dark mode
- [templates/components.html](templates/components.html) - Dark mode component library
- [templates/toggle.html](templates/toggle.html) - Light/dark mode switcher

## Accessibility

### Contrast Ratios (WCAG AA)

```css
/* Primary text: 13.5:1 (AAA) */
color: #e8e8e8 on #0f0f0f

/* Secondary text: 7.2:1 (AA) */
color: #a8a8a8 on #0f0f0f

/* Accent text: 4.8:1 (AA) */
color: #3b82f6 on #0f0f0f
```

### Focus Indicators

```css
*:focus-visible {
    outline: 2px solid var(--dark-accent-blue);
    outline-offset: 2px;
}
```

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
    * {
        animation: none !important;
        transition: none !important;
    }
}
```

## Performance Optimization

1. **Use CSS variables** for instant theme switching
2. **Minimize repaints** with GPU-accelerated properties
3. **Lazy load** dark mode styles if needed
4. **Prefers-color-scheme** for automatic detection

## Design Best Practices

### DO ✅

- Use pure black (#000) sparingly
- Layer backgrounds (#0f0f0f → #1a1a1a → #242424)
- Reduce text contrast slightly (not pure white)
- Add subtle gradients for depth
- Use accent colors strategically
- Maintain WCAG AA contrast ratios

### DON'T ❌

- Use pure white text (#fff) everywhere
- Apply bright accent colors to large areas
- Use heavy shadows
- Ignore system preferences
- Forget about accessibility

## Common Use Cases

- SaaS dashboards
- Developer tools
- Content management systems
- Mobile applications
- E-commerce platforms
- Social media apps
- Video streaming sites

## Related Skills

- For glass effects: See `../glassmorphism/SKILL.md`
- For cyberpunk style: See `../cyberpunk-neon/SKILL.md`
