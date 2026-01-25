---
name: minimax-voice-prompt-optimizer
description: Optimizes user input prompts for MiniMax Text-to-Speech API (speech-02-hd) to produce natural, emotionally rich voice audio. Transforms creative briefs into structured TTS requests with voice selection, emotion control, prosody tuning, and technical parameter optimization. Specializes in restaurant industry voice applications (in-store broadcasting, phone IVR, brand TVC dubbing).
version: 1.0.0
author: ZTL Digital Intelligence Operations Center - 创意组
allowed-tools: ["Read", "Write"]
---

# MiniMax Voice Prompt Optimizer

## 📋 Overview

This skill optimizes prompts for MiniMax Text-to-Speech APIs (`mcp__minimax-mcp__text_to_audio`), transforming user creative intentions into technically precise voice generation requests that produce professional-quality, emotionally rich audio content.

**Supported Models**:
- **speech-02-hd**: Latest high-definition model with advanced emotion control
- **speech-02-turbo**: Fast generation with emotion support
- **speech-01-hd**: High-definition model (legacy)
- **speech-01-turbo**: Fast generation (legacy)

**Core Value**: Bridge the gap between creative vision ("I need an energetic store announcement") and technical API requirements (structured text + voice_id + emotion + prosody parameters).

## 🎯 Quick Start

```python
# Basic TTS usage
input = "欢迎光临本店,今日特价火锅套餐8.8折优惠!"
optimized = optimize_voice_prompt(input, voice_type="female", emotion="happy")
# Output: {
#   "model": "speech-02-hd",
#   "text": "欢迎光临本店!今日特价火锅套餐,八点八折优惠!",
#   "voice_id": "female-shaonv",
#   "emotion": "happy",
#   "speed": 1.0,
#   "vol": 1.2,
#   "pitch": 0
# }

# Advanced emotion control
input = "本店因装修暂停营业,给您带来不便敬请谅解"
optimized = optimize_voice_prompt(input, voice_type="male", emotion="sad", purpose="phone-ivr")
# Output: {
#   "text": "本店因装修暂停营业。给您带来不便,敬请谅解。",
#   "voice_id": "male-qn-qingse",
#   "emotion": "sad",
#   "speed": 0.9,
#   "vol": 0.9,
#   "pitch": -2
# }

# Voice cloning workflow
input = {
  "text": "欢迎来到XX火锅店,正宗川味等您品尝",
  "voice_clone_source": "path/to/brand_voice.mp3",
  "purpose": "brand-tvc"
}
optimized = optimize_voice_prompt(input, use_cloning=True)
# Output: {
#   "text": "欢迎来到XX火锅店,正宗川味等您品尝!",
#   "voice_id": "cloned_voice_123",
#   "emotion": "happy",
#   "language_boost": "Chinese"
# }
```

## 🎬 Core Capabilities

### 1. Model-Specific Optimization

**speech-02-hd (High-Definition)**:
- **Best for**: Professional dubbing, brand TVC, high-quality content
- **Emotion support**: 7 emotions (happy, sad, angry, fearful, disgusted, surprised, neutral)
- **Features**: Advanced prosody control, natural intonation, multi-language

**speech-02-turbo (Fast Generation)**:
- **Best for**: Real-time applications, in-store broadcasting, phone IVR
- **Emotion support**: 7 emotions
- **Features**: 3x faster than HD, still maintains natural quality

**speech-01-hd (Legacy HD)**:
- **Best for**: Stable production environments
- **Emotion support**: Limited (happy, neutral)
- **Features**: Proven reliability, backward compatibility

### 2. Voice Selection System (300+ Voices)

**Voice Categories**:

| Category | Voice IDs | Use Case |
|----------|-----------|----------|
| **Female Young** | `female-shaonv`, `female-yujie`, `female-chengshu` | Store announcements, promotional content |
| **Male Mature** | `male-qn-qingse`, `male-qn-jingying`, `male-qn-badao` | Brand dubbing, authority messaging |
| **Audiobook** | `audiobook_male_1`, `audiobook_female_1` | Long-form content, storytelling |
| **Character** | `cute_boy`, `Charming_Lady`, `warm_man` | Themed restaurants, special campaigns |

