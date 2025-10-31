#!/usr/bin/env python3
"""
MiniMax Music Prompt Optimizer
Transforms raw creative briefs into optimized MiniMax Music API prompts.

Author: ZTL Digital Intelligence Operations Center - 创意组
Version: 1.0.0
"""

import re
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, asdict


@dataclass
class MusicPromptInput:
    """Input schema for music prompt optimization."""
    creative_brief: str
    restaurant_type: Optional[str] = None  # hotpot, fine-dining, cafe, fast-casual
    music_purpose: Optional[str] = None    # background, promo, event, brand
    mood_preference: Optional[str] = None  # festive, elegant, energetic, relaxing
    vocal_preference: Optional[str] = None # instrumental, male-vocal, female-vocal, mixed
    lyrics_draft: Optional[str] = None
    duration_seconds: int = 60
    technical_params: Optional[Dict] = None


@dataclass
class OptimizedOutput:
    """Output schema for optimized music prompt."""
    prompt: str
    lyrics: str
    analysis: Dict[str, str]
    api_params: Dict[str, Union[str, int]]
    optimization_notes: List[str]


class MusicPromptOptimizer:
    """Core optimizer for MiniMax Music API prompts."""

    # Style keywords mapping
    STYLE_KEYWORDS = {
        "火锅": ["Chinese folk fusion", "festive", "traditional instruments"],
        "西餐": ["elegant jazz", "sophisticated", "piano trio"],
        "咖啡": ["acoustic indie folk", "warm cozy", "guitar"],
        "快餐": ["upbeat pop", "energetic", "catchy melody"],
        "烧烤": ["rock", "energetic fun", "electric guitar"],
        "日料": ["ambient electronic", "zen minimalist", "koto and shamisen"],
        "川菜": ["Sichuan folk", "spicy energetic", "traditional percussion"],
    }

    # Mood mapping (Chinese → English)
    MOOD_MAP = {
        "喜庆": "festive",
        "欢快": "upbeat",
        "轻松": "relaxing",
        "优雅": "elegant",
        "热闹": "lively",
        "温馨": "warm",
        "激情": "energetic",
        "浪漫": "romantic",
        "庄重": "solemn",
        "活泼": "playful",
    }

    # Purpose templates
    PURPOSE_TEMPLATES = {
        "background": "{style} instrumental background music, {mood} atmosphere, suitable for {restaurant_type} restaurants",
        "promo": "{style} promotional song, {mood} and engaging, {vocal_type}, suitable for {marketing_channel}",
        "event": "{event_type} themed music, {style}, {mood} mood, suitable for {specific_occasion}",
        "brand": "{style} brand anthem, {mood} and memorable, {vocal_type}, reflects brand identity",
    }

    # Lyrics structure tags
    LYRIC_TAGS = ["[Intro]", "[Verse]", "[Chorus]", "[Bridge]", "[Outro]", "[Instrumental]"]

    def __init__(self):
        self.notes = []

    def optimize(self, input_data: Union[Dict, MusicPromptInput, str]) -> OptimizedOutput:
        """
        Main optimization entry point.

        Args:
            input_data: Can be a dict, MusicPromptInput object, or simple string

        Returns:
            OptimizedOutput with prompt, lyrics, analysis, and API params
        """
        self.notes = []

        # Normalize input
        if isinstance(input_data, str):
            input_obj = MusicPromptInput(creative_brief=input_data)
        elif isinstance(input_data, dict):
            input_obj = MusicPromptInput(**input_data)
        else:
            input_obj = input_data

        # Step 1: Analyze creative intent
        analysis = self._analyze_intent(input_obj)

        # Step 2: Build optimized prompt
        prompt = self._build_prompt(input_obj, analysis)

        # Step 3: Format lyrics (if applicable)
        lyrics = self._format_lyrics(input_obj, analysis)

        # Step 4: Set API parameters
        api_params = self._build_api_params(input_obj)

        # Step 5: Validate all constraints
        self._validate_constraints(prompt, lyrics)

        return OptimizedOutput(
            prompt=prompt,
            lyrics=lyrics,
            analysis=analysis,
            api_params=api_params,
            optimization_notes=self.notes.copy()
        )

    def _analyze_intent(self, input_obj: MusicPromptInput) -> Dict[str, str]:
        """Extract style, mood, scene, and vocal type from creative brief."""
        brief = input_obj.creative_brief.lower()

        # Detect restaurant type
        detected_restaurant = input_obj.restaurant_type
        if not detected_restaurant:
            for keyword, _ in self.STYLE_KEYWORDS.items():
                if keyword in brief:
                    detected_restaurant = keyword
                    self.notes.append(f"Detected restaurant type: {keyword}")
                    break

        # Detect style
        style_hints = self.STYLE_KEYWORDS.get(detected_restaurant, ["pop", "modern"])
        detected_style = style_hints[0]

        # Detect mood
        detected_mood = input_obj.mood_preference or "upbeat"
        for chinese_mood, english_mood in self.MOOD_MAP.items():
            if chinese_mood in brief:
                detected_mood = english_mood
                self.notes.append(f"Detected mood from brief: {chinese_mood} → {english_mood}")
                break

        # Detect scene/purpose
        detected_scene = input_obj.music_purpose or "background"
        if "开业" in brief or "庆典" in brief:
            detected_scene = "promo"
            self.notes.append("Detected scene: grand opening promotional music")
        elif "背景" in brief or "氛围" in brief:
            detected_scene = "background"
            self.notes.append("Detected scene: background ambiance music")

        # Detect vocal preference
        detected_vocal = input_obj.vocal_preference or "instrumental"
        if "歌词" in brief or input_obj.lyrics_draft:
            detected_vocal = "vocal"
            self.notes.append("Detected vocal requirement from lyrics presence")
        elif "纯音乐" in brief or "背景" in brief:
            detected_vocal = "instrumental"
            self.notes.append("Detected instrumental-only requirement")

        return {
            "detected_style": detected_style,
            "detected_mood": detected_mood,
            "detected_scene": detected_scene,
            "vocal_type": detected_vocal,
            "restaurant_type": detected_restaurant or "restaurant"
        }

    def _build_prompt(self, input_obj: MusicPromptInput, analysis: Dict) -> str:
        """Construct optimized prompt string (10-300 chars)."""
        template = self.PURPOSE_TEMPLATES.get(analysis["detected_scene"],
                                               self.PURPOSE_TEMPLATES["background"])

        # Fill template
        prompt = template.format(
            style=analysis["detected_style"],
            mood=analysis["detected_mood"],
            vocal_type="with vocals" if analysis["vocal_type"] == "vocal" else "instrumental",
            restaurant_type=analysis["restaurant_type"],
            marketing_channel="social media and in-store displays",
            event_type="seasonal celebration",
            specific_occasion="special events"
        )

        # Truncate if exceeds 300 chars
        if len(prompt) > 300:
            prompt = prompt[:297] + "..."
            self.notes.append(f"Truncated prompt to 300 characters")

        # Ensure minimum 10 chars
        if len(prompt) < 10:
            prompt = "Modern instrumental background music for restaurant ambiance"
            self.notes.append("Padded prompt to meet 10 character minimum")

        return prompt

    def _format_lyrics(self, input_obj: MusicPromptInput, analysis: Dict) -> str:
        """Format lyrics with proper structure tags and line breaks."""
        if analysis["vocal_type"] == "instrumental":
            return ""  # No lyrics for instrumental

        if not input_obj.lyrics_draft:
            return ""  # No lyrics provided

        lyrics = input_obj.lyrics_draft.strip()

        # Add structure tags if missing
        if not any(tag in lyrics for tag in self.LYRIC_TAGS):
            # Simple structure: Verse → Chorus → Verse → Chorus
            lines = [line.strip() for line in lyrics.split('\n') if line.strip()]

            if len(lines) <= 4:
                # Short lyrics: just add Verse tag
                lyrics = "[Verse]\n" + "\n".join(lines)
            else:
                # Split into verse and chorus
                mid = len(lines) // 2
                verse_lines = lines[:mid]
                chorus_lines = lines[mid:]

                lyrics = "[Verse]\n" + "\n".join(verse_lines) + "\n\n" + \
                         "[Chorus]\n" + "\n".join(chorus_lines)

            self.notes.append("Added structure tags: [Verse] and [Chorus]")

        # Ensure proper line breaks
        # Single \n for lines, double \n\n for pauses
        lyrics = re.sub(r'\n{3,}', '\n\n', lyrics)  # Max 2 consecutive newlines

        # Validate character limit (10-600)
        if len(lyrics) > 600:
            lyrics = lyrics[:597] + "..."
            self.notes.append("Truncated lyrics to 600 characters")

        if len(lyrics) < 10:
            self.notes.append("Warning: Lyrics below 10 characters, may not be valid")

        return lyrics

    def _build_api_params(self, input_obj: MusicPromptInput) -> Dict:
        """Construct API parameters with defaults."""
        defaults = {
            "sample_rate": 32000,
            "bitrate": 128000,
            "format": "mp3"
        }

        if input_obj.technical_params:
            defaults.update(input_obj.technical_params)

        # Validate params
        valid_sample_rates = [16000, 24000, 32000, 44100]
        valid_bitrates = [32000, 64000, 128000, 256000]
        valid_formats = ["mp3", "wav", "pcm"]

        if defaults["sample_rate"] not in valid_sample_rates:
            self.notes.append(f"Invalid sample_rate {defaults['sample_rate']}, using 32000")
            defaults["sample_rate"] = 32000

        if defaults["bitrate"] not in valid_bitrates:
            self.notes.append(f"Invalid bitrate {defaults['bitrate']}, using 128000")
            defaults["bitrate"] = 128000

        if defaults["format"] not in valid_formats:
            self.notes.append(f"Invalid format {defaults['format']}, using mp3")
            defaults["format"] = "mp3"

        return defaults

    def _validate_constraints(self, prompt: str, lyrics: str):
        """Final validation of all API constraints."""
        errors = []

        # Prompt length
        if not (10 <= len(prompt) <= 300):
            errors.append(f"Prompt length {len(prompt)} outside valid range [10, 300]")

        # Lyrics length (if present)
        if lyrics and not (10 <= len(lyrics) <= 600):
            errors.append(f"Lyrics length {len(lyrics)} outside valid range [10, 600]")

        if errors:
            raise ValueError("Validation failed: " + "; ".join(errors))

        self.notes.append(f"✓ Validation passed: prompt={len(prompt)} chars, lyrics={len(lyrics)} chars")

    def validate_for_api(self, optimized: OptimizedOutput) -> Dict:
        """
        Final validation and packaging for MiniMax API call.

        Returns:
            Dict ready to pass to mcp__minimax-mcp__music_generation
        """
        return {
            "prompt": optimized.prompt,
            "lyrics": optimized.lyrics,
            "sample_rate": optimized.api_params["sample_rate"],
            "bitrate": optimized.api_params["bitrate"],
            "format": optimized.api_params["format"],
            # output_directory should be set by calling agent
        }


# CLI for testing
if __name__ == "__main__":
    import json

    optimizer = MusicPromptOptimizer()

    # Test case 1: Background music
    print("=== Test 1: Hotpot Background Music ===")
    result1 = optimizer.optimize("轻快的火锅店背景音乐")
    print(json.dumps(asdict(result1), ensure_ascii=False, indent=2))

    # Test case 2: Opening promo with lyrics
    print("\n=== Test 2: Grand Opening with Lyrics ===")
    result2 = optimizer.optimize({
        "creative_brief": "火锅店开业庆典音乐",
        "restaurant_type": "hotpot",
        "lyrics_draft": "火锅飘香迎客来\n欢聚一堂庆开业\n麻辣鲜香味无穷\n宾客满堂乐开怀"
    })
    print(json.dumps(asdict(result2), ensure_ascii=False, indent=2))

    # Test case 3: Validation
    print("\n=== Test 3: API Validation ===")
    api_ready = optimizer.validate_for_api(result2)
    print(json.dumps(api_ready, ensure_ascii=False, indent=2))
