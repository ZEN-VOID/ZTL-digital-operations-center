---
name: minimax-video-prompt-optimizer
description: Optimizes user input prompts for MiniMax Video Generation API (T2V-01, I2V-01, Hailuo-02) to produce high-quality cinematic videos. Transforms creative briefs into structured prompts with camera movements, subject descriptions, motion details, and aesthetic atmosphere. Specializes in restaurant industry promotional content, menu showcases, and brand storytelling.
version: 1.0.0
author: ZTL Digital Intelligence Operations Center - 创意组
allowed-tools: ["Read", "Write"]
---

# MiniMax Video Prompt Optimizer

## 📋 Overview

This skill optimizes prompts for MiniMax Video Generation APIs (`mcp__minimax-mcp__generate_video`), transforming user creative intentions into technically precise video generation requests that produce professional-quality cinematic content.

**Supported Models**:
- **T2V-01**: Text-to-Video (standard generation)
- **T2V-01-Director**: Text-to-Video with camera movement control
- **I2V-01**: Image-to-Video (animate static images)
- **I2V-01-Director**: Image-to-Video with camera control
- **I2V-01-live**: Image-to-Video for live-action style
- **MiniMax-Hailuo-02**: Latest ultra-clear model with precise response

**Core Value**: Bridge the gap between creative vision ("I need a hotpot promotional video") and technical API requirements (structured prompts with subject + motion + camera + atmosphere).

## 🎯 Quick Start

```python
# Basic T2V usage
input = "火锅店菜品展示视频"
optimized = optimize_video_prompt(input, model="T2V-01")
# Output: {
#   "model": "T2V-01",
#   "prompt": "Close-up of bubbling Sichuan hotpot with fresh ingredients, steam rising elegantly, chopsticks lifting red chili peppers and beef slices, warm ambient lighting, appetizing cinematic style",
#   "duration": 6,
#   "resolution": "1080P"
# }

# Advanced Director Mode with camera movements
input = "展示火锅店环境,从入口推进到用餐区"
optimized = optimize_video_prompt(input, model="T2V-01-Director")
# Output: {
#   "prompt": "[Push in] Entrance of modern hotpot restaurant with red lanterns, [Pan right] revealing cozy dining area with customers, warm inviting atmosphere, cinematic establishing shot"
# }

# I2V usage (animate existing image)
input = {
  "first_frame_image": "path/to/dish_photo.jpg",
  "creative_brief": "让菜品冒出热气,筷子夹起一片肉"
}
optimized = optimize_video_prompt(input, model="I2V-01")
# Output: {
#   "model": "I2V-01",
#   "first_frame_image": "path/to/dish_photo.jpg",
#   "prompt": "Steam rises from hotpot, chopsticks lift a piece of meat from the bubbling broth, appetizing motion"
# }
```

## 🎬 Core Capabilities

### 1. Model-Specific Optimization

**T2V-01 (Text-to-Video)**:
- Pure text-based generation
- No camera control (natural cinematography)
- Best for: Quick content generation, simple scenes
- Prompt structure: Subject + Motion + Aesthetic

**T2V-01-Director**:
- Text-to-Video with **15 camera movement instructions**
- Precise control: [Push in], [Pan left], [Zoom out], etc.
- Best for: Professional cinematography, complex shots
- Prompt structure: [Camera] + Subject + Motion + [Camera] + Aesthetic

**I2V-01 (Image-to-Video)**:
- Animate static first frame image
- Maintains first frame composition and subject
- Best for: Product showcases, dish presentations
- Prompt structure: First frame motion description + Camera (optional)

**Hailuo-02**:
- Latest model with ultra-clear quality (768P/1080P)
- Enhanced physics and natural movement
- Best for: Premium content, brand videos
- Duration: 6 or 10 seconds

### 2. Camera Movement System (Director Mode)

**15 Supported Camera Movements**:

