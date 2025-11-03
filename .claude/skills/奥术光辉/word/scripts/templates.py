"""
Document Template System

Provides predefined document templates for common business scenarios.

Author: ZTL数智化作战中心
Version: 1.0.0
"""

from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod


class DocumentTemplate(ABC):
    """Base class for document templates."""

    @abstractmethod
    def render(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Render template with provided data.

        Args:
            data: Template data dictionary

        Returns:
            List of content elements for document generation
        """
        pass


class ReportTemplate(DocumentTemplate):
    """Business report template."""

    def render(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        content = []

        # Executive summary
        if data.get("summary"):
            content.append({"type": "heading", "level": 1, "text": "执行摘要"})
            content.append({"type": "paragraph", "text": data["summary"]})

        # Main sections
        for section in data.get("sections", []):
            content.append({
                "type": "heading",
                "level": section.get("level", 1),
                "text": section["title"]
            })

            # Section content
            if "text" in section:
                content.append({"type": "paragraph", "text": section["text"]})

            # Tables
            if "table" in section:
                content.append({
                    "type": "table",
                    "headers": section["table"]["headers"],
                    "rows": section["table"]["rows"]
                })

            # Lists
            if "bullet_list" in section:
                content.append({
                    "type": "bullet_list",
                    "items": section["bullet_list"]
                })

            # Images/charts
            if "image" in section:
                content.append({
                    "type": "image",
                    "path": section["image"]["path"],
                    "width": section["image"].get("width", 6),
                    "caption": section["image"].get("caption")
                })

        # Conclusion
        if data.get("conclusion"):
            content.append({"type": "heading", "level": 1, "text": "结论"})
            content.append({"type": "paragraph", "text": data["conclusion"]})

        # Recommendations
        if data.get("recommendations"):
            content.append({"type": "heading", "level": 1, "text": "建议"})
            content.append({"type": "bullet_list", "items": data["recommendations"]})

        return content


class ProposalTemplate(DocumentTemplate):
    """Project proposal template."""

    def render(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        content = []

        # Background
        content.append({"type": "heading", "level": 1, "text": "项目背景"})
        content.append({"type": "paragraph", "text": data.get("background", "")})

        # Objectives
        content.append({"type": "heading", "level": 1, "text": "项目目标"})
        content.append({"type": "bullet_list", "items": data.get("objectives", [])})

        # Scope
        content.append({"type": "heading", "level": 1, "text": "项目范围"})
        content.append({"type": "paragraph", "text": data.get("scope", "")})

        # Deliverables
        content.append({"type": "heading", "level": 1, "text": "交付成果"})
        content.append({"type": "bullet_list", "items": data.get("deliverables", [])})

        # Timeline
        if data.get("timeline"):
            content.append({"type": "heading", "level": 1, "text": "项目时间表"})
            content.append({
                "type": "table",
                "headers": ["阶段", "任务", "开始日期", "结束日期"],
                "rows": data["timeline"]
            })

        # Budget
        if data.get("budget"):
            content.append({"type": "heading", "level": 1, "text": "项目预算"})
            content.append({
                "type": "table",
                "headers": ["项目", "金额", "说明"],
                "rows": data["budget"]
            })

        # Team
        if data.get("team"):
            content.append({"type": "heading", "level": 1, "text": "项目团队"})
            content.append({
                "type": "table",
                "headers": ["姓名", "角色", "职责"],
                "rows": data["team"]
            })

        return content


class MeetingMinutesTemplate(DocumentTemplate):
    """Meeting minutes template."""

    def render(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        content = []

        # Meeting info
        content.append({"type": "heading", "level": 1, "text": "会议信息"})
        info_items = [
            f"日期: {data.get('date', 'N/A')}",
            f"时间: {data.get('time', 'N/A')}",
            f"地点: {data.get('location', 'N/A')}",
            f"主持人: {data.get('host', 'N/A')}"
        ]
        for item in info_items:
            content.append({"type": "paragraph", "text": item})

        # Attendees
        content.append({"type": "heading", "level": 1, "text": "参会人员"})
        attendees = data.get("attendees", [])
        content.append({"type": "paragraph", "text": ", ".join(attendees)})

        # Agenda and discussion
        for topic in data.get("topics", []):
            content.append({"type": "heading", "level": 1, "text": topic["topic"]})
            content.append({"type": "paragraph", "text": topic.get("discussion", "")})

            # Action items
            if topic.get("action_items"):
                content.append({"type": "heading", "level": 2, "text": "行动项"})
                content.append({
                    "type": "table",
                    "headers": ["任务", "负责人", "截止日期"],
                    "rows": [
                        [item["task"], item["owner"], item["deadline"]]
                        for item in topic["action_items"]
                    ]
                })

        # Next meeting
        if data.get("next_meeting"):
            content.append({"type": "heading", "level": 1, "text": "下次会议"})
            content.append({"type": "paragraph", "text": data["next_meeting"]})

        return content


class ContractTemplate(DocumentTemplate):
    """Contract/agreement template."""

    def render(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        content = []

        # Parties
        content.append({"type": "paragraph", "text": f"甲方(授权方): {data.get('party_a', '__________')}"})
        content.append({"type": "paragraph", "text": f"乙方(加盟方): {data.get('party_b', '__________')}"})
        content.append({"type": "paragraph", "text": ""})

        # Recitals
        if data.get("recitals"):
            content.append({"type": "heading", "level": 1, "text": "鉴于"})
            content.append({"type": "paragraph", "text": data["recitals"]})

        # Terms
        for i, term in enumerate(data.get("terms", []), start=1):
            content.append({
                "type": "heading",
                "level": 1,
                "text": f"第{i}条 {term['title']}"
            })

            for j, clause in enumerate(term.get("clauses", []), start=1):
                content.append({
                    "type": "paragraph",
                    "text": f"{i}.{j} {clause}"
                })

        # Signatures
        content.append({"type": "page_break"})
        content.append({"type": "heading", "level": 1, "text": "签署"})
        content.append({"type": "paragraph", "text": ""})
        content.append({"type": "paragraph", "text": "甲方签字: __________ 日期: __________"})
        content.append({"type": "paragraph", "text": ""})
        content.append({"type": "paragraph", "text": "乙方签字: __________ 日期: __________"})

        return content


class ManualTemplate(DocumentTemplate):
    """User manual/guide template."""

    def render(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        content = []

        # Introduction
        content.append({"type": "heading", "level": 1, "text": "简介"})
        content.append({"type": "paragraph", "text": data.get("introduction", "")})

        # Features
        if data.get("features"):
            content.append({"type": "heading", "level": 1, "text": "功能特性"})
            content.append({"type": "bullet_list", "items": data["features"]})

        # Instructions sections
        for section in data.get("sections", []):
            content.append({
                "type": "heading",
                "level": section.get("level", 1),
                "text": section["title"]
            })

            # Steps
            if section.get("steps"):
                content.append({"type": "numbered_list", "items": section["steps"]})

            # Text content
            if section.get("text"):
                content.append({"type": "paragraph", "text": section["text"]})

            # Screenshots
            if section.get("image"):
                content.append({
                    "type": "image",
                    "path": section["image"]["path"],
                    "width": section["image"].get("width", 6),
                    "caption": section["image"].get("caption")
                })

        # Troubleshooting
        if data.get("troubleshooting"):
            content.append({"type": "heading", "level": 1, "text": "故障排除"})
            content.append({
                "type": "table",
                "headers": ["问题", "原因", "解决方案"],
                "rows": data["troubleshooting"]
            })

        # FAQ
        if data.get("faq"):
            content.append({"type": "heading", "level": 1, "text": "常见问题"})
            for qa in data["faq"]:
                content.append({"type": "heading", "level": 2, "text": f"Q: {qa['question']}"})
                content.append({"type": "paragraph", "text": f"A: {qa['answer']}"})

        return content


class LetterTemplate(DocumentTemplate):
    """Business letter template."""

    def render(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        content = []

        # Sender info
        content.append({"type": "paragraph", "text": data.get("sender_name", ""), "align": "right"})
        content.append({"type": "paragraph", "text": data.get("sender_address", ""), "align": "right"})
        content.append({"type": "paragraph", "text": data.get("sender_contact", ""), "align": "right"})
        content.append({"type": "paragraph", "text": ""})

        # Date
        content.append({"type": "paragraph", "text": data.get("date", ""), "align": "right"})
        content.append({"type": "paragraph", "text": ""})

        # Recipient info
        content.append({"type": "paragraph", "text": data.get("recipient_name", "")})
        content.append({"type": "paragraph", "text": data.get("recipient_address", "")})
        content.append({"type": "paragraph", "text": ""})

        # Subject
        if data.get("subject"):
            content.append({
                "type": "paragraph",
                "text": f"主题: {data['subject']}",
                "bold": True
            })
            content.append({"type": "paragraph", "text": ""})

        # Salutation
        content.append({"type": "paragraph", "text": data.get("salutation", "尊敬的先生/女士:")})
        content.append({"type": "paragraph", "text": ""})

        # Body
        for paragraph in data.get("body", []):
            content.append({"type": "paragraph", "text": paragraph})
            content.append({"type": "paragraph", "text": ""})

        # Closing
        content.append({"type": "paragraph", "text": data.get("closing", "此致敬礼")})
        content.append({"type": "paragraph", "text": ""})
        content.append({"type": "paragraph", "text": data.get("signature", "")})

        return content


class TemplateRegistry:
    """Registry for document templates."""

    _templates = {
        "report": ReportTemplate(),
        "proposal": ProposalTemplate(),
        "meeting-minutes": MeetingMinutesTemplate(),
        "contract": ContractTemplate(),
        "manual": ManualTemplate(),
        "letter": LetterTemplate()
    }

    @classmethod
    def get_template(cls, template_type: str) -> Optional[DocumentTemplate]:
        """Get template by type."""
        return cls._templates.get(template_type)

    @classmethod
    def list_templates(cls) -> List[str]:
        """List available template types."""
        return list(cls._templates.keys())

    @classmethod
    def register_template(cls, template_type: str, template: DocumentTemplate):
        """Register custom template."""
        cls._templates[template_type] = template
