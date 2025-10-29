---
name: algorithmic-art-restaurant
description: Generate algorithmic art and procedural patterns for restaurant branding using p5.js. Creates unique backgrounds, decorative elements, and brand patterns with seeded randomness for reproducibility. Perfect for menu backgrounds, packaging patterns, and brand visual elements.
allowed-tools: ["Read", "Write", "Bash", "WebFetch"]
---

# Algorithmic Art for Restaurant Design

Generate unique, reproducible algorithmic art using p5.js for restaurant branding and design materials. This skill creates procedural patterns, flow fields, particle systems, and generative designs perfect for menu backgrounds, packaging patterns, store decorations, and brand visual identity.

## Core Capabilities

### 1. Pattern Generation
- **Flow Fields**: Organic, flowing patterns inspired by nature (water, steam, fire)
- **Particle Systems**: Dynamic particle arrangements (bubbles, sparkles, food elements)
- **Geometric Patterns**: Structured designs (tiles, grids, tessellations)
- **Noise-Based Art**: Perlin/Simplex noise for natural textures
- **Grid Systems**: Modular pattern systems for consistency

### 2. Restaurant-Specific Themes

**Chinese Cuisine**:
- Red and gold color schemes
- Flowing patterns suggesting steam and tradition
- Calligraphic-inspired brush strokes
- Auspicious geometric arrangements

**Western Cuisine**:
- Clean, minimalist geometric patterns
- Elegant monochrome or muted tones
- Grid-based sophisticated layouts
- Modern abstract compositions

**Japanese Cuisine**:
- Zen-inspired minimalism
- Wave and ripple patterns (seigaiha)
- Cherry blossom particle systems
- Balanced asymmetry

**Hotpot/BBQ**:
- Dynamic fire-inspired flow fields
- Steam and smoke particle effects
- Vibrant red, orange, yellow gradients
- Energetic, lively compositions

**Dessert/Cafe**:
- Soft pastel color palettes
- Gentle particle systems (bubbles, stars)
- Sweet, playful geometric patterns
- Light, airy compositions

### 3. Seeded Randomness
- Generate reproducible patterns with seed values
- Create brand-consistent variations
- Version control for pattern families
- Systematic exploration of design space

## Quick Start

### Basic Pattern Generation

```javascript
// Example: Generate a Chinese restaurant background pattern
// Seed: 12345 for reproducibility
let seed = 12345;
let colors = ['#DC143C', '#FFD700', '#8B0000']; // Red, Gold, Dark Red

function setup() {
  createCanvas(1920, 1080);
  randomSeed(seed);
  noiseSeed(seed);
  background(250, 245, 235); // Warm off-white

  // Generate flowing steam pattern
  for (let i = 0; i < 500; i++) {
    let x = random(width);
    let y = random(height);
    let size = random(2, 20);
    let alpha = random(50, 150);

    fill(colors[int(random(colors.length))], alpha);
    noStroke();
    circle(x, y, size);
  }
}
```

### Restaurant Menu Background

```javascript
// Subtle texture for menu background
function setup() {
  createCanvas(1200, 1600);
  randomSeed(seed);
  background(255);

  // Noise-based texture
  loadPixels();
  for (let x = 0; x < width; x++) {
    for (let y = 0; y < height; y++) {
      let noiseVal = noise(x * 0.01, y * 0.01);
      let brightness = map(noiseVal, 0, 1, 240, 255);
      set(x, y, color(brightness));
    }
  }
  updatePixels();
}
```

## Workflow Integration

### For X3-平面设计师

**1. Pattern Brief**:
- Specify cuisine type and brand personality
- Define color palette (provide hex codes)
- Specify output dimensions and resolution
- Provide seed value for reproducibility

**2. Generate Patterns**:
- Run p5.js sketch with parameters
- Export as PNG (300 DPI minimum)
- Save seed value for future variations

**3. Apply to Designs**:
- Use as menu backgrounds
- Apply to packaging templates
- Create branded patterns for store materials
- Generate social media backgrounds

### Output Specification

**File Format**: PNG with transparency support
**Resolution**:
- Print: 300 DPI minimum
- Digital: 150 DPI (screens)
- Social Media: 72 DPI optimized

**Naming Convention**:
```
pattern_[type]_[cuisine]_seed[number]_[dimensions].png

Examples:
- pattern_flowfield_chinese_seed12345_1920x1080.png
- pattern_particles_japanese_seed67890_1200x1600.png
```

## Restaurant Design Use Cases

### 1. Menu Backgrounds
- Subtle, non-distracting textures
- Neutral colors that support text readability
- Consistent with brand aesthetic
- Print-ready resolution