| Movement | Syntax | Use Case |
|----------|--------|----------|
| **Truck** | `[Truck left]` / `[Truck right]` | Follow subject sideways, parallel tracking |
| **Pan** | `[Pan left]` / `[Pan right]` | Rotate camera horizontally, reveal scene |
| **Push/Pull** | `[Push in]` / `[Pull out]` | Zoom effect by moving camera |
| **Pedestal** | `[Pedestal up]` / `[Pedestal down]` | Vertical camera movement |
| **Tilt** | `[Tilt up]` / `[Tilt down]` | Rotate camera vertically |
| **Zoom** | `[Zoom in]` / `[Zoom out]` | Lens zoom (optical zoom) |
| **Shake** | `[Shake]` | Handheld effect, urgency |
| **Follow** | `[Tracking shot]` | Follow moving subject |
| **Static** | `[Static shot]` | No camera movement |

**Usage Rules**:
- Maximum 3 camera movements per prompt
- Use square brackets: `[Push in]`
- Combine movements: `[Truck left, Pan right, Zoom in]`
- Best practice: 1-2 movements for stability

### 3. Precise Prompt Formula

#### T2V-01-Director Structure:
```
[Camera Movement] + Main Subject + Scene + Motion + [Camera Movement] + Aesthetic Atmosphere
```

**Example**:
```
[Push in] Close-up of steaming Sichuan hotpot with vibrant red broth,
fresh beef slices and vegetables floating, [Zoom in] focusing on rising steam,
warm golden lighting, appetizing cinematic food photography style
```

#### I2V-01 Structure:
```
Main Subject in first frame + Motion/Change + Camera movement (optional)
```

**Example** (with first frame image):
```
First Frame: Static dish photo of hotpot
Prompt: "Steam rises from the bubbling broth, chopsticks enter frame and lift
a piece of meat, [Tilt down] camera reveals full table setting, warm ambiance"
```

### 4. Restaurant Industry Specialization

#### Menu Showcase Videos
```yaml
Model: I2V-01 (animate dish photos)
Duration: 6 seconds
Resolution: 1080P

Template:
  First Frame: Professional dish photo
  Prompt: "Steam rises elegantly, [Zoom in] highlighting fresh ingredients,
  appetizing presentation, warm lighting, food photography style"

Examples:
  - Hotpot: "Bubbling red broth with fresh ingredients, steam swirling, [Pan right] revealing variety of meats and vegetables"
  - Noodles: "Chopsticks lift noodles from bowl, [Tilt up] steam rises, savory aroma implied"
  - Stir-fry: "Sizzling wok with colorful vegetables, [Shake] dynamic cooking motion, appetizing sound implied"
```

#### Restaurant Environment Tours
```yaml
Model: T2V-01-Director (camera control essential)
Duration: 10 seconds (Hailuo-02)
Resolution: 1080P

Template:
  Prompt: "[Push in] Entrance with [restaurant style] decor, [Pan right] revealing [key features], [Pull out] establishing wide shot, [mood] atmosphere, cinematic lighting"

Examples:
  - Hotpot Restaurant: "[Push in] Red lantern-lit entrance of modern hotpot restaurant, [Pan right] revealing bustling dining area with steam rising from tables, [Pull out] warm inviting atmosphere, festive cinematic style"
  - Fine Dining: "[Truck right] Elegant white-tablecloth tables, [Tilt down] focusing on exquisite plating, [Static shot] sophisticated ambiance, soft luxury lighting"
  - Cafe: "[Pan left] Cozy corner with vintage furniture, [Zoom in] barista preparing latte art, [Pull out] warm afternoon sunlight, indie film aesthetic"
```

#### Promotional Content
```yaml
Model: T2V-01-Director or Hailuo-02
Duration: 6 seconds (teaser) or 10 seconds (full)
Resolution: 1080P

Template:
  Prompt: "[Camera] [Key visual element], [Motion description], [Camera] [Secondary element], [Emotional tone], cinematic commercial style"

Examples:
  - Grand Opening: "[Zoom in] Red ribbon-cutting ceremony at restaurant entrance, confetti falling, [Pan left] revealing excited crowd, celebratory energetic atmosphere, cinematic event coverage"
  - Seasonal Promo: "[Push in] Autumn-themed table setting with pumpkin soup, [Tilt up] warm candlelight, [Pull out] cozy seasonal ambiance, warm color grading"
  - Brand Story: "[Tracking shot] Chef preparing signature dish with passion, [Zoom in] hands carefully plating, [Static shot] pride and craftsmanship, documentary style"
```

