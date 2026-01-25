# MiniMax Music Prompt Optimizer - Extended Reference

## Complete API Specification

### MiniMax Music Generation API v1.0

**Base Endpoint**: Via `mcp__minimax-mcp__music_generation` tool

**Authentication**: API key managed by minimax-mcp server

**Rate Limits**:
- **1 concurrent request per account**
- Wait for previous generation to complete before starting new one

**Pricing**: $0.035 per generation (60 seconds of music)

### Request Parameters

```python
{
  "prompt": str,              # Required, 10-300 characters
  "lyrics": str,              # Required, "" for instrumental, 10-600 chars for vocal
  "sample_rate": int,         # Optional, default 32000 Hz
                              # Valid: 16000, 24000, 32000, 44100
  "bitrate": int,             # Optional, default 128000 bps
                              # Valid: 32000, 64000, 128000, 256000
  "format": str,              # Optional, default "mp3"
                              # Valid: "mp3", "wav", "pcm"
  "output_directory": str     # Required, where to save output file
}
```

### Response Format

```python
{
  "status": "success",
  "file_path": "/path/to/output/music_20251030_143522.mp3",
  "duration": 60,                    # seconds
  "file_size": 1.2,                  # MB
  "sample_rate": 32000,
  "bitrate": 128000,
  "credits_used": 1,
  "remaining_credits": 99
}
```

### Error Responses

```python
{
  "status": "error",
  "error_code": "INVALID_PROMPT_LENGTH",
  "message": "Prompt must be between 10 and 300 characters",
  "details": {
    "current_length": 5,
    "min_length": 10,
    "max_length": 300
  }
}
```

**Common Error Codes**:
- `INVALID_PROMPT_LENGTH`: Prompt outside 10-300 range
- `INVALID_LYRICS_LENGTH`: Lyrics outside 10-600 range (when provided)
- `CONCURRENT_LIMIT_REACHED`: Another generation in progress
- `INSUFFICIENT_CREDITS`: Account credits depleted
- `INVALID_SAMPLE_RATE`: Sample rate not in [16000, 24000, 32000, 44100]
- `INVALID_FORMAT`: Format not in ["mp3", "wav", "pcm"]
- `API_RATE_LIMIT`: Rate limit exceeded (429)

## Advanced Prompt Engineering

### Genre-Specific Templates

#### 1. Chinese Folk Fusion (中国民乐)
```yaml
Keywords: Chinese folk, traditional instruments, erhu, pipa, guzheng, dizi
Mood: festive, nostalgic, elegant
Tempo: 100-120 BPM (upbeat), 60-80 BPM (slow)
Instrumentation: erhu (二胡), pipa (琵琶), guzheng (古筝), dizi (笛子)

Example Prompts:
  - "Traditional Chinese folk instrumental, festive erhu and pipa melody, 110 BPM, suitable for hotpot restaurant ambiance"
  - "Nostalgic Chinese classical music, elegant guzheng solo, 70 BPM, refined atmosphere for tea house"
  - "Modern Chinese folk fusion, electronic beats with traditional dizi, 120 BPM, youthful energy for fast-casual dining"
```

#### 2. Jazz & Blues (爵士蓝调)
```yaml
Keywords: jazz, blues, swing, bebop, smooth jazz
Mood: sophisticated, relaxing, elegant, romantic
Tempo: 80-120 BPM (swing), 60-80 BPM (smooth jazz)
Instrumentation: piano trio, saxophone, double bass, brush drums

Example Prompts:
  - "Smooth jazz instrumental, elegant piano trio, 90 BPM, sophisticated atmosphere for fine dining"
  - "Upbeat swing jazz, playful saxophone and trumpet, 120 BPM, lively ambiance for American diner"
  - "Intimate blues instrumental, soulful electric guitar, 70 BPM, romantic mood for date-night restaurant"
```

#### 3. Electronic & Ambient (电子氛围)
```yaml
Keywords: electronic, ambient, downtempo, chillout, lo-fi
Mood: modern, relaxing, futuristic, zen
Tempo: 80-100 BPM (downtempo), 120-140 BPM (house)
Instrumentation: synthesizers, electronic drums, atmospheric pads

Example Prompts:
  - "Ambient electronic instrumental, atmospheric synth pads, 85 BPM, zen minimalist mood for modern cafe"
  - "Lo-fi chillout music, relaxing beats and vinyl crackle, 80 BPM, cozy atmosphere for specialty coffee shop"
  - "Deep house electronic, groovy bassline and filtered vocals, 125 BPM, energetic vibe for trendy bar"
```