**Voice Selection Logic**:
```yaml
Restaurant Type → Voice Mapping:
  火锅店 (Hotpot):
    - Primary: female-shaonv (young, energetic)
    - Secondary: male-qn-jingying (mature, trustworthy)

  西餐厅 (Fine Dining):
    - Primary: female-chengshu (elegant, sophisticated)
    - Secondary: male-qn-qingse (refined, calm)

  快餐店 (Fast Food):
    - Primary: cute_boy (friendly, approachable)
    - Secondary: female-yujie (professional, efficient)

  咖啡厅 (Cafe):
    - Primary: warm_man (cozy, relaxing)
    - Secondary: Charming_Lady (warm, inviting)
```

### 3. Emotion Control System

**7 Emotion Types**:

| Emotion | Chinese | Use Case | Speed | Volume | Pitch |
|---------|---------|----------|-------|--------|-------|
| **happy** | 开心 | Promotions, celebrations, welcome messages | 1.1 | 1.2 | +1 |
| **sad** | 悲伤 | Apologies, closure notices, condolences | 0.9 | 0.9 | -2 |
| **angry** | 愤怒 | Urgent warnings, emergency alerts | 1.0 | 1.3 | +2 |
| **fearful** | 恐惧 | Safety warnings, cautionary messages | 0.95 | 1.0 | 0 |
| **disgusted** | 厌恶 | Quality complaints, rejection statements | 1.0 | 1.0 | -1 |
| **surprised** | 惊喜 | Surprise announcements, special reveals | 1.15 | 1.25 | +3 |
| **neutral** | 中性 | Standard information, routine announcements | 1.0 | 1.0 | 0 |

**Emotion Detection from Text**:
```python
emotion_keywords = {
    "happy": ["欢迎", "恭喜", "祝贺", "特价", "优惠", "开业", "庆祝"],
    "sad": ["抱歉", "遗憾", "暂停", "关闭", "不便", "道歉"],
    "angry": ["警告", "禁止", "严禁", "立即", "紧急"],
    "surprised": ["惊喜", "特大", "超值", "限时", "爆款"]
}
```

### 4. Prosody Tuning System

**Speed Control** (`speed: 0.5 - 2.0`):
- **0.5 - 0.8**: Slow, dramatic, emphasizing important information
- **0.9 - 1.1**: Natural conversational speed (recommended)
- **1.2 - 2.0**: Fast, energetic, attention-grabbing

**Volume Control** (`vol: 0 - 10`):
- **0.5 - 0.8**: Soft, intimate, background ambiance
- **0.9 - 1.2**: Normal speaking volume (recommended)
- **1.3 - 2.0**: Loud, commanding, in-store broadcasting

**Pitch Control** (`pitch: -12 to +12`):
- **-12 to -5**: Very low, authoritative, serious
- **-4 to -1**: Slightly low, calm, professional
- **0**: Natural pitch (default)
- **+1 to +4**: Slightly high, friendly, approachable
- **+5 to +12**: Very high, cute, childlike

### 5. Precise Prompt Formula

#### Text-to-Speech Structure:
```
Optimized Text + Voice Selection + Emotion Mapping + Prosody Tuning + Technical Parameters
```

**Example**:
```
Text: "欢迎光临本店!今日特价火锅套餐,八点八折优惠!"
Voice: female-shaonv (young female, energetic)
Emotion: happy (promotional excitement)
Speed: 1.1 (slightly faster, energetic)
Volume: 1.2 (louder for attention)
Pitch: +1 (friendly, approachable)
Format: mp3, 32000 Hz sample rate
```

#### Voice Cloning Structure:
```
Source Audio (≥10s) → Clone Training → Cloned Voice ID + Text + Emotion
```

**Example**:
```
Source: brand_founder_voice.mp3 (15 seconds)
Clone Training: ~30 seconds processing
Cloned Voice: custom_voice_abc123
Text: "欢迎来到XX火锅店,正宗川味等您品尝!"
Emotion: happy
Usage: Brand TVC dubbing, store announcements
```

### 6. Restaurant Industry Specialization

#### In-Store Broadcasting (店内广播)
```yaml
Model: speech-02-turbo (real-time generation)
Voice: female-shaonv (young, energetic)
Emotion: happy or surprised
Speed: 1.0 - 1.1 (natural to slightly fast)
Volume: 1.2 - 1.5 (louder for public space)

Template:
  Welcome: "欢迎光临[店名]![停顿]今日特色菜品有[菜名1]、[菜名2]。"
  Promotion: "好消息![停顿]本店[活动内容],仅限今日,欢迎品尝!"
  Closing: "各位顾客请注意,[停顿]本店即将于[时间]结束营业,请您合理安排用餐时间。"

Examples:
  - Welcome: "欢迎光临川味小馆!今日特色菜品有麻辣牛蛙、泉水鱼、手撕包菜。"
  - Promotion: "好消息!本店啤酒买二送一,仅限今日,欢迎品尝!"
  - Closing: "各位顾客请注意,本店即将于晚上十点结束营业,请您合理安排用餐时间。"
```

