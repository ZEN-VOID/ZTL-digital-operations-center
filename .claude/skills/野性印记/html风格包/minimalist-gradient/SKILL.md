---
name: Minimalist Gradient Design
description: Create elegant minimalist interfaces with subtle gradients, clean layouts, muted color palettes, and strategic bold accents. Use when designing corporate websites, product pages, or when user mentions minimalist design, subtle gradients, or clean UI. Professional and sophisticated aesthetic.
---

# Minimalist Gradient Design

## Quick Start

### Basic Minimalist Card

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Minimalist Gradient</title>
    <style>
        body {
            margin: 0;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            /* Subtle gradient background */
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }

        .minimal-card {
            /* Clean white background */
            background: #ffffff;

            /* Subtle shadow for depth */
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);

            /* Soft rounded corners */
            border-radius: 24px;

            /* Generous spacing */
            padding: 64px;
            max-width: 600px;
        }

        .minimal-card h2 {
            margin: 0 0 16px 0;
            font-size: 40px;
            font-weight: 700;
            /* Gradient text */
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .minimal-card p {
            margin: 0 0 32px 0;
            line-height: 1.8;
            font-size: 18px;
            color: #64748b;
        }

        .minimal-button {
            /* Gradient background */
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 16px 40px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
            transition: all 0.3s ease;
        }

        .minimal-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }
    </style>
</head>
<body>
    <div class="minimal-card">
        <h2>Minimalist Design</h2>
        <p>Clean layouts with subtle gradients, muted colors, and strategic bold accents for modern elegance.</p>
        <button class="minimal-button">Get Started</button>
    </div>
</body>
</html>
```

## Core Principles

### Color Philosophy

```css
:root {
    /* Neutral base */
    --neutral-50: #f8fafc;
    --neutral-100: #f1f5f9;
    --neutral-200: #e2e8f0;
    --neutral-300: #cbd5e1;
    --neutral-400: #94a3b8;
    --neutral-500: #64748b;
    --neutral-600: #475569;
    --neutral-700: #334155;
    --neutral-800: #1e293b;
    --neutral-900: #0f172a;

    /* Subtle gradients */
    --gradient-subtle-1: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    --gradient-subtle-2: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
    --gradient-subtle-3: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%);

    /* Accent gradients */
    --gradient-accent-1: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --gradient-accent-2: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    --gradient-accent-3: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}
```

## Gradient Techniques

### Background Gradients

```css
/* Subtle neutral gradient */
.gradient-bg-subtle {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

/* Warm subtle gradient */
.gradient-bg-warm {
    background: linear-gradient(135deg, #fff5f5 0%, #ffe4e6 100%);
}

/* Cool subtle gradient */
.gradient-bg-cool {
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
}
```

### Text Gradients

```css
.gradient-text {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    color: transparent; /* Fallback */
}

.gradient-text-warm {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
```

### Button Gradients

```css
.gradient-button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 16px 40px;
    cursor: pointer;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    transition: all 0.3s ease;
}

.gradient-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

/* Outline gradient button */
.gradient-button-outline {
    background: white;
    color: #667eea;
    border: 2px solid transparent;
    background-image:
        linear-gradient(white, white),
        linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    background-origin: border-box;
    background-clip: padding-box, border-box;
    border-radius: 12px;
    padding: 14px 38px;
}
```

### Card Overlays

```css
.gradient-overlay {
    position: relative;
}

.gradient-overlay::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(
        180deg,
        transparent 0%,
        rgba(0, 0, 0, 0.8) 100%
    );
    border-radius: inherit;
}
```

## Layout Components

### Hero Section

```css
.minimal-hero {
    min-height: 80vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    text-align: center;
    padding: 80px 24px;
}

.minimal-hero h1 {
    font-size: 72px;
    font-weight: 800;
    margin: 0 0 24px 0;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.minimal-hero p {
    font-size: 24px;
    color: #64748b;
    max-width: 600px;
    margin: 0 auto 48px;
}
```

### Card Grid

```css
.card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 32px;
    padding: 80px 24px;
    max-width: 1200px;
    margin: 0 auto;
}

.minimal-card {
    background: white;
    border-radius: 24px;
    padding: 48px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
    transition: all 0.3s ease;
}

.minimal-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.12);
}
```

### Pricing Table

```css
.pricing-card {
    background: white;
    border-radius: 24px;
    padding: 48px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
    text-align: center;
}