#### 4. Acoustic & Folk (原声民谣)
```yaml
Keywords: acoustic, folk, indie, singer-songwriter
Mood: warm, cozy, organic, intimate
Tempo: 80-110 BPM
Instrumentation: acoustic guitar, light percussion, harmonica

Example Prompts:
  - "Acoustic indie folk instrumental, warm guitar fingerpicking, 90 BPM, cozy ambiance for artisan bakery"
  - "Upbeat folk music, playful mandolin and banjo, 110 BPM, cheerful atmosphere for farm-to-table restaurant"
  - "Intimate singer-songwriter style, gentle acoustic guitar, 85 BPM, organic mood for health food cafe"
```

### Lyrics Optimization Strategies

#### Structure Tag Usage

```
[Intro]
- Purpose: Musical opening, set the mood
- Duration: 4-8 seconds
- Content: Instrumental only or "Oh oh oh" vocalizations
- Example: "(Instrumental intro with rising strings)"

[Verse]
- Purpose: Tell the story, introduce concepts
- Duration: 15-20 seconds
- Lines: 2-4 lines per verse
- Content: Descriptive narrative, scene-setting
- Example:
  火锅飘香迎客来
  麻辣鲜香味无穷
  欢聚一堂庆开业
  宾客满堂乐开怀

[Chorus]
- Purpose: Main hook, most memorable part
- Duration: 10-15 seconds
- Lines: 2-3 lines, repeat 2x in full song
- Content: Core message, brand name, catchphrase
- Example:
  来吧来吧, 火锅盛宴
  美食狂欢, 欢乐无限

[Bridge]
- Purpose: Musical variation, build tension
- Duration: 8-12 seconds
- Lines: 2-3 lines
- Content: Contrast from verse/chorus, new perspective
- Example:
  麻辣鲜香四重奏
  味蕾狂欢不停歇

[Outro]
- Purpose: Closing, resolution
- Duration: 4-8 seconds
- Content: Fade out or final statement
- Example: "(Instrumental fade out with echoing vocals)"
```

#### Line Break Strategies

**Single `\n` (Line Break)**:
- Use between lyric lines within same section
- Creates natural phrasing pause (breath)
- Maintains rhythmic flow

```
火锅飘香迎客来\n麻辣鲜香味无穷\n欢聚一堂庆开业
```
**Rendering**: Each line sung sequentially with brief pause

**Double `\n\n` (Section Break)**:
- Use between sections (Verse → Chorus)
- Creates musical pause/transition (2-4 beats)
- Allows instrumentation to shine

```
[Verse]\n火锅飘香迎客来\n\n[Chorus]\n来吧来吧, 火锅盛宴
```
**Rendering**: Musical interlude between verse and chorus

#### Rhyme & Rhythm Tips

1. **Consistent Syllable Count**
   - Chinese: 7-character lines work well (七言诗)
   - English: 8-10 syllable lines
   - Example (Chinese 7-char):
     ```
     火锅飘香迎客来  (7 chars)
     麻辣鲜香味无穷  (7 chars)
     ```

2. **End Rhymes** (尾韵)
   - Match last character/syllable across lines
   - Example:
     ```
     火锅飘香迎客**来**  (lái)
     欢聚一堂庆开**业**  (yè) - different, but...
     麻辣鲜香味无**穷**  (qióng)
     宾客满堂乐开**怀**  (huái) - lái/huái partial rhyme
     ```

3. **Internal Rhythm** (内在节奏)
   - Use 2-2-3 or 3-2-2 syllable grouping in Chinese
   - Example: 火锅/飘香/迎客来 (2-2-3)

4. **Repetition for Catchiness**
   - Repeat key phrases in chorus
   - Example: "来吧来吧, 火锅盛宴" (repeat "来吧")

### Multi-Language Lyrics Handling

#### Chinese Lyrics (中文歌词)
- **Character Count**: Each Chinese character = 1 count
- **Punctuation**: Commas, periods also count
- **Max 600 chars**: ~100-150 Chinese characters for full lyrics
- **Structure**: Works well with traditional poetry formats (五言/七言)

**Example** (82 characters):
```
[Verse]
火锅飘香迎客来
麻辣鲜香味无穷
欢聚一堂庆开业
宾客满堂乐开怀

[Chorus]
来吧来吧,火锅盛宴
美食狂欢,欢乐无限
```

