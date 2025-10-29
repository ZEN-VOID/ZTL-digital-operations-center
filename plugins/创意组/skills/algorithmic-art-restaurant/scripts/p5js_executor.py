#!/usr/bin/env python3
"""
P5.js Algorithmic Art Executor for Restaurant Design
======================================================
Generates procedural patterns and algorithmic art using p5.js.
Creates unique, reproducible backgrounds and patterns for restaurant branding.

Core Capabilities:
- Flow fields (organic, flowing patterns)
- Particle systems (dynamic arrangements)
- Geometric patterns (structured designs)
- Noise-based textures (natural textures)
"""

import json
import subprocess
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Literal


# ============================================
# Configuration
# ============================================

@dataclass
class PatternConfig:
    """Pattern generation configuration"""
    pattern_type: Literal["flowfield", "particles", "geometric", "noise"]
    cuisine_type: str
    seed: int
    width: int = 1920
    height: int = 1080
    dpi: int = 300
    colors: List[str] = None  # Hex colors

    def __post_init__(self):
        if self.colors is None:
            self.colors = COLOR_PALETTES.get(self.cuisine_type, COLOR_PALETTES["chinese"])


# ============================================
# Color Palettes
# ============================================

COLOR_PALETTES = {
    "chinese": ["#DC143C", "#FFD700", "#8B0000", "#F5F5DC"],
    "japanese": ["#E8E8E8", "#333333", "#FFC0CB", "#4A4A4A"],
    "italian": ["#228B22", "#FFFFFF", "#FF0000", "#F5DEB3"],
    "french": ["#002395", "#FFFFFF", "#ED2939", "#C0C0C0"],
    "hotpot": ["#FF4500", "#FFD700", "#DC143C", "#FF6347"],
    "cafe": ["#F4A460", "#DEB887", "#FFFACD", "#FFE4B5"]
}


# ============================================
# P5.js Template Generator
# ============================================