#### Phone IVR (电话语音)
```yaml
Model: speech-02-hd (high quality)
Voice: female-chengshu or male-qn-qingse (professional)
Emotion: neutral (standard information)
Speed: 0.9 - 1.0 (clear, understandable)
Volume: 1.0 (normal speaking level)
Pitch: 0 (natural pitch)

Template:
  Greeting: "您好,欢迎致电[店名]。[停顿]营业时间为每日[时间段]。"
  Menu: "如需预订座位,请按1;[停顿]如需外卖服务,请按2;[停顿]如需了解菜单,请按3。"
  Busy: "您好,客服人员正在忙碌中,[停顿]请稍后再拨,感谢您的耐心等待。"
  Closed: "本店因[原因]暂停营业,[停顿]给您带来不便,敬请谅解。恢复营业时间将另行通知。"

Examples:
  - Greeting: "您好,欢迎致电巴蜀火锅。营业时间为每日上午十一点至晚上十点。"
  - Busy: "您好,客服人员正在忙碌中,请稍后再拨,感谢您的耐心等待。"
```

#### Brand TVC Dubbing (品牌广告配音)
```yaml
Model: speech-02-hd (highest quality)
Voice: Custom cloned voice (brand spokesperson) or male-qn-badao (authoritative)
Emotion: happy or surprised (engaging)
Speed: 1.0 (natural, clear)
Volume: 1.1 (slightly elevated)
Pitch: 0 to +1 (natural to slightly warm)

Template:
  Brand Story: "[品牌名],始于[年份],[停顿]专注[核心价值],为您带来[独特体验]。"
  Product Highlight: "[产品名],[停顿]精选[食材特点],匠心[制作工艺],[停顿]只为一口[味觉体验]。"
  Call-to-Action: "立即预订,[停顿]享受[优惠内容]。[品牌名],期待您的光临!"

Examples:
  - Brand Story: "川味小馆,始于一九九八年,专注正宗川菜二十五年,为您带来地道巴蜀风味。"
  - Product Highlight: "麻辣牛蛙,精选本地活蛙,匠心秘制辣椒酱,只为一口鲜香麻辣。"
  - Call-to-Action: "立即预订,享受八折优惠。川味小馆,期待您的光临!"
```

#### Employee Training Narration (员工培训旁白)
```yaml
Model: speech-02-hd (clear articulation)
Voice: audiobook_male_1 or audiobook_female_1 (professional narrator)
Emotion: neutral (educational tone)
Speed: 0.9 - 1.0 (clear, easy to follow)
Volume: 1.0 (normal)
Pitch: 0 (natural)

Template:
  Introduction: "欢迎参加[主题]培训。[停顿]本次课程将涵盖[内容要点]。"
  Section: "第[序号]部分:[标题]。[停顿][详细内容]。"
  Emphasis: "请注意,[停顿][重点内容]。这是服务质量的关键要素。"
  Summary: "本次培训总结:[停顿][要点1]、[要点2]、[要点3]。请在实际工作中认真践行。"

Examples:
  - Introduction: "欢迎参加火锅店服务流程培训。本次课程将涵盖迎宾礼仪、点菜技巧、餐中服务、结账送客四大环节。"
  - Emphasis: "请注意,客人入座后,需在三十秒内递上热毛巾和茶水。这是服务质量的关键要素。"
```

#### Background Music Narration (背景音乐旁白)
```yaml
Model: speech-02-hd (natural voice)
Voice: warm_man or Charming_Lady (warm, friendly)
Emotion: happy or neutral (relaxed)
Speed: 0.95 - 1.0 (slow, soothing)
Volume: 0.8 - 1.0 (softer, background level)
Pitch: 0 to -1 (natural to slightly calm)

Template:
  Ambient: "[品牌名],[停顿]为您营造舒适用餐氛围。[停顿]愿您享受美好时光。"
  Seasonal: "[季节]来临,[停顿][品牌名]特别推出[季节主题菜品],[停顿]与您共度[季节特点]。"

Examples:
  - Ambient: "川味小馆,为您营造舒适用餐氛围。愿您享受美好时光。"
  - Seasonal: "春天来临,川味小馆特别推出春季养生火锅,与您共度温暖春日。"
```

