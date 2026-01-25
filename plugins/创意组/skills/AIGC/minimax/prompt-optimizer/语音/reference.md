# MiniMax Voice Prompt Optimizer - Extended Reference

## Complete Voice Library (300+ Voices)

### Female Voice Categories

#### Young Female Voices (少女音)
- **female-shaonv** (少女): Young, energetic, cheerful. Best for: Store announcements, promotions
- **female-tianmei** (甜美): Sweet, gentle. Best for: Dessert shops, bakeries
- **female-qingxin** (清新): Fresh, natural. Best for: Cafes, health food stores

#### Mature Female Voices (御姐音)
- **female-yujie** (御姐): Mature, confident, professional. Best for: Business presentations
- **female-chengshu** (成熟): Sophisticated, elegant. Best for: Fine dining, luxury brands
- **female-zhishi** (知识): Intellectual, authoritative. Best for: Training, educational content

### Male Voice Categories

#### Calm Male Voices (清澈音)
- **male-qn-qingse** (清澈): Calm, clear, refined. Best for: Phone IVR, formal announcements
- **male-qn-jingying** (精英): Professional, trustworthy. Best for: Corporate messaging
- **male-qn-mone** (磁性): Deep, magnetic. Best for: Brand storytelling

#### Authoritative Male Voices (霸道音)
- **male-qn-badao** (霸道): Strong, commanding, authoritative. Best for: Leadership messages
- **male-qn-daxuesheng** (大学生): Young, vibrant. Best for: Youth-oriented campaigns
- **male-qn-chunhou** (淳厚): Warm, sincere. Best for: Family restaurants

### Audiobook Narrators
- **audiobook_male_1**: Professional male narrator, clear articulation. Best for: Training videos
- **audiobook_female_1**: Professional female narrator, engaging tone. Best for: Long-form content
- **audiobook_male_2**: Deep voice narrator, storytelling style. Best for: Brand history

### Character Voices
- **cute_boy** (可爱男孩): Cute, friendly, approachable. Best for: Fast food, children's menus
- **Charming_Lady** (迷人女士): Warm, charming, inviting. Best for: Romantic dining
- **warm_man** (温暖男声): Cozy, reassuring, comfortable. Best for: Cafes, lounges
- **energetic_girl** (活力女孩): High energy, exciting. Best for: Sports bars, event promotions

## Advanced Emotion Control

### Emotion Intensity Levels

MiniMax TTS supports nuanced emotion control through parameter combinations:

```yaml
Subtle Emotion (10-30% intensity):
  happy: speed=1.02, vol=1.05, pitch=+0
  sad: speed=0.98, vol=0.98, pitch=-1

Moderate Emotion (40-60% intensity):
  happy: speed=1.1, vol=1.2, pitch=+1
  sad: speed=0.9, vol=0.9, pitch=-2

Strong Emotion (70-100% intensity):
  happy: speed=1.2, vol=1.4, pitch=+3
  sad: speed=0.8, vol=0.8, pitch=-3
```

### Emotion Transitions

For dynamic content with emotion shifts:

```python
# Segment 1: Apology (sad)
segment1 = {
    "text": "本店因装修暂停营业,给您带来不便。",
    "emotion": "sad",
    "speed": 0.9,
    "vol": 0.9,
    "pitch": -2
}

# Segment 2: Announcement (neutral)
segment2 = {
    "text": "预计三天后恢复营业。",
    "emotion": "neutral",
    "speed": 1.0,
    "vol": 1.0,
    "pitch": 0
}

# Segment 3: Gratitude (happy)
segment3 = {
    "text": "感谢您的理解与支持!",
    "emotion": "happy",
    "speed": 1.05,
    "vol": 1.1,
    "pitch": +1
}
```

### Emotion Mixing Techniques

Combine multiple emotions for nuanced expression:

```yaml
Apologetic but Hopeful:
  Base emotion: sad (primary)
  Speed: 0.9 (slow, sincere)
  Volume: 1.0 (normal, clear)
  Pitch: -1 (slightly low, but not too sad)
  Text: "本店暂停营业,但很快回归,敬请期待。"

Excited but Professional:
  Base emotion: happy (primary)
  Speed: 1.05 (slightly fast, not rushed)
  Volume: 1.15 (elevated, but controlled)
  Pitch: +1 (friendly, not overly high)
  Text: "新品上市,欢迎品尝。"
```

