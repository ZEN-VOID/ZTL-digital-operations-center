---
name: minimax-music-prompt-optimizer
description: Optimizes user input prompts for MiniMax Music Generation API to produce high-quality music compositions. Transforms raw creative ideas into structured prompts with proper style descriptions, lyric formatting, and technical parameters. Ensures optimal results for restaurant/hospitality industry background music, promotional content, and brand audio identity.
version: 1.0.0
author: ZTL Digital Intelligence Operations Center - 创意组
allowed-tools: ["Read", "Write"]
---

# MiniMax Music Prompt Optimizer

## 📋 Overview

This skill optimizes prompts for the MiniMax Music Generation API (`mcp__minimax-mcp__music_generation`), transforming user creative intentions into technically precise API requests that produce professional-quality music compositions.

**Core Value**: Bridge the gap between creative vision ("I need upbeat restaurant music") and technical API requirements (structured prompts with style, mood, instrumentation, and properly formatted lyrics).

## 🎯 Quick Start

```python
# Basic usage - optimize a simple request
input = "轻快的火锅店背景音乐"
optimized = optimize_music_prompt(input)
# Output: {
#   "prompt": "Upbeat instrumental background music, Chinese folk fusion style, festive atmosphere, suitable for hotpot restaurants",
#   "lyrics": "",  # No vocals for background music
#   "duration": 60
# }

# Advanced usage - with lyrics
input = {
  "creative_brief": "开业庆典主题曲",
  "mood": "喜庆热闹",
  "lyrics_draft": "火锅飘香迎客来\n欢聚一堂庆开业"
}
optimized = optimize_music_prompt(input)
# Output: Structured prompt + formatted lyrics with proper line breaks
```

## 🎼 Core Capabilities

### 1. Creative Intent Analysis
- Extracts **style** (pop, rock, classical, electronic, Chinese folk, etc.)
- Identifies **mood** (happy, energetic, relaxing, festive, elegant)
- Determines **scene** (restaurant background, promotional video, brand anthem)
- Specifies **instrumentation** (vocal/instrumental, acoustic/electronic)

### 2. Prompt Structure Optimization
Transforms vague ideas into MiniMax-optimized prompts:

```yaml
Before: "需要一首开业音乐"
After: "Festive opening ceremony music, Chinese traditional instruments with modern pop fusion, uplifting tempo 120 BPM, celebratory brass and percussion, suitable for restaurant grand opening events"

Character length: 10-300 (enforced)
Style keywords: Genre + mood + scene + instrumentation
```

### 3. Lyrics Formatting
Optimizes lyrics for MiniMax API requirements:

**Rules**:
- Single `\n`: Separate lyric lines (standard line break)
- Double `\n\n`: Add musical pause between verses
- Support structure tags: `[Intro]`, `[Verse]`, `[Chorus]`, `[Bridge]`, `[Outro]`
- Character limit: 10-600 characters (Chinese/English/punctuation each counts as 1)
- Minimum 10 characters for meaningful lyrics

**Example**:
```
[Intro]
(Instrumental)

[Verse]
火锅飘香迎客来
欢聚一堂庆开业

[Chorus]
味蕾狂欢,欢乐无限
美食盛宴,共度好时光

[Outro]
(Fade out)
```

### 4. Parameter Validation
- **Duration**: Max 60 seconds (current API limit, future 3 minutes)
- **Format**: mp3 (default), wav, pcm
- **Sample rate**: 16000, 24000, 32000 (default), 44100 Hz
- **Bitrate**: 32000, 64000, 128000 (default), 256000 bps

## 🍲 Restaurant Industry Specialization

### Scenario Templates

#### Background Music (无人声 Instrumental)
```yaml
Category: Ambiance Enhancement
Prompt Template: "[Style] instrumental background music, [mood] atmosphere, [tempo] BPM, suitable for [restaurant type]"

Examples:
  - Hotpot: "Chinese folk fusion instrumental, festive upbeat mood, 110 BPM, traditional erhu and pipa, suitable for Sichuan hotpot restaurants"
  - Fine Dining: "Elegant jazz instrumental, sophisticated relaxing mood, 90 BPM, piano trio with soft brush drums, suitable for upscale Western restaurants"
  - Cafe: "Acoustic indie folk instrumental, warm cozy mood, 85 BPM, guitar and light percussion, suitable for specialty coffee shops"

Lyrics: "" (empty - instrumental only)
Duration: 60 seconds (loop-friendly)
```

