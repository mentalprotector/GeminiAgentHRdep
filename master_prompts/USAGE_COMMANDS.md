## 🤖 Agentic Workflow
To start a new task (use Router first):
```bash
python scripts/agent_orchestrator.py add --role router --instruction "YOUR_REQUEST"
```

To execute the next task in queue:
```bash
python scripts/agent_orchestrator.py run
```

To list all tasks:
```bash
python scripts/agent_orchestrator.py list
```

To mark a task as completed:
```bash
python scripts/agent_orchestrator.py complete TASK-ID
```