#### English Lyrics
- **Character Count**: Each letter, space, punctuation = 1 count
- **Max 600 chars**: ~80-100 words for full lyrics
- **Structure**: Verse-Chorus-Verse-Chorus-Bridge-Chorus

**Example** (312 characters):
```
[Verse]
Welcome to the grand opening day
Hotpot flavors lead the way
Spicy, savory, rich and bold
Stories here are yet untold

[Chorus]
Come together, taste the fire
Flavors rising ever higher
Celebration, joy and cheer
Your new favorite place is here

[Bridge]
Bubbling broth and laughter loud
Bringing together quite a crowd
```

#### Mixed Language Lyrics (中英混合)
- **Strategy**: Use English for brand names, Chinese for core message
- **Character Count**: All chars (Chinese + English) count equally
- **Cultural Fit**: Ensure language choice matches target audience

**Example** (128 characters):
```
[Verse]
欢迎来到 Hotpot Paradise
麻辣鲜香，味蕾的盛宴
Come together, 欢聚一堂
庆祝开业，joy and celebration

[Chorus]
Hotpot Paradise, 火锅天堂
美食狂欢，never stops the fun
```

## Edge Case Handling

### Very Short Requests (< 20 chars)
```python
Input: "火锅音乐"
Problem: Too vague, lacks mood/style/purpose

Strategy:
1. Expand with default assumptions
2. Add optimization note
3. Use genre-appropriate defaults

Output Prompt:
"Chinese folk fusion instrumental background music, festive upbeat atmosphere,
traditional erhu and pipa, suitable for Sichuan hotpot restaurants"

Notes: ["Expanded vague request with hotpot default template"]
```

### Very Long Requests (> 500 chars)
```python
Input: "我需要一首非常喜庆的、充满节日气氛的、适合火锅店新店开业庆典使用的、
包含传统中国民乐元素但又有现代流行音乐感觉的、节奏要欢快但不能太吵闹的、
最好有一些二胡和琵琶的旋律、还要有一点电子音乐的元素、总之要让顾客感到..."

Problem: Exceeds 300 char prompt limit, too many conflicting requirements

Strategy:
1. Extract core keywords: 喜庆, 火锅店, 开业, 传统+现代, 二胡/琵琶, 电子
2. Prioritize: Genre > Mood > Instrumentation > Purpose
3. Truncate gracefully at 297 chars + "..."

Output Prompt:
"Festive Chinese folk fusion with modern electronic elements, upbeat but not
overwhelming, traditional erhu and pipa melodies with electronic beats, suitable
for hotpot restaurant grand opening celebration, joyful atmosphere, 110 BPM..."

Notes: [
  "Truncated long request from 500+ to 300 characters",
  "Preserved core elements: festive mood, Chinese fusion, erhu/pipa, opening event"
]
```

### Conflicting Requirements
```python
Input: {
  "creative_brief": "安静的背景音乐",
  "mood_preference": "energetic"
}
Problem: "安静" (quiet) conflicts with "energetic"

Strategy:
1. Detect conflicts in analysis phase
2. Prioritize explicit parameters (mood_preference) over brief
3. Add warning note

Output:
Analysis: {"detected_mood": "energetic", "warning": "Mood conflict detected"}
Notes: [
  "Conflict: brief says 'quiet' but mood_preference='energetic'",
  "Resolved: Using explicit mood_preference (energetic)"
]
```

### Missing Restaurant Type
```python
Input: "开业音乐"
Problem: No restaurant type context

Strategy:
1. Use generic "restaurant" in prompt
2. Apply universal "festive opening" template
3. Note lack of specificity

Output Prompt:
"Festive opening ceremony music, upbeat pop with traditional elements, celebratory
atmosphere, suitable for restaurant grand opening events"

Notes: ["No restaurant type specified, using generic template"]
```

## Performance Optimization

### Prompt Template Caching
```python
# Cache frequently used templates to avoid re-generation
TEMPLATE_CACHE = {
  "hotpot_background": "Chinese folk fusion instrumental...",
  "fine_dining_background": "Elegant jazz instrumental...",
  "opening_promo": "Festive promotional song..."
}

def get_cached_template(restaurant_type, purpose):
    cache_key = f"{restaurant_type}_{purpose}"
    return TEMPLATE_CACHE.get(cache_key)
```

### Batch Optimization
```python
def optimize_batch(input_list: List[MusicPromptInput]) -> List[OptimizedOutput]:
    """Optimize multiple prompts in one pass."""
    optimizer = MusicPromptOptimizer()
    return [optimizer.optimize(inp) for inp in input_list]

# Useful for X10 batch generation mode
```

