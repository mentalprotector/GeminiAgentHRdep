# 🤖 Agent Nexus: Master Prompts Registry

This repository contains the "Golden Source" prompts for the Agent Nexus ecosystem. 
These prompts are version-controlled, sourced from industry best practices (Google, Awesome Lists), and adapted for our specific architecture.

## 📂 Active Agents

| Role | Description | Source / Origin | File |
| :--- | :--- | :--- | :--- |
| **Planner** | Technical Lead & Orchestrator. Breaks down tasks into JSON plans. | [Google Agent Cookbook](https://github.com/arham-kk/gemini-agent-cookbook) | [`planner.md`](planner.md) |
| **Coder** | Principal Software Engineer. Implements code with TDD & Google-quality standards. | [Awesome Gemini CLI](https://github.com/Piebald-AI/awesome-gemini-cli) | [`coder.md`](coder.md) |
| **Reviewer** | QA & Security Specialist. Critiques code and enforces quality gates. | [Gemini Agent Cookbook](https://github.com/arham-kk/gemini-agent-cookbook) | [`reviewer.md`](reviewer.md) |
| **Architect** | System Architect. Decisions on scalability, schema, and patterns. | [System Prompts (x1xhlol)](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools) | [`architect.md`](architect.md) |
| **Router** | Intelligent Router. Classifies requests (Bug/Feature/Question). | [Agentic Prompts](https://github.com/tallesborges/agentic-system-prompts) | [`router.md`](router.md) |
| **Product Owner** | Business <-> Tech Translator. Converts requirements to specs. | Custom / Synthetic | [`product_owner.md`](product_owner.md) |
| **DevOps** | Production Manager. Handles Deployment, SSH, Docker, and Safety Protocols. | Custom (Project Specific) | [`devops.md`](devops.md) |
| **Sweeper** | Technical Debt Collector. Refactoring, cleanup, formatting. | [Awesome Gemini AI](https://github.com/ZeroLu/awesome-gemini-ai) | [`sweeper.md`](sweeper.md) |

## 🔄 Synchronization

Use the `nexus sync` command (future implementation) or the `migrate_prompts.py` script to propagate these prompts to target projects.

### Migration Script
A script `scripts/migrate_prompts.py` was used to import these from `@fitnessapp`.

## 🛠 Adding New Agents
1. Create a new `role_name.md` file.
2. Add the required YAML frontmatter:
   ```yaml
   ---
   role: Role Name
   source: Origin Source
   origin_repo: repo/path
   added: YYYY-MM-DD
   description: Brief description.
   ---
   ```
3. Update this README.

## 📚 Sources & References
- **Google Agent Cookbook:** `arham-kk/gemini-agent-cookbook`
- **Awesome Gemini CLI:** `Piebald-AI/awesome-gemini-cli`
- **System Prompts & Models:** `x1xhlol/system-prompts-and-models-of-ai-tools`
- **Agentic System Prompts:** `tallesborges/agentic-system-prompts`
