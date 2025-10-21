---
name: Neubrutalism Design
description: Create neubrutalism (brutalist revival) UI with bold colors, heavy fonts, sharp borders, raw aesthetic, and strong shadows. Use when designing creative portfolios, art platforms, or when user mentions neubrutalism, brutalism, or raw minimalist design. High contrast and accessibility-focused.
---

# Neubrutalism Design

## Quick Start

### Basic Neubrutalist Card

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Neubrutalism Card</title>
    <style>
        body {
            margin: 0;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #f5f5f0;
            font-family: 'Space Grotesk', 'Arial Black', sans-serif;
        }

        .brutal-card {
            /* Bold solid background */
            background: #ffeb3b;

            /* Heavy black border */
            border: 4px solid #000;

            /* No border-radius (sharp corners) */
            border-radius: 0;

            /* Strong shadow (offset) */
            box-shadow: 8px 8px 0 #000;

            /* Layout */
            padding: 48px;
            max-width: 400px;
        }

        .brutal-card h2 {
            margin: 0 0 16px 0;
            font-size: 40px;
            font-weight: 900;
            color: #000;
            text-transform: uppercase;
            letter-spacing: -1px;
        }

        .brutal-card p {
            margin: 0;
            line-height: 1.5;
            font-size: 18px;
            font-weight: 700;
            color: #000;
        }

        .brutal-button {
            background: #000;
            color: #ffeb3b;
            border: 4px solid #000;
            padding: 16px 32px;
            margin-top: 24px;
            font-size: 18px;
            font-weight: 900;
            text-transform: uppercase;
            cursor: pointer;
            box-shadow: 4px 4px 0 #ffeb3b;
            transition: all 0.1s ease;
        }

        .brutal-button:hover {
            transform: translate(2px, 2px);
            box-shadow: 2px 2px 0 #ffeb3b;
        }

        .brutal-button:active {
            transform: translate(4px, 4px);
            box-shadow: none;
        }
    </style>
</head>
<body>
    <div class="brutal-card">
        <h2>Brutal</h2>
        <p>Bold colors, heavy fonts, and raw minimalist aesthetic.</p>
        <button class="brutal-button">Click</button>
    </div>
</body>
</html>
```

## Core CSS Principles

### Neubrutalism Formula

```css
.neubrutalist {
    /* 1. Bold solid colors */
    background: #ffeb3b;

    /* 2. Heavy black borders (3-5px) */
    border: 4px solid #000;

    /* 3. NO border-radius (sharp corners) */
    border-radius: 0;

    /* 4. Strong offset shadow */
    box-shadow: 8px 8px 0 #000;

    /* 5. High contrast text */
    color: #000;
    font-weight: 900;
}
```

## Color Palettes

### Bold Primary Colors

```css
/* Yellow accent */
.brutal-yellow {
    background: #ffeb3b;
    border: 4px solid #000;
    box-shadow: 8px 8px 0 #000;
}

/* Cyan accent */
.brutal-cyan {
    background: #00e5ff;
    border: 4px solid #000;
    box-shadow: 8px 8px 0 #000;
}

/* Pink accent */
.brutal-pink {
    background: #ff4081;
    border: 4px solid #000;
    box-shadow: 8px 8px 0 #000;
    color: #fff;
}

/* Green accent */
.brutal-green {
    background: #76ff03;
    border: 4px solid #000;
    box-shadow: 8px 8px 0 #000;
}
```

### Monochrome Scheme

```css
.brutal-mono-light {
    background: #fff;
    border: 4px solid #000;
    box-shadow: 8px 8px 0 #000;
    color: #000;
}

.brutal-mono-dark {
    background: #000;
    border: 4px solid #fff;
    box-shadow: 8px 8px 0 #fff;
    color: #fff;
}
```

## Typography

### Font Recommendations

```css
/* Bold sans-serif fonts */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700;900&display=swap');

.brutal-text {
    font-family: 'Space Grotesk', 'Arial Black', sans-serif;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: -1px;
}
```

### Text Hierarchy

```css
/* Heading 1 */
.brutal-h1 {
    font-size: 64px;
    font-weight: 900;
    line-height: 1;
    text-transform: uppercase;
}

/* Heading 2 */
.brutal-h2 {
    font-size: 40px;
    font-weight: 900;
    text-transform: uppercase;
}