class P5jsTemplateGenerator:
    """Generate p5.js sketch code from configuration"""

    def generate_flowfield_sketch(self, config: PatternConfig) -> str:
        """Generate flow field pattern sketch"""
        colors_js = json.dumps(config.colors)

        return f"""
// Flow Field Pattern for {config.cuisine_type}
// Seed: {config.seed}

let seed = {config.seed};
let colors = {colors_js};

function setup() {{
  createCanvas({config.width}, {config.height});
  randomSeed(seed);
  noiseSeed(seed);
  background(250, 245, 235);
  noLoop();
}}

function draw() {{
  let resolution = 20;
  let cols = width / resolution;
  let rows = height / resolution;

  for (let i = 0; i < cols; i++) {{
    for (let j = 0; j < rows; j++) {{
      let x = i * resolution;
      let y = j * resolution;

      let angle = noise(i * 0.1, j * 0.1) * TWO_PI * 2;
      let length = 20;

      push();
      translate(x, y);
      rotate(angle);

      let colorIndex = floor(random(colors.length));
      let col = color(colors[colorIndex]);
      col.setAlpha(150);
      stroke(col);
      strokeWeight(2);
      line(0, 0, length, 0);
      pop();
    }}
  }}

  // Save
  saveCanvas('output', 'png');
}}
"""

    def generate_particles_sketch(self, config: PatternConfig) -> str:
        """Generate particle system sketch"""
        colors_js = json.dumps(config.colors)

        return f"""
// Particle System for {config.cuisine_type}
// Seed: {config.seed}

let seed = {config.seed};
let colors = {colors_js};

function setup() {{
  createCanvas({config.width}, {config.height});
  randomSeed(seed);
  noiseSeed(seed);
  background(250, 245, 235);
  noLoop();
}}

function draw() {{
  for (let i = 0; i < 500; i++) {{
    let x = random(width);
    let y = random(height);
    let size = random(2, 20);
    let alpha = random(50, 150);

    let colorIndex = floor(random(colors.length));
    let col = color(colors[colorIndex]);
    col.setAlpha(alpha);

    fill(col);
    noStroke();
    circle(x, y, size);
  }}

  saveCanvas('output', 'png');
}}
"""

    def generate_geometric_sketch(self, config: PatternConfig) -> str:
        """Generate geometric pattern sketch"""
        colors_js = json.dumps(config.colors)

        return f"""
// Geometric Pattern for {config.cuisine_type}
// Seed: {config.seed}

let seed = {config.seed};
let colors = {colors_js};

function setup() {{
  createCanvas({config.width}, {config.height});
  randomSeed(seed);
  background(255);
  noLoop();
}}

function draw() {{
  let gridSize = 80;
  let cols = width / gridSize;
  let rows = height / gridSize;

  for (let i = 0; i < cols; i++) {{
    for (let j = 0; j < rows; j++) {{
      let x = i * gridSize;
      let y = j * gridSize;

      let colorIndex = floor(random(colors.length));
      let col = color(colors[colorIndex]);
      col.setAlpha(180);
      fill(col);
      noStroke();

      let shapeType = floor(random(3));
      if (shapeType === 0) {{
        rect(x + 10, y + 10, gridSize - 20, gridSize - 20);
      }} else if (shapeType === 1) {{
        circle(x + gridSize/2, y + gridSize/2, gridSize - 20);
      }} else {{
        triangle(
          x + gridSize/2, y + 10,
          x + 10, y + gridSize - 10,
          x + gridSize - 10, y + gridSize - 10
        );
      }}
    }}
  }}

  saveCanvas('output', 'png');
}}
"""

    def generate_noise_sketch(self, config: PatternConfig) -> str:
        """Generate noise-based texture sketch"""
        return f"""
// Noise Texture for {config.cuisine_type}
// Seed: {config.seed}

let seed = {config.seed};

function setup() {{
  createCanvas({config.width}, {config.height});
  randomSeed(seed);
  noiseSeed(seed);
  noLoop();
}}

function draw() {{
  loadPixels();
  for (let x = 0; x < width; x++) {{
    for (let y = 0; y < height; y++) {{
      let noiseVal = noise(x * 0.01, y * 0.01);
      let brightness = map(noiseVal, 0, 1, 240, 255);
      set(x, y, color(brightness));
    }}
  }}
  updatePixels();

  saveCanvas('output', 'png');
}}
"""


# ============================================
# P5.js Executor
# ============================================