## 🔧 API Integration Points

### Input Schema
```python
{
  "creative_brief": str,         # Required: Raw user request
  "model": str,                  # Optional: speech-02-hd / speech-02-turbo / speech-01-hd / speech-01-turbo
  "voice_type": str,             # Optional: female / male / audiobook / character
  "voice_id": str,               # Optional: Specific voice ID (overrides voice_type)
  "restaurant_type": str,        # Optional: hotpot, fine-dining, fast-food, cafe
  "voice_purpose": str,          # Optional: in-store, phone-ivr, brand-tvc, training, ambient
  "emotion_preference": str,     # Optional: happy, sad, angry, fearful, disgusted, surprised, neutral
  "speed": float,                # Optional: 0.5 - 2.0 (default 1.0)
  "vol": float,                  # Optional: 0 - 10 (default 1.0)
  "pitch": int,                  # Optional: -12 to +12 (default 0)
  "format": str,                 # Optional: mp3, pcm, flac, wav (default mp3)
  "sample_rate": int,            # Optional: 8000, 16000, 22050, 24000, 32000, 44100 (default 32000)
  "bitrate": int,                # Optional: 32000, 64000, 128000, 256000 (default 128000)
  "language_boost": str,         # Optional: Chinese, English, auto, etc. (default auto)
  "voice_clone_source": str,     # Optional: Path to source audio for cloning
  "use_cloning": bool            # Optional: Whether to use voice cloning workflow
}
```

### Output Schema
```python
{
  "model": str,                  # Selected model (speech-02-hd / speech-02-turbo)
  "text": str,                   # Optimized text with punctuation and pauses
  "voice_id": str,               # Selected voice ID
  "emotion": str,                # Detected or specified emotion
  "speed": float,                # Optimized speech speed
  "vol": float,                  # Optimized volume
  "pitch": int,                  # Optimized pitch
  "format": str,                 # Audio format (mp3, pcm, flac, wav)
  "sample_rate": int,            # Sample rate (8000-44100)
  "bitrate": int,                # Bitrate (32000-256000)
  "channel": int,                # Audio channels (1 or 2)
  "language_boost": str,         # Language optimization
  "analysis": {
    "detected_purpose": str,     # in-store / phone-ivr / brand-tvc / training / ambient
    "detected_emotion": str,     # Emotion detected from text
    "restaurant_context": str,   # Restaurant type context
    "text_length": int,          # Character count
    "estimated_duration": float  # Estimated audio duration (seconds)
  },
  "api_params": {
    "model": str,
    "text": str,
    "voice_id": str,
    "emotion": str,
    "speed": float,
    "vol": float,
    "pitch": int,
    "format": str,
    "sample_rate": int,
    "bitrate": int,
    "channel": int,
    "language_boost": str,
    "output_directory": str
  },
  "optimization_notes": list[str]
}
```

## 📚 Best Practices

### Voice Selection Guidelines

#### 1. Match Voice to Purpose
- **In-Store Broadcasting**: Young, energetic voices (female-shaonv, cute_boy)
- **Phone IVR**: Professional, mature voices (female-chengshu, male-qn-qingse)
- **Brand TVC**: Custom cloned voices or authoritative voices (male-qn-badao)
- **Training Narration**: Audiobook voices (audiobook_male_1, audiobook_female_1)
- **Ambient Background**: Warm, soothing voices (warm_man, Charming_Lady)

#### 2. Match Voice to Restaurant Type
- **Hotpot/Chinese**: Female young voices with energy (female-shaonv)
- **Fine Dining**: Mature, sophisticated voices (female-chengshu)
- **Fast Food**: Friendly, approachable voices (cute_boy)
- **Cafe**: Warm, relaxing voices (warm_man)

### Text Optimization Principles

#### 1. Punctuation for Natural Pauses
- ❌ Raw: "欢迎光临本店今日特价火锅套餐8.8折优惠"
- ✅ Optimized: "欢迎光临本店!今日特价火锅套餐,八点八折优惠!"

