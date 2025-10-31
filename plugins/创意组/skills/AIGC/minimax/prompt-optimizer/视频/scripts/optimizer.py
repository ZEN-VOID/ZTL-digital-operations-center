#!/usr/bin/env python3
"""
MiniMax Video Prompt Optimizer
Transforms creative briefs into optimized MiniMax Video API prompts.

Author: ZTL Digital Intelligence Operations Center - 创意组
Version: 1.0.0
"""

import re
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, asdict


@dataclass
class VideoPromptInput:
    """Input schema for video prompt optimization."""
    creative_brief: str
    model: Optional[str] = "T2V-01"  # T2V-01, T2V-01-Director, I2V-01, I2V-01-Director, I2V-01-live, MiniMax-Hailuo-02
    first_frame_image: Optional[str] = None
    restaurant_type: Optional[str] = None
    video_purpose: Optional[str] = None  # menu-showcase, environment-tour, promo, social-media
    camera_preference: Optional[List[str]] = None
    duration: Optional[int] = None  # 6 or 10 (Hailuo-02 only)
    resolution: Optional[str] = None  # 768P or 1080P (Hailuo-02 only)
    aesthetic_style: Optional[str] = None


@dataclass
class OptimizedVideoOutput:
    """Output schema for optimized video prompt."""
    model: str
    prompt: str
    first_frame_image: Optional[str]
    duration: Optional[int]
    resolution: Optional[str]
    analysis: Dict[str, Union[str, List]]
    api_params: Dict
    optimization_notes: List[str]


