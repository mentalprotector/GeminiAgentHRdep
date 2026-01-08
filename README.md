# 👔 Gemini Agent HR Department

<details>
<summary><b>🇷🇺 Нажмите здесь, чтобы прочитать версию на русском языке</b></summary>

## 👔 Отдел Кадров AI-Агентов

**Хватит хранить промпты в текстовых файлах. Начните управлять штатом AI-сотрудников.**

Этот репозиторий служит **Центральным Штабом (HR-департаментом)** для ваших автономных агентов. Он предоставляет CLI-панель (Nexus) для "найма" (установки) агентов в ваши проекты, управления их "навыками" и оркестрации работы.

---

### 🌟 Философия и Возможности

Мы вышли за рамки простого "чата с LLM". Мы относимся к AI-агентам как к **сотрудникам** с конкретными ролями и навыками.

#### 1. HR-менеджер (`nexus.py`)
TUI-панель для просмотра всех ваших проектов в одном месте. Вы видите статус очередей задач и активность агентов.

<details>
<summary><b>📸 Скриншот: Панель Управления (Dashboard)</b></summary>

> *Вставьте скриншот главного списка проектов сюда*
> `![Dashboard](INSERT_LINK_HERE)`

</details>

#### 2. Реестр и Найм (`master_prompts/`)
"Золотой источник" правды. Вы выбираете Роли (Coder, QA) и Навыки (React, SQL) из списка и "инсталлируете" их в проект одной кнопкой.

<details>
<summary><b>📸 Скриншот: Установка Агентов (Installer)</b></summary>

> *Вставьте скриншот модального окна инсталляции сюда*
> `![Installer](INSERT_LINK_HERE)`

</details>

#### 3. Queue Driven Development
Мы не используем чаты для управления работой. Мы используем **Очередь Задач** (JSON). Если задачи нет в очереди — её не существует. Nexus позволяет визуализировать этот процесс.

<details>
<summary><b>📸 Скриншот: Очередь Задач (Task Queue)</b></summary>

> *Вставьте скриншот таблицы задач проекта сюда*
> `![Task Queue](INSERT_LINK_HERE)`

</details>

#### 4. Оркестратор (`agent_orchestrator.py`)
Менеджер уровня проекта. Он работает локально, управляет JSON-файлами и **динамически собирает промпты** для LLM на основе установленных навыков. **API-ключи не нужны!**

---

### 🚀 Как это работает (The Gemini CLI Flow)

Этот инструмент создан для работы в паре с **Gemini CLI** (или веб-интерфейсом).

1.  **Bootstrap:** Скормите Gemini системный контекст (`GEMINI_TEMPLATE.md`).
2.  **Task:** Поставьте задачу Роутеру через терминал: `python scripts/agent_orchestrator.py add --role router ...`
3.  **Magic:** Оркестратор соберет "Меню" агентов и подготовит промпт.
4.  **Execute:** Вы копируете промпт в чат, Gemini выдает решение (JSON или код).

---

### 📂 Структура

```
GeminiAgentHRdep/
├── nexus.py                 # Admin TUI (Дашборд и Инсталлятор)
├── templates/
│   └── agent_orchestrator.py # V3 Оркестратор (Скопируйте это в свои проекты!)
├── master_prompts/          # Золотой Реестр
│   ├── roles/               # Личности (Coder, Planner, Reviewer)
│   ├── skills/              # Хард-скиллы (Стеки, Фреймворки)
│   └── ...
```

</details>

## 👔 Gemini Agent HR Department

**Stop managing prompts in text files. Start managing an AI Workforce.**

This repository serves as the **Central Headquarters (HR Department)** for your autonomous AI agents. It provides a CLI dashboard to "hire" (install) agents into your projects, manage their "skills" (context modules), and orchestrate their work.

---

### 🌟 Philosophy & Features

We moved beyond simple "chat with LLM". We treat AI Agents as **employees** with specific roles and skills.

#### 1. The HR Manager (`nexus.py`)
A TUI dashboard to view all your projects in one place. Monitor task queues and agent activity at a glance.

<details>
<summary><b>📸 Screenshot: Command Center (Dashboard)</b></summary>

> *Insert Dashboard screenshot link here*
> `![Dashboard](INSERT_LINK_HERE)`

</details>

#### 2. The Registry & Hiring (`master_prompts/`)
The golden source of truth. Select Personas (Roles) and Knowledge Modules (Skills) from the registry and "install" them into your project with one click.

<details>
<summary><b>📸 Screenshot: Agent Installer</b></summary>

> *Insert Installer screenshot link here*
> `![Installer](INSERT_LINK_HERE)`

</details>

#### 3. Queue Driven Development
We don't use "chats" to manage work state. We use a **Task Queue** (JSON). If it's not in the queue, it doesn't exist. Nexus visualizes this flow.

<details>
<summary><b>📸 Screenshot: Task Queue Monitoring</b></summary>

> *Insert Task Queue screenshot link here*
> `![Task Queue](INSERT_LINK_HERE)`

</details>

#### 4. The Orchestrator (`agent_orchestrator.py`)
The project-level manager. It runs locally, manages JSON task files, and **dynamically builds prompts** for the LLM based on installed skills. **No API Keys required!**

---

### 🚀 The Gemini CLI Workflow

This toolset is designed to empower your **Gemini CLI** (or Web Interface) sessions.

1.  **Bootstrap:** Feed the system context (`GEMINI_TEMPLATE.md`) to your chat.
2.  **Task:** Assign a task to the Router via terminal: `python scripts/agent_orchestrator.py add --role router ...`
3.  **Magic:** The Orchestrator scans installed agents/skills and builds a dynamic prompt.
4.  **Execute:** Copy the prompt to the chat. Gemini executes the role.

---

### 📂 Structure

```
GeminiAgentHRdep/
├── nexus.py                 # Admin TUI (Dashboard & Installer)
├── templates/
│   └── agent_orchestrator.py # V3 Orchestrator (Copy this to your projects!)
├── master_prompts/          # The Golden Registry
│   ├── roles/               # Agent Personas (Coder, Planner, Reviewer)
│   ├── skills/              # Hard Skills (Tech Stacks, Frameworks)
│   └── ...
```

---

### 📦 Requirements
- Python 3.10+
- `rich`, `textual`, `pyyaml`, `pyperclip`
- **NO API KEYS REQUIRED:** All interaction happens via your existing Chat Interface (CLI/Web). The Python scripts simply manage the file system state.
