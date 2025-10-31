#!/usr/bin/env python3
"""
MiniMax Voice Prompt Optimizer
Transforms creative briefs into optimized MiniMax TTS API prompts.

Author: ZTL Digital Intelligence Operations Center - 创意组
Version: 1.0.0
"""

import re
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, asdict


@dataclass
class VoicePromptInput:
    """Input schema for voice prompt optimization."""
    creative_brief: str
    model: Optional[str] = "speech-02-hd"  # speech-02-hd, speech-02-turbo, speech-01-hd, speech-01-turbo
    voice_type: Optional[str] = None  # female, male, audiobook, character
    voice_id: Optional[str] = None  # Specific voice ID (overrides voice_type)
    restaurant_type: Optional[str] = None  # hotpot, fine-dining, fast-food, cafe
    voice_purpose: Optional[str] = None  # in-store, phone-ivr, brand-tvc, training, ambient
    emotion_preference: Optional[str] = None  # happy, sad, angry, fearful, disgusted, surprised, neutral
    speed: Optional[float] = None  # 0.5 - 2.0
    vol: Optional[float] = None  # 0 - 10
    pitch: Optional[int] = None  # -12 to +12
    format: Optional[str] = "mp3"  # mp3, pcm, flac, wav
    sample_rate: Optional[int] = 32000  # 8000, 16000, 22050, 24000, 32000, 44100
    bitrate: Optional[int] = 128000  # 32000, 64000, 128000, 256000
    language_boost: Optional[str] = "auto"  # Chinese, English, auto, etc.
    voice_clone_source: Optional[str] = None  # Path to source audio for cloning
    use_cloning: bool = False


@dataclass
class OptimizedVoiceOutput:
    """Output schema for optimized voice prompt."""
    model: str
    text: str
    voice_id: str
    emotion: str
    speed: float
    vol: float
    pitch: int
    format: str
    sample_rate: int
    bitrate: int
    channel: int
    language_boost: str
    analysis: Dict[str, Union[str, int, float]]
    api_params: Dict
    optimization_notes: List[str]