**Key Rules**:
- Use `!` for excitement and emphasis
- Use `,` for natural breath pauses
- Use `。` for sentence endings
- Use `[停顿]` for explicit pauses (converted to `...` or silence)

#### 2. Number Conversion
- ❌ Digits: "8.8折", "12:00", "100元"
- ✅ Chinese: "八点八折", "十二点", "一百元"

**Why**: TTS reads Chinese characters more naturally than digits

#### 3. Simplified Language
- ❌ Complex: "本店因装修升级改造工程需要暂时停止对外营业"
- ✅ Simple: "本店因装修暂停营业"

**Why**: Short sentences are clearer and easier to understand

#### 4. Avoid Homophone Ambiguity
- ❌ "请问您几位" (几位 = how many people OR distinguished guests?)
- ✅ "请问您一共有几位客人"

### Emotion Mapping Logic

#### 1. Keyword-Based Detection
```python
emotion_detection = {
    "happy": ["欢迎", "恭喜", "祝贺", "特价", "优惠", "开业", "庆祝", "好消息"],
    "sad": ["抱歉", "遗憾", "暂停", "关闭", "不便", "道歉", "失望"],
    "angry": ["警告", "禁止", "严禁", "立即", "紧急", "注意"],
    "surprised": ["惊喜", "特大", "超值", "限时", "爆款", "震撼"],
    "neutral": ["通知", "信息", "查询", "预订", "营业时间"]
}
```

#### 2. Context-Aware Adjustments
- **Promotions → happy + increased speed + higher volume**
- **Apologies → sad + decreased speed + softer volume**
- **Warnings → angry or fearful + normal speed + increased volume**
- **Standard Info → neutral + normal all parameters**

### Prosody Tuning Strategy

#### 1. Speed Adjustments
```yaml
Purpose-Based Speed:
  in-store broadcasting: 1.0 - 1.1 (slightly fast for attention)
  phone-ivr: 0.9 - 1.0 (clear, understandable)
  brand-tvc: 1.0 (natural, professional)
  training: 0.9 - 1.0 (clear, easy to follow)
  ambient: 0.95 - 1.0 (slow, soothing)

Emotion-Based Speed:
  happy: 1.05 - 1.15 (energetic)
  sad: 0.85 - 0.95 (slow, somber)
  angry: 1.0 (normal, controlled)
  surprised: 1.1 - 1.2 (fast, excited)
  neutral: 1.0 (natural)
```

#### 2. Volume Adjustments
```yaml
Purpose-Based Volume:
  in-store broadcasting: 1.2 - 1.5 (loud, public space)
  phone-ivr: 1.0 (normal, clear)
  brand-tvc: 1.1 (slightly elevated)
  training: 1.0 (normal)
  ambient: 0.8 - 1.0 (soft, background)

Emotion-Based Volume:
  happy: 1.1 - 1.3 (louder, exciting)
  sad: 0.9 - 1.0 (softer, subdued)
  angry: 1.3 - 1.5 (loud, commanding)
  surprised: 1.2 - 1.4 (loud, shocking)
  neutral: 1.0 (normal)
```

#### 3. Pitch Adjustments
```yaml
Purpose-Based Pitch:
  in-store broadcasting: +1 to +2 (friendly)
  phone-ivr: 0 (natural)
  brand-tvc: 0 to +1 (natural to warm)
  training: 0 (natural)
  ambient: 0 to -1 (natural to calm)

Emotion-Based Pitch:
  happy: +1 to +3 (higher, cheerful)
  sad: -2 to -3 (lower, somber)
  angry: +2 to +3 (higher, intense)
  surprised: +3 to +4 (highest, shocked)
  neutral: 0 (natural)
```

### Common Pitfalls to Avoid

1. **❌ Too Long Text**
   - Single TTS request should be < 600 characters
   - **Fix**: Split into multiple shorter segments

2. **❌ Missing Punctuation**
   - No pauses makes speech robotic
   - **Fix**: Add commas, periods, exclamation marks

3. **❌ Extreme Parameter Values**
   - speed=2.0, vol=10, pitch=+12 sound unnatural
   - **Fix**: Keep parameters within reasonable ranges (speed: 0.9-1.2, vol: 0.8-1.5, pitch: -2 to +3)

4. **❌ Wrong Voice for Context**
   - Using cute_boy for funeral announcements
   - **Fix**: Match voice personality to content tone

