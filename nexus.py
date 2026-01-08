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
from textual.containers import Container, Vertical
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
    
    # 1. Add Master Registry
    nexus_project = parse_nexus_master()
    if nexus_project:
        projects.append(nexus_project)

    if not DEV_ROOT.exists():
        return projects

    for item in DEV_ROOT.iterdir():
        if item.is_dir() and item.name != "agent-nexus":
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
        if pfile.name == "README.md": continue
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
    #dialog { padding: 1 2; width: 60; height: 20; border: thick $background 80%; background: $surface; layout: vertical; }
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
        sl = self.query_one("#agent_list", SelectionList)
        master_path = NEXUS_ROOT / "master_prompts"
        target_prompts_dir = self.project_path / ".gemini" / "agents" / "prompts"

        if master_path.exists():
            for pfile in master_path.rglob("*.md"):
                if pfile.name == "README.md": continue
                rel_path = pfile.relative_to(master_path)
                category = rel_path.parts[0] if len(rel_path.parts) > 1 else "root"
                
                # Resolve target path
                check_path = str(rel_path.name)
                if category == "skills":
                    check_path = str(Path("skills") / rel_path.name)
                
                target_file = target_prompts_dir / check_path
                is_installed = target_file.exists()
                match_status = ""

                if is_installed:
                    try:
                        # Compare content (stripping CR for Windows safety)
                        with open(pfile, 'r', encoding='utf-8') as f1: m_content = f1.read().replace('\r\n', '\n')
                        with open(target_file, 'r', encoding='utf-8') as f2: t_content = f2.read().replace('\r\n', '\n')
                        
                        if m_content == t_content:
                            match_status = " [green](Synced)[/]"
                        else:
                            match_status = " [yellow](Differs)[/]"
                    except:
                        match_status = " [red](Error)[/]"

                meta = extract_metadata(pfile)
                p_code = meta.get("project_code")
                
                label = f"[{category.upper()}] {pfile.stem}"
                if p_code:
                    label = f"[[b]{p_code}[/]] {label}"
                
                label += match_status
                
                # Pre-select only if NOT installed
                sl.add_option((label, str(rel_path)))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel_btn": self.dismiss()
        elif event.button.id == "install_btn":
            self.install_agents(self.query_one("#agent_list", SelectionList).selected)
            self.dismiss(True)

    def install_agents(self, selected_rel_paths):
        target_root = self.project_path / ".gemini" / "agents" / "prompts"
        target_root.mkdir(parents=True, exist_ok=True)
        source_root = NEXUS_ROOT / "master_prompts"
        config_path = self.project_path / ".gemini" / "agent_flow.yaml"
        new_agents = {}

        for rel_path_str in selected_rel_paths:
            try:
                source_path = source_root / rel_path_str
                rel_path = Path(rel_path_str)
                category = rel_path.parts[0]
                dest_file = target_root / "skills" / rel_path.name if category == "skills" else target_root / rel_path.name
                if category == "skills": (target_root / "skills").mkdir(exist_ok=True)
                shutil.copy2(source_path, dest_file)
                if category in ["roles", "root", "ported"]: new_agents[rel_path.stem.lower()] = rel_path.name
            except: pass

        if config_path.exists() and new_agents:
            try:
                with open(config_path, "r", encoding="utf-8") as f: config = yaml.safe_load(f) or {}
                if "agents" not in config: config["agents"] = {}
                config["agents"].update(new_agents)
                with open(config_path, "w", encoding="utf-8") as f: yaml.dump(config, f, sort_keys=False)
            except: pass

