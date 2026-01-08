# 🧠 Project System Context: Agent Nexus (V3.0)

You are operating within the **Agent Nexus** environment. This project uses a **Filesystem-as-State** architecture where work is managed through an atomic Task Queue.

## 🏗️ Architecture: Filesystem-as-State
- **State Store:** `.gemini/agents/tasks/` (JSON files).
- **Execution Engine:** `python scripts/agent_orchestrator.py`
- **Workflow:** You do not just "chat". You analyze the queue, assume a specific **Role**, apply necessary **Skills**, and provide actionable outputs.

## 👥 Available Roles (Installed in this Project)
{{DYNAMIC_ROLES}}

## 🧠 Mode Detection & Strategy

| Mode | Keywords | Agent Strategy (V3.0) |
| :--- | :--- | :--- |
| 🐛 **Debug** | "error", "traceback", "crash" | `add --role coder --instruction "Fix bug in X" --context test_X.py` |
| 🧱 **Feature** | "add", "new", "create" | `add --role planner --instruction "Plan feature Y"` |
| 🔄 **Continuation** | "continue", "next", "resume" | Resume from the next `pending` task in the queue. |
| 🛡️ **Audit** | "check", "review", "audit" | `add --role reviewer --instruction "Analyze security of Y"` |

## 🤖 Interaction Protocol
1. **Self-Orchestration:** You are responsible for managing your workflow. Use `python scripts/agent_orchestrator.py` to add, run, and complete tasks.
2. **Context Awareness:** Before starting any task, ensure you have run the `run` command to receive the latest system prompt and skills.
3. **Atomic Execution:** Focus strictly on the single task provided by the orchestrator.
4. **Closing the Loop:** Once a task is finished, you MUST call the `complete` command to mark progress in the filesystem.

---
**Initial Action:** 
If you are starting now, run the Router to analyze the project state:
`python scripts/agent_orchestrator.py add --role router --instruction "Analyze project and suggest next steps"`