5. **❌ Ignoring Language Boost**
   - Mixing Chinese and English without language_boost
   - **Fix**: Set language_boost to "Chinese" or "auto"

## 🚀 Workflow Integration

### Step 1: Receive Input
```python
# From X12-AIGC语音合成 agent
raw_input = {
  "creative_brief": "火锅店开业大酬宾,全场8.8折,欢迎品尝!",
  "restaurant_type": "hotpot",
  "voice_purpose": "in-store"
}
```

### Step 2: Analyze & Select Voice
```python
from scripts.optimizer import VoicePromptOptimizer

optimizer = VoicePromptOptimizer()

# Optimizer decides:
# - Purpose: in-store → energetic, loud
# - Emotion: "优惠", "欢迎" → happy
# - Voice: hotpot → female-shaonv (young, energetic)
```

### Step 3: Optimize Prompt
```python
optimized = optimizer.optimize(raw_input)

# Output:
# {
#   "model": "speech-02-turbo",
#   "text": "火锅店开业大酬宾!全场八点八折,欢迎品尝!",
#   "voice_id": "female-shaonv",
#   "emotion": "happy",
#   "speed": 1.1,
#   "vol": 1.3,
#   "pitch": +2
# }
```

### Step 4: Validate & Call API
```python
validated = optimizer.validate_for_api(optimized)

result = mcp__minimax-mcp__text_to_audio(
  text=validated["text"],
  voice_id=validated["voice_id"],
  model=validated["model"],
  emotion=validated["emotion"],
  speed=validated["speed"],
  vol=validated["vol"],
  pitch=validated["pitch"],
  format="mp3",
  sample_rate=32000,
  bitrate=128000,
  output_directory=f"output/{project_name}/X12-AIGC语音合成/"
)
```

### Step 5: Return Results
```python
# X12 agent receives audio file
return {
  "status": "success",
  "audio_file": result["file_path"],
  "optimization_details": optimized["optimization_notes"],
  "voice_used": optimized["voice_id"],
  "emotion_applied": optimized["emotion"]
}
```

## 🧪 Testing & Quality Assurance

### Validation Checklist
```yaml
Text Quality:
  - [ ] Punctuation added for natural pauses
  - [ ] Numbers converted to Chinese characters
  - [ ] Text length ≤ 600 characters
  - [ ] Language is simplified and clear
  - [ ] Homophone ambiguity resolved

Voice Selection:
  - [ ] Voice matches purpose (in-store, phone-ivr, etc.)
  - [ ] Voice matches restaurant type
  - [ ] Voice matches content tone
  - [ ] Voice ID is valid (300+ available)

Emotion Mapping:
  - [ ] Emotion detected from keywords
  - [ ] Emotion matches content tone
  - [ ] Emotion is supported by model (speech-02 series)
  - [ ] Prosody parameters adjusted accordingly

Technical Params:
  - [ ] Speed: 0.5 - 2.0 (recommended 0.9 - 1.2)
  - [ ] Volume: 0 - 10 (recommended 0.8 - 1.5)
  - [ ] Pitch: -12 to +12 (recommended -2 to +3)
  - [ ] Format: mp3, pcm, flac, or wav
  - [ ] Sample rate: 8000 - 44100 Hz
  - [ ] Bitrate: 32000 - 256000

Restaurant Fit:
  - [ ] Content matches restaurant type
  - [ ] Tone appropriate for brand
  - [ ] Audio suitable for intended use case
```

## 📖 Extended Documentation

See `reference.md` for:
- Complete MiniMax TTS API specification
- All 300+ voice IDs with descriptions
- Advanced emotion control techniques (LoRA fine-tuning)
- Voice cloning workflow step-by-step
- Multi-language support details
- Edge case handling (extreme texts, mixed languages)
- Performance optimization tips
- Troubleshooting guide

## 🔗 Related Components

- **X12-AIGC语音合成 Agent**: Primary consumer of this skill
- **minimax-mcp**: MCP server providing `text_to_audio`, `voice_clone`, `voice_design` tools
- **Output Convention**: `output/[项目名]/X12-AIGC语音合成/`

## 📝 Version History

- **v1.0.0** (2025-10-30): Initial release
  - Support for speech-02-hd and speech-02-turbo models
  - 300+ voice selection system
  - 7 emotion control types
  - Restaurant industry templates
  - Prosody tuning optimization
  - Voice cloning workflow support
  - Text optimization engine
  - API parameter validation