#### Social Media Clips
```yaml
Model: Hailuo-02 (premium quality)
Duration: 6 seconds (optimal for attention span)
Resolution: 768P (Instagram/TikTok optimized)

Template:
  Prompt: "[Dynamic camera] [Eye-catching action], [Trendy visual style], engaging fast-paced energy"

Examples:
  - TikTok Hook: "[Shake] Chopsticks dramatically lifting noodles from boiling pot, [Zoom in] close-up of sauce drip, trendy food ASMR style"
  - Instagram Reel: "[Pan right] Colorful array of hotpot ingredients, [Push in] focusing on premium wagyu beef, vibrant appetizing colors, food influencer aesthetic"
```

## 🔧 API Integration Points

### Input Schema
```python
{
  "creative_brief": str,         # Required: Raw user request
  "model": str,                  # Required: T2V-01 / T2V-01-Director / I2V-01 / I2V-01-Director / I2V-01-live / MiniMax-Hailuo-02
  "first_frame_image": str,      # Required for I2V models: Path to initial image
  "restaurant_type": str,        # Optional: hotpot, fine-dining, cafe, etc.
  "video_purpose": str,          # Optional: menu-showcase, environment-tour, promo, social-media
  "camera_preference": list,     # Optional: ["Push in", "Pan right"] for Director mode
  "duration": int,               # Optional: 6 or 10 seconds (Hailuo-02 only)
  "resolution": str,             # Optional: "768P" or "1080P" (Hailuo-02 only)
  "aesthetic_style": str         # Optional: cinematic, documentary, trendy, food-photography
}
```

### Output Schema
```python
{
  "model": str,                  # Selected model (optimized from input)
  "prompt": str,                 # Optimized prompt with/without [Camera] tags
  "first_frame_image": str,      # For I2V models (if applicable)
  "duration": int,               # 6 or 10 seconds (Hailuo-02 models)
  "resolution": str,             # "768P" or "1080P" (Hailuo-02 models)
  "analysis": {
    "detected_purpose": str,     # menu-showcase / environment-tour / promo / social-media
    "recommended_cameras": list, # Camera movements used
    "subject_focus": str,        # Main subject in frame
    "motion_type": str          # static / dynamic / complex
  },
  "api_params": {
    "model": str,
    "prompt": str,
    "first_frame_image": str,   # Optional
    "duration": int,            # Optional
    "resolution": str,          # Optional
    "async_mode": bool          # Optional: default False
  },
  "optimization_notes": list[str]
}
```

## 📚 Best Practices

### Camera Movement Guidelines

#### 1. One Camera Movement (Simplest)
- **Best for**: Beginners, simple reveals
- **Example**: `[Push in] Close-up of hotpot dish, steam rising`
- **Stability**: ⭐⭐⭐⭐⭐

#### 2. Two Camera Movements (Recommended)
- **Best for**: Professional look, storytelling
- **Example**: `[Pan right] Restaurant interior, [Tilt down] focusing on table setting`
- **Stability**: ⭐⭐⭐⭐

#### 3. Three Camera Movements (Advanced)
- **Best for**: Complex cinematography, experienced users
- **Example**: `[Truck left, Pan right, Zoom in] following waiter through dining room`
- **Stability**: ⭐⭐⭐ (may cause issues if overused)

### Prompt Engineering Principles

#### 1. Subject Clarity
- ❌ Vague: "餐厅视频"
- ✅ Clear: "Modern hotpot restaurant interior with red lanterns and marble tables"

#### 2. Motion Description
- ❌ Static: "一盘火锅"
- ✅ Dynamic: "Bubbling hotpot with steam rising, chopsticks lifting beef slices"

#### 3. Aesthetic Atmosphere
- ❌ Missing: "火锅店环境"
- ✅ Complete: "火锅店环境, warm inviting atmosphere, cinematic golden hour lighting"

#### 4. Camera Movement Logic
- ❌ Random: `[Shake, Zoom in, Pan left]` (chaotic)
- ✅ Logical: `[Push in, Tilt down]` (smooth transition)

### Model Selection Strategy

```yaml
Decision Tree:

Have first frame image?
  Yes → Use I2V-01 series
    Need camera control? → I2V-01-Director
    Live-action style? → I2V-01-live
    Standard animation? → I2V-01

  No → Use T2V-01 series or Hailuo-02
    Need precise camera control? → T2V-01-Director
    Need premium quality (1080P/10s)? → MiniMax-Hailuo-02
    Quick standard generation? → T2V-01
```