### 2. Packaging Patterns
- Repeatable tile patterns
- Brand color integration
- Distinctive visual signature
- Works across various box sizes

### 3. Store Decorations
- Large-scale wall graphics
- Window decals
- Table surface patterns
- Ceiling/floor elements

### 4. Brand Identity Elements
- Business card backgrounds
- Letterhead watermarks
- Website backgrounds
- Social media templates

## Technical Parameters

### Color Palettes by Cuisine

```javascript
const colorPalettes = {
  chinese: ['#DC143C', '#FFD700', '#8B0000', '#F5F5DC'],
  japanese: ['#E8E8E8', '#333333', '#FFC0CB', '#4A4A4A'],
  italian: ['#228B22', '#FFFFFF', '#FF0000', '#F5DEB3'],
  french: ['#002395', '#FFFFFF', '#ED2939', '#C0C0C0'],
  hotpot: ['#FF4500', '#FFD700', '#DC143C', '#FF6347'],
  cafe: ['#F4A460', '#DEB887', '#FFFACD', '#FFE4B5']
};
```

### Pattern Types

**Flow Field**:
- Parameters: grid resolution, noise scale, flow strength
- Best for: Organic, fluid brand identities
- Cuisine fit: Chinese, Japanese, seafood

**Particle System**:
- Parameters: particle count, size range, speed
- Best for: Dynamic, energetic brands
- Cuisine fit: Hotpot, BBQ, bar/lounge

**Geometric Grid**:
- Parameters: grid size, shape type, color distribution
- Best for: Modern, clean aesthetics
- Cuisine fit: Western, fine dining, cafe

**Noise Texture**:
- Parameters: noise scale, contrast, detail
- Best for: Subtle backgrounds
- Cuisine fit: All cuisines (universal)

## Quality Standards

✅ **Resolution**: Minimum 300 DPI for print
✅ **Color Mode**: RGB for digital, CMYK for print
✅ **File Format**: PNG with transparency, PDF for vector
✅ **Reproducibility**: Always document seed values
✅ **Brand Consistency**: Use approved color palettes
✅ **Readability**: Ensure text overlays remain legible
✅ **Cultural Sensitivity**: Respect cultural design principles

## Example Prompts

**For Claude when using this skill**:

1. "Generate a Chinese restaurant menu background pattern with red and gold colors, seed 12345, 1200x1600px at 300 DPI"

2. "Create a subtle geometric pattern for an Italian restaurant packaging design, neutral warm colors, seed 67890, tileable"

3. "Design a dynamic particle system for a hotpot restaurant poster background, fire-inspired colors, seed 11111, 1920x1080px"

4. "Generate a minimalist Japanese-style wave pattern for a sushi bar menu, monochrome with single accent color, seed 22222"

## Integration with Other Skills

**Combines well with**:
- `canvas-design-restaurant`: Use generated patterns in full design compositions
- `theme-factory-restaurant`: Apply patterns across themed design systems
- `brand-guidelines-restaurant`: Ensure pattern consistency with brand rules

## Output Path Convention

All generated patterns save to:
```
output/[项目名]/X3-平面设计师/algorithmic-art/
├── patterns/
│   ├── [pattern-name]_seed[number].png
│   └── [pattern-name]_seed[number]_preview.jpg
└── metadata/
    └── [pattern-name]_specs.json
```

**Metadata JSON structure**:
```json
{
  "pattern_name": "flowfield_chinese_hotpot",
  "seed": 12345,
  "dimensions": "1920x1080",
  "dpi": 300,
  "color_palette": ["#DC143C", "#FFD700", "#8B0000"],
  "cuisine_type": "chinese_hotpot",
  "use_case": "menu_background",
  "generated_date": "2025-01-28",
  "reproducible": true
}
```

## Tips for Best Results

1. **Start with Brand Colors**: Always use the restaurant's approved color palette
2. **Test Readability**: Overlay sample text to ensure backgrounds don't interfere
3. **Generate Variations**: Create 3-5 seed variations for client selection
4. **Document Everything**: Save seed values and parameters for future consistency
5. **Consider Context**: Match pattern energy to cuisine type and brand personality
6. **Optimize File Size**: Balance quality with practical file sizes for production

## Advanced Techniques

### Responsive Patterns
Generate patterns that adapt to different aspect ratios while maintaining visual coherence.

### Animated Patterns
Create frame sequences for digital signage and video backgrounds.

### Layered Compositions
Combine multiple algorithmic layers for complex, rich visual textures.

### Data-Driven Design
Use restaurant data (sales, popularity) to influence pattern generation parameters.

---

**Remember**: Algorithmic art should enhance the brand story, not distract from it. Keep patterns subtle for text-heavy materials, bold for pure visual impact pieces.
