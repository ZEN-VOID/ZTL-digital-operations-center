"""
PowerPoint Template System

Provides predefined presentation templates for common use cases:
- Business reports
- Product launches
- Training materials
- Investor pitches
"""

from typing import Dict, Any, List
from abc import ABC, abstractmethod


class PresentationTemplate(ABC):
    """Base class for presentation templates."""

    @abstractmethod
    def render(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Render template with provided data.

        Args:
            data: Template data dictionary

        Returns:
            List of slide dictionaries
        """
        pass


class BusinessReportTemplate(PresentationTemplate):
    """Template for business reports and quarterly reviews."""

    def render(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Render business report template.

        Expected data keys:
            - title: Report title
            - period: Report period (e.g., "Q3 2025")
            - executive_summary: Summary text
            - metrics: Dict with key metrics
            - achievements: List of achievements
            - challenges: List of challenges
            - next_steps: List of action items
        """
        slides = []

        # Executive Summary
        slides.append({
            "type": "content",
            "title": "Executive Summary",
            "content": [
                data.get("executive_summary", ""),
                f"Reporting Period: {data.get('period', 'N/A')}"
            ]
        })

        # Key Metrics
        if "metrics" in data:
            metrics_rows = [
                [k, str(v)] for k, v in data["metrics"].items()
            ]
            slides.append({
                "type": "table",
                "title": "Key Performance Metrics",
                "headers": ["Metric", "Value"],
                "rows": metrics_rows
            })

        # Achievements
        if "achievements" in data:
            slides.append({
                "type": "content",
                "title": "Key Achievements",
                "content": data["achievements"]
            })

        # Challenges
        if "challenges" in data:
            slides.append({
                "type": "content",
                "title": "Challenges & Learnings",
                "content": data["challenges"]
            })

        # Next Steps
        if "next_steps" in data:
            slides.append({
                "type": "content",
                "title": "Next Steps",
                "content": data["next_steps"]
            })

        return slides


class ProductLaunchTemplate(PresentationTemplate):
    """Template for product launches and marketing campaigns."""

    def render(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Render product launch template.

        Expected data keys:
            - product_name: Product name
            - tagline: Product tagline
            - problem: Problem being solved
            - solution: How product solves it
            - features: List of key features
            - benefits: List of customer benefits
            - target_audience: Target market description
            - timeline: Launch timeline milestones
        """
        slides = []

        # Problem Statement
        if "problem" in data:
            slides.append({
                "type": "content",
                "title": "The Problem",
                "content": [data["problem"]]
            })

        # Solution Overview
        if "solution" in data:
            slides.append({
                "type": "content",
                "title": "Our Solution",
                "content": [
                    data["solution"],
                    f"Introducing: {data.get('product_name', 'Our Product')}"
                ]
            })

        # Key Features
        if "features" in data:
            slides.append({
                "type": "content",
                "title": "Key Features",
                "content": data["features"]
            })

        # Customer Benefits
        if "benefits" in data:
            slides.append({
                "type": "content",
                "title": "Customer Benefits",
                "content": data["benefits"]
            })

        # Target Audience
        if "target_audience" in data:
            slides.append({
                "type": "content",
                "title": "Target Market",
                "content": [data["target_audience"]]
            })

        # Launch Timeline
        if "timeline" in data:
            timeline_rows = [
                [item.get("date", ""), item.get("milestone", "")]
                for item in data["timeline"]
            ]
            slides.append({
                "type": "table",
                "title": "Launch Timeline",
                "headers": ["Date", "Milestone"],
                "rows": timeline_rows
            })

        return slides


class TrainingTemplate(PresentationTemplate):
    """Template for training materials and workshops."""

    def render(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Render training template.

        Expected data keys:
            - course_name: Training course name
            - objectives: List of learning objectives
            - agenda: List of agenda items
            - modules: List of training modules, each with:
                - title: Module title
                - content: Module content points
                - exercise: Optional exercise description
            - resources: List of additional resources
        """
        slides = []

        # Learning Objectives
        if "objectives" in data:
            slides.append({
                "type": "content",
                "title": "Learning Objectives",
                "content": data["objectives"]
            })

        # Agenda
        if "agenda" in data:
            slides.append({
                "type": "content",
                "title": "Agenda",
                "content": data["agenda"]
            })

        # Training Modules
        if "modules" in data:
            for module in data["modules"]:
                slides.append({
                    "type": "content",
                    "title": module.get("title", "Module"),
                    "content": module.get("content", [])
                })

                # Add exercise slide if present
                if "exercise" in module:
                    slides.append({
                        "type": "content",
                        "title": f"Exercise: {module.get('title', 'Module')}",
                        "content": [module["exercise"]]
                    })

        # Additional Resources
        if "resources" in data:
            slides.append({
                "type": "content",
                "title": "Additional Resources",
                "content": data["resources"]
            })

        return slides


class PitchTemplate(PresentationTemplate):
    """Template for investor pitches and proposals."""

    def render(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Render pitch deck template.

        Expected data keys:
            - company_name: Company name
            - tagline: Company tagline
            - problem: Problem statement
            - solution: Solution description
            - market_size: Market opportunity
            - business_model: Revenue model
            - traction: Key metrics and traction
            - competition: Competitive landscape
            - team: Team members
            - ask: Funding ask and use of funds
        """
        slides = []

        # Problem
        if "problem" in data:
            slides.append({
                "type": "content",
                "title": "Problem",
                "content": [data["problem"]]
            })

        # Solution
        if "solution" in data:
            slides.append({
                "type": "content",
                "title": "Solution",
                "content": [data["solution"]]
            })

        # Market Opportunity
        if "market_size" in data:
            slides.append({
                "type": "content",
                "title": "Market Opportunity",
                "content": [data["market_size"]]
            })

        # Business Model
        if "business_model" in data:
            slides.append({
                "type": "content",
                "title": "Business Model",
                "content": [data["business_model"]]
            })

        # Traction
        if "traction" in data:
            if isinstance(data["traction"], dict):
                traction_rows = [
                    [k, str(v)] for k, v in data["traction"].items()
                ]
                slides.append({
                    "type": "table",
                    "title": "Traction",
                    "headers": ["Metric", "Value"],
                    "rows": traction_rows
                })
            else:
                slides.append({
                    "type": "content",
                    "title": "Traction",
                    "content": data["traction"] if isinstance(data["traction"], list) else [data["traction"]]
                })

        # Competition
        if "competition" in data:
            slides.append({
                "type": "content",
                "title": "Competitive Landscape",
                "content": [data["competition"]]
            })

        # Team
        if "team" in data:
            team_rows = [
                [member.get("name", ""), member.get("role", ""), member.get("background", "")]
                for member in data["team"]
            ]
            slides.append({
                "type": "table",
                "title": "Team",
                "headers": ["Name", "Role", "Background"],
                "rows": team_rows
            })

        # The Ask
        if "ask" in data:
            slides.append({
                "type": "content",
                "title": "The Ask",
                "content": [data["ask"]]
            })

        return slides


class TemplateRegistry:
    """Registry of available presentation templates."""

    _templates = {
        "business-report": BusinessReportTemplate(),
        "product-launch": ProductLaunchTemplate(),
        "training": TrainingTemplate(),
        "pitch": PitchTemplate()
    }

    @classmethod
    def get_template(cls, template_type: str) -> PresentationTemplate:
        """
        Get template by type.

        Args:
            template_type: Template identifier

        Returns:
            Template instance

        Raises:
            KeyError: If template type not found
        """
        if template_type not in cls._templates:
            available = ", ".join(cls._templates.keys())
            raise KeyError(
                f"Template '{template_type}' not found. "
                f"Available templates: {available}"
            )

        return cls._templates[template_type]

    @classmethod
    def list_templates(cls) -> List[str]:
        """Get list of available template types."""
        return list(cls._templates.keys())

    @classmethod
    def register_template(cls, name: str, template: PresentationTemplate):
        """
        Register a custom template.

        Args:
            name: Template identifier
            template: Template instance
        """
        cls._templates[name] = template