#### Promotional Content (有人声 Vocal)
```yaml
Category: Marketing & Branding
Prompt Template: "[Style] promotional song, [mood] and engaging, [vocal type], suitable for [marketing channel]"

Examples:
  - Grand Opening: "Pop rock promotional song, festive and energetic, uplifting male vocals, catchy melody, suitable for restaurant opening ceremony and social media"
  - Brand Anthem: "Modern Chinese pop brand song, warm and inviting, clear female vocals, memorable chorus, suitable for brand identity and video marketing"

Lyrics: User-provided or AI-generated (formatted with structure tags)
Duration: 30-60 seconds (attention span optimized)
```

#### Seasonal/Event Music
```yaml
Category: Special Occasions
Prompt Template: "[Holiday/Event] themed music, [cultural style], [mood], suitable for [specific celebration]"

Examples:
  - Chinese New Year: "Spring Festival themed music, traditional Chinese orchestral style, jubilant and auspicious mood, loud gongs and firecrackers, suitable for Lunar New Year restaurant promotions"
  - Summer BBQ Event: "Upbeat summer party music, tropical house electronic style, energetic fun mood, steel drums and electronic beats, suitable for outdoor BBQ events"

Lyrics: Optional (event-specific messaging)
Duration: 60 seconds
```

## 🔧 API Integration Points

### Input Schema
```python
{
  "creative_brief": str,        # Raw user request (required)
  "restaurant_type": str,       # Optional: hotpot, fine-dining, cafe, fast-casual, etc.
  "music_purpose": str,         # Optional: background, promo, event, brand
  "mood_preference": str,       # Optional: festive, elegant, energetic, relaxing
  "vocal_preference": str,      # Optional: instrumental, male-vocal, female-vocal, mixed
  "lyrics_draft": str,          # Optional: user-provided lyrics (will be formatted)
  "duration_seconds": int,      # Optional: default 60, max 60
  "technical_params": dict      # Optional: format, sample_rate, bitrate overrides
}
```

### Output Schema
```python
{
  "prompt": str,                # Optimized 10-300 char prompt for MiniMax API
  "lyrics": str,                # Formatted lyrics with \n separators and tags
  "analysis": {
    "detected_style": str,      # Identified music genre
    "detected_mood": str,       # Identified emotional tone
    "detected_scene": str,      # Identified use case
    "vocal_type": str          # instrumental / vocal
  },
  "api_params": {
    "prompt": str,              # Same as top-level prompt
    "lyrics": str,              # Same as top-level lyrics
    "sample_rate": int,         # 32000 (default)
    "bitrate": int,             # 128000 (default)
    "format": str              # "mp3" (default)
  },
  "optimization_notes": list[str]  # What was changed and why
}
```

## 📚 Best Practices

### Prompt Engineering Principles

1. **Be Specific, Not Vague**
   - ❌ "好听的音乐" (sounds nice)
   - ✅ "Upbeat Chinese folk instrumental, 110 BPM, erhu and pipa, festive atmosphere, hotpot restaurant background"

2. **Layer Keywords for Precision**
   - Genre: pop, rock, jazz, electronic, Chinese folk, classical
   - Mood: upbeat, relaxing, festive, elegant, energetic, warm
   - Instrumentation: acoustic guitar, piano, electronic synth, traditional instruments
   - Scene: restaurant background, promotional video, brand identity

3. **Optimize Character Budget** (10-300 chars)
   - Include: Style + Mood + Key instruments + Use case
   - Exclude: Overly poetic descriptions, redundant adjectives
   - Example: "Festive pop rock, male vocals, catchy chorus, restaurant opening promo" (72 chars)

4. **Lyrics Structure Matters**
   - Use `[Intro]`, `[Verse]`, `[Chorus]` tags for musical structure
   - Single `\n` for line breaks, double `\n\n` for pauses
   - Keep verses 2-4 lines, chorus 2-3 lines (repeatability)
   - Minimum 10 characters for lyrics to be valid