### Common Pitfalls to Avoid

1. **❌ Too Many Camera Movements**
   - Using all 15 movements in one prompt
   - **Fix**: Limit to 1-2 movements, 3 maximum

2. **❌ Conflicting Camera Directions**
   - `[Pan left, Pan right]` in same prompt
   - **Fix**: Choose one consistent direction

3. **❌ Missing Subject Focus**
   - Only camera movements, no subject description
   - **Fix**: Always describe what the camera is seeing

4. **❌ Wrong Model for Task**
   - Using T2V for animating existing dish photo
   - **Fix**: Use I2V-01 for first-frame animation

5. **❌ Ignoring Duration Limits**
   - Trying to generate 30-second video
   - **Fix**: Current limit is 6s (standard) or 10s (Hailuo-02)

## 🚀 Workflow Integration

### Step 1: Receive Input
```python
# From X11-AIGC视频生成 agent
raw_input = {
  "creative_brief": "火锅店菜品展示,要有蒸汽和筷子夹起食材的镜头",
  "restaurant_type": "hotpot",
  "video_purpose": "menu-showcase"
}
```

### Step 2: Analyze & Select Model
```python
from scripts.optimizer import VideoPromptOptimizer

optimizer = VideoPromptOptimizer()

# Optimizer decides: Menu showcase → I2V-01 best (if first frame available)
# Or T2V-01-Director (if generating from scratch with camera control)
```

### Step 3: Optimize Prompt
```python
optimized = optimizer.optimize(raw_input)

# Output:
# {
#   "model": "T2V-01-Director",
#   "prompt": "[Push in] Close-up of bubbling Sichuan hotpot with red broth,
#              [Zoom in] steam rising elegantly, chopsticks lift beef slice,
#              warm appetizing lighting, cinematic food photography"
# }
```

### Step 4: Validate & Call API
```python
validated = optimizer.validate_for_api(optimized)

result = mcp__minimax-mcp__generate_video(
  model=validated["model"],
  prompt=validated["prompt"],
  duration=validated.get("duration", 6),  # Hailuo-02 only
  resolution=validated.get("resolution", "1080P"),  # Hailuo-02 only
  output_directory=f"output/{project_name}/X11-AIGC视频生成/",
  async_mode=False
)
```

### Step 5: Return Results
```python
# X11 agent receives video file
return {
  "status": "success",
  "video_file": result["file_path"],
  "optimization_details": optimized["optimization_notes"],
  "camera_movements_used": optimized["analysis"]["recommended_cameras"]
}
```

## 🧪 Testing & Quality Assurance

### Validation Checklist
```yaml
Prompt Quality:
  - [ ] Clear main subject description
  - [ ] Motion/action described
  - [ ] Aesthetic atmosphere included
  - [ ] Camera movements ≤ 3 (Director mode)
  - [ ] Camera syntax correct: [Movement name]

Model Selection:
  - [ ] I2V-01 used when first_frame_image provided
  - [ ] T2V-01-Director used when camera control needed
  - [ ] Hailuo-02 used for premium quality
  - [ ] Model matches user intent

Technical Params (Hailuo-02):
  - [ ] Duration: 6 or 10 seconds only
  - [ ] Resolution: "768P" or "1080P" only
  - [ ] first_frame_image valid for I2V models

Restaurant Fit:
  - [ ] Scene matches restaurant type
  - [ ] Aesthetic appropriate for brand
  - [ ] Motion natural and appetizing
```

## 📖 Extended Documentation

See `reference.md` for:
- Complete MiniMax Video API specification
- All 15 camera movement examples with screenshots
- Advanced multi-shot prompt composition
- Restaurant video production workflow
- Edge case handling (extreme prompts)
- Performance optimization tips
- Troubleshooting guide

## 🔗 Related Components

- **X11-AIGC视频生成 Agent**: Primary consumer of this skill
- **minimax-mcp**: MCP server providing `generate_video` tool
- **Output Convention**: `output/[项目名]/X11-AIGC视频生成/`

## 📝 Version History

- **v1.0.0** (2025-10-30): Initial release
  - Support for all 5 MiniMax video models
  - 15 camera movement optimization
  - Restaurant industry templates
  - Precise prompt formula implementation
  - API parameter validation