## Voice Cloning Workflow

### Step-by-Step Guide

#### Step 1: Prepare Source Audio
```yaml
Requirements:
  - Duration: ≥10 seconds (recommended 15-30 seconds)
  - Format: WAV, MP3, FLAC
  - Quality: Clear voice, minimal background noise
  - Content: Natural speech, varied intonation
  - Sample rate: ≥16000 Hz

Good Examples:
  - Brand founder introduction video
  - CEO speech excerpt
  - Professional voice actor demo

Bad Examples:
  - Phone call recording (poor quality)
  - Music with vocals (background interference)
  - Robot TTS audio (unnatural)
```

#### Step 2: Call Voice Clone API
```python
result = mcp__minimax-mcp__voice_clone(
    voice_id="custom_hotpot_brand_voice",
    file="path/to/founder_voice.mp3",
    text="欢迎来到XX火锅店,正宗川味等您品尝",
    output_directory="output/voice_clones/"
)

# API processes for ~30 seconds
# Returns: cloned_voice_id
```

#### Step 3: Use Cloned Voice
```python
optimized = optimizer.optimize({
    "creative_brief": "新品上市,麻辣牛蛙,欢迎品尝",
    "voice_id": result["cloned_voice_id"],
    "emotion": "happy",
    "voice_purpose": "in-store"
})

audio = mcp__minimax-mcp__text_to_audio(
    text=optimized["text"],
    voice_id=optimized["voice_id"],
    emotion=optimized["emotion"]
)
```

#### Step 4: Quality Check
```yaml
Checklist:
  - [ ] Voice timbre matches source
  - [ ] Pronunciation is clear
  - [ ] Emotion is expressed naturally
  - [ ] No artifacts or glitches
  - [ ] Consistent quality across multiple generations

If quality is poor:
  - Retry with longer source audio
  - Improve source audio quality (denoise)
  - Use different source audio clip
```

### Voice Cloning Best Practices

```yaml
Use Cases:
  ✅ Brand spokesperson voice (CEO, founder)
  ✅ Signature character voice (mascot, host)
  ✅ Celebrity endorsement (with permission)
  ✅ Multilingual content (same voice, different languages)

Avoid:
  ❌ Mimicking real people without permission
  ❌ Using poor-quality source audio
  ❌ Cloning voices with heavy accents (may reduce clarity)
  ❌ Using for malicious purposes (deepfakes, fraud)
```

## Multi-Language Support

### Language Boost Configuration

```yaml
Chinese (Mandarin):
  language_boost: "Chinese"
  Best for: Mainland China restaurants
  Pronunciation: Standard Putonghua

Yue (Cantonese):
  language_boost: "Chinese,Yue"
  Best for: Hong Kong, Guangdong restaurants
  Pronunciation: Cantonese dialect

English (US):
  language_boost: "English"
  Best for: International chains, Western restaurants
  Pronunciation: American English

Mixed Language:
  language_boost: "auto"
  Best for: Bilingual content (e.g., "Welcome to XX火锅店")
  Auto-detects language per sentence
```

### Multilingual Example

```python
# English TVC
optimized_en = optimizer.optimize({
    "creative_brief": "Welcome to Sichuan Hotpot House, authentic flavors await you.",
    "language_boost": "English",
    "voice_id": "male-qn-jingying",
    "voice_purpose": "brand-tvc"
})

# Chinese equivalent (same voice timbre via cloning)
optimized_zh = optimizer.optimize({
    "creative_brief": "欢迎来到川味火锅,正宗川味等您品尝。",
    "language_boost": "Chinese",
    "voice_id": "custom_cloned_voice",
    "voice_purpose": "brand-tvc"
})
```

## Restaurant-Specific Templates

### Hotpot Restaurant Complete Pack

#### Welcome Announcement
```yaml
Scenario: Customer enters store
Text: "欢迎光临[店名]!今日特色锅底有麻辣牛油、清汤养生、菌菇山珍。"
Voice: female-shaonv (young, energetic)
Emotion: happy
Speed: 1.05
Volume: 1.3
Pitch: +2
Purpose: in-store broadcasting
```

#### Promotional Campaign
```yaml
Scenario: Limited-time discount
Text: "好消息!本店推出会员充值活动,充五百送一百,仅限本周!名额有限,先到先得!"
Voice: female-shaonv or cute_boy
Emotion: surprised
Speed: 1.15
Volume: 1.4
Pitch: +3
Purpose: in-store broadcasting
```