/* Body text */
.brutal-body {
    font-size: 18px;
    font-weight: 700;
    line-height: 1.5;
}
```

## Interactive Components

### Button

```css
.brutal-button {
    background: #000;
    color: #ffeb3b;
    border: 4px solid #000;
    padding: 16px 32px;
    font-size: 18px;
    font-weight: 900;
    text-transform: uppercase;
    cursor: pointer;
    box-shadow: 4px 4px 0 #ffeb3b;
    transition: all 0.1s ease;
}

.brutal-button:hover {
    transform: translate(2px, 2px);
    box-shadow: 2px 2px 0 #ffeb3b;
}

.brutal-button:active {
    transform: translate(4px, 4px);
    box-shadow: none;
}
```

### Input Field

```css
.brutal-input {
    background: #fff;
    border: 4px solid #000;
    border-radius: 0;
    padding: 16px;
    font-size: 18px;
    font-weight: 700;
    box-shadow: 4px 4px 0 #000;
}

.brutal-input:focus {
    outline: none;
    box-shadow: 6px 6px 0 #000;
    transform: translate(-2px, -2px);
}
```

### Card with Hover Effect

```css
.brutal-card {
    background: #ffeb3b;
    border: 4px solid #000;
    padding: 32px;
    box-shadow: 8px 8px 0 #000;
    transition: all 0.2s ease;
}

.brutal-card:hover {
    transform: translate(-4px, -4px);
    box-shadow: 12px 12px 0 #000;
}
```

## Layout Patterns

### Grid Layout

```css
.brutal-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 48px;
    padding: 48px;
    background: #f5f5f0;
}
```

### Asymmetric Layout

```css
.brutal-asymmetric {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 32px;
}

@media (max-width: 768px) {
    .brutal-asymmetric {
        grid-template-columns: 1fr;
    }
}
```

## Shadow Variations

### Standard Shadow

```css
box-shadow: 8px 8px 0 #000;
```

### Heavy Shadow

```css
box-shadow: 12px 12px 0 #000;
```

### Minimal Shadow

```css
box-shadow: 4px 4px 0 #000;
```

### Colored Shadow

```css
box-shadow: 8px 8px 0 #ff4081;
```

## Templates

- [templates/complete.html](templates/complete.html) - Full portfolio page
- [templates/components.html](templates/components.html) - Component library
- [templates/minimal.html](templates/minimal.html) - Basic card

## Accessibility

### High Contrast (WCAG AAA)

Neubrutalism naturally provides excellent contrast:

```css
/* Black on yellow: 11.7:1 ratio */
.brutal-accessible-1 {
    background: #ffeb3b;
    color: #000;
}

/* White on black: 21:1 ratio */
.brutal-accessible-2 {
    background: #000;
    color: #fff;
}
```

### Focus States

```css
.brutal-button:focus {
    outline: 4px solid #ff4081;
    outline-offset: 4px;
}
```

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
    .brutal-button {
        transition: none;
    }

    .brutal-button:hover {
        transform: none;
    }
}
```

## Browser Support

| Browser | Support |
|---------|---------|
| All modern browsers | ✅ Full support |
| IE11 | ✅ Works (basic CSS) |

## Performance

Neubrutalism is highly performant:
- Simple CSS properties
- No backdrop-filter or complex shadows
- Minimal repaints
- Fast rendering

## Design Guidelines

### DO ✅

- Use bold, saturated colors
- Heavy black borders (3-5px)
- Sharp corners (no border-radius)
- Strong offset shadows
- High contrast text
- Uppercase typography
- Generous white space

### DON'T ❌

- Use gradients
- Add border-radius
- Use soft shadows
- Use subtle colors
- Use thin borders
- Use light font weights

## Common Use Cases

- Creative agency portfolios
- Art and design platforms
- Indie game websites
- Personal brand sites
- Music and event pages
- Bold call-to-actions
- Statement headers

## Inspiration & References

Neubrutalism combines:
- **Brutalist architecture**: Raw, unpolished aesthetic
- **Swiss design**: Bold typography, grid systems
- **Memphis design**: Bold colors, geometric shapes
- **Modern minimalism**: Clean, functional layouts

## Related Skills

- For minimalist approach: See `../minimalist-gradient/SKILL.md`
- For dark themes: See `../dark-mode-premium/SKILL.md`