class VideoPromptOptimizer:
    """Core optimizer for MiniMax Video API prompts."""

    # 15 Camera movements
    CAMERA_MOVEMENTS = [
        "Truck left", "Truck right", "Pan left", "Pan right",
        "Push in", "Pull out", "Pedestal up", "Pedestal down",
        "Tilt up", "Tilt down", "Zoom in", "Zoom out",
        "Shake", "Tracking shot", "Static shot"
    ]

    # Purpose-specific templates
    PURPOSE_TEMPLATES = {
        "menu-showcase": {
            "t2v": "Close-up of {dish}, steam rising, [Zoom in] highlighting fresh ingredients, appetizing presentation, warm lighting, food photography style",
            "i2v": "Steam rises from {dish}, [Tilt down] revealing full presentation, appetizing motion, warm ambiance"
        },
        "environment-tour": {
            "t2v": "[Push in] {location} entrance with {decor}, [Pan right] revealing {features}, warm inviting atmosphere, cinematic lighting"
        },
        "promo": {
            "t2v": "[Zoom in] {highlight}, {action}, [Pan left] {secondary}, {emotional_tone}, cinematic commercial style"
        },
        "social-media": {
            "t2v": "[Shake] {dynamic_action}, [Zoom in] {close_up}, trendy {style}, engaging fast-paced energy"
        }
    }

    def __init__(self):
        self.notes = []

    def optimize(self, input_data: Union[Dict, VideoPromptInput, str]) -> OptimizedVideoOutput:
        """Main optimization entry point."""
        self.notes = []

        # Normalize input
        if isinstance(input_data, str):
            input_obj = VideoPromptInput(creative_brief=input_data)
        elif isinstance(input_data, dict):
            input_obj = VideoPromptInput(**input_data)
        else:
            input_obj = input_data

        # Step 1: Select optimal model
        model = self._select_model(input_obj)

        # Step 2: Analyze intent
        analysis = self._analyze_intent(input_obj, model)

        # Step 3: Build prompt
        prompt = self._build_prompt(input_obj, model, analysis)

        # Step 4: Set parameters
        api_params = self._build_api_params(input_obj, model)

        return OptimizedVideoOutput(
            model=model,
            prompt=prompt,
            first_frame_image=input_obj.first_frame_image,
            duration=input_obj.duration,
            resolution=input_obj.resolution,
            analysis=analysis,
            api_params=api_params,
            optimization_notes=self.notes.copy()
        )

    def _select_model(self, input_obj: VideoPromptInput) -> str:
        """Select optimal model based on input."""
        # If model explicitly specified, use it
        if input_obj.model and input_obj.model != "T2V-01":
            self.notes.append(f"Using user-specified model: {input_obj.model}")
            return input_obj.model

        # Auto-select based on requirements
        if input_obj.first_frame_image:
            # Has first frame → I2V models
            if input_obj.camera_preference:
                model = "I2V-01-Director"
                self.notes.append("Auto-selected I2V-01-Director (first frame + camera control)")
            else:
                model = "I2V-01"
                self.notes.append("Auto-selected I2V-01 (first frame animation)")
        else:
            # No first frame → T2V models
            if input_obj.duration in [6, 10] or input_obj.resolution in ["768P", "1080P"]:
                model = "MiniMax-Hailuo-02"
                self.notes.append("Auto-selected Hailuo-02 (premium quality requested)")
            elif input_obj.camera_preference or "镜头" in input_obj.creative_brief:
                model = "T2V-01-Director"
                self.notes.append("Auto-selected T2V-01-Director (camera control needed)")
            else:
                model = "T2V-01"
                self.notes.append("Auto-selected T2V-01 (standard generation)")

        return model

    def _analyze_intent(self, input_obj: VideoPromptInput, model: str) -> Dict:
        """Analyze creative brief to extract key elements."""
        brief = input_obj.creative_brief.lower()

        # Detect purpose
        detected_purpose = input_obj.video_purpose or "promo"
        if "菜品" in brief or "dish" in brief or "menu" in brief:
            detected_purpose = "menu-showcase"
        elif "环境" in brief or "environment" in brief or "tour" in brief:
            detected_purpose = "environment-tour"
        elif "social" in brief or "抖音" in brief or "tiktok" in brief:
            detected_purpose = "social-media"

        # Extract camera movements from brief
        detected_cameras = []
        if "-Director" in model or input_obj.camera_preference:
            # Check for camera keywords in brief
            camera_keywords = {
                "推进": "Push in", "拉远": "Pull out",
                "左移": "Pan left", "右移": "Pan right",
                "特写": "Zoom in", "广角": "Pull out",
                "跟随": "Tracking shot", "环视": "Pan right",
                "俯视": "Tilt down", "仰视": "Tilt up"
            }

            for chinese, english in camera_keywords.items():
                if chinese in brief:
                    detected_cameras.append(english)

            # Add user preferences
            if input_obj.camera_preference:
                detected_cameras.extend(input_obj.camera_preference)

            # Limit to 3 max
            if len(detected_cameras) > 3:
                detected_cameras = detected_cameras[:3]
                self.notes.append(f"Limited camera movements to 3 (was {len(detected_cameras)})")

        # Detect subject focus
        subject_focus = "restaurant scene"
        if "火锅" in brief or "hotpot" in brief:
            subject_focus = "hotpot dish"
        elif "面条" in brief or "noodles" in brief:
            subject_focus = "noodles"
        elif "环境" in brief:
            subject_focus = "restaurant interior"

        return {
            "detected_purpose": detected_purpose,
            "recommended_cameras": detected_cameras,
            "subject_focus": subject_focus,
            "motion_type": "dynamic" if "动" in brief else "static"
        }

    def _build_prompt(self, input_obj: VideoPromptInput, model: str, analysis: Dict) -> str:
        """Construct optimized prompt."""
        # For I2V models with first frame
        if input_obj.first_frame_image:
            prompt = f"Motion in first frame: {input_obj.creative_brief}"

            # Add camera if Director mode
            if "-Director" in model and analysis["recommended_cameras"]:
                cameras_str = ", ".join([f"[{cam}]" for cam in analysis["recommended_cameras"][:2]])
                prompt = f"{cameras_str} {prompt}"

            return prompt

        # For T2V models (text-to-video)
        purpose = analysis["detected_purpose"]
        template = self.PURPOSE_TEMPLATES.get(purpose, {}).get("t2v", "{creative_brief}, cinematic style")

        # Build from template
        if purpose == "menu-showcase":
            prompt = template.format(dish=analysis["subject_focus"])
        elif purpose == "environment-tour":
            prompt = template.format(
                location=input_obj.restaurant_type or "restaurant",
                decor="modern decor",
                features="dining area"
            )
        else:
            # Generic construction
            prompt = input_obj.creative_brief

            # Add camera movements for Director mode
            if "-Director" in model and analysis["recommended_cameras"]:
                cameras = analysis["recommended_cameras"][:2]  # Max 2 for stability
                prompt = f"[{cameras[0]}] " + prompt
                if len(cameras) > 1:
                    prompt += f" [{cameras[1]}]"

            # Add aesthetic
            aesthetic = input_obj.aesthetic_style or "cinematic style"
            if aesthetic not in prompt:
                prompt += f", {aesthetic}"

        return prompt

    def _build_api_params(self, input_obj: VideoPromptInput, model: str) -> Dict:
        """Build API parameters."""
        params = {
            "model": model,
            "prompt": "",  # Will be filled by caller
            "async_mode": False
        }

        # Add Hailuo-02 specific params
        if model == "MiniMax-Hailuo-02":
            params["duration"] = input_obj.duration or 6
            params["resolution"] = input_obj.resolution or "1080P"

            # Validate
            if params["duration"] not in [6, 10]:
                params["duration"] = 6
                self.notes.append("Invalid duration, using 6 seconds")

            if params["resolution"] not in ["768P", "1080P"]:
                params["resolution"] = "1080P"
                self.notes.append("Invalid resolution, using 1080P")

        # Add first frame for I2V models
        if input_obj.first_frame_image:
            params["first_frame_image"] = input_obj.first_frame_image

        return params

    def validate_for_api(self, optimized: OptimizedVideoOutput) -> Dict:
        """Final validation for API call."""
        return {
            "model": optimized.model,
            "prompt": optimized.prompt,
            "first_frame_image": optimized.first_frame_image,
            "duration": optimized.duration,
            "resolution": optimized.resolution,
            "async_mode": optimized.api_params.get("async_mode", False)
        }


# CLI testing
if __name__ == "__main__":
    import json

    optimizer = VideoPromptOptimizer()

    # Test 1: Menu showcase
    print("=== Test 1: Menu Showcase ===")
    result1 = optimizer.optimize("火锅菜品展示视频,要有蒸汽")
    print(json.dumps(asdict(result1), ensure_ascii=False, indent=2))

    # Test 2: Environment tour with camera
    print("\n=== Test 2: Environment Tour ===")
    result2 = optimizer.optimize({
        "creative_brief": "展示火锅店环境,从入口推进到用餐区",
        "restaurant_type": "hotpot",
        "camera_preference": ["Push in", "Pan right"]
    })
    print(json.dumps(asdict(result2), ensure_ascii=False, indent=2))

    # Test 3: I2V with first frame
    print("\n=== Test 3: I2V with First Frame ===")
    result3 = optimizer.optimize({
        "creative_brief": "让菜品冒出热气",
        "first_frame_image": "dish.jpg"
    })
    print(json.dumps(asdict(result3), ensure_ascii=False, indent=2))
