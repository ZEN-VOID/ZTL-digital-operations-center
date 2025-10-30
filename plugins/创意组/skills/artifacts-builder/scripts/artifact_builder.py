#!/usr/bin/env python3
"""
Artifacts Builder Execution Engine
==================================

Orchestrates the creation of complex React artifacts for claude.ai using:
- React 18 + TypeScript + Vite
- Tailwind CSS + shadcn/ui components
- Parcel bundling to single HTML file

Output Path Convention (follows global CLAUDE.md rules):
    output/[项目名]/X4-平面设计师/artifacts-builder/[artifact-name]/

Usage:
    from scripts.artifact_builder import ArtifactBuilder

    builder = ArtifactBuilder(
        project_name="餐饮网站原型",
        agent_name="X4-平面设计师"
    )

    result = builder.create_artifact(
        artifact_name="hotpot-menu-app",
        description="交互式火锅菜单应用"
    )
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Literal, Optional, Dict, Any, List
from dataclasses import dataclass, asdict


@dataclass
class ArtifactSpec:
    """Artifact specification following Layer 2 (Plan/Configuration Layer)"""

    # Identity
    project_name: str
    agent_name: str
    artifact_name: str
    description: str

    # Technical Stack
    use_react: bool = True
    use_typescript: bool = True
    use_tailwind: bool = True
    use_shadcn: bool = True

    # Features
    components: List[str] = None  # shadcn/ui components to use
    routing: bool = False
    state_management: str = "useState"  # useState | zustand | redux

    # Metadata
    timestamp: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if self.components is None:
            self.components = []


class ArtifactBuilder:
    """
    Main execution engine for artifacts-builder skill.

    Follows three-layer architecture:
    - Layer 1: Development guidelines (SKILL.md)
    - Layer 2: Artifact specifications (this class, JSON config)
    - Layer 3: Shell scripts execution (init-artifact.sh, bundle-artifact.sh)
    """

    def __init__(
        self,
        project_name: str,
        agent_name: str = "X4-平面设计师",
        workspace_dir: Optional[Path] = None
    ):
        """
        Initialize artifact builder with output path configuration.

        Args:
            project_name: 项目名称 (e.g., "餐饮网站原型")
            agent_name: 智能体名称 (default: "X4-平面设计师")
            workspace_dir: Working directory for artifact development
        """
        self.project_name = project_name
        self.agent_name = agent_name

        # Scripts directory
        self.scripts_dir = Path(__file__).parent
        self.init_script = self.scripts_dir / "init-artifact.sh"
        self.bundle_script = self.scripts_dir / "bundle-artifact.sh"

        # Output base path (following global convention)
        self.output_base = Path("output") / project_name / agent_name / "artifacts-builder"

        # Workspace for development
        if workspace_dir is None:
            self.workspace_dir = self.output_base / "workspace"
        else:
            self.workspace_dir = Path(workspace_dir)

    def _get_output_paths(self, artifact_name: str) -> Dict[str, Path]:
        """
        Generate standard output paths following global CLAUDE.md convention.

        Returns dict with keys: plans, results, logs, metadata, workspace
        """
        artifact_dir = self.output_base / artifact_name

        return {
            "plans": artifact_dir / "plans",
            "results": artifact_dir / "results",
            "logs": artifact_dir / "logs",
            "metadata": artifact_dir / "metadata",
            "workspace": artifact_dir / "workspace"
        }

    def _ensure_output_dirs(self, artifact_name: str):
        """Create output directory structure if not exists."""
        paths = self._get_output_paths(artifact_name)
        for path in paths.values():
            path.mkdir(parents=True, exist_ok=True)

    def create_artifact(
        self,
        artifact_name: str,
        description: str,
        components: Optional[List[str]] = None,
        routing: bool = False,
        state_management: str = "useState"
    ) -> Dict[str, Any]:
        """
        Complete workflow: initialize → develop → bundle.

        Args:
            artifact_name: Artifact identifier (kebab-case, e.g., "hotpot-menu-app")
            description: Human-readable description
            components: List of shadcn/ui components to use
            routing: Whether to use React Router
            state_management: State management solution

        Returns:
            Dict with result metadata including paths
        """
        # Ensure output directories exist
        self._ensure_output_dirs(artifact_name)
        paths = self._get_output_paths(artifact_name)

        # Create artifact specification
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        spec = ArtifactSpec(
            project_name=self.project_name,
            agent_name=self.agent_name,
            artifact_name=artifact_name,
            description=description,
            components=components or [],
            routing=routing,
            state_management=state_management,
            timestamp=timestamp
        )

        # Save specification to plans/ directory
        spec_filename = f"{artifact_name}_{timestamp}_spec.json"
        spec_path = paths["plans"] / spec_filename

        with open(spec_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(spec), f, ensure_ascii=False, indent=2)

        # Step 1: Initialize project
        workspace = paths["workspace"] / artifact_name
        init_result = self._run_init_script(artifact_name, workspace, paths)

        if not init_result["success"]:
            return {
                "status": "error",
                "phase": "initialization",
                "error": init_result["error"],
                "logs": init_result["logs"]
            }

        # Save metadata
        metadata = {
            "project_name": self.project_name,
            "agent_name": self.agent_name,
            "artifact_name": artifact_name,
            "description": description,
            "timestamp": timestamp,
            "workspace": str(workspace),
            "spec_file": str(spec_path),
            "components": spec.components,
            "routing": routing,
            "state_management": state_management,
            "phase": "initialized"
        }

        metadata_file = paths["metadata"] / f"{artifact_name}_{timestamp}_metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        return {
            "status": "initialized",
            "message": (
                f"✅ Artifact initialized: {workspace}\n"
                f"Next steps:\n"
                f"1. Develop your artifact by editing files in {workspace}\n"
                f"2. Call bundle_artifact() to create bundle.html\n"
                f"3. Share bundle.html with user"
            ),
            "workspace": workspace,
            "spec_file": spec_path,
            "metadata_file": metadata_file,
            "phase": "development_ready"
        }

    def bundle_artifact(
        self,
        artifact_name: str,
        workspace: Optional[Path] = None
    ) -> Dict[str, Any]:
        """
        Bundle the developed artifact into a single HTML file.

        Args:
            artifact_name: Artifact identifier
            workspace: Path to artifact workspace (if None, auto-detect)

        Returns:
            Dict with bundling result and output file path
        """
        paths = self._get_output_paths(artifact_name)

        if workspace is None:
            workspace = paths["workspace"] / artifact_name

        if not workspace.exists():
            return {
                "status": "error",
                "message": f"Workspace not found: {workspace}"
            }

        # Run bundle script
        bundle_result = self._run_bundle_script(workspace, paths)

        if not bundle_result["success"]:
            return {
                "status": "error",
                "phase": "bundling",
                "error": bundle_result["error"],
                "logs": bundle_result["logs"]
            }

        # Move bundle.html to results/
        bundle_source = workspace / "bundle.html"
        if not bundle_source.exists():
            return {
                "status": "error",
                "message": f"bundle.html not found in {workspace}"
            }

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        bundle_dest = paths["results"] / f"{artifact_name}_{timestamp}.html"

        import shutil
        shutil.copy(bundle_source, bundle_dest)

        # Update metadata
        metadata_files = sorted(paths["metadata"].glob(f"{artifact_name}_*_metadata.json"))
        if metadata_files:
            with open(metadata_files[-1], 'r', encoding='utf-8') as f:
                metadata = json.load(f)

            metadata["phase"] = "bundled"
            metadata["bundle_file"] = str(bundle_dest)
            metadata["bundle_timestamp"] = timestamp

            with open(metadata_files[-1], 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)

        return {
            "status": "success",
            "message": f"✅ Artifact bundled: {bundle_dest}",
            "bundle_file": bundle_dest,
            "workspace": workspace,
            "phase": "completed"
        }

    def _run_init_script(
        self,
        artifact_name: str,
        workspace: Path,
        paths: Dict[str, Path]
    ) -> Dict[str, Any]:
        """Run init-artifact.sh script."""
        log_file = paths["logs"] / f"init_{artifact_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

        try:
            # Create parent directory for workspace
            workspace.parent.mkdir(parents=True, exist_ok=True)

            # Run initialization script
            result = subprocess.run(
                ["bash", str(self.init_script), artifact_name],
                cwd=workspace.parent,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )

            # Save logs
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write("=== STDOUT ===\n")
                f.write(result.stdout)
                f.write("\n\n=== STDERR ===\n")
                f.write(result.stderr)

            if result.returncode != 0:
                return {
                    "success": False,
                    "error": f"Initialization failed with exit code {result.returncode}",
                    "logs": log_file
                }

            return {
                "success": True,
                "logs": log_file
            }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Initialization timed out (5 minutes)",
                "logs": log_file
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "logs": log_file
            }

    def _run_bundle_script(
        self,
        workspace: Path,
        paths: Dict[str, Path]
    ) -> Dict[str, Any]:
        """Run bundle-artifact.sh script."""
        artifact_name = workspace.name
        log_file = paths["logs"] / f"bundle_{artifact_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

        try:
            # Run bundling script
            result = subprocess.run(
                ["bash", str(self.bundle_script)],
                cwd=workspace,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )

            # Save logs
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write("=== STDOUT ===\n")
                f.write(result.stdout)
                f.write("\n\n=== STDERR ===\n")
                f.write(result.stderr)

            if result.returncode != 0:
                return {
                    "success": False,
                    "error": f"Bundling failed with exit code {result.returncode}",
                    "logs": log_file
                }

            return {
                "success": True,
                "logs": log_file
            }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Bundling timed out (5 minutes)",
                "logs": log_file
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "logs": log_file
            }


def example_usage():
    """Example usage demonstrating the workflow."""

    # Initialize builder
    builder = ArtifactBuilder(
        project_name="餐饮网站原型",
        agent_name="X4-平面设计师"
    )

    # Step 1: Initialize artifact
    result = builder.create_artifact(
        artifact_name="hotpot-menu-app",
        description="交互式火锅菜单应用",
        components=["button", "card", "dialog", "tabs"],
        routing=False,
        state_management="useState"
    )

    if result["status"] == "initialized":
        print(result["message"])
        print(f"\n📁 Workspace: {result['workspace']}")

        # Step 2: User develops the artifact
        # (Edit files in workspace)

        # Step 3: Bundle the artifact
        bundle_result = builder.bundle_artifact("hotpot-menu-app")

        if bundle_result["status"] == "success":
            print(f"\n{bundle_result['message']}")
            print(f"📦 Bundle: {bundle_result['bundle_file']}")
    else:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")


if __name__ == "__main__":
    print("Artifacts Builder Execution Engine")
    print("See README.md or reference.md for usage examples")