5. **Duration Planning**
   - Background loops: 60 seconds (repeatable without jarring transitions)
   - Promotional clips: 30-45 seconds (attention span sweet spot)
   - Full songs: 60 seconds (current API limit)

### Common Pitfalls to Avoid

1. **❌ Exceeding Character Limits**
   - Prompt: 300 char max
   - Lyrics: 600 char max
   - **Fix**: Prioritize core keywords, remove filler words

2. **❌ Unclear Vocal Intent**
   - "轻松的音乐" could be instrumental OR vocal
   - **Fix**: Explicitly specify "instrumental background" or "with [gender] vocals"

3. **❌ Missing Lyrics Formatting**
   - Plain text without `\n` breaks → poor musical phrasing
   - **Fix**: Always format with single/double line breaks and structure tags

4. **❌ Inappropriate Style for Scene**
   - Heavy metal for fine dining 😅
   - **Fix**: Match style to restaurant type and customer demographics

5. **❌ Ignoring Cultural Context**
   - Western pop for traditional Chinese restaurant may miss the mark
   - **Fix**: Consider cultural alignment (e.g., Chinese folk fusion for hotpot)

## 🚀 Workflow Integration

### Step 1: Receive Raw Input
```python
# From X10-AIGC音乐创作 agent
raw_input = {
  "creative_brief": "需要一首火锅店开业的喜庆音乐,要有歌词",
  "restaurant_type": "hotpot"
}
```

### Step 2: Analyze & Optimize
```python
from scripts.optimizer import MusicPromptOptimizer

optimizer = MusicPromptOptimizer()
optimized = optimizer.optimize(raw_input)
```

### Step 3: Validate API Compatibility
```python
# Ensure all parameters meet MiniMax API requirements
validated = optimizer.validate_for_api(optimized)
```

### Step 4: Return to Agent
```python
# X10 agent receives optimized prompt and passes to minimax-mcp
return {
  "status": "optimized",
  "optimized_prompt": validated["prompt"],
  "optimized_lyrics": validated["lyrics"],
  "api_params": validated["api_params"],
  "notes": validated["optimization_notes"]
}
```

### Step 5: Agent Executes API Call
```python
# X10 agent uses mcp__minimax-mcp__music_generation
result = mcp__minimax-mcp__music_generation(
  prompt=validated["prompt"],
  lyrics=validated["lyrics"],
  sample_rate=validated["api_params"]["sample_rate"],
  bitrate=validated["api_params"]["bitrate"],
  format=validated["api_params"]["format"],
  output_directory="output/[项目名]/X10-AIGC音乐创作/"
)
```

## 🧪 Testing & Quality Assurance

### Validation Checklist
```yaml
Prompt Quality:
  - [ ] 10-300 characters
  - [ ] Contains genre + mood + scene
  - [ ] Specifies vocal type (if applicable)
  - [ ] Restaurant-industry relevant

Lyrics Quality (if applicable):
  - [ ] 10-600 characters
  - [ ] Proper \n and \n\n formatting
  - [ ] Structure tags ([Verse], [Chorus], etc.)
  - [ ] Culturally appropriate language

Technical Params:
  - [ ] Duration ≤ 60 seconds
  - [ ] Valid format (mp3/wav/pcm)
  - [ ] Valid sample_rate (16k/24k/32k/44.1k)
  - [ ] Valid bitrate (32k/64k/128k/256k)

Restaurant Fit:
  - [ ] Style matches restaurant type
  - [ ] Mood appropriate for use case
  - [ ] Length suitable for purpose
```

## 📖 Extended Documentation

See `reference.md` for:
- Complete MiniMax Music API specification
- Advanced prompt engineering techniques
- Genre-specific optimization strategies
- Multi-language lyrics handling
- Edge case handling (very short/long requests)
- Performance optimization tips

## 🔗 Related Components

- **X10-AIGC音乐创作 Agent**: Primary consumer of this skill
- **minimax-mcp**: MCP server providing `music_generation` tool
- **Output Convention**: `output/[项目名]/X10-AIGC音乐创作/`

## 📝 Version History

- **v1.0.0** (2025-10-30): Initial release
  - Restaurant industry templates
  - Prompt optimization engine
  - Lyrics formatting with structure tags
  - API parameter validation