class ProjectDetailScreen(Screen):
    CSS = """
    Screen { layout: vertical; }
    DataTable { height: 1fr; border: solid cyan; }
    #title_label { padding: 1; background: $primary; color: white; text-align: center; width: 100%; }
    .micro-toolbar { height: 3; align: right middle; padding: 0 1; background: $boost; }
    .micro-btn { margin-left: 1; min-width: 15; }
    """
    BINDINGS = [("escape", "app.pop_screen", "Back"), ("i", "install_agent", "Install Agent")]

    def __init__(self, project_data):
        super().__init__()
        self.project_data = project_data

    def compose(self) -> ComposeResult:
        p = self.project_data
        yield Header(show_clock=True)
        yield Label(f"📂 Project: {p['name']} | Env: {p['config'].get('environment', 'N/A')}", id="title_label")
        with TabbedContent(initial="tasks"):
            with TabPane("Tasks", id="tasks"): yield DataTable(id="tasks_table", cursor_type="row")
            with TabPane("Agents", id="agents"):
                yield Container(Button("📄 Open Prompt", id="btn_agent_file", variant="primary", classes="micro-btn"), Button("📂 Agents Folder", id="btn_agent_folder", variant="default", classes="micro-btn"), classes="micro-toolbar")
                yield DataTable(id="agents_table", cursor_type="row")
            with TabPane("GEMINI.md", id="readme"):
                yield Container(
                    Button("📋 Copy Usage", id="btn_copy_usage", variant="warning", classes="micro-btn"),
                    Button("📄 Open File", id="btn_md_file", variant="primary", classes="micro-btn"),
                    Button("📂 Project Folder", id="btn_md_folder", variant="default", classes="micro-btn"),
                    classes="micro-toolbar"
                )
                yield Markdown(id="md_viewer")
        yield Footer()

    def on_mount(self):
        self.refresh_ui()

    def refresh_ui(self):
        table = self.query_one("#tasks_table", DataTable)
        table.clear(columns=True)
        table.add_columns("ID", "Role", "Status", "Instruction", "Date")
        for t in self.project_data["tasks"]:
            status = t.get("status", "")
            if status == "completed": status = "[green]completed[/]"
            elif status == "in_progress": status = "[blue]in_progress[/]"
            elif status == "pending": status = "[yellow]pending[/]"
            instr = t.get("instruction", "").strip().replace("\n", " ")[:57] + "..."
            table.add_row(t.get("id"), t.get("role"), status, instr, t.get("created_at", "")[:16].replace("T", " "))

        agent_table = self.query_one("#agents_table", DataTable)
        agent_table.clear(columns=True)
        agent_table.add_columns("Category", "Role", "Source", "Origin Repo", "Added", "File")
        for a in self.project_data["config"].get("enriched_agents", []):
            cat = a.get('category') or ('skills' if 'skills/' in a.get('file', '').replace('\\', '/') else 'roles')
            cat_styled = f"[magenta]{cat}[/]" if cat == 'skills' else f"[cyan]{cat}[/]"
            
            p_code = a.get('project_code')
            role_display = f"[bold]{a['role']}[/]"
            if p_code: role_display = f"[red bold][{p_code}][/] {role_display}"
            
            agent_table.add_row(cat_styled, role_display, a['source'], a['origin'], a['added'], a['file'])

        md_view = self.query_one("#md_viewer", Markdown)
        md_path = self.project_data["path"] / "GEMINI.md"
        if md_path.exists():
            with open(md_path, "r", encoding="utf-8") as f: md_view.update(f.read())
        else: md_view.update("# GEMINI.md not found")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_copy_usage":
            try:
                import pyperclip
                usage_path = NEXUS_ROOT / "master_prompts" / "USAGE_COMMANDS.md"
                if usage_path.exists():
                    with open(usage_path, "r", encoding="utf-8") as f:
                        pyperclip.copy(f.read())
                    self.notify("Usage commands copied to clipboard!", severity="information")
                else:
                    self.notify("USAGE_COMMANDS.md not found in master_prompts", severity="error")
            except ImportError:
                self.notify("Install 'pyperclip' to use this feature.", severity="error")
            except Exception as e:
                self.notify(f"Copy failed: {e}", severity="error")
        elif event.button.id == "btn_md_file": self._open_path(self.project_data["path"] / "GEMINI.md")
        elif event.button.id == "btn_md_folder": self._open_path(self.project_data["path"])
        elif event.button.id == "btn_agent_folder": self._open_path(self.project_data["path"] / ".gemini" / "agents" / "prompts")
        elif event.button.id == "btn_agent_file":
            try:
                table = self.query_one("#agents_table", DataTable)
                row = table.get_row(table.coordinate_to_cell_key(table.cursor_coordinate).row_key)
                filename = row[5]
                
                prompts_dir = self.project_data["path"] / ".gemini" / "agents" / "prompts"
                agent_path = prompts_dir / filename
                if agent_path.exists():
                    self._open_path(agent_path)
                    return
                found = list(prompts_dir.rglob(Path(filename).name))
                if found: self._open_path(found[0])
                else: self.notify(f"File not found: {filename}", severity="error")
            except: self.notify("Select an agent row first.", severity="warning")

    def _open_path(self, path):
        if not path.exists(): return
        if sys.platform == "win32": os.startfile(path)
        elif sys.platform == "darwin": subprocess.call(["open", str(path)])
        else: subprocess.call(["xdg-open", str(path)])

    def action_install_agent(self):
        def check_result(installed):
            if installed:
                self.notify("Agents installed successfully!")
                self.project_data = parse_project(self.project_data["path"])
                self.refresh_ui()
        self.app.push_screen(InstallAgentModal(self.project_data["path"]), check_result)

class NexusApp(App):
    BINDINGS = [("q", "quit", "Quit"), ("r", "refresh_list", "Refresh")]
    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("🤖 Agent Nexus: Project Dashboard", id="title_label")
        yield DataTable(id="projects_table", cursor_type="row")
        yield Footer()
    def on_mount(self): self.load_projects()
    def action_refresh_list(self): self.load_projects()
    def load_projects(self):
        table = self.query_one("#projects_table", DataTable)
        table.clear(columns=True)
        table.add_columns("Project", "Environment", "Pending", "In Progress", "Completed", "Last Task")
        self.projects = scan_projects()
        for p in self.projects:
            last = f"{p['tasks'][0]['id']} - {p['tasks'][0]['instruction'][:37]}..." if p["tasks"] else "-"
            table.add_row(p["name"], p["config"].get("environment", "default"), str(p["counts"]["pending"]), str(p["counts"]["in_progress"]), str(p["counts"]["completed"]), last, key=p["name"])
    def on_data_table_row_selected(self, event: DataTable.RowSelected):
        project = next((p for p in self.projects if p["name"] == event.row_key.value), None)
        if project: self.push_screen(ProjectDetailScreen(project))

if __name__ == "__main__": NexusApp().run()