### Validation Short-Circuits
```python
# Fail fast on obvious invalid inputs
def quick_validate(input_obj):
    if not input_obj.creative_brief:
        raise ValueError("creative_brief is required")

    if input_obj.duration_seconds > 60:
        raise ValueError("Duration exceeds API limit of 60 seconds")

    # More validations before expensive optimization
```

## Integration Patterns

### X10 Agent Workflow

```python
# X10-AIGC音乐创作 calls this skill internally

# Step 1: Receive user request
user_request = "为新开的麻辣火锅店创作一首开业音乐,要有喜庆的歌词"

# Step 2: Call optimizer skill
from skills.AIGC.minimax.prompt_optimizer.音乐.scripts.optimizer import MusicPromptOptimizer

optimizer = MusicPromptOptimizer()
optimized = optimizer.optimize({
  "creative_brief": user_request,
  "restaurant_type": "hotpot",
  "music_purpose": "promo",
  "lyrics_draft": "火锅飘香迎客来\n麻辣鲜香味无穷\n欢聚一堂庆开业\n宾客满堂乐开怀"
})

# Step 3: Log optimization for traceability
with open(f"output/{project_name}/X10-AIGC音乐创作/plan_{timestamp}.json", "w") as f:
    json.dump({
      "user_request": user_request,
      "optimized_prompt": optimized.prompt,
      "optimized_lyrics": optimized.lyrics,
      "analysis": optimized.analysis,
      "notes": optimized.optimization_notes
    }, f, ensure_ascii=False, indent=2)

# Step 4: Call MiniMax API via MCP
result = mcp__minimax-mcp__music_generation(
  prompt=optimized.prompt,
  lyrics=optimized.lyrics,
  sample_rate=optimized.api_params["sample_rate"],
  bitrate=optimized.api_params["bitrate"],
  format=optimized.api_params["format"],
  output_directory=f"output/{project_name}/X10-AIGC音乐创作/"
)

# Step 5: Return to user
return {
  "status": "success",
  "music_file": result["file_path"],
  "optimization_details": optimized.optimization_notes
}
```

### Batch Processing Pattern

```python
# For processing multiple music requests in one session

batch_requests = [
  {"creative_brief": "火锅店背景音乐", "restaurant_type": "hotpot"},
  {"creative_brief": "西餐厅优雅音乐", "restaurant_type": "fine-dining"},
  {"creative_brief": "咖啡店温馨音乐", "restaurant_type": "cafe"}
]

optimizer = MusicPromptOptimizer()
optimized_batch = []

for req in batch_requests:
    try:
        opt = optimizer.optimize(req)
        optimized_batch.append({
          "status": "success",
          "request": req,
          "optimized": opt
        })
    except Exception as e:
        optimized_batch.append({
          "status": "error",
          "request": req,
          "error": str(e)
        })

# All optimized, ready for sequential API calls (remember: 1 concurrent limit!)
for item in optimized_batch:
    if item["status"] == "success":
        # Call API with rate limiting
        result = call_minimax_api(item["optimized"])
        time.sleep(2)  # Respect rate limits
```

## Testing & Quality Assurance

### Unit Test Examples

```python
import unittest
from optimizer import MusicPromptOptimizer

class TestMusicPromptOptimizer(unittest.TestCase):

    def setUp(self):
        self.optimizer = MusicPromptOptimizer()

    def test_simple_background_music(self):
        """Test basic instrumental background request."""
        result = self.optimizer.optimize("火锅店背景音乐")

        self.assertEqual(result.analysis["detected_scene"], "background")
        self.assertEqual(result.analysis["vocal_type"], "instrumental")
        self.assertEqual(result.lyrics, "")  # No lyrics for background
        self.assertGreaterEqual(len(result.prompt), 10)
        self.assertLessEqual(len(result.prompt), 300)

    def test_lyrics_formatting(self):
        """Test lyrics structure tag insertion."""
        result = self.optimizer.optimize({
          "creative_brief": "开业歌曲",
          "lyrics_draft": "火锅飘香迎客来\n麻辣鲜香味无穷"
        })

        self.assertIn("[Verse]", result.lyrics)
        self.assertGreaterEqual(len(result.lyrics), 10)
        self.assertLessEqual(len(result.lyrics), 600)

    def test_prompt_truncation(self):
        """Test prompt truncation to 300 chars."""
        long_brief = "我需要一首" + "非常" * 100 + "喜庆的音乐"

        result = self.optimizer.optimize(long_brief)

        self.assertLessEqual(len(result.prompt), 300)
        self.assertIn("Truncated prompt", " ".join(result.optimization_notes))

    def test_api_params_validation(self):
        """Test API parameter validation."""
        result = self.optimizer.optimize({
          "creative_brief": "火锅音乐",
          "technical_params": {
            "sample_rate": 99999,  # Invalid
            "bitrate": 128000      # Valid
          }
        })

        # Should fallback to valid default
        self.assertEqual(result.api_params["sample_rate"], 32000)
        self.assertEqual(result.api_params["bitrate"], 128000)

if __name__ == '__main__':
    unittest.main()
```