#### Safety Reminder
```yaml
Scenario: Hot pot safety warning
Text: "温馨提示:锅底温度较高,请小心烫伤。用餐时请注意安全。"
Voice: female-chengshu (mature, responsible)
Emotion: neutral
Speed: 0.95
Volume: 1.1
Pitch: 0
Purpose: in-store broadcasting
```

#### Closing Announcement
```yaml
Scenario: Store closing soon
Text: "各位顾客请注意,本店即将于晚上十点结束营业。请您合理安排用餐时间,感谢光临!"
Voice: female-yujie (mature, professional)
Emotion: neutral
Speed: 1.0
Volume: 1.2
Pitch: 0
Purpose: in-store broadcasting
```

### Fine Dining Complete Pack

#### Reservation Confirmation (Phone IVR)
```yaml
Text: "您好,您已成功预订[日期][时间]的[人数]位座位。我们期待您的光临,祝您用餐愉快。"
Voice: female-chengshu (elegant)
Emotion: neutral
Speed: 0.95
Volume: 1.0
Pitch: 0
Purpose: phone-ivr
```

#### Wine Recommendation (Ambient Background)
```yaml
Text: "本店精选法国波尔多红酒、意大利托斯卡纳白葡萄酒,为您的晚餐增添浪漫气息。"
Voice: male-qn-qingse (refined)
Emotion: neutral
Speed: 0.95
Volume: 0.9
Pitch: 0
Purpose: ambient background
```

#### Chef's Special Announcement
```yaml
Text: "主厨特别推荐:法式烩海鲜,精选时令海鲜,搭配白葡萄酒奶油汁,限量供应。"
Voice: male-qn-badao (authoritative)
Emotion: neutral
Speed: 1.0
Volume: 1.1
Pitch: +1
Purpose: in-store broadcasting
```

### Fast Food Complete Pack

#### Order Ready Notification
```yaml
Text: "[订单号],您的餐已准备好,请到取餐台领取。"
Voice: cute_boy (friendly)
Emotion: happy
Speed: 1.1
Volume: 1.3
Pitch: +2
Purpose: in-store broadcasting
```

#### Combo Deal Promotion
```yaml
Text: "超值套餐来啦!双人套餐只要三十九块九,包含汉堡、薯条、可乐。快来尝鲜!"
Voice: energetic_girl (high energy)
Emotion: surprised
Speed: 1.2
Volume: 1.4
Pitch: +3
Purpose: in-store broadcasting
```

#### Health & Safety Reminder
```yaml
Text: "请出示健康码,配合体温检测,感谢您的配合。"
Voice: female-yujie (professional)
Emotion: neutral
Speed: 1.0
Volume: 1.1
Pitch: 0
Purpose: in-store broadcasting
```

### Cafe Complete Pack

#### Morning Greeting
```yaml
Text: "早上好,欢迎来到[咖啡店名]。今日特饮是榛果拿铁,配巧克力可颂,享受美好清晨。"
Voice: warm_man (cozy)
Emotion: happy
Speed: 0.95
Volume: 0.9
Pitch: 0
Purpose: ambient background
```

#### Afternoon Special
```yaml
Text: "下午茶时光,推荐芒果冰沙配提拉米苏,让您度过惬意午后。"
Voice: Charming_Lady (warm)
Emotion: neutral
Speed: 1.0
Volume: 0.9
Pitch: 0
Purpose: ambient background
```

## Edge Case Handling

### Very Long Text
**Input**: 800-character promotional speech

**Strategy**: Automatic segmentation
```python
def segment_long_text(text, max_length=500):
    segments = []
    while len(text) > max_length:
        # Find natural breakpoint (punctuation)
        breakpoint = text.rfind("。", 0, max_length)
        if breakpoint == -1:
            breakpoint = text.rfind(",", 0, max_length)
        if breakpoint == -1:
            breakpoint = max_length

        segments.append(text[:breakpoint + 1])
        text = text[breakpoint + 1:]

    if text:
        segments.append(text)

    return segments
```

**Resolution**: Generate multiple audio files, then concatenate

### Mixed Language Text
**Input**: "Welcome to XX火锅店, 今日特价8.8折!"

**Strategy**: Set `language_boost="auto"` to auto-detect per sentence

**Result**: Natural pronunciation of both English and Chinese