class P5jsExecutor:
    """
    Execute p5.js sketches using Node.js and p5.js-svg
    Generates PNG output from p5.js code
    """

    def __init__(self):
        self.template_gen = P5jsTemplateGenerator()
        self._check_dependencies()

    def _check_dependencies(self):
        """Check if Node.js and p5.js are available"""
        try:
            subprocess.run(["node", "--version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️  Warning: Node.js not found. P5.js execution requires Node.js")
            print("   Install: https://nodejs.org/")

    def execute(
        self,
        config: PatternConfig,
        output_dir: Optional[Path] = None,
        project_name: str = "算法艺术"
    ) -> Dict:
        """
        Execute p5.js pattern generation

        Args:
            config: Pattern configuration
            output_dir: Output directory
            project_name: Project name

        Returns:
            Execution result
        """
        # Set output directory
        if output_dir is None:
            output_dir = Path("output") / project_name / "X4-平面设计师" / "algorithmic-art" / config.pattern_type

        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate p5.js sketch code
        if config.pattern_type == "flowfield":
            sketch_code = self.template_gen.generate_flowfield_sketch(config)
        elif config.pattern_type == "particles":
            sketch_code = self.template_gen.generate_particles_sketch(config)
        elif config.pattern_type == "geometric":
            sketch_code = self.template_gen.generate_geometric_sketch(config)
        elif config.pattern_type == "noise":
            sketch_code = self.template_gen.generate_noise_sketch(config)
        else:
            raise ValueError(f"Unknown pattern type: {config.pattern_type}")

        # Save sketch
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sketch_filename = f"pattern_{config.pattern_type}_{config.cuisine_type}_seed{config.seed}_{timestamp}.js"
        sketch_path = output_dir / sketch_filename
        sketch_path.write_text(sketch_code, encoding="utf-8")

        # Build metadata
        metadata = {
            "pattern_type": config.pattern_type,
            "cuisine_type": config.cuisine_type,
            "seed": config.seed,
            "dimensions": f"{config.width}x{config.height}",
            "dpi": config.dpi,
            "colors": config.colors,
            "timestamp": datetime.now().isoformat(),
            "sketch_path": str(sketch_path),
            "reproducible": True
        }

        # Save metadata
        metadata_path = output_dir / f"pattern_{config.pattern_type}_seed{config.seed}_{timestamp}_metadata.json"
        metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")

        print(f"✅ P5.js sketch generated: {sketch_path}")
        print(f"📋 Metadata saved: {metadata_path}")
        print(f"\n{'='*60}")
        print("📢 MANUAL STEP REQUIRED:")
        print("="*60)
        print(f"\nThe p5.js sketch has been generated at:")
        print(f"  {sketch_path}")
        print(f"\nTo complete the pattern generation:")
        print(f"1. Open the sketch in p5.js editor: https://editor.p5js.org/")
        print(f"2. Copy the code from: {sketch_path}")
        print(f"3. Run the sketch (it will auto-download as PNG)")
        print(f"4. Move the downloaded 'output.png' to: {output_dir}/")
        print(f"5. Rename to: pattern_{config.pattern_type}_seed{config.seed}.png")
        print(f"\nAlternatively, run with p5-node if installed:")
        print(f"  node {sketch_path}")
        print(f"\n{'='*60}\n")

        return {
            "success": True,
            "sketch_path": str(sketch_path),
            "metadata_path": str(metadata_path),
            "output_dir": str(output_dir),
            "expected_filename": f"pattern_{config.pattern_type}_seed{config.seed}.png",
            "metadata": metadata,
            "message": "P5.js sketch generated. Manual execution step required."
        }


# ============================================
# High-Level API
# ============================================

def generate_pattern(
    pattern_type: str,
    cuisine_type: str = "chinese",
    seed: int = 12345,
    width: int = 1920,
    height: int = 1080,
    project_name: str = "餐饮图案生成"
) -> Dict:
    """
    Generate algorithmic pattern

    Args:
        pattern_type: "flowfield", "particles", "geometric", "noise"
        cuisine_type: Cuisine for color palette
        seed: Random seed for reproducibility
        width: Pattern width in pixels
        height: Pattern height in pixels
        project_name: Project name

    Returns:
        Execution result
    """
    config = PatternConfig(
        pattern_type=pattern_type,
        cuisine_type=cuisine_type,
        seed=seed,
        width=width,
        height=height,
        dpi=300
    )

    executor = P5jsExecutor()
    return executor.execute(config, project_name=project_name)


# ============================================
# CLI Interface
# ============================================

def main():
    """Command-line interface"""
    import argparse

    parser = argparse.ArgumentParser(description="P5.js Algorithmic Art Generator")
    parser.add_argument("type", choices=["flowfield", "particles", "geometric", "noise"],
                       help="Pattern type")
    parser.add_argument("--cuisine", default="chinese",
                       choices=list(COLOR_PALETTES.keys()),
                       help="Cuisine type (for color palette)")
    parser.add_argument("--seed", type=int, default=12345, help="Random seed")
    parser.add_argument("--width", type=int, default=1920, help="Width in pixels")
    parser.add_argument("--height", type=int, default=1080, help="Height in pixels")
    parser.add_argument("--project", default="算法艺术", help="Project name")

    args = parser.parse_args()

    result = generate_pattern(
        pattern_type=args.type,
        cuisine_type=args.cuisine,
        seed=args.seed,
        width=args.width,
        height=args.height,
        project_name=args.project
    )

    if result["success"]:
        print(f"\n✨ Pattern sketch generated successfully!")
        print(f"📁 Sketch: {result['sketch_path']}")
        print(f"📋 Metadata: {result['metadata_path']}")
        print(f"💡 Follow the instructions above to complete pattern generation.")
    else:
        print(f"\n❌ Pattern generation failed: {result.get('error')}")


if __name__ == "__main__":
    main()
