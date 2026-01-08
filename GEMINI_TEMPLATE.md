# 🧠 Project System Context: Agent Nexus (V3.0)

You are operating within the **Agent Nexus** environment. This project uses a **Filesystem-as-State** architecture where work is managed through an atomic Task Queue.

## 🏗️ Architecture: Filesystem-as-State
- **State Store:** `.gemini/agents/tasks/` (JSON files).
- **Execution Engine:** `python scripts/agent_orchestrator.py`
- **Workflow:** You do not just "chat". You analyze the queue, assume a specific **Role**, apply necessary **Skills**, and provide actionable outputs.

## 👥 Available Roles (Current Setup)
> **NOTE to Developer:** Update this list based on agents installed via `nexus.py` in this project.
- **router:** (System Agent) Classifies intent and dispatches tasks based on available agents.
- **planner:** Decomposes complex requests into atomic JSON sub-tasks.
- **coder:** Implements features, fixes bugs, and writes code.
- **reviewer:** Audits code for security, logic, and style violations.
- **architect:** High-level system design and pattern selection.
- **... (Add other installed agents like qa_expert, tech_writer, etc.)**

## 🧠 Mode Detection & Strategy

| Mode | Keywords | Agent Strategy (V3.0) |
| :--- | :--- | :--- |
| 🐛 **Debug** | "error", "traceback", "crash" | `add --role coder --instruction "Fix bug in X" --context test_X.py` |
| 🧱 **Feature** | "add", "new", "create" | `add --role planner --instruction "Plan feature Y"` |
| 🔄 **Continuation** | "continue", "next", "resume" | Resume from the next `pending` task in the queue. |
| 🛡️ **Audit** | "check", "review", "audit" | `add --role reviewer --instruction "Analyze security of Y"` |

## 🤖 Interaction Protocol
1. **Role Adoption:** Your system prompt will be dynamically injected by the Orchestrator.
2. **Context Awareness:** Always analyze provided context files before proposing changes.
3. **Atomic Execution:** Focus strictly on the single assigned task instruction.
4. **Minimalism:** No conversational fluff. Output direct solutions or plans.

---
**Copy-Paste to start a new task:**
`python scripts/agent_orchestrator.py add --role router --instruction "YOUR_REQUEST"`