### Homophone Ambiguity
**Input**: "本店有十几位厨师" (十几位 = more than ten OR distinguished chefs?)

**Strategy**: Contextual rewriting
```python
ambiguous_phrases = {
    "几位": "几个人",  # Clarify "how many"
    "几位客人": "几个客人",
    "几位厨师": "十多个厨师"
}
```

**Resolution**: "本店有十多个厨师"

### Extreme Prosody Values
**Input**: `speed=3.0, vol=15, pitch=+20`

**Strategy**: Automatic clamping
```python
validated_speed = max(0.5, min(speed, 2.0))
validated_vol = max(0.0, min(vol, 10.0))
validated_pitch = max(-12, min(pitch, 12))
```

**Resolution**: Clamp to valid ranges, log warning

## API Error Handling

### Common Errors

#### INVALID_VOICE_ID
```yaml
Error: Voice ID does not exist
Cause: Typo in voice_id or non-existent voice
Fix: Validate voice_id against VOICE_MAPPING, fallback to default
```

#### TEXT_TOO_LONG
```yaml
Error: Text exceeds 600 characters
Cause: Input text is too long for single TTS request
Fix: Segment text into multiple requests
```

#### UNSUPPORTED_EMOTION
```yaml
Error: Emotion not supported by model
Cause: Using emotion with speech-01 model (limited support)
Fix: Switch to speech-02-hd or speech-02-turbo, or use neutral emotion
```

#### VOICE_CLONE_FAILED
```yaml
Error: Voice cloning failed
Cause: Source audio too short or poor quality
Fix: Use longer, clearer source audio (≥15 seconds)
```

### Retry Strategy

```python
def call_with_retry(api_params, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = mcp__minimax-mcp__text_to_audio(**api_params)
            return result
        except Exception as e:
            error_msg = str(e)

            if "TEXT_TOO_LONG" in error_msg:
                # Segment text and retry
                segments = segment_long_text(api_params["text"])
                return [call_with_retry({**api_params, "text": seg}) for seg in segments]

            elif "INVALID_VOICE_ID" in error_msg:
                # Fallback to default voice
                api_params["voice_id"] = "female-shaonv"
                continue

            elif attempt < max_retries - 1:
                # Generic retry with backoff
                time.sleep(2 ** attempt)
                continue

            raise
```

## Performance Optimization

### Batch Generation Strategy
```python
# Efficient batch processing for multiple announcements
announcements = [
    "欢迎光临本店!",
    "今日特价火锅套餐八折优惠!",
    "营业时间为每日上午十一点至晚上十点。"
]

# Generate all in parallel (if API supports concurrent requests)
from concurrent.futures import ThreadPoolExecutor

def generate_audio(text):
    optimized = optimizer.optimize(text)
    return mcp__minimax-mcp__text_to_audio(**optimized["api_params"])

with ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(generate_audio, announcements))
```

### Prompt Caching
```python
# Cache restaurant-specific templates
template_cache = {
    "hotpot_welcome": {
        "voice_id": "female-shaonv",
        "emotion": "happy",
        "speed": 1.05,
        "vol": 1.3,
        "pitch": +2
    }
}

# Reuse cached config for similar requests
def optimize_with_cache(text, template_key):
    if template_key in template_cache:
        config = template_cache[template_key]
        optimized_text = optimizer._optimize_text(text)
        return {**config, "text": optimized_text}
    else:
        return optimizer.optimize(text)
```

## Troubleshooting

### Issue: "Voice sounds unnatural"
- **Check**: Punctuation and pauses in text
- **Check**: Speed is within 0.9-1.2 range
- **Fix**: Add commas and periods, slow down speed to 0.95-1.0

### Issue: "Emotion not expressed"
- **Cause**: Using speech-01 model (limited emotion support)
- **Fix**: Switch to speech-02-hd or speech-02-turbo

### Issue: "Audio too quiet"
- **Cause**: Volume set too low for purpose
- **Fix**: Increase `vol` to 1.2-1.5 for in-store broadcasting

### Issue: "Pronunciation errors"
- **Cause**: Homophone ambiguity or non-standard phrases
- **Fix**: Rewrite text for clarity, use standard Chinese

## Version History

- **v1.0.0** (2025-10-30): Initial release with all features

## License

**Author**: ZTL Digital Intelligence Operations Center - 创意组
**License**: MIT