.pricing-card.featured {
    position: relative;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    transform: scale(1.05);
    box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
}

.pricing-card .price {
    font-size: 56px;
    font-weight: 800;
    margin: 24px 0;
}
```

## Typography

### Font Pairing

```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
```

```css
body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

h1, h2, h3 {
    font-weight: 800;
    letter-spacing: -0.02em;
}

p {
    font-weight: 400;
    line-height: 1.8;
    color: #64748b;
}
```

### Text Hierarchy

```css
.text-display {
    font-size: 72px;
    font-weight: 800;
    line-height: 1.1;
}

.text-headline {
    font-size: 48px;
    font-weight: 700;
    line-height: 1.2;
}

.text-title {
    font-size: 32px;
    font-weight: 700;
    line-height: 1.3;
}

.text-body {
    font-size: 18px;
    font-weight: 400;
    line-height: 1.8;
    color: #64748b;
}

.text-small {
    font-size: 14px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #94a3b8;
}
```

## Spacing System

```css
:root {
    /* 8px base unit */
    --space-1: 8px;
    --space-2: 16px;
    --space-3: 24px;
    --space-4: 32px;
    --space-5: 40px;
    --space-6: 48px;
    --space-8: 64px;
    --space-10: 80px;
    --space-12: 96px;
    --space-16: 128px;
}
```

## Texture Overlays

### Noise Texture

```css
.textured-bg {
    position: relative;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.textured-bg::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: url('data:image/svg+xml,%3Csvg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"%3E%3Cfilter id="noise"%3E%3CfeTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="4" /%3E%3C/filter%3E%3Crect width="100%25" height="100%25" filter="url(%23noise)" opacity="0.05"/%3E%3C/svg%3E');
    opacity: 0.5;
}
```

### Mesh Gradient

```css
.mesh-gradient {
    background:
        radial-gradient(at 0% 0%, rgba(102, 126, 234, 0.1) 0%, transparent 50%),
        radial-gradient(at 100% 0%, rgba(118, 75, 162, 0.1) 0%, transparent 50%),
        radial-gradient(at 100% 100%, rgba(240, 147, 251, 0.1) 0%, transparent 50%),
        radial-gradient(at 0% 100%, rgba(79, 172, 254, 0.1) 0%, transparent 50%),
        #ffffff;
}
```

## Templates

- [templates/complete.html](templates/complete.html) - Full corporate website
- [templates/landing.html](templates/landing.html) - Product landing page
- [templates/components.html](templates/components.html) - Component showcase

## Responsive Design

```css
/* Mobile first approach */
.minimal-card {
    padding: 32px;
}

@media (min-width: 768px) {
    .minimal-card {
        padding: 48px;
    }
}

@media (min-width: 1024px) {
    .minimal-card {
        padding: 64px;
    }
}
```

## Accessibility

### Contrast Requirements

```css
/* Ensure WCAG AA compliance */
.text-on-gradient {
    /* For gradient backgrounds, ensure text has sufficient contrast */
    color: #1e293b; /* Dark on light gradient */
    text-shadow: 0 1px 2px rgba(255, 255, 255, 0.5);
}
```

### Focus States

```css
button:focus-visible {
    outline: 2px solid #667eea;
    outline-offset: 4px;
}
```

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
    * {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}
```

## Performance

1. **Use CSS gradients** instead of images
2. **Limit shadow complexity** (max 2-3 layers)
3. **Optimize animations** with `transform` and `opacity`
4. **Lazy load** background images
5. **Use system fonts** as fallback

## Design Guidelines

### DO ✅

- Use generous white space (48px+ padding)
- Limit to 2-3 colors + neutrals
- Keep gradients subtle (10-20% opacity difference)
- Use 8px grid system for spacing
- Maintain high text contrast
- Use single accent gradient

### DON'T ❌

- Overuse gradients (max 2-3 per view)
- Use harsh color transitions
- Crowd elements together
- Mix multiple gradient styles
- Sacrifice readability for aesthetics

## Common Use Cases

- Corporate websites
- SaaS landing pages
- Product showcase pages
- Portfolio websites
- Mobile app presentations
- Startup homepages
- Professional services sites

## Related Skills

- For glass effects: See `../glassmorphism/SKILL.md`
- For dark themes: See `../dark-mode-premium/SKILL.md`
