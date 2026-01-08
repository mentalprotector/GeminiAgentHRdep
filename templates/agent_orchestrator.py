import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

# --- CONFIGURATION ---
AGENT_ROOT = Path(".gemini/agents")
TASKS_DIR = AGENT_ROOT / "tasks"
LOGS_DIR = AGENT_ROOT / "logs"
PROMPTS_DIR = AGENT_ROOT / "prompts"

# Ensure UTF-8 Output on Windows
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

def init_dirs():
    for d in [TASKS_DIR, LOGS_DIR, PROMPTS_DIR]:
        d.mkdir(parents=True, exist_ok=True)

def load_prompt(role):
    prompt_path = PROMPTS_DIR / f"{role}.md"
    try:
        if prompt_path.exists():
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
    except Exception as e:
        print(f"⚠️ Warning: Could not load prompt for role '{role}': {e}", file=sys.stderr)
    return "You are a helpful AI assistant."

def list_tasks():
    tasks = list(TASKS_DIR.glob("*.json"))
    if not tasks:
        print("No tasks found.")
        return

    print(f"{ 'ID':<18} | {'Role':<10} | {'Status':<12} | {'Retry':<5} | {'Instruction'}")
    print("-" * 100)
    
    # Sort by creation time inferred from ID or mtime
    sorted_tasks = sorted(tasks, key=lambda p: p.name)
    
    for task_path in sorted_tasks:
        try:
            with open(task_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                instr = data.get('instruction', '').replace('\n', ' ')
                if len(instr) > 50:
                    instr = instr[:47] + "..."
                
                print(f"{data.get('id', 'N/A'):<18} | {data.get('role', 'N/A'):<10} | {data.get('status', 'N/A'):<12} | {data.get('retry_count', 0):<5} | {instr}")
        except Exception as e:
            print(f"Error reading {task_path.name}: {e}", file=sys.stderr)

def add_task(role, instruction, context_paths=None):
    # Sanitize inputs
    if context_paths is None:
        context_paths = []
        
    task_id = f"TASK-{datetime.now().strftime('%m%d-%H%M%S')}"
    
    task_data = {
        "id": task_id,
        "role": role,
        "instruction": instruction,
        "context_paths": context_paths,
        "status": "pending",
        "retry_count": 0,
        "created_at": datetime.now().isoformat(),
        "log": [],
        "output_log": f".gemini/agents/logs/{task_id}.log"
    }
    
    task_file = TASKS_DIR / f"{task_id}.json"
    try:
        with open(task_file, 'w', encoding='utf-8') as f:
            json.dump(task_data, f, indent=2, ensure_ascii=False)
        print(f"✅ Added task: {task_id}")
    except Exception as e:
        print(f"❌ Failed to write task file: {e}", file=sys.stderr)

def get_next_task():
    tasks = sorted(TASKS_DIR.glob("*.json"), key=lambda p: p.name)
    for t in tasks:
        try:
            with open(t, 'r', encoding='utf-8') as f:
                data = json.load(f)
                status = data.get("status")
                retries = data.get("retry_count", 0)
                
                if status == "pending" or (status == "failed" and retries < 3):
                    return t, data
        except Exception:
            continue
    return None, None


def log_task_event(task_path, data, event_text):
    if "log" not in data: data["log"] = []
    entry = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {event_text}"
    data["log"].append(entry)
    with open(task_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def update_task_status(task_path, data, status):
    data["status"] = status
    data["updated_at"] = datetime.now().isoformat()
    with open(task_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def read_context_files(file_paths):
    content = ""
    for path_str in file_paths:
        p = Path(path_str)
        if p.exists() and p.is_file():
            try:
                with open(p, 'r', encoding='utf-8') as f:
                    content += f"\n--- File: {path_str} ---"
                    # Read first 8KB only to save context
                    content += f.read(8192) 
                    content += "\n--- End of File ---"
            except Exception as e:
                content += f"\n--- Error reading {path_str}: {e} ---"
        else:
            content += f"\n--- Warning: File not found {path_str} ---"
    return content


def get_available_agents_info():
    """Scans prompts dir for agents and their descriptions."""
    info = ["\n--- AVAILABLE AGENTS (DYNAMIC REGISTRY) ---"]
    
    # Scan Roles
    for f in PROMPTS_DIR.glob("*.md"):
        role_name = f.stem
        desc = "General Agent"
        try:
            with open(f, 'r', encoding='utf-8') as pf:
                # Simple text scan for description to avoid yaml dependency dependency
                for line in pf:
                    if line.startswith("description:"):
                        desc = line.split(":", 1)[1].strip()
                        break
        except: pass
        info.append(f"- {role_name}: {desc}")
        
    # Scan Skills
    skills_dir = PROMPTS_DIR / "skills"
    if skills_dir.exists():
        info.append("\n--- AVAILABLE SKILLS ---")
        for f in skills_dir.glob("*.md"):
            skill_name = f.stem
            info.append(f"- {skill_name}")
            
    return "\n".join(info)


def run_task():
    task_path, data = get_next_task()
    if not task_path:
        print("No pending tasks found.")
        return

    # Don't update status yet to allow re-run if script fails mid-way

    # # --- V4 LOGGING ---
    # skills_str = f" with skills: {', '.join(skills)}" if skills else ""
    # log_task_event(task_path, data, f"PROMPT GENERATED for {data['role']}{skills_str}")
    # # ------------------

    # update_task_status(task_path, data, "in_progress")
    
    print(f"🚀 PROCESSING TASK: {data['id']} ({data['role']})")
    
    # Load Role Prompt
    role_prompt = load_prompt(data['role'])

    # --- ROUTER V3 INJECTION ---
    if data['role'] == 'router':
    agent_menu = get_available_agents_info()
    role_prompt += "\n" + agent_menu
    print(f"  + Injected System Registry ({len(agent_menu)} chars)")
    # ---------------------------


    # --- SKILL INJECTION (V2) ---
    skill_content = ""
    skills = data.get('skills', [])
    if skills:
    print(f"  + Injecting Skills: {', '.join(skills)}")
    for skill in skills:
    skill_path = PROMPTS_DIR / "skills" / f"{skill}.md"
    if skill_path.exists():
    try:
    with open(skill_path, 'r', encoding='utf-8') as f:
    skill_content += f"

    --- SKILL: {skill} ---
    " + f.read()
    except Exception as e:
    print(f"    Error loading skill {skill}: {e}")
    else:
    print(f"    Warning: Skill file not found: {skill_path}")

    role_prompt += skill_content
    # ----------------------------

    
    # Load Context Files
    context_content = read_context_files(data.get('context_paths', []))
    
    # Construct the FINAL PROMPT for the User/Agent
    final_prompt = f"""
================================================================================
🚨 AGENT TASK TRIGGERED: {data['id']}
================================================================================

ROLE: {data['role']}
INSTRUCTION: {data['instruction']}

SYSTEM PROMPT:
{role_prompt}

CONTEXT FILES CONTENT:
{context_content}

================================================================================
👉 TO THE AGENT (YOU):
Please execute the instruction above using the provided context. 
When finished, mark this task as completed by running:
   python scripts/agent_orchestrator.py complete {data['id']}
================================================================================
"""
    print(final_prompt)
    
    # Mark as in_progress AFTER printing successfully

    # --- V4 LOGGING ---
    skills_str = f" with skills: {', '.join(skills)}" if skills else ""
    log_task_event(task_path, data, f"PROMPT GENERATED for {data['role']}{skills_str}")
    # ------------------

    update_task_status(task_path, data, "in_progress")

def complete_task(task_id):
    # Find task file
    task_file = TASKS_DIR / f"{task_id}.json"
    if not task_file.exists():
         # Try matching partial ID
         matches = list(TASKS_DIR.glob(f"*{task_id}*.json"))
         if len(matches) == 1:
             task_file = matches[0]
         else:
             print(f"❌ Task {task_id} not found.")
             return

    try:
        with open(task_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        log_task_event(task_file, data, "TASK COMPLETED")
        update_task_status(task_file, data, "completed")
        print(f"✅ Task {data['id']} marked as COMPLETED.")
    except Exception as e:
        print(f"❌ Error updating task: {e}")

def main():
    parser = argparse.ArgumentParser(description="Gemini Agent Orchestrator")
    subparsers = parser.add_subparsers(dest="command")

    # List
    subparsers.add_parser("list", help="List all tasks")

    # Add
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("--role", required=True, help="Agent role")
    add_parser.add_argument("--instruction", required=True)
    add_parser.add_argument("--context", nargs="*", help="Context paths")

    # Run
    subparsers.add_parser("run", help="Output the prompt for the next pending task")

    # Complete
    complete_parser = subparsers.add_parser("complete", help="Mark a task as completed")
    complete_parser.add_argument("task_id", help="Task ID (e.g., TASK-0101-...")

    args = parser.parse_args()

    init_dirs()

    if args.command == "list":
        list_tasks()
    elif args.command == "add":
        add_task(args.role, args.instruction, args.context)
    elif args.command == "run":
        run_task()
    elif args.command == "complete":
        complete_task(args.task_id)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()