class VoicePromptOptimizer:
    """Core optimizer for MiniMax TTS API prompts."""

    # Voice selection mapping
    VOICE_MAPPING = {
        "female": {
            "young": "female-shaonv",
            "mature": "female-yujie",
            "sophisticated": "female-chengshu"
        },
        "male": {
            "calm": "male-qn-qingse",
            "professional": "male-qn-jingying",
            "authoritative": "male-qn-badao"
        },
        "audiobook": {
            "male": "audiobook_male_1",
            "female": "audiobook_female_1"
        },
        "character": {
            "cute": "cute_boy",
            "charming": "Charming_Lady",
            "warm": "warm_man"
        }
    }

    # Restaurant type to voice mapping
    RESTAURANT_VOICE_MAPPING = {
        "hotpot": ("female", "young"),  # Energetic
        "fine-dining": ("female", "sophisticated"),  # Elegant
        "fast-food": ("character", "cute"),  # Friendly
        "cafe": ("character", "warm")  # Cozy
    }

    # Purpose-specific voice preferences
    PURPOSE_VOICE_MAPPING = {
        "in-store": ("female", "young"),  # Energetic
        "phone-ivr": ("female", "mature"),  # Professional
        "brand-tvc": ("male", "authoritative"),  # Authority
        "training": ("audiobook", "male"),  # Clear narrator
        "ambient": ("character", "warm")  # Soothing
    }

    # Emotion keywords detection
    EMOTION_KEYWORDS = {
        "happy": ["欢迎", "恭喜", "祝贺", "特价", "优惠", "开业", "庆祝", "好消息"],
        "sad": ["抱歉", "遗憾", "暂停", "关闭", "不便", "道歉", "失望"],
        "angry": ["警告", "禁止", "严禁", "立即", "紧急", "注意"],
        "surprised": ["惊喜", "特大", "超值", "限时", "爆款", "震撼"],
        "neutral": ["通知", "信息", "查询", "预订", "营业时间"]
    }

    # Emotion-based prosody defaults
    EMOTION_PROSODY = {
        "happy": {"speed": 1.1, "vol": 1.2, "pitch": +1},
        "sad": {"speed": 0.9, "vol": 0.9, "pitch": -2},
        "angry": {"speed": 1.0, "vol": 1.3, "pitch": +2},
        "fearful": {"speed": 0.95, "vol": 1.0, "pitch": 0},
        "disgusted": {"speed": 1.0, "vol": 1.0, "pitch": -1},
        "surprised": {"speed": 1.15, "vol": 1.25, "pitch": +3},
        "neutral": {"speed": 1.0, "vol": 1.0, "pitch": 0}
    }

    # Purpose-based prosody adjustments
    PURPOSE_PROSODY = {
        "in-store": {"speed_range": (1.0, 1.1), "vol_range": (1.2, 1.5)},
        "phone-ivr": {"speed_range": (0.9, 1.0), "vol_range": (1.0, 1.0)},
        "brand-tvc": {"speed_range": (1.0, 1.0), "vol_range": (1.1, 1.1)},
        "training": {"speed_range": (0.9, 1.0), "vol_range": (1.0, 1.0)},
        "ambient": {"speed_range": (0.95, 1.0), "vol_range": (0.8, 1.0)}
    }

    def __init__(self):
        self.notes = []

    def optimize(self, input_data: Union[Dict, VoicePromptInput, str]) -> OptimizedVoiceOutput:
        """Main optimization entry point."""
        self.notes = []

        # Normalize input
        if isinstance(input_data, str):
            input_obj = VoicePromptInput(creative_brief=input_data)
        elif isinstance(input_data, dict):
            input_obj = VoicePromptInput(**input_data)
        else:
            input_obj = input_data

        # Step 1: Analyze intent
        analysis = self._analyze_intent(input_obj)

        # Step 2: Select voice
        voice_id = self._select_voice(input_obj, analysis)

        # Step 3: Optimize text
        optimized_text = self._optimize_text(input_obj.creative_brief)

        # Step 4: Determine emotion
        emotion = self._determine_emotion(input_obj, analysis)

        # Step 5: Set prosody parameters
        prosody = self._set_prosody(input_obj, emotion, analysis)

        # Step 6: Build API parameters
        api_params = self._build_api_params(input_obj, voice_id, optimized_text, emotion, prosody)

        # Step 7: Estimate duration
        estimated_duration = self._estimate_duration(optimized_text, prosody["speed"])

        return OptimizedVoiceOutput(
            model=input_obj.model,
            text=optimized_text,
            voice_id=voice_id,
            emotion=emotion,
            speed=prosody["speed"],
            vol=prosody["vol"],
            pitch=prosody["pitch"],
            format=input_obj.format,
            sample_rate=input_obj.sample_rate,
            bitrate=input_obj.bitrate,
            channel=1,  # Mono by default
            language_boost=input_obj.language_boost,
            analysis={
                "detected_purpose": analysis["detected_purpose"],
                "detected_emotion": analysis["detected_emotion"],
                "restaurant_context": input_obj.restaurant_type or "general",
                "text_length": len(optimized_text),
                "estimated_duration": estimated_duration
            },
            api_params=api_params,
            optimization_notes=self.notes.copy()
        )

    def _analyze_intent(self, input_obj: VoicePromptInput) -> Dict:
        """Analyze creative brief to extract key elements."""
        brief = input_obj.creative_brief.lower()

        # Detect purpose
        detected_purpose = input_obj.voice_purpose or "in-store"
        if "电话" in brief or "ivr" in brief or "预订" in brief:
            detected_purpose = "phone-ivr"
        elif "广告" in brief or "tvc" in brief or "宣传" in brief:
            detected_purpose = "brand-tvc"
        elif "培训" in brief or "学习" in brief or "教学" in brief:
            detected_purpose = "training"
        elif "背景" in brief or "氛围" in brief:
            detected_purpose = "ambient"
        elif "播报" in brief or "广播" in brief or "通知" in brief:
            detected_purpose = "in-store"

        # Detect emotion from keywords
        detected_emotion = "neutral"
        for emotion, keywords in self.EMOTION_KEYWORDS.items():
            if any(keyword in brief for keyword in keywords):
                detected_emotion = emotion
                break

        return {
            "detected_purpose": detected_purpose,
            "detected_emotion": detected_emotion
        }

    def _select_voice(self, input_obj: VoicePromptInput, analysis: Dict) -> str:
        """Select optimal voice based on input."""
        # If voice_id explicitly specified, use it
        if input_obj.voice_id:
            self.notes.append(f"Using user-specified voice: {input_obj.voice_id}")
            return input_obj.voice_id

        # Auto-select based on priority: purpose > restaurant_type > voice_type
        voice_category = None
        voice_subcategory = None

        # Priority 1: Purpose
        if input_obj.voice_purpose or analysis["detected_purpose"]:
            purpose = input_obj.voice_purpose or analysis["detected_purpose"]
            voice_category, voice_subcategory = self.PURPOSE_VOICE_MAPPING.get(
                purpose, ("female", "young")
            )
            self.notes.append(f"Voice selected by purpose: {purpose}")

        # Priority 2: Restaurant type (if no purpose or override)
        elif input_obj.restaurant_type:
            voice_category, voice_subcategory = self.RESTAURANT_VOICE_MAPPING.get(
                input_obj.restaurant_type, ("female", "young")
            )
            self.notes.append(f"Voice selected by restaurant type: {input_obj.restaurant_type}")

        # Priority 3: Voice type
        elif input_obj.voice_type:
            voice_category = input_obj.voice_type
            voice_subcategory = "young" if voice_category == "female" else "calm"
            self.notes.append(f"Voice selected by voice type: {input_obj.voice_type}")

        # Default fallback
        else:
            voice_category, voice_subcategory = ("female", "young")
            self.notes.append("Using default voice: female-shaonv")

        # Map to actual voice ID
        if voice_category in self.VOICE_MAPPING:
            voice_id = self.VOICE_MAPPING[voice_category].get(
                voice_subcategory,
                list(self.VOICE_MAPPING[voice_category].values())[0]
            )
        else:
            voice_id = "female-shaonv"  # Ultimate fallback

        return voice_id

    def _optimize_text(self, raw_text: str) -> str:
        """Optimize text for natural TTS."""
        text = raw_text.strip()

        # Step 1: Convert numbers to Chinese characters
        text = self._convert_numbers_to_chinese(text)

        # Step 2: Add punctuation for natural pauses
        text = self._add_punctuation(text)

        # Step 3: Simplify complex sentences
        # (This is context-dependent, so we'll keep it simple for now)

        # Step 4: Limit length
        if len(text) > 600:
            self.notes.append(f"Text truncated from {len(text)} to 600 characters")
            text = text[:600]

        return text

    def _convert_numbers_to_chinese(self, text: str) -> str:
        """Convert Arabic numerals to Chinese characters."""
        # Simple conversion for common patterns
        conversions = {
            "8.8": "八点八",
            "9.9": "九点九",
            "12:00": "十二点",
            "18:00": "十八点",
            "100": "一百",
            "200": "两百",
            "50": "五十",
            "80": "八十"
        }

        for arabic, chinese in conversions.items():
            text = text.replace(arabic, chinese)

        return text

    def _add_punctuation(self, text: str) -> str:
        """Add punctuation for natural pauses."""
        # Add exclamation marks for excitement keywords
        excitement_keywords = ["欢迎", "恭喜", "好消息", "特价", "优惠"]
        for keyword in excitement_keywords:
            if keyword in text and not any(p in text for p in ["!", "。", "!"]):
                text = text.replace(keyword, f"{keyword}!", 1)

        # Add commas before common conjunctions
        conjunctions = ["今日", "本店", "仅限", "请您"]
        for conjunction in conjunctions:
            if conjunction in text and "," not in text[:text.index(conjunction) + len(conjunction)]:
                text = text.replace(conjunction, f",{conjunction}", 1)

        # Ensure ending punctuation
        if not text.endswith(("。", "!", "?", "。", "!", "?")):
            text += "。"

        return text

    def _determine_emotion(self, input_obj: VoicePromptInput, analysis: Dict) -> str:
        """Determine optimal emotion."""
        # Priority 1: User specified
        if input_obj.emotion_preference:
            self.notes.append(f"Using user-specified emotion: {input_obj.emotion_preference}")
            return input_obj.emotion_preference

        # Priority 2: Detected from text
        detected_emotion = analysis["detected_emotion"]
        if detected_emotion != "neutral":
            self.notes.append(f"Emotion detected from text: {detected_emotion}")
            return detected_emotion

        # Priority 3: Default based on purpose
        purpose = analysis["detected_purpose"]
        purpose_emotion_map = {
            "in-store": "happy",
            "phone-ivr": "neutral",
            "brand-tvc": "happy",
            "training": "neutral",
            "ambient": "neutral"
        }
        default_emotion = purpose_emotion_map.get(purpose, "neutral")
        self.notes.append(f"Using default emotion for {purpose}: {default_emotion}")
        return default_emotion

    def _set_prosody(self, input_obj: VoicePromptInput, emotion: str, analysis: Dict) -> Dict:
        """Set prosody parameters (speed, volume, pitch)."""
        # Start with emotion-based defaults
        prosody = self.EMOTION_PROSODY.get(emotion, self.EMOTION_PROSODY["neutral"]).copy()

        # Adjust based on purpose
        purpose = analysis["detected_purpose"]
        if purpose in self.PURPOSE_PROSODY:
            purpose_adjust = self.PURPOSE_PROSODY[purpose]
            speed_range = purpose_adjust["speed_range"]
            vol_range = purpose_adjust["vol_range"]

            # Clamp to purpose-specific ranges
            prosody["speed"] = max(speed_range[0], min(prosody["speed"], speed_range[1]))
            prosody["vol"] = max(vol_range[0], min(prosody["vol"], vol_range[1]))

        # Override with user-specified values
        if input_obj.speed is not None:
            prosody["speed"] = input_obj.speed
            self.notes.append(f"Using user-specified speed: {input_obj.speed}")

        if input_obj.vol is not None:
            prosody["vol"] = input_obj.vol
            self.notes.append(f"Using user-specified volume: {input_obj.vol}")

        if input_obj.pitch is not None:
            prosody["pitch"] = input_obj.pitch
            self.notes.append(f"Using user-specified pitch: {input_obj.pitch}")

        # Validate ranges
        prosody["speed"] = max(0.5, min(prosody["speed"], 2.0))
        prosody["vol"] = max(0.0, min(prosody["vol"], 10.0))
        prosody["pitch"] = max(-12, min(prosody["pitch"], 12))

        return prosody

    def _build_api_params(
        self,
        input_obj: VoicePromptInput,
        voice_id: str,
        text: str,
        emotion: str,
        prosody: Dict
    ) -> Dict:
        """Build API parameters."""
        params = {
            "model": input_obj.model,
            "text": text,
            "voice_id": voice_id,
            "emotion": emotion,
            "speed": prosody["speed"],
            "vol": prosody["vol"],
            "pitch": prosody["pitch"],
            "format": input_obj.format,
            "sample_rate": input_obj.sample_rate,
            "bitrate": input_obj.bitrate,
            "channel": 1,
            "language_boost": input_obj.language_boost,
            "output_directory": None  # Will be set by caller
        }

        # Voice cloning workflow
        if input_obj.use_cloning and input_obj.voice_clone_source:
            params["voice_clone_source"] = input_obj.voice_clone_source
            self.notes.append("Voice cloning workflow enabled")

        return params

    def _estimate_duration(self, text: str, speed: float) -> float:
        """Estimate audio duration in seconds."""
        # Average Chinese character speaking rate: ~3-4 chars/second at speed=1.0
        chars_per_second = 3.5 * speed
        duration = len(text) / chars_per_second
        return round(duration, 2)

    def validate_for_api(self, optimized: OptimizedVoiceOutput) -> Dict:
        """Final validation for API call."""
        return {
            "model": optimized.model,
            "text": optimized.text,
            "voice_id": optimized.voice_id,
            "emotion": optimized.emotion,
            "speed": optimized.speed,
            "vol": optimized.vol,
            "pitch": optimized.pitch,
            "format": optimized.format,
            "sample_rate": optimized.sample_rate,
            "bitrate": optimized.bitrate,
            "channel": optimized.channel,
            "language_boost": optimized.language_boost
        }


# CLI testing
if __name__ == "__main__":
    import json

    optimizer = VoicePromptOptimizer()

    # Test 1: In-store broadcasting
    print("=== Test 1: In-Store Broadcasting ===")
    result1 = optimizer.optimize("欢迎光临本店,今日特价火锅套餐8.8折优惠!")
    print(json.dumps(asdict(result1), ensure_ascii=False, indent=2))

    # Test 2: Phone IVR
    print("\n=== Test 2: Phone IVR ===")
    result2 = optimizer.optimize({
        "creative_brief": "本店因装修暂停营业,给您带来不便敬请谅解",
        "voice_purpose": "phone-ivr",
        "emotion_preference": "sad"
    })
    print(json.dumps(asdict(result2), ensure_ascii=False, indent=2))

    # Test 3: Brand TVC
    print("\n=== Test 3: Brand TVC ===")
    result3 = optimizer.optimize({
        "creative_brief": "川味小馆,始于1998年,专注正宗川菜25年",
        "restaurant_type": "hotpot",
        "voice_purpose": "brand-tvc",
        "voice_type": "male"
    })
    print(json.dumps(asdict(result3), ensure_ascii=False, indent=2))