### Integration Test Workflow

```python
# Full end-to-end test with mock MiniMax API

def test_full_workflow():
    """Test complete X10 → Optimizer → MiniMax flow."""

    # Step 1: User request
    user_request = "轻快的川菜馆背景音乐,要有四川民乐特色"

    # Step 2: Optimize
    optimizer = MusicPromptOptimizer()
    optimized = optimizer.optimize({
      "creative_brief": user_request,
      "restaurant_type": "川菜",
      "music_purpose": "background"
    })

    # Assertions
    assert "Sichuan" in optimized.prompt or "Chinese folk" in optimized.prompt
    assert "instrumental" in optimized.prompt.lower()
    assert optimized.lyrics == ""
    assert 10 <= len(optimized.prompt) <= 300

    # Step 3: Validate for API
    api_params = optimizer.validate_for_api(optimized)

    assert "prompt" in api_params
    assert "lyrics" in api_params
    assert api_params["sample_rate"] in [16000, 24000, 32000, 44100]

    # Step 4: Mock API call (in real test, would call actual MiniMax)
    # mock_result = call_minimax_api(api_params)
    # assert mock_result["status"] == "success"

    print("✓ Full workflow test passed")
```

## Troubleshooting Guide

### Common Issues

**Issue 1: "Prompt length 8 outside valid range [10, 300]"**
- **Cause**: User input too short (e.g., "火锅")
- **Fix**: Optimizer should auto-expand with defaults
- **Code**: Check `_build_prompt()` padding logic

**Issue 2: "Lyrics length 5 outside valid range [10, 600]"**
- **Cause**: User provided very short lyrics
- **Fix**: Add warning note, but don't fail hard
- **Alternative**: Suggest instrumental mode if lyrics < 10 chars

**Issue 3: "Detected mood conflict"**
- **Cause**: Brief says "quiet" but mood_preference="energetic"
- **Fix**: Prioritize explicit parameters, log warning
- **Code**: Check `_analyze_intent()` conflict resolution

**Issue 4: "API returns empty music file"**
- **Cause**: MiniMax API issue or invalid prompt format
- **Fix**: Validate prompt meets all requirements (genre + mood + scene)
- **Debug**: Log full API request/response

**Issue 5: "Music doesn't match restaurant style"**
- **Cause**: Generic template used instead of restaurant-specific
- **Fix**: Ensure STYLE_KEYWORDS mapping includes all restaurant types
- **Enhancement**: Add more restaurant types to mapping

## Version History & Roadmap

### v1.0.0 (2025-10-30)
- ✅ Core prompt optimization engine
- ✅ Lyrics formatting with structure tags
- ✅ Restaurant industry templates (hotpot, fine-dining, cafe)
- ✅ API parameter validation
- ✅ X10 agent integration pattern

### Planned v1.1.0 (Q1 2026)
- 🔄 Support for MiniMax Music-02 (3-minute duration)
- 🔄 Voice reference audio optimization
- 🔄 Multi-language lyrics expansion (English, Japanese)
- 🔄 A/B testing framework for prompt variations
- 🔄 Real-time streaming mode support

### Planned v1.2.0 (Q2 2026)
- 🔄 Machine learning prompt quality scoring
- 🔄 Automatic genre classification from audio reference
- 🔄 Collaborative filtering for style recommendations
- 🔄 Integration with more restaurant types (fast-food, buffet, etc.)

## License & Attribution

**Author**: ZTL Digital Intelligence Operations Center - 创意组
**Version**: 1.0.0
**License**: MIT
**Documentation**: Based on MiniMax Music API official docs and community best practices

**Credits**:
- MiniMax (Hailuo AI) for Music Generation API
- 创意组 X10-AIGC音乐创作 agent for workflow integration
- ZTL Digital Operations Center for restaurant industry expertise
