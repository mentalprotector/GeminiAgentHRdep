import os
import sys
import json
import yaml
import shutil
import subprocess
import re
from pathlib import Path
from datetime import datetime

from textual.app import App, ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Header, Footer, DataTable, TabbedContent, TabPane, Markdown, Static, Label, Button, SelectionList
from textual.screen import Screen, ModalScreen
from textual.binding import Binding

# --- CONFIG & LOGIC ---
DEV_ROOT = Path(".." ).resolve()
NEXUS_ROOT = Path(__file__).parent.resolve()

def extract_metadata(file_path):
    """Extracts YAML frontmatter from a markdown file."""
    if not file_path.exists():
        return {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
            if match:
                return yaml.safe_load(match.group(1))
    except Exception:
        pass
    return {}

def scan_projects():
    """Scans DEV_ROOT for projects with .gemini configuration + includes Nexus itself."""
    projects = []
    nexus_project = parse_nexus_master()
    if nexus_project:
        projects.append(nexus_project)

    if not DEV_ROOT.exists():
        return projects

    for item in DEV_ROOT.iterdir():
        if item.is_dir() and item.name != "agent-nexus" and item.name != "GeminiAgentHRdep":
            gemini_dir = item / ".gemini"
            if gemini_dir.exists():
                projects.append(parse_project(item))
    return projects

def parse_project(path):
    """Reads project state."""
    config_path = path / ".gemini" / "agent_flow.yaml"
    tasks_dir = path / ".gemini" / "agents" / "tasks"
    prompts_dir = path / ".gemini" / "agents" / "prompts"
    
    config = {}
    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f) or {}
        except Exception:
            pass

    enriched_agents = []
    found_files = {}
    if prompts_dir.exists():
        for f in prompts_dir.rglob("*.md"):
            found_files[f.name] = f
            
    processed_files = set()
    if "agents" in config:
        for role, pfile in config["agents"].items():
            prompt_path = prompts_dir / pfile
            if not prompt_path.exists():
                prompt_path = path / ".gemini" / pfile
            
            if prompt_path.exists():
                processed_files.add(prompt_path.name)
                
            meta = extract_metadata(prompt_path)
            enriched_agents.append({
                "role": role,
                "file": pfile,
                "source": meta.get("source", "Unknown"),
                "origin": meta.get("origin_repo", "-"),
                "added": meta.get("added", "-"),
                "project_code": meta.get("project_code"),
                "description": meta.get("description", "")
            })

    for fname, fpath in found_files.items():
        if fname not in processed_files and fname not in [a['file'] for a in enriched_agents]:
             meta = extract_metadata(fpath)
             role = meta.get("role", fpath.stem.capitalize())
             enriched_agents.append({
                "role": role,
                "file": fname,
                "source": meta.get("source", "Unknown"),
                "origin": meta.get("origin_repo", "-"),
                "added": meta.get("added", "-"),
                "project_code": meta.get("project_code"),
                "description": meta.get("description", "")
            })
            
    config["enriched_agents"] = enriched_agents

    tasks = []
    if tasks_dir.exists():
        for t_file in tasks_dir.glob("*.json"):
            try:
                with open(t_file, "r", encoding="utf-8") as f:
                    tasks.append(json.load(f))
            except: pass
    
    tasks.sort(key=lambda x: x.get('created_at', ''), reverse=True)

    return {
        "name": path.name,
        "path": path,
        "config": config,
        "tasks": tasks,
        "counts": {
            "pending": sum(1 for t in tasks if t.get("status") == "pending"),
            "completed": sum(1 for t in tasks if t.get("status") == "completed"),
            "in_progress": sum(1 for t in tasks if t.get("status") == "in_progress"),
            "total": len(tasks)
        }
    }

def parse_nexus_master():
    """Parses the master prompts directory including subfolders."""
    path = NEXUS_ROOT
    master_dir = path / "master_prompts"
    if not master_dir.exists(): return None
        
    enriched_agents = []
    for pfile in master_dir.rglob("*.md"):
        if pfile.name in ["README.md", "USAGE_COMMANDS.md", "SESSION_BOOTSTRAP.md"]: continue
        rel_path = pfile.relative_to(master_dir)
        category = rel_path.parts[0] if len(rel_path.parts) > 1 else "root"
        meta = extract_metadata(pfile)
        enriched_agents.append({
            "role": meta.get("role", meta.get("name", pfile.stem.capitalize())),
            "category": category,
            "file": str(rel_path),
            "source": meta.get("source", "Unknown"),
            "origin": meta.get("origin_repo", "-"),
            "added": meta.get("added", "-"),
            "project_code": meta.get("project_code"),
            "description": meta.get("description", "")
        })

    return {
        "name": "⭐ Master Registry",
        "path": path,
        "config": {"environment": "Global", "enriched_agents": enriched_agents},
        "tasks": [],
        "counts": {"pending": 0, "completed": 0, "in_progress": 0, "total": 0}
    }

# --- TUI SCREENS ---

class InstallAgentModal(ModalScreen):
    CSS = """
    InstallAgentModal { align: center middle; }
    #dialog { padding: 1 2; width: 80; height: 24; border: thick $background 80%; background: $surface; layout: vertical; }
    #question { width: 100%; content-align: center middle; margin-bottom: 1; }
    SelectionList { height: 1fr; border: solid $secondary; margin-bottom: 1; }
    #btn_container { height: 3; layout: horizontal; align: center middle; }
    Button { width: 50%; }
    """

    def __init__(self, project_path):
        super().__init__()
        self.project_path = project_path

    def compose(self) -> ComposeResult:
        yield Container(
            Label("Select agents to install:", id="question"),
            SelectionList(id="agent_list"),
            Container(Button("Install", variant="primary", id="install_btn"), Button("Cancel", variant="error", id="cancel_btn"), id="btn_container"),
            id="dialog",
        )

    def on_mount(self):
        try:
            sl = self.query_one("#agent_list", SelectionList)
            master_path = NEXUS_ROOT / "master_prompts"
            target_prompts_dir = self.project_path / ".gemini" / "agents" / "prompts"

            if master_path.exists():
                for pfile in master_path.rglob("*.md"):
                    if pfile.name in ["README.md", "USAGE_COMMANDS.md", "SESSION_BOOTSTRAP.md"]: continue
                    rel_path = pfile.relative_to(master_path)
                    category = rel_path.parts[0] if len(rel_path.parts) > 1 else "root"
                    
                    check_path = rel_path.name
                    if category == "skills": check_path = f"skills/{rel_path.name}"
                    
                    target_file = target_prompts_dir / check_path
                    is_installed = target_file.exists()
                    match_status = ""

                    if is_installed:
                        try:
                            with open(pfile, 'r', encoding='utf-8') as f1: m_content = f1.read().replace('\r\n', '\n')
                            with open(target_file, 'r', encoding='utf-8') as f2: t_content = f2.read().replace('\r\n', '\n')
                            match_status = " [green](Synced)[